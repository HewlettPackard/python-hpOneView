#!/usr/bin/env python3
###
# (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
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
import re
if sys.version_info < (3, 2):
    raise Exception('Must use Python 3.2 or later')

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


def deligs(net):
    ligs = net.get_ligs()
    for lig in ligs:
        net.delete_lig(lig)


def deflig(net, con):
    prog = re.compile('.*-A')
    fcnets = net.get_fc_networks()
    neta_uris = []
    netb_uris = []
    for fcnet in fcnets:
        if fcnet['name'] == '3PAR SAN A':
            fcneta = fcnet['uri']
        if fcnet['name'] == '3PAR SAN B':
            fcnetb = fcnet['uri']
    enets = net.get_enet_networks()
    for enet in enets:
        if prog.match(enet['name']):
                neta_uris.append(enet['uri'])
        else:
                netb_uris.append(enet['uri'])

    lig = hpov.common.make_lig_dict('VC FlexFabric Production')
    swtype = con.get_entity_byfield(hpov.common.uri['ictype'],
                                    'partNumber', '691367-B21')
    hpov.common.set_iobay_occupancy(lig['interconnectMapTemplate'],
                               [1, 2], swtype['uri'])

    #### Uplink Set 1-A port X7 and X8
    uplinkSet = hpov.common.make_uplink_set_dict('Uplink Set 1-A', neta_uris)
    # Get Port Number
    for port in swtype['portInfos']:
        if port['portName'] == 'X7':
            uplinkSet['logicalPortConfigInfos'].append(
                    hpov.common.make_port_config_info(1, 1, port['portNumber']))
        if port['portName'] == 'X8':
            uplinkSet['logicalPortConfigInfos'].append(
                    hpov.common.make_port_config_info(1, 1, port['portNumber']))
    lig['uplinkSets'].append(uplinkSet)

    #### Uplink Set 1-B port X7 and X8
    uplinkSet = hpov.common.make_uplink_set_dict('Uplink Set 1-B', netb_uris)
    # Get Port Number
    for port in swtype['portInfos']:
        if port['portName'] == 'X7':
            uplinkSet['logicalPortConfigInfos'].append(
                    hpov.common.make_port_config_info(1, 2, port['portNumber']))
        if port['portName'] == 'X8':
            uplinkSet['logicalPortConfigInfos'].append(
                    hpov.common.make_port_config_info(1, 2, port['portNumber']))
    lig['uplinkSets'].append(uplinkSet)

    #### Uplink Set 3PAR SAN A port X3 and X4
    uplinkSet = hpov.common.make_uplink_set_dict('3PAR SAN A', [fcneta],
                                            'FibreChannel')
    # Get Port Numbers
    for port in swtype['portInfos']:
        if port['portName'] == 'X3':
            uplinkSet['logicalPortConfigInfos'].append(
                    hpov.common.make_port_config_info(1, 1, port['portNumber']))
        if port['portName'] == 'X4':
            uplinkSet['logicalPortConfigInfos'].append(
                    hpov.common.make_port_config_info(1, 1, port['portNumber']))
    lig['uplinkSets'].append(uplinkSet)

    #### Uplink Set 3PAR SAN B port X3 and X4
    uplinkSet = hpov.common.make_uplink_set_dict('3PAR SAN B', [fcnetb],
                                            'FibreChannel')
    # Get Port Numbers
    for port in swtype['portInfos']:
        if port['portName'] == 'X3':
            uplinkSet['logicalPortConfigInfos'].append(
                    hpov.common.make_port_config_info(1, 2, port['portNumber']))
        if port['portName'] == 'X4':
            uplinkSet['logicalPortConfigInfos'].append(
                    hpov.common.make_port_config_info(1, 2, port['portNumber']))
    lig['uplinkSets'].append(uplinkSet)

    lig = net.create_lig(lig)
    print('\nCreating Logical Interconnect Group\n')
    pprint(lig)


def main():
    parser = argparse.ArgumentParser(add_help=True, description='Usage')
    parser.add_argument('-a', '--appliance', dest='host', required=True,
                        help='HP OneView Appliance hostname or IP')
    parser.add_argument('-u', '--user', dest='user', required=False,
                        default='Administrator', help='HP OneView Username')
    parser.add_argument('-p', '--pass', dest='passwd', required=False,
                        help='HP OneView Password')
    parser.add_argument('-c', '--certificate', dest='cert', required=False,
                        help='Trusted SSL Certificate Bundle in PEM '
                        '(Base64 Encoded DER) Format')
    parser.add_argument('-r', '--proxy', dest='proxy', required=False,
                        help='Proxy (host:port format')
    parser.add_argument('-d', dest='delete', required=False,
                        action='store_true', help='Delete all LIGs and exit')

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
    if args.delete:
        deligs(net)
        sys.exit()

    deflig(net, con)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
