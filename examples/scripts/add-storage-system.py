#!/usr/bin/env python
###
# (C) Copyright (2012-2015) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import range
from future import standard_library
standard_library.install_aliases()
import sys

PYTHON_VERSION = sys.version_info[:3]
PY2 = (PYTHON_VERSION[0] == 2)
if PY2:
    if PYTHON_VERSION < (2, 7, 9):
        raise Exception('Must use Python 2.7.9 or later')
elif PYTHON_VERSION < (3, 4):
    raise Exception('Must use Python 3.4 or later')

import hpOneView as hpov
from ast import literal_eval
from pprint import pprint


def acceptEULA(con):
    # See if we need to accept the EULA before we try to log in
    con.get_eula_status()
    try:
        if con.get_eula_status() is True:
            print('EULA display needed')
            con.set_eula('no')
    except Exception as e:
        print('EXCEPTION:')
        print(e)


def login(con, credential):
    # Login with givin credentials
    try:
        con.login(credential)
    except:
        print('Login failed')


def add_storage_system(sto, ip, usr, pas, domain, import_pools):
    TB = 1000 * 1000 * 1000 * 1000
    ret = sto.add_storage_system(ip, usr, pas)
    retdict = literal_eval(ret)
    print('Adding Storage System: ', retdict['ip_hostname'])
    found = False
    systems = sto.get_storage_systems()
    conSys = None
    for system in systems:
        if system['credentials']['ip_hostname'] == ip:
            conSys = system

    if not conSys:
        print('Unable to locale a connected system')
        sys.exit()

    for port in reversed(conSys['unmanagedPorts']):
        if port['actualNetworkUri'] != 'unknown':
            conSys['managedPorts'].append(port)
            conSys['unmanagedPorts'].remove(port)
    for port in conSys['managedPorts']:
        port['expectedNetworkUri'] = port['actualNetworkUri']
        port['groupName'] = 'Auto'
    for dom in reversed(conSys['unmanagedDomains']):
        if dom == domain:
            conSys['managedDomain'] = dom
            conSys['unmanagedDomains'].remove(dom)
            found = True
    if not found:
        print('Storage Domain "',domain,'" not found. The following domains '
              'have been found on the storage system')
        for dom in reversed(conSys['unmanagedDomains']):
            pprint(dom)
        sto.remove_storage_system(conSys)
        sys.exit()
    if import_pools:
        found = False
        for pool in reversed(conSys['unmanagedPools']):
            if pool['domain'] == domain:
                conSys['managedPools'].append(pool)
                conSys['unmanagedPools'].remove(pool)
                found = True
        if not found:
            print('Could not locate storage pool for domain:"', domain, '" Verify'
                  ' the pool exsits on the storage system')
            sys.exit()

    ret = sto.update_storage_system(conSys)
    print()
    print('Name:          ', conSys['name'])
    print('Serial Number: ', conSys['serialNumber'])
    print('Model:         ', conSys['model'])
    print('WWN:           ', conSys['wwn'])
    print('Firmware:      ', conSys['firmware'])
    print()
    print('Total:         ', format(int(conSys['totalCapacity']) / TB, '.0f'),
          'TB')
    print('Allocated:     ', format(int(conSys['allocatedCapacity']) / TB,
                                    '.0f'), 'TB')
    print('Free:          ', format(int(conSys['freeCapacity']) / TB, '.0f'),
          'TB')
    print()
    print('uri: ', conSys['uri'])


def main():
    parser = argparse.ArgumentParser(add_help=True,
                        formatter_class=argparse.RawTextHelpFormatter,
                                     description='''
    Import a supported Storage System. In order for the Storage Ports to be
    mapped to Expected Networks, either a Supported SAN Manager will need to
    be configured, or 3PAR Direct Attach networks will have to exist.

    When adding supported HP 3PAR storage systems, please make sure
    "startwsapi" has been executed from the HP 3PAR CLI, which enables the
    HP 3PAR REST API that is required by HP OneView.

    Usage: ''')
    parser.add_argument('-a', dest='host', required=True,
                        help='''
    HP OneView Appliance hostname or IP address''')
    parser.add_argument('-u', dest='user', required=False,
                        default='Administrator',
                        help='''
    HP OneView Username''')
    parser.add_argument('-p', dest='passwd', required=True,
                        help='''
    HP OneView Password''')
    parser.add_argument('-c', dest='cert', required=False,
                        help='''
    Trusted SSL Certificate Bundle in PEM (Base64 Encoded DER) Format''')
    parser.add_argument('-y', dest='proxy', required=False,
                        help='''
    Proxy (host:port format''')
    parser.add_argument('-j', dest='domain', required=False,
                        default='Local',
                        help='''
    HP OneView Authorized Login Domain''')
    parser.add_argument('-sh', dest='storage', required=True,
                        help='''
    IP address of the storage system to add''')
    parser.add_argument('-su', dest='stousr', required=False,
                        help='''
    Administrative username for the storage system''')
    parser.add_argument('-sp', dest='stopass', required=False,
                        help='''
    Administrative password for the storage system''')
    parser.add_argument('-sd', dest='stodom', required=True,
                        help='''
    Storage Domain on the storage system''')
    parser.add_argument('-ip',  dest='import_pools', required=False,
                        default=False, action='store_true',
                        help='''
    Import all of the storage pools from the array''')

    args = parser.parse_args()
    credential = {'authLoginDomain': args.domain.upper(), 'userName': args.user, 'password': args.passwd}

    con = hpov.connection(args.host)
    sto = hpov.storage(con)

    if args.proxy:
        con.set_proxy(args.proxy.split(':')[0], args.proxy.split(':')[1])
    if args.cert:
        con.set_trusted_ssl_bundle(args.cert)

    login(con, credential)
    acceptEULA(con)

    add_storage_system(sto, args.storage, args.stousr, args.stopass,
                       args.stodom, args.import_pools)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
