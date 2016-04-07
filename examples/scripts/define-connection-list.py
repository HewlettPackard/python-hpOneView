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


def define_boot_list(function_type, boot_priority, boot_target, boot_lun):

    if boot_priority == 'Primary' or boot_priority == 'Secondary':
        if function_type == 'Ethernet':
            if boot_target or boot_lun:
                print('Boot target and LUN can only be specified for '
                      'FibreChannel networks')
                sys.exit(2)
            boot = hpov.common.make_ConnectionBoot(boot_priority, None, None)
        else:
            if boot_target and boot_lun is None:
                print('Boot LUN is required when defining a boot target')
                sys.exit(3)
            boot = hpov.common.make_ConnectionBoot(boot_priority, boot_target,
                                                   boot_lun)
    else:
        boot = None

    return boot

def define_connection_list(net, name, cid, net_name, conn_list, append, portId,
                           function_type, mac, macType, net_set, reqGbps, wwnn,
                           wwpn, wwpnType, boot, spt):

    reqMbps = None
    if function_type == 'Ethernet' and not net_set:
        networks = net.get_enet_networks()
        if reqGbps:
            reqGbps = reqGbps
            if (reqGbps < .1 or reqGbps > 20):
                print('Error: preferred bandwidth must be between .1 and 20 Gbps')
                sys.exit(1)
            reqMbps = int(reqGbps * 1000)
    elif function_type == 'Ethernet' and net_set:
        networks = net.get_networksets()
        if reqGbps:
            reqGbps = reqGbps
            if (reqGbps < .1 or reqGbps > 20):
                print('Error: preferred bandwidth must be between .1 and 20 Gbps')
                sys.exit(1)
            reqMbps = int(reqGbps * 1000)
    elif function_type == 'FibreChannel':
        networks = net.get_fc_networks()

    netw = None
    for network in networks:
        if network['name'] == net_name:
            netw = network
            break
    if netw is None:
        print(function_type, 'network: ', net, ' not found')
        sys.exit(1)

    print('Defining connection', name)
    conn = hpov.common.make_ProfileConnectionV4(cid=cid,
                                                name=name,
                                                networkUri=network['uri'],
                                                profileTemplateConnection=spt,
                                                connectionBoot=boot,
                                                functionType=function_type,
                                                mac=mac,
                                                macType=macType,
                                                portId=portId,
                                                requestedMbps=reqMbps,
                                                wwnn=wwnn,
                                                wwpn=wwpn,
                                                wwpnType=wwpnType)

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
    parser = argparse.ArgumentParser(add_help=True,
                        formatter_class=argparse.RawTextHelpFormatter,
                                     description='''
    Define a OneView network connection list for use with defining a server
    profile with connections.

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
    parser.add_argument('-n', dest='name',
                        required=True,
                        help='''
    Name of the network connection''')
    parser.add_argument('-i', dest='cid',
                        required=True,
                        help='''
    Unique ID for the network connection''')
    parser.add_argument('-net', dest='network',
                        required=True,
                        help='''
    The name of the Ethernet network, network set, or Fibre Channel network to
    use for this connection.''')
    parser.add_argument('-cl', dest='conn_list',
                        required=True,
                        help='''
    Name of file for connection list''')
    parser.add_argument('-app', dest='append',
                        required=False,
                        action='store_true',
                        help='''
    Causes connection list to be appended to the file''')
    parser.add_argument('-ns', dest='net_set',
                        required=False,
                        action='store_true',
                        help='''
    Required to mark the connection type as a Network Set''')
    parser.add_argument('-port', dest='portId',
                        required=False,
                        default='Auto',
                        help='''
    Identifies the port (FlexNIC) used for this connection, for example
    'Flb 1:1-a'. The port can be automatically selected by specifying 'Auto',
    'None', or a physical port when creating or editing the connection.
    If 'Auto' is specified, a port that provides access to the selected
    network (networkUri) will be selected. A physical port (e.g. 'Flb 1:2')
    can be specified if the choice of a specific FlexNIC on the physical
    port is not important. If 'None' is specified, the connection will not
    be configured on the server hardware.''')
    parser.add_argument('-func', dest='func',
                        required=False,
                        choices=['Ethernet', 'FibreChannel'],
                        default='Ethernet',
                        help='''
    Ethernet or FibreChannel''')
    parser.add_argument('-mac', dest='mac',
                        required=False,
                        help='''
    The MAC address that is currently programmed on the FlexNic. The value can
    be virtual, user defined or physical MAC address read from the device.''')
    parser.add_argument('-mt', dest='macType',
                        required=False,
                        choices=['Physical', 'UserDefined', 'Virtual'],
                        default='Virtual',
                        help='''
    Specifies the type of MAC address to be programmed into the IO Devices.''')
    parser.add_argument('-gbps', dest='reqGbps',
                        required=False,
                        type=float,
                        help='''
    Transmit thorougput for this connection in Gbps Must be between .1 and
    20 Gbps''')
    parser.add_argument('-wwnn', dest='wwnn',
                        required=False,
                        help='''
    The node WWN address that is currently programmed on the FlexNic. The
    value can be a virtual WWNN, user defined WWNN or physical WWNN read from
    the device.''')
    parser.add_argument('-wwpn', dest='wwpn',
                        required=False,
                        help='''
    The port WWN address that is currently programmed on the FlexNIC. The
    value can be a virtual WWPN, user defined WWPN or the physical WWPN read
    from the device.''')
    parser.add_argument('-wt', dest='wwpnType',
                        required=False,
                        choices=['Physical', 'UserDefined', 'Virtual'],
                        default='Virtual',
                        help='''
    Specifies the type of WWN address to be porgrammed on the FlexNIC. The
    value can be 'Virtual', 'Physical' or 'UserDefined'.''')
    parser.add_argument('-bp', dest='boot_priority',
                        required=False,
                        choices=['Primary', 'Secondary', 'NotBootable'],
                        default='NotBootable',
                        help='''
    Primary or Secondary or NotBootable''')
    parser.add_argument('-t', dest='boot_target',
                        required=False,
                        help='''
    The wwpn of the target device that provides access to the Boot Volume.
    This value must contain 16 HEX digits''')
    parser.add_argument('-l', dest='boot_lun',
                        required=False,
                        type=int,
                        help='''
    The LUN of the Boot Volume presented by the target device. This value can
    bein the range 0 to 255.''')
    parser.add_argument('-spt', dest='spt',
                        required=False,
                        action='store_true',
                        help='''
    Specifies if the connection list is to be used in defining a server profile 
    template.''')


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

    if args.boot_lun:
        if args.boot_lun < 0 or args.boot_lun > 255:
            print('Error: boot lun value must be between 0 and 255')
            sys.exit(1)

    if args.cid:
        if int(args.cid) <1 or int(args.cid) > 999:
            print('Error: connection ID value must be between 1 and 999')
            sys.exit(2)


    boot = define_boot_list(args.func, args.boot_priority, args.boot_target,
                            args.boot_lun)

    define_connection_list(net, args.name, args.cid, args.network,
                           args.conn_list, args.append, args.portId, args.func,
                           args.mac, args.macType, args.net_set,
                           args.reqGbps, args.wwnn, args.wwpn, args.wwpnType,
                           boot, args.spt)


if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
