#!/usr/bin/env python
###
# (C) Copyright (2012-2017) Hewlett Packard Enterprise Development LP
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


def add_powerdevice(fac, name, deviceType, feedIdentifier,
                    lineVoltage, model,  partNumber,
                    phaseType, ratedCapacity, serialNumber):

    powerdevice = hpov.common.make_powerdevice_dict(name, deviceType,
                                                    feedIdentifier,
                                                    lineVoltage,
                                                    model, partNumber,
                                                    phaseType,
                                                    ratedCapacity,
                                                    serialNumber)

    ret = fac.add_powerdevice(powerdevice)
    if 'feedIdentifier' in ret:
        print('Name:                       ', ret['name'])
        print('Feed Identifier:            ', ret['feedIdentifier'])
        print('Line Voltage:               ', ret['lineVoltage'])
        print('Model:                      ', ret['model'])
        print('Part Number:                ', ret['partNumber'])
        print('Phase Type:                 ', ret['phaseType'])
        print('Rated Capacity:             ', ret['ratedCapacity'])
        print('Serial Number:              ', ret['serialNumber'])
    else:
        pprint(ret)


def main():
    parser = argparse.ArgumentParser(add_help=True,
                        formatter_class=argparse.RawTextHelpFormatter,
                                     description='''
    Add a non iPDU Power Device

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
    Name of the Data Center''')
    parser.add_argument('-dt', dest='deviceType',
                        choices=['BranchCircuit', 'BreakerPanel',
                                 'HPIpduAcModule', 'HPIpduCore',
                                 'HPIpduLoadSegment', 'HPIpduOutlet',
                                 'HPIpduOutletBar', 'LoadSegment', 'Outlet',
                                 'PowerFeed', 'PowerStrip', 'RackPdu',
                                 'RackUps'],
                        default='BranchCircuit',
                        required=False,
                        help='''
    The type that this power delivery device represents,
    default is BranchCircuit''')
    parser.add_argument('-fi', dest='feedIdentifier',
                        required=False,
                        help='''
    A user provided power feed identifier string. This is an
    arbitrary string that the user may specify to describe how
    this power device is connected into their power infrastructure''')
    parser.add_argument('-lv', dest='lineVoltage', type=int,
                        required=False,
                        help='''
    The line voltage (input) of this power device in volts.
    If unspecified, the default line voltage will be used
    for power calculations.''')
    parser.add_argument('-mo', dest='model',
                        required=False,
                        help='''
    Model name of the power device''')
    parser.add_argument('-pn', dest='partNumber',
                        required=False,
                        help='''
    Part number of the power device''')
    parser.add_argument('-pt', dest='phaseType',
                        required=True,
                        choices=['SinglePhase', 'SinglePhaseIntl',
                                 'ThreePhaseDelta', 'ThreePhaseUnknown',
                                 'ThreePhaseWye', 'Unknown'],
                        help='''
    The phase type of this power device. This value is used in
    conjunction with the capacity and line voltage to determine
    the total output power for this device in watts.''')
    parser.add_argument('-rc', dest='ratedCapacity',
                        required=True, type=int,
                        help='''
    The rated capacity of this power delivery device in Amps.
    This may come from the inherent capacity of the device, or
    by an explicit circuit breaker rating between 0 and 9999.''')
    parser.add_argument('-sn', dest='serialNumber',
                        required=False,
                        help='''
    Serial number of the power device''')

    args = parser.parse_args()
    credential = {'authLoginDomain': args.domain.upper(), 'userName': args.user, 'password': args.passwd}

    con = hpov.connection(args.host)
    fac = hpov.facilities(con)

    if args.proxy:
        con.set_proxy(args.proxy.split(':')[0], args.proxy.split(':')[1])
    if args.cert:
        con.set_trusted_ssl_bundle(args.cert)

    if args.ratedCapacity < 0 or args.ratedCapacity > 9999:
        print('Error, the rated cpacity must be between 0 and 9999 Amps')
        sys.exit()

    login(con, credential)
    acceptEULA(con)

    add_powerdevice(fac, args.name, args.deviceType, args.feedIdentifier,
                    args.lineVoltage, args.model,  args.partNumber,
                    args.phaseType, args.ratedCapacity, args.serialNumber)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
