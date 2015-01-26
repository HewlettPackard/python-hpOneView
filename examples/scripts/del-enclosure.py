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


def del_all_enclosures(srv):
    enclosures = srv.get_enclosures()
    for enclosure in enclosures:
        print(('Removing Enclosure %s' % enclosure['serialNumber']))
        srv.remove_enclosure(enclosure, force=True)


def del_enclosure_by_name(srv, name):
    enclosures = srv.get_enclosures()
    for enclosure in enclosures:
        if enclosure['name'] == name:
            print(('Removing Enclosure %s' % enclosure['name']))
            srv.remove_enclosure(enclosure, force=True)


def del_enclosure_by_serial(srv, serialNumber):
    enclosures = srv.get_enclosures()
    for enclosure in enclosures:
        if enclosure['serialNumber'] == serialNumber:
            print(('Removing Enclosure %s' % enclosure['serialNumber']))
            srv.remove_enclosure(enclosure, force=True)


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
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', dest='delete_all', action='store_true',
                       help='Delete all Enclosures and exit')
    group.add_argument('-en', '--enc_name', dest='ename',
                       help='Name of enclosure to be deleted')
    group.add_argument('-es', '--enc_serial', dest='serialNo',
                       help='SerialNumber of enclosure to be deleted')

    args = parser.parse_args()
    credential = {'userName': args.user, 'password': args.passwd}

    con = hpov.connection(args.host)
    srv = hpov.servers(con)
    sts = hpov.settings(con)

    if args.proxy:
        con.set_proxy(args.proxy.split(':')[0], args.proxy.split(':')[1])
    if args.cert:
        con.set_trusted_ssl_bundle(args.cert)

    login(con, credential)
    acceptEULA(con)
    if args.delete_all:
        del_all_enclosures(srv)
        sys.exit()

    if args.serialNo:
        del_enclosure_by_serial(srv, args.serialNo)
        sys.exit()

    del_enclosure_by_name(srv, args.ename)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
