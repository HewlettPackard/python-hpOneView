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


def add_datacenter(fac, name, cool, coolMultiplier, currency, cost,
                   lineVoltage, width, depth, deratingType, deratingPercent):

    datacenter = hpov.common.make_datacenter_dict(name, cool, coolMultiplier,
                                                  currency, cost, lineVoltage,
                                                  width, depth, deratingType,
                                                  deratingPercent)

    ret = fac.add_datacenter(datacenter)
    if 'coolingMultiplier' in ret:
        print('Name:                       ', ret['name'])
        print('Cooling Capacity:           ', ret['coolingCapacity'])
        print('Cooling Multiplier:         ', ret['coolingMultiplier'])
        print('Cost Per Kilowatt Hour:     ', ret['costPerKilowattHour'])
        print('Currency:                   ', ret['currency'])
        print('Default Power Line Voltage: ', ret['defaultPowerLineVoltage'])
        print('Derating Type:              ', ret['deratingType'])
        print('Derating Percentage:        ', ret['deratingPercentage'])
        print('Depth:                      ', ret['depth'])
        print('Width:                      ', ret['width'])
    else:
        pprint(ret)


def main():
    parser = argparse.ArgumentParser(add_help=True,
                        formatter_class=argparse.RawTextHelpFormatter,
                                     description='''
    Add a new Data Center resource

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
    parser.add_argument('-j', dest='domain', required=False,
                        default='Local',
                        help='''
    HP OneView Authorized Login Domain''')
    parser.add_argument('-n', dest='name',
                        required=True,
                        help='''
    Name of the Data Center''')
    parser.add_argument('-co', dest='cool', type=int,
                        default=0,
                        required=False,
                        help='''
    Maximum cooling capacity for the data center in watts''')
    parser.add_argument('-cm', dest='coolMultiplier',
                        required=False,
                        default=1.5, type=float,
                        help='''
    The ratio of cooling costs to power costs of the IT equipment. This
    value represents the relative cost of cooling the system compared to
    the cost of powering the system. The default value of 1.5 indicates
    that it costs 1.5 as much to cool the system as it does to power the
    system. This value is multiplied by the kilowatt - hours used by the
    system to obtain the cooling kilowatt - hours that are used in the
    analysis section of graphs that display power consumption.''')
    parser.add_argument('-ct', dest='cost', type=float,
                        required=False,
                        help='''
    Enegery cost per kilowatt-hour''')
    parser.add_argument('-cu', dest='currency',
                        default='USD',
                        required=False,
                        help='''
    The currency unit for energy cost, default is "USD"''')
    parser.add_argument('-lv', dest='lineVoltage', type=int,
                        default=220,
                        required=False,
                        help='''
    The default power line voltage used for watts/amps translation
    when voltage is not otherwise available (for example when summarizing
    power at the rack or data center level), default is 220''')
    parser.add_argument('-wi', dest='width', type=int,
                        required=True,
                        help='''
    Data Center width in millimeters''')
    parser.add_argument('-de', dest='depth', type=int,
                        required=True,
                        help='''
    Data Center depth in millimeters''')
    parser.add_argument('-dt', dest='deratingType',
                        required=True, choices=['NaJp', 'Custom', 'None'],
                        default='NaJp',
                        help='''
    The default power line voltage used for watts/amps
    translation when voltage is not otherwise available (for
    example when summarizing power at the rack or data
    center level''')
    parser.add_argument('-dp', dest='deratingPercent',
                        required=False, type=float,
                        help='''
    Custom eletrical derating percentage, this value is
    specified by the drating type, unless the type is
    Custom, then is must be specified here''')
    args = parser.parse_args()
    credential = {'authLoginDomain': args.domain.upper(), 'userName': args.user, 'password': args.passwd}

    con = hpov.connection(args.host)
    fac = hpov.facilities(con)

    if args.proxy:
        con.set_proxy(args.proxy.split(':')[0], args.proxy.split(':')[1])
    if args.cert:
        con.set_trusted_ssl_bundle(args.cert)

    if args.depth < 1000 or args.depth > 50000:
        print('Error, the depth of the data center must be between 1000 and 50000 millimeters')
        sys.exit()
    if args.width < 1000 or args.width > 50000:
        print('Error, the width of the data center must be between 1000 and 50000 millimeters')
        sys.exit()
    if args.deratingType == 'Custom' and not args.deratingPercent:
        print('Error, the derating percentage must be specified when using the Custom derating type')
        sys.exit()

    login(con, credential)
    acceptEULA(con)

    add_datacenter(fac, args.name, args.cool, args.coolMultiplier,
                   args.currency, args.cost, args.lineVoltage, args.width,
                   args.depth, args.deratingType, args.deratingPercent)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
