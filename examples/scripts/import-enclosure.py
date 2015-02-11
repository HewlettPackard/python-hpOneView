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


def impenc(srv, sts, eg, ip, usr, pas, lic, baseline):
    # Locate the enclosure group
    egroups = srv.get_enclosure_groups()
    for group in egroups:
        if group['name'] == eg:
            egroup = group
        else:
            print('ERROR: Importing Enclosure')
            print('Enclosure Group: "%s" has not been defined' % eg)
            print('')
            sys.exit()

    print('Adding Enclosure')
    # Find the first Firmware Baseline
    uri = ''
    if baseline:
        spps = sts.get_spps()
        for spp in spps:
            if spp['isoFileName'] == baseline:
                uri = spp['uri']
        if not uri:
            print('ERROR: Locating Firmeware Baseline SPP')
            print('Baseline: "%s" can not be located' % baseline)
            print('')
            sys.exit()

    if not uri:
        add_enclosure = hpov.common.make_enclosure_dict(ip, usr, pas,
                                                        egroup['uri'],
                                                        licenseIntent=lic)
    else:
        add_enclosure = hpov.common.make_enclosure_dict(ip, usr, pas,
                                                        egroup['uri'],
                                                        licenseIntent=lic,
                                                        firmwareBaseLineUri=uri)

    enclosure = srv.add_enclosure(add_enclosure)
    pprint(enclosure)


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
    parser.add_argument('-eu', '--enc_user', dest='encusr', required=True,
                        help='Administrative username for the c7000 enclosure OA')
    parser.add_argument('-ep', '--enc_pass', dest='encpass', required=True,
                        help='Administrative password for the c7000 enclosure OA')
    parser.add_argument('-e', dest='enc', required=True,
                        help='IP address of the c7000 to import into HP OneView')
    parser.add_argument('-n', '--name', dest='egroup', required=True,
                        help='Enclosure Group to add the enclosure to')
    parser.add_argument('-s', '--spp', dest='spp', required=False,
                        help='SPP file name to use as the firmware baseline')
    parser.add_argument('-l', '--license', dest='license', required=False,
                        help='Apply OneView or OneView w/o iLO license to '
                        'servers in the enclosure specify either OneView or '
                        'OneViewNoiLO')

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

    impenc(srv, sts, args.egroup, args.enc, args.encusr, args.encpass,
           args.license, args.spp)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
