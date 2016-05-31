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
import re

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


def add_rack(fac, name, sn, thermal, height, depth, width, uheight):
    rack = hpov.common.make_rack_dict(name, sn, thermal, height, depth,
                                      width, uheight)
    ret = fac.add_rack(rack)
    if 'model' in ret:
        print('Name:          ', ret['name'])
        print('Model:         ', ret['model'])
        print('Thermal Limit: ', ret['thermalLimit'])
        print('Depth:         ', ret['depth'])
        print('Width:         ', ret['width'])
        print('Height:        ', ret['height'])
        print('U-Height:      ', ret['uHeight'])
    else:
        pprint(ret)


def main():
    parser = argparse.ArgumentParser(add_help=True,
                        formatter_class=argparse.RawTextHelpFormatter,
                                     description='''
    Add a new Rack resource

    Usage: ''')
    parser.add_argument('-a', dest='host', required=True,
                        help='''
    HPE OneView Appliance hostname or IP address''')
    parser.add_argument('-u', dest='user', required=False,
                        default='Administrator',
                        help='''
    HPE OneView Username''')
    parser.add_argument('-p', dest='passwd', required=True,
                        help='''
    HPE OneView Password''')
    parser.add_argument('-c', dest='cert', required=False,
                        help='''
    Trusted SSL Certificate Bundle in PEM (Base64 Encoded DER) Format''')
    parser.add_argument('-y', dest='proxy', required=False,
                        help='''
    Proxy (host:port format''')
    parser.add_argument('-j', dest='domain', required=False,
                        default='Local',
                        help='''
    HPE OneView Authorized Login Domain''')
    parser.add_argument('-n', dest='name',
                        required=True,
                        help='''
    Name of the Rack''')
    parser.add_argument('-sn', dest='sn',
                        required=False,
                        help='''
    Serial Number of the Rack''')
    parser.add_argument('-th', dest='thermal',
                        required=False,
                        help='''
    The maximum acceptable watts of heat output for the rack''')
    parser.add_argument('-he', dest='height', type=int, default=2004,
                        required=False,
                        help='''
    Rack height in millimeters''')
    parser.add_argument('-de', dest='depth', type=int, default=1000,
                        required=False,
                        help='''
    Rack depth in millimeters''')
    parser.add_argument('-wi', dest='width', type=int, default=600,
                        required=False,
                        help='''
    Rack width in millimeters''')
    parser.add_argument('-us', dest='uheight', type=int, default=42,
                        required=False,
                        help='''
    The number of u-slots in the rack between 1 and 60, default is 42''')

    args = parser.parse_args()
    credential = {'authLoginDomain': args.domain.upper(), 'userName': args.user, 'password': args.passwd}

    con = hpov.connection(args.host)
    fac = hpov.facilities(con)

    if args.proxy:
        con.set_proxy(args.proxy.split(':')[0], args.proxy.split(':')[1])
    if args.cert:
        con.set_trusted_ssl_bundle(args.cert)

    if args.uheight < 1 or args.uheight > 60:
        print('Error, the number of u-slots must be between 1 and 60')
        sys.exit()

    login(con, credential)
    acceptEULA(con)

    add_rack(fac, args.name, args.sn, args.thermal, args.height, args.depth,
             args.width, args.uheight)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
