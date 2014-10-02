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
if sys.version_info < (3, 2):
    raise Exception('Must use Python 3.2 or later')

import hpOneView as hpov


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


def delnetworks(net):
    networksets = net.get_networksets()
    for networkset in networksets:
        net.delete_networkset(networkset)
    fcnets = net.get_fc_networks()
    for fcnet in fcnets:
        net.delete_network(fcnet)
    enets = net.get_enet_networks()
    for enet in enets:
        net.delete_network(enet)


def defnetwork(net):
    bandDict = hpov.common.make_bw_dict(maxbw=10000, minbw=2500)
    nseta = []
    nsetb = []
    print('\nCreating Ethernet Networks\n')
    print('{0:<15}\t{1:<15}\t{2:<15}'.format('NAME', 'VLAN', 'STATE'))
    print('{0:<15}\t{1:<15}\t{2:<15}'.format('-------', '-------', '-------'))
    enet = net.create_enet_network('VLAN-10-A',
                                   10,
                                   smartLink=True,
                                   privateNetwork=False,
                                   bw=bandDict)
    nseta.append(enet['uri'])
    print('{0:<15}\t{1:<15}\t{2:<15}'.format(enet['name'], enet['vlanId'], enet['state']))

    enet = net.create_enet_network('VLAN-20-A',
                                   20,
                                   smartLink=True,
                                   privateNetwork=False,
                                   ethernetNetworkType='Tagged',
                                   bw=bandDict)
    nseta.append(enet['uri'])
    print('{0:<15}\t{1:<15}\t{2:<15}'.format(enet['name'], enet['vlanId'], enet['state']))

    enet = net.create_enet_network('VLAN-30-A',
                                   30,
                                   smartLink=True,
                                   privateNetwork=False,
                                   ethernetNetworkType='Tagged',
                                   bw=bandDict)
    nseta.append(enet['uri'])
    print('{0:<15}\t{1:<15}\t{2:<15}'.format(enet['name'], enet['vlanId'], enet['state']))

    enet = net.create_enet_network('VLAN-40-A',
                                   40,
                                   smartLink=True,
                                   privateNetwork=False,
                                   ethernetNetworkType='Tagged',
                                   bw=bandDict)
    nseta.append(enet['uri'])
    print('{0:<15}\t{1:<15}\t{2:<15}'.format(enet['name'], enet['vlanId'], enet['state']))

    enet = net.create_enet_network('VLAN-50-A',
                                   50,
                                   smartLink=True,
                                   privateNetwork=False,
                                   ethernetNetworkType='Tagged',
                                   bw=bandDict)
    nseta.append(enet['uri'])
    print('{0:<15}\t{1:<15}\t{2:<15}'.format(enet['name'], enet['vlanId'], enet['state']))

    enet = net.create_enet_network('VLAN-60-A',
                                   60,
                                   smartLink=True,
                                   privateNetwork=False,
                                   bw=bandDict)
    nseta.append(enet['uri'])
    print('{0:<15}\t{1:<15}\t{2:<15}'.format(enet['name'], enet['vlanId'], enet['state']))

    enet = net.create_enet_network('VLAN-10-B',
                                   10,
                                   smartLink=True,
                                   privateNetwork=False,
                                   bw=bandDict)
    nsetb.append(enet['uri'])
    print('{0:<15}\t{1:<15}\t{2:<15}'.format(enet['name'], enet['vlanId'], enet['state']))

    enet = net.create_enet_network('VLAN-20-B',
                                   20,
                                   smartLink=True,
                                   privateNetwork=False,
                                   ethernetNetworkType='Tagged',
                                   bw=bandDict)
    nsetb.append(enet['uri'])
    print('{0:<15}\t{1:<15}\t{2:<15}'.format(enet['name'], enet['vlanId'], enet['state']))

    enet = net.create_enet_network('VLAN-30-B',
                                   30,
                                   smartLink=True,
                                   privateNetwork=False,
                                   ethernetNetworkType='Tagged',
                                   bw=bandDict)
    nsetb.append(enet['uri'])
    print('{0:<15}\t{1:<15}\t{2:<15}'.format(enet['name'], enet['vlanId'], enet['state']))

    enet = net.create_enet_network('VLAN-40-B',
                                   40,
                                   smartLink=True,
                                   privateNetwork=False,
                                   ethernetNetworkType='Tagged',
                                   bw=bandDict)
    nsetb.append(enet['uri'])
    print('{0:<15}\t{1:<15}\t{2:<15}'.format(enet['name'], enet['vlanId'], enet['state']))

    enet = net.create_enet_network('VLAN-50-B',
                                   50,
                                   smartLink=True,
                                   privateNetwork=False,
                                   ethernetNetworkType='Tagged',
                                   bw=bandDict)
    nsetb.append(enet['uri'])
    print('{0:<15}\t{1:<15}\t{2:<15}'.format(enet['name'], enet['vlanId'], enet['state']))

    enet = net.create_enet_network('VLAN-60-B',
                                   60,
                                   smartLink=True,
                                   privateNetwork=False,
                                   bw=bandDict)
    nsetb.append(enet['uri'])
    print('{0:<15}\t{1:<15}\t{2:<15}'.format(enet['name'], enet['vlanId'], enet['state']))

    print('\nCreating Network Sets\n')
    nseta = net.create_networkset('Network Set 1-A',
                                 nets=nseta,
                                 bw=bandDict)
    nsetb = net.create_networkset('Network Set 1-B',
                                 nets=nsetb,
                                 bw=bandDict)
    print('{0:<20}\t{1:<15}\t{2:<15}'.format('NAME', 'STATUS', 'STATE'))
    print('{0:<20}\t{1:<15}\t{2:<15}'.format('-------', '-------', '-------'))
    print('{0:<20}\t{1:<15}\t{2:<15}'.format(nseta['name'], nseta['status'], nseta['state']))
    print('{0:<20}\t{1:<15}\t{2:<15}'.format(nsetb['name'], nsetb['status'], nsetb['state']))
    print('')

    print('\nCreating FC Networks\n')
    fcneta = net.create_fc_network('SAN A', bw=bandDict)
    fcnetb = net.create_fc_network('SAN B', bw=bandDict)
    daneta = net.create_fc_network('3PAR SAN A',
                                   attach='DirectAttach', bw=bandDict)
    danetb = net.create_fc_network('3PAR SAN B',
                                   attach='DirectAttach', bw=bandDict)
    print('{0:<20}\t{1:<15}\t{2:<15}'.format('NAME', 'TYPE', 'STATE'))
    print('{0:<20}\t{1:<15}\t{2:<15}'.format('-------', '-------', '-------'))
    print('{0:<20}\t{1:<15}\t{2:<15}'.format(fcneta['name'],
                                             fcneta['fabricType'],
                                             fcneta['state']))
    print('{0:<20}\t{1:<15}\t{2:<15}'.format(fcnetb['name'],
                                             fcnetb['fabricType'],
                                             fcnetb['state']))
    print('{0:<20}\t{1:<15}\t{2:<15}'.format(daneta['name'],
                                             daneta['fabricType'],
                                             daneta['state']))
    print('{0:<20}\t{1:<15}\t{2:<15}'.format(danetb['name'],
                                             danetb['fabricType'],
                                             danetb['state']))
    print('')


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
                        action='store_true', help='Delete ALL NETWORKS and exit')

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
        delnetworks(net)
        sys.exit()

    defnetwork(net)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
