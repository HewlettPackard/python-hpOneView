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


def adduplinkset(con, net, name, ligname, networks, utype, etype,
                 native, icports, lacp, connection):

    net_uris = []
    native_uri = []
    port_uris = []

    ligs = net.get_ligs()
    # Locate the user supplied LIG
    for tlig in ligs:
        if tlig['name'] == ligname:
            lig = tlig
            print('Using Logical Interconnect Group: ', ligname)

    if not lig:
        print('Error can not locate Logical Interconnect Group: ', ligname)
        sys.exit()

    # Locate the user supplied networks
    if networks:
        if utype == 'FibreChannel':
            fcnets = net.get_fc_networks()
            for fcnet in fcnets:
                if fcnet['name'] in networks:
                    print('Adding FC Network: ', fcnet['name'])
                    net_uris.append(fcnet['uri'])
        if utype == 'Ethernet':
            enets = net.get_enet_networks()
            for enet in enets:
                if enet['name'] in networks:
                    print('Adding Ethernet Network: ', enet['name'])
                    net_uris.append(enet['uri'])
                if native:
                    if enet['name'] in native:
                        native_uri = enet['uri']

    if native and not native_uri:
        print('Error can not locate the native network: ', native)

    if not native_uri:
        native_uri = None

    # Validate the use supplied Bay and Port options
    bay_list = set()
    ics = {}
    if icports:
        for items in icports:
            bay, port = items.split(':')
            bay = int(bay)
            bay_list.add(bay)
            port = int(port)
            if bay < 1 or bay > 8:
                print('Error, invalid BAY specified: ', items)
                sys.exit()
            if port < 1 or port > 10:
                print('Error, invalid PORT specified: ', items)
                sys.exit()

        # Find the interconnect modules that are installed in the bays
        # and store that in a dictionary of {Bay, Interconnect URI}
        icmap = lig['interconnectMapTemplate']['interconnectMapEntryTemplates']
        for interconnects in icmap:
            for item in interconnects['logicalLocation']['locationEntries']:
                if item['type'] == 'Bay' and item['relativeValue'] in bay_list:
                    ics[int(item['relativeValue'])] = interconnects['permittedInterconnectTypeUri']

        # Iterate through the bay and ports supplied by the user and lookup
        # the corresponding protConfigInfos port number for each port in
        # each bay to create the list of portConfigInfo URI's
        for items in icports:
            bay, pn = items.split(':')
            ictype = con.get_by_uri(ics[int(bay)])
            for port in ictype['portInfos']:
                if port['portName'] == 'X' + pn:
                    print('Adding Interconnect Bay: %s Port: %s (%s)' %
                          (bay, pn, port['portNumber']))
                    port_uris.append(hpov.common.make_port_config_info(1,
                                     int(bay), port['portNumber']))

    # Create a new uplink set to append to the logical interconnect group
    uset = hpov.common.make_UplinkSetGroupV2(name,
                                             ethernetNetworkType=etype,
                                             lacpTimer=lacp,
                                             logicalPortConfigInfos=port_uris,
                                             mode=connection,
                                             nativeNetworkUri=native_uri,
                                             networkType=utype,
                                             networkUris=net_uris)

    lig['uplinkSets'].append(uset)
    lig = net.update_lig(lig)


def main():
    parser = argparse.ArgumentParser(add_help=True,
                        formatter_class=argparse.RawTextHelpFormatter,
                                     description='''
    Define new Uplink Set

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
    parser.add_argument('-n', dest='uplink_set_name', required=True,
                        help='''
    Name of the uplink  set''')
    parser.add_argument('-i', dest='logical_interconnect_group_name',
                        required=True,
                        help='''
    Name of the associated Logical Interconnect Group''')
    parser.add_argument('-l', dest='list_of_networks', required=False,
                        nargs='+',
                        help='''
    List of network names to add to the uplink set, encapsulated with quotes
    and seperated by spaces. For example:

                -l "Net One" "Net Two" "Net Three"''')
    parser.add_argument('-t', dest='uplink_type', choices=['Ethernet',
                        'FibreChannel'], required=True,
                        help='''
    Uplink Type''')
    parser.add_argument('-e', dest='ethernet_type', choices=['Tagged',
                        'Tunnel', 'Untagged'], required=False,
                        default='Tagged',
                        help='''
    Ethernet Type''')
    parser.add_argument('-x', dest='native_network', required=False,
                        help='''
    Name of the network to be marked as native''')
    parser.add_argument('-o', dest='uplink_ports', required=False,
                        nargs='+',
                        help='''
    List of uplink ports connected to the uplink sets specified as BAY:PORT
    and seperated by spaces. For example BAY 1 PORT X2 and BAY 1 PORT X3
    would be specified as:
                        -o 1:2 1:3''')
    parser.add_argument('-m', dest='lacp_mode', required=False,
                        choices=['Long', 'Short'], default='Long',
                        help='''
    LACP mode on ETHERNET uplink ports''')
    parser.add_argument('-g', dest='connection_mode', choices=['Auto',
                        'FailOver'], required=False, default='Auto',
                        help='''
    Ethernet connection mode''')

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

    adduplinkset(con, net, args.uplink_set_name,
                 args.logical_interconnect_group_name, args.list_of_networks,
                 args.uplink_type, args.ethernet_type, args.native_network,
                 args.uplink_ports, args.lacp_mode, args.connection_mode)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
