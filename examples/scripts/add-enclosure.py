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


def import_enclosure(srv, sts, eg, ip, usr, pas, lic, baseline, force, forcefw):
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
                                                        licenseIntent=lic,
                                                        force=force,
                                                        forcefw=forcefw)
    else:
        add_enclosure = hpov.common.make_enclosure_dict(ip, usr, pas,
                                                        egroup['uri'],
                                                        licenseIntent=lic,
                                                        firmwareBaseLineUri=uri,
                                                        force=force,
                                                        forcefw=forcefw)

    enclosure = srv.add_enclosure(add_enclosure)
    if 'enclosureType' in enclosure:
        print('Type:          ', enclosure['enclosureType'])
        print('Name:          ', enclosure['name'])
        print('Rack:          ', enclosure['rackName'])
        print('Serial Number: ', enclosure['serialNumber'])
    else:
        pprint(enclosure)


def main():
    parser = argparse.ArgumentParser(add_help=True,
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description='''
    This example script will import an enclosure into HP OneView as a
    managed device.  The Onboard Administrator needs to have IP Address
    configured for each module, and a valid Administrator account with a
    password.

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
    parser.add_argument('-eu', dest='encusr', required=True,
                        help='''
    Administrative username for the c7000 enclosure OA''')
    parser.add_argument('-ep',  dest='encpass', required=True,
                        help='''
    Administrative password for the c7000 enclosure OA''')
    parser.add_argument('-oa', dest='enc', required=True,
                        help='''
    IP address of the c7000 to import into HP OneView''')
    parser.add_argument('-eg', dest='egroup', required=True,
                        help='''
    Enclosure Group to add the enclosure to''')
    parser.add_argument('-s', dest='spp', required=False,
                        help='''
    SPP Baseline file name. e.g. SPP2013090_2013_0830_30.iso''')
    parser.add_argument('-l', dest='license', required=False,
                        choices=['OneView', 'OneViewNoiLO'],
                        default='OneView',
                        help='''
    Specifies whether the intent is to apply either OneView or
    OneView w/o iLO licenses to the servers in the enclosure
    being imported.

    Accepted values are:

        - OneView
        - OneViewNoiLO ''')
    parser.add_argument('-f', dest='force', action='store_true',
                        required=False,
                        help='''
    When attempting to add an Enclosure to the appliance, the appliance will
    validate the target Enclosure is not already claimed.  If it is, this
    parameter is used when the Enclosure has been claimed by another appliance
    to bypass the confirmation prompt, and force add the import of the
    Enclosure ''')
    parser.add_argument('-fw', dest='forcefw', action='store_true',
                        required=False,
                        help='''
    Force the installation of the provided Firmware Baseline. ''')
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

    import_enclosure(srv, sts, args.egroup, args.enc, args.encusr,
                     args.encpass, args.license, args.spp, args.force,
                     args.forcefw)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
