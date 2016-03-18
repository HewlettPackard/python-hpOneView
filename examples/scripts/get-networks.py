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
import re

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


def get_networks(net, ntype, name, report):

    if report:
        if name:
            if not ntype or ntype == 'Ethernet':
                enets = net.get_enet_networks()
                print('\nEthernet Networks')
                print('-----------------')
                print('\n{0:20}  {1:7}  {2:7}  {3:9}  {4:7}  {5:6}'.format(
                    'Name', 'VLAN ID', 'Purpose', 'Smartlink', 'Private',
                    'Status'))
                print('{0:20}  {1:7}  {2:7}  {3:9}  {4:7}  {5:6}'.format(
                    '----', '-------', '-------', '---------', '-------',
                    '------'))
                for enet in enets:
                    if enet['name'] == name:
                        print('{0:20}  {1:7}  {2:7}  {3:9}  {4:7}  {5:6}'.format(
                            enet['name'], enet['vlanId'], enet['purpose'],
                            str(enet['smartLink']),
                            str(enet['privateNetwork']), enet['status']))
            if not ntype or ntype == 'FC':
                print('\nFC Networks')
                print('-----------')
                print('\n{0:20}  {1:12}  {2:19}  {3:25}  {4:6}'.format(
                    'Name', 'Fabric Type', 'Link Stability Time',
                    'Auto Login Redistirbution', 'Status'))
                print('{0:20}  {1:12}  {2:19}  {3:25}  {4:6}'.format(
                    '----', '-----------', '-------------------',
                    '-------------------------', '------'))
                fnets = net.get_fc_networks()
                for fnet in fnets:
                    if fnet['name'] == name:
                        print('{0:20}  {1:12}  {2:19}  {3:25}  {4:6}'.format(
                            fnet['name'], fnet['fabricType'],
                            fnet['linkStabilityTime'],
                            str(fnet['autoLoginRedistribution']),
                            fnet['status']))
        else:
            if not ntype or ntype == 'Ethernet':
                print('\nEthernet Networks')
                print('-----------------')
                print('\n{0:20}  {1:7}  {2:7}  {3:9}  {4:7}  {5:6}'.format(
                    'Name', 'VLAN ID', 'Purpose', 'Smartlink', 'Private',
                    'Status'))
                print('{0:20}  {1:7}  {2:7}  {3:9}  {4:7}  {5:6}'.format(
                    '----', '-------', '-------', '---------', '-------',
                    '------'))
                enets = net.get_enet_networks()
                for enet in enets:
                    print('{0:20}  {1:7}  {2:7}  {3:9}  {4:7}  {5:6}'.format(
                        enet['name'], enet['vlanId'], enet['purpose'],
                        str(enet['smartLink']), enet['privateNetwork'],
                        str(enet['privateNetwork']), enet['status']))
            if not ntype or ntype == 'FC':
                fnets = net.get_fc_networks()
                print('\nFC Networks')
                print('-----------')
                print('\n{0:20}  {1:12}  {2:19}  {3:25}  {4:6}'.format(
                    'Name', 'Fabric Type', 'Link Stability Time',
                    'Auto Login Redistirbution', 'Status'))
                print('{0:20}  {1:12}  {2:19}  {3:25}  {4:6}'.format(
                    '----', '-----------', '-------------------',
                    '-------------------------', '------'))
                for fnet in fnets:
                    print('{0:20}  {1:12}  {2:19}  {3:25}  {4:6}'.format(
                        fnet['name'], fnet['fabricType'],
                        fnet['linkStabilityTime'],
                        str(fnet['autoLoginRedistribution']),
                        fnet['status']))
    else:
        if name:
            if not ntype or ntype == 'Ethernet':
                enets = net.get_enet_networks()
                for enet in enets:
                    if enet['name'] == name:
                        pprint(enet)
            if not ntype or ntype == 'FC':
                fnets = net.get_fc_networks()
                for fnet in fnets:
                    if fnet['name'] == name:
                        pprint(fnet)
        else:
            if not ntype or ntype == 'Ethernet':
                enets = net.get_enet_networks()
                pprint(enets)
            if not ntype or ntype == 'FC':
                fc = net.get_fc_networks()
                pprint(fc)


def main():
    parser = argparse.ArgumentParser(add_help=True,
                        formatter_class=argparse.RawTextHelpFormatter,
                                     description='''
    Display the collection of network resources

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
    parser.add_argument('-t', dest='ntype', required=False,
                        choices=['Ethernet', 'FC'],
                        help='''
    The type of the network resource to be returned''')
    parser.add_argument('-n', dest='name', required=False,
                        help='''
    The name of the network resource to be returned''')
    parser.add_argument('-r', dest='report',
                        required=False, action='store_true',
                        help='''
    Format the output using a human readable report format''')

    args = parser.parse_args()
    credential = {'authLoginDomain': args.domain.upper(), 'userName': args.user, 'password': args.passwd}

    con = hpov.connection(args.host)
    net = hpov.networking(con)

    if args.proxy:
        con.set_proxy(args.proxy.split(':')[0], args.proxy.split(':')[1])
    if args.cert:
        con.set_trusted_ssl_bundle(args.cert)

    login(con, credential)
    acceptEULA(con)

    get_networks(net, args.ntype, args.name, args.report)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
