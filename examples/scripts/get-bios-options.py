#!/usr/bin/env python
###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
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
from pprint import pprint
import json


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
    # Login with given credentials
    try:
        con.login(credential)
    except:
        print('Login failed')



def get_bios_options(con, srv, server_id, server_hwt, bios_list):
    defined_bios = []
    sht = select_sht(con, srv, server_id, server_hwt)
    if sht:
        print('Building BIOS options list for', server_id, 'with SHT', sht['name'])
        for bios in sht['biosSettings']:
            bios_setting = {}
            bios_setting['id'] = bios['id']
            bios_setting['name'] = bios['name']
            bios_setting['help'] = bios['helpText']
            if bios.get('options'):
                bios_options = []
                for option in bios.get('options'):
                    opt = {}
                    opt['id'] = option['id']
                    opt['name'] = option['name']
                    bios_options.append(opt)
                    bios_setting['options'] = bios_options
            defined_bios.append(bios_setting)
        f = open(bios_list, 'w')
        out = json.dumps(defined_bios, indent=4)
        f.write('/*\nThis file needs to be modified before it can be used to define a'
        + ' server profile.\nEdit the options for each BIOS setting to select the option'
        + ' you want to override\nin the profile. Only include in the list the BIOS'
        + 'settings you wish to override.\nRemove this comment block when finished editing'
        + ' the file.*/\n')
        f.write(out)
        f.close()


def select_sht(con, srv, server_id, server_hwt):
    if server_id:
        servers = srv.get_servers()
        located_server = None
        for server in servers:
            ips = server['mpHostInfo']['mpIpAddresses']
            for ip in ips:
                if server_id == server['name'] or server_id == ip['address']:
                    located_server = server
                    break

        if not located_server:
            print('Server ', server_id, ' not found')
            sys.exit(1)

        sht = con.get(located_server['serverHardwareTypeUri'])
        if not sht:
            print('Error, server hardware type not found')
            sys.exit()
        return sht
    else:
        shts = srv.get_server_hardware_types()
        for sht in shts:
            if sht['name'] == server_hwt:
                return sht
        print('Error, server hardware type not found')
        sys.exit()

def main():
    parser = argparse.ArgumentParser(add_help=True,
                        formatter_class=argparse.RawTextHelpFormatter,
                                     description='''
    Define the BIOS options of a OneView server profile. Use when defining a
    server profile with manage BIOS.  Server hardware name or server hardware
    type name can be used to create the BIOS list.

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
    parser.add_argument('-bl', dest='bios_list',
                        required=True,
                        help='''
    Name of file for BIOS options list.  File will be created in JSON format
    and need to be edited to select the desired options to manage in the server
    profile.''')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s', dest='server_id',
                        help='''
    Server identification. There are multiple ways to specify the server id:

        . Hostname or IP address of the stand-alone server iLO
        . The "Server Hardware Name" of a server than has already been imported
          into HP OneView and is listed under Server Hardware''')
    group.add_argument('-sh', dest='server_hwt',
                        help='''
    Server hardware type is required for defining BIOS options without
    secifying a specific server identification. The Server Hardware Type must
    be present in the HP OneView appliance before it can be used. For example,
    a single server with the specific server hardware type must have been added
    to OneView for that hardware type to be used. The example script
    get-server-hardware-types.py with the -l argument can be used to get a list
    of server hardware types that have been imported into the OneView
    appliance''')

    args = parser.parse_args()
    credential = {'userName': args.user, 'password': args.passwd}

    con = hpov.connection(args.host)
    srv = hpov.servers(con)

    if args.proxy:
        con.set_proxy(args.proxy.split(':')[0], args.proxy.split(':')[1])
    if args.cert:
        con.set_trusted_ssl_bundle(args.cert)

    login(con, credential)
    acceptEULA(con)

    get_bios_options(con, srv, args.server_id, args.server_hwt, args.bios_list)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
