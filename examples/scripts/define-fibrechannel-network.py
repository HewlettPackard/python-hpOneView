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
if sys.version_info < (3, 4):
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


def addnetwork(net, name, minbw, maxbw, san, link, dist, direct, fabric):
    # Invert the auto redistribution boolean value
    dist = not dist

    maxbw = int(maxbw * 1000)
    minbw = int(minbw * 1000)

    bandDict = hpov.common.make_bw_dict(maxbw, minbw)

    if direct:
        fcnet = net.create_fc_network(name, attach='DirectAttach', bw=bandDict)
        print('\nCreated FC Network\n')
        print('{0:<20}\t{1:<15}\t{2:<15}'.format('NAME', 'TYPE', 'STATE'))
        print('{0:<20}\t{1:<15}\t{2:<15}'.format('-------', '-------',
                                                 '-------'))
        print('{0:<20}\t{1:<15}\t{2:<15}'.format(fcnet['name'],
                                                 fcnet['fabricType'],
                                                 fcnet['state']))
        print('')
    else:
        fcnet = net.create_fc_network(name, attach='FabricAttach',
                                      autodist=dist, linktime=link,
                                      bw=bandDict, managedSanUri=san)
        print('\nCreated FC Network\n')
        print('{0:<20}\t{1:<15}\t{2:<11}\t{3:<9}\t{4:<15}'.format('NAME', 'TYPE', 'AUTO REDIST',
                                                 'STABILITY', 'SAN URI'))
        print('{0:<20}\t{1:<15}\t{2:<11}\t{3:<9}\t{4:<15}'.format('-------', '-------',
                                                 '-----------', '---------',
                                                 '-------'))
        print('{0:<20}\t{1:<15}\t{2:<11}\t{3:<9}\t{4:<15}'.format(fcnet['name'],
                                                 fcnet['fabricType'],
                                                 str(fcnet['autoLoginRedistribution']),
                                                 fcnet['linkStabilityTime'],
                                                 str(fcnet['managedSanUri'])))
        print('')


def main():
    parser = argparse.ArgumentParser(add_help=True, description='Usage')
    parser.add_argument('-a', '--appliance', dest='host', required=True,
                        help='HP OneView Appliance hostname or IP')
    parser.add_argument('-u', '--user', dest='user', required=False,
                        default='Administrator', help='HP OneView Username')
    parser.add_argument('-p', '--pass', dest='passwd', required=True,
                        help='HP OneView Password')
    parser.add_argument('-c', '--certificate', dest='cert', required=False,
                        help='Trusted SSL Certificate Bundle in PEM '
                        '(Base64 Encoded DER) Format')
    parser.add_argument('-y', dest='proxy', required=False,
                        help='Proxy (host:port format')
    parser.add_argument('-n', dest='network_name', required=True,
                        help='Name of the network')
    parser.add_argument('-b', dest='prefered_bandwidth', type=float,
                        required=False, default=2.5, help='Typical '
                        'bandwidth between .1  and 20 Gb/s')
    parser.add_argument('-m', dest='max_bandwidth', type=float, required=False,
                        default=10, help='Maximum bandwidth between .1 and '
                        '20 Gb/s')
    parser.add_argument('-s', dest='managed_san', required=False,
                        help='URI of the associated managed SAN')
    parser.add_argument('-l', dest='link_stability', type=int, required=False,
                        default=30, help='Link Stability Interval between 1 '
                        ' and 1800 seconds')
    parser.add_argument('-x', dest='dist', required=False, action='store_true',
                        help='Disable AUTO loging redistribution')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', dest='direct', action='store_true',
                       help='DirectAttach Fabric Type')
    group.add_argument('-f', dest='fabric', action='store_true',
                       help='FabricAttach Fabric Type')

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

    if args.prefered_bandwidth < .1 or args.prefered_bandwidth > 20:
        print('Error, prefered bandwidth must be between .1 and 20 Gb/s')
        sys.exit()
    if args.max_bandwidth < .1 or args.max_bandwidth > 20:
        print('Error, max bandwidth must be between .1 and 20 Gb/s')
        sys.exit()
    if args.prefered_bandwidth > args.max_bandwidth:
        print('Error, prefered bandwidth must be less than or equal '
              'to the maximum bandwidth')
        sys.exit()
    if args.link_stability < 1 or args.link_stability > 1800:
        print('Error, prefered bandwidth must be between .1 and 20 Gb/s')
        sys.exit()

    addnetwork(net, args.network_name, args.prefered_bandwidth,
               args.max_bandwidth, args.managed_san, args.link_stability,
               args.dist, args.direct, args.fabric)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
