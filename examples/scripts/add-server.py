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

def add_server(srv, hostname, username, password, force, license, monitor):
    print('Adding Server')

    if monitor:
        server = hpov.make_server_dict(hostname,username, password, force,
                                       'OneViewStandard', 'Monitored')
    else:
        server = hpov.make_server_dict(hostname,username, password, force,
                                       license)

    ret = srv.add_server(server)
    if 'model' in ret:
        print('Model:         ', ret['model'])
        print('Serial Number: ', ret['serialNumber'])
        print('ROM FW:        ', ret['romVersion'])
        print('Proc Count     ', ret['processorCount'])
        print('Proc Cores     ', ret['processorCoreCount'])
        print('Proc Speed     ', ret['processorSpeedMhz'])
        print('Proc Type      ', ret['processorType'])
        print('iLO FW:        ', ret['mpFirmwareVersion'])
        print('iLO Version:    ', ret['mpModel'])
    else:
        pprint(ret)


def main():
    parser = argparse.ArgumentParser(add_help=True,
                        formatter_class=argparse.RawTextHelpFormatter,
                                     description='''
    Import a physical stand-alone rackmount server.

    This exmaple script IS NOT USED to add a Blade Server to the appliance.
    A BL server will automatically be discovered once it inserted into an
    enclosure being managed by the appliance.

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
    parser.add_argument('-sh', dest='hostname', required=True,
                        help='''
    Hostname or IP address  of the server iLO''')
    parser.add_argument('-su', dest='username', required=True,
                        help='''
    Administrative username for the server iLO''')
    parser.add_argument('-sp',  dest='password', required=True,
                        help='''
    Administrative password for the server iLO''')
    parser.add_argument('-l', dest='license', required=False,
                        choices=['OneView', 'OneViewNoiLO'],
                        default='OneView',
                        help='''
    Specifies whether the intent is to apply either OneView or
    OneView w/o iLO licenses to the servers in the enclosure
    being imported.

    Accepted values are:

        - OneView
        - OneViewNoiLO ''')
    parser.add_argument('-f', dest='force',
                        action='store_true',
                        help='''
    Force adding the server when currently managed by another OneView
    appliance.''')
    parser.add_argument('-m', dest='monitor',
                        action='store_true',
                        help='''
    Add the server as a monitored device.''')

    args = parser.parse_args()
    credential = {'authLoginDomain': args.domain.upper(), 'userName': args.user, 'password': args.passwd}

    con = hpov.connection(args.host)
    srv = hpov.servers(con)

    if args.proxy:
        con.set_proxy(args.proxy.split(':')[0], args.proxy.split(':')[1])
    if args.cert:
        con.set_trusted_ssl_bundle(args.cert)

    login(con, credential)
    acceptEULA(con)

    add_server(srv, args.hostname, args.username, args.password, args.force,
               args.license, args.monitor)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
