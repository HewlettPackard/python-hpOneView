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


def getenc(srv, net):
    enclosures = srv.get_enclosures()
    for enc in enclosures:
        print('\n{0:15} {1:13} {2:15}\t\t\t{3:9} {4:10} {5:13}'.format(
            'Enclosure Name', 'Serial Number', 'Enclosure Model',
            'Rack Name', 'FW Managed', 'Baseline Name'))
        print('\n{0:15} {1:13} {2:15}\t\t\t{3:9} {4:10} {5:13}'.format(
            '--------------', '-------------', '---------------',
            '---------', '----------', '-------------'))
        print('\n{0:15} {1:13} {2:15}\t{3:9} {4:10} {5:13}'.format(
            enc['name'], enc['serialNumber'], enc['enclosureType'],
            enc['rackName'], enc['isFwManaged'], enc['fwBaselineName']))
        print('\n\n')
        print('{0:7}  {1:13} {2:15} {3:9}'.format(
            'OA Bay', 'Role', 'IP Address', 'Firmware Version'))
        print('{0:7}  {1:13} {2:15} {3:9}'.format(
            '------', '----', '----------', '----------------'))
        for oa in enc['oa']:
            print('{0:7}  {1:13} {2:15} {3:9}'.format(
                oa['bayNumber'], oa['role'], oa['ipAddress'],
                oa['fwVersion']))
        print('\n\n')
        print('\n{0:15} {1:13} {2:15} {3:20} {4:25} {5:20} {6:10}'.format(
            'Server Name', 'Serial Num', 'Model', 'Systerm ROM',
            'iLO Firmware Verision', 'State', 'Licensing'))
        print('{0:15} {1:13} {2:15} {3:20} {4:25} {5:20} {6:10}\n'.format(
            '-----------', '----------', '-----------', '-----------',
            '----------------------', '-------', '----------'))
        servers = srv.get_servers()
        for ser in servers:
            print('{0:15} {1:13} {2:15} {3:20} {4:25} {5:20} {6:10}'.format(
                ser['name'], ser['serialNumber'],
                ser['shortModel'], ser['romVersion'],
                ser['mpFirmwareVersion'], ser['state'], ser['licensingIntent']))
        print('\n\n')
        print('\n{0:25} {1:45} {2:15} {3:15}'.format('Interconnect Name',
              'Module', 'Serial Number', 'FW Version'))
        print('{0:25} {1:45} {2:15} {3:15}\n'.format('-----------------',
              '------', '-------------', '----------'))
        interconnects = net.get_interconnects()
        for ic in interconnects:
            print('{0:25} {1:45} {2:15} {3:15}'.format(ic['name'],
                  ic['model'], ic['serialNumber'], ic['firmwareVersion']))
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
    parser.add_argument('-y', dest='proxy', required=False,
                        help='Proxy (host:port format')

    args = parser.parse_args()
    credential = {'userName': args.user, 'password': args.passwd}

    con = hpov.connection(args.host)
    srv = hpov.servers(con)
    net = hpov.networking(con)

    if args.proxy:
        con.set_proxy(args.proxy.split(':')[0], args.proxy.split(':')[1])
    if args.cert:
        con.set_trusted_ssl_bundle(args.cert)

    login(con, credential)
    acceptEULA(con)

    getenc(srv, net)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
