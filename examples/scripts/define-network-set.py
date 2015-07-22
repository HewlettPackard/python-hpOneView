#!/usr/bin/env python3
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


def add_network_set(net, name, networks, minbw, maxbw):

    nset = []

    maxbw = int(maxbw * 1000)
    minbw = int(minbw * 1000)
    bandDict = hpov.common.make_bw_dict(maxbw, minbw)

    if networks:
        enets = net.get_enet_networks()
        for enet in enets:
            if enet['name'] in networks:
                nset.append(enet['uri'])

    nset = net.create_networkset(name, nets=nset, bw=bandDict)
    if 'connectionTemplateUri' in nset:
        print('\n\nName:           ', nset['name'])
        print('Type:           ', nset['type'])
        print('Description:    ', nset['description'])
        print('State:          ', nset['state'])
        print('Status:         ', nset['status'])
        print('Created:        ', nset['created'])
        print('Uri:            ', nset['uri'])
        print('networkUris:    ')
        for net in nset['networkUris']:
            print('\t\t', net)
    else:
        pprint(nset)


def main():
    parser = argparse.ArgumentParser(add_help=True,
                        formatter_class=argparse.RawTextHelpFormatter,
                                     description='''
    Define new Network Set

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
    parser.add_argument('-n', dest='network_set_name', required=True,
                        help='''
    Name of the network set''')
    parser.add_argument('-l', dest='list_of_networks', required=False,
                        nargs='+',
                        help='''
    List of network names to add to the network set, seperated by spaces.
    For example:
            -t "Net One" "Net Two" "Net Three"''')
    parser.add_argument('-b', dest='prefered_bandwidth', type=float,
                        required=False, default=2.5,
                        help='''
    Typical bandwidth between .1  and 20 Gb/s''')
    parser.add_argument('-m', dest='max_bandwidth', type=float, required=False,
                        default=10,
                        help='''
    Maximum bandwidth between .1 and 20 Gb/s''')

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

    add_network_set(net, args.network_set_name, args.list_of_networks,
                    args.prefered_bandwidth, args.max_bandwidth)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
