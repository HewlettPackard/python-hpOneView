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


def delprofiles(srv):
    srvrs = srv.get_servers()
    for server in srvrs:
        if server['powerState'] == 'On':
            print(('Powering Off Server:  %s' % server['name']))
            ret = srv.set_server_powerstate(server, 'Off', force=True)
            pprint(ret)

    profiles = srv.get_server_profiles()
    for profile in profiles:
        print(('Removing Profile %s' % profile['name']))
        ret = srv.remove_server_profile(profile)
        pprint(ret)


def defprofile(srv, sts, net):
    # See if we need to turn any servers off
    connections = []
    servers = srv.get_servers()
    ser = None
    for server in servers:
        if server['state'] == 'NoProfileApplied':
            if server['powerState'] == 'On':
                srv.set_server_powerstate(server, 'Off', force=True)
            ser = server
            break
    if not ser:
        print('Error, no valid server found to install profile')
        return
    print('Creating profile for %s' % (ser['name']))
    spp = sts.get_spps()[0]
    enets = net.get_enet_networks()
    enet = None
    networks = ['VLAN-10-A', 'VLAN-10-B', 'VLAN-20-A', 'VLAN-20-B']
    lom = dict.fromkeys(networks)
    for network in enets:
        name = network['name']
        if network['name'] in networks:
            lom[network['name']] = network

    for name, enet in sorted(lom.items()):
        if enet is None:
            print('Error, can not find network: %s' % name)
            return
        connections.append(hpov.common.make_profile_connection_dict(enet, requestedMbps=1500))

    fcnets = net.get_fc_networks()
    for fcnet in fcnets:
        if fcnet['name'] == '3PAR SAN A':
            fcneta = fcnet
        if fcnet['name'] == '3PAR SAN B':
            fcnetb = fcnet

    connections.append(hpov.common.make_profile_connection_dict(fcneta,
                       functionType='FibreChannel',
                       boot=hpov.common.make_profile_connection_boot_dict(priority='Primary')))
    connections.append(hpov.common.make_profile_connection_dict(fcnetb,
                       functionType='FibreChannel',
                       boot=hpov.common.make_profile_connection_boot_dict(priority='Secondary')))
    profile = hpov.common.make_profile_dict('Profile-' + ser['serialNumber'],
                                            ser, connections=connections)
    profile = srv.create_server_profile(profile)
    pprint(profile)


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
                        action='store_true', help='Delete all sever profiles and exit')

    args = parser.parse_args()
    credential = {'userName': args.user, 'password': args.passwd}

    con = hpov.connection(args.host)
    srv = hpov.servers(con)
    net = hpov.networking(con)
    sts = hpov.settings(con)

    if args.proxy:
        con.set_proxy(args.proxy.split(':')[0], args.proxy.split(':')[1])
    if args.cert:
        con.set_trusted_ssl_bundle(args.cert)

    login(con, credential)
    acceptEULA(con)
    if args.delete:
        delprofiles(srv)
        sys.exit()

    defprofile(srv, sts, net)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
