#!/usr/bin/env python3
###
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
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
import sys
if sys.version_info < (3, 4):
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
    # Login with givin credentials
    try:
        con.login(credential)
    except:
        print('Login failed')


def define_connection_list(net, name, conn_list, append, portId, func, mac,
                           macType, reqGbps, wwnn, wwpn, wwpnType,
                           boot_priority, boot):

    reqMbps = None
    if func == 'Ethernet':
        nets = net.get_enet_networks()
        if reqGbps:
            reqGbps = reqGbps
            if (reqGbps < .1 or reqGbps > 20):
                print('Error: preferred bandwidth must be between .1 and 20 Gbps')
                sys.exit(1)
            reqMbps = int(reqGbps * 1000)
    elif func == 'FibreChannel':
        nets = net.get_fc_networks()

    netw = None
    for network in nets:
        if network['name'] == name:
            netw = network
            break
    if netw is None:
        print(func, 'network: ', name, ' not found')
        sys.exit(1)
    if boot_priority:
        boot = hpov.common.make_profile_connection_boot_dict(priority=boot_priority)
    else:
        boot = None

    conn = hpov.common.make_profile_connection_dict(netw,
                                                    portId,
                                                    func,
                                                    mac,
                                                    macType,
                                                    reqMbps,
                                                    wwnn,
                                                    wwpn,
                                                    wwpnType,
                                                    boot)
    if append:
        # read in the json data from the connection list file
        data = json.loads(open(conn_list).read())
        data.append(conn)
    else:
        data = [conn]
    f = open(conn_list, 'w')
    out = json.dumps(data, indent=4)
    f.write(out)
    f.close()


def main():
    parser = argparse.ArgumentParser(add_help=True, description='Usage',
                        formatter_class=argparse.RawTextHelpFormatter)
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
    parser.add_argument('-n', dest='name',
                        required=True,
                        help='''
    Name of the network''')
    parser.add_argument('-cl', dest='conn_list',
                        required=True,
                        help='''
    Name of file for connection list''')
    parser.add_argument('-app', dest='append',
                        required=False,
                        action='store_true',
                        help='''
    Causes connection list to be appended to the file''')
    parser.add_argument('-port', dest='portId',
                        required=False,
                        default='Auto',
                        help='''
    FlexNIC to use''')
    parser.add_argument('-func', dest='func',
                        required=False,
                        choices=('Ethernet', 'FibreChannel'),
                        default='Ethernet',
                        help='''
    Ethernet or FibreChannel''')
    parser.add_argument('-mac', dest='mac',
                        required=False,
                        default=None,
                        help='''
    MAC address''')
    parser.add_argument('-mt', dest='macType',
                        required=False,
                        choices=('Physical', 'UserDefined', 'Virtual'),
                        default='Virtual',
                        help='''
    MAC address type''')
    parser.add_argument('-gbps', dest='reqGbps',
                        required=False,
                        type=float,
                        default=None,
                        help='''
    Transmit thorougput for this connection in Gbps
    Must be between .1 and 20 Gbps''')
    parser.add_argument('-wwnn', dest='wwnn',
                        required=False,
                        default=None,
                        help='''
    Node WWN address on the FlexNIC''')
    parser.add_argument('-wwpn', dest='wwpn',
                        required=False,
                        default=None,
                        help='''
    Port WWN address on the FlexNIC''')
    parser.add_argument('-wt', dest='wwpnType',
                        required=False,
                        choices=('Physical', 'UserDefined', 'Virtual'),
                        default='Virtual',
                        help='''
    WWPN address type''')
    parser.add_argument('-bp', dest='boot_priority',
                        required=False,
                        choices=('Primary', 'Secondary', 'NotBootable'),
                        default='NotBootable',
                        help='''
    Primary or Secondary or NotBootable''')
    parser.add_argument('-boot', dest='boot',
                        required=False,
                        default=None,
                        help='''
    Boot connection (Not yet implemented)''')

    args = parser.parse_args()
    credential = {'userName': args.user, 'password': args.passwd}

    con = hpov.connection(args.host)
    net = hpov.networking(con)

    if args.proxy:
        con.set_proxy(args.proxy.split(':')[0], args.proxy.split(':')[1])
    if args.cert:
        con.set_trusted_ssl_bundle(args.cert)

    login(con, credential)
    acceptEULA(con)

    define_connection_list(net, args.name, args.conn_list, args.append,
                           args.portId, args.func, args.mac, args.macType,
                           args.reqGbps, args.wwnn, args.wwpn, args.wwpnType,
                           args.boot_priority, args.boot)


if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
