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
sys_ver = sys.version_info
if sys_ver == 2:
	if sys.version_info < (2, 9):
		raise Exception('Must use Python 2.9 or later')
elif sys_ver == 3:
	if sys.version_info < (3, 4):
		raise Exception('Must use Python 3.4 or later')

import hpOneView as hpov
from pprint import pprint


def acceptEULA(con):
    # See if we need to accept the EULA before we try to log in
    con.get_eula_status()
    try:
        if con.get_eula_status() is True:
            print("EULA display needed")
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


def get_alerts(act, status, severity, category):
    if status:
        alerts = act.get_alerts(status)
    else:
        alerts = act.get_alerts()

    for alert in alerts:
        if not severity and not category:
                pprint(alert)
        elif not severity and category:
            if alert['healthCategory'] == category:
                pprint(alert)
        elif not category and severity:
            if alert['severity'] == severity:
                pprint(alert)
        elif category and severity:
            if alert['healthCategory'] == category and \
               alert['severity'] == severity:
                pprint(alert)


def main():
    parser = argparse.ArgumentParser(add_help=True,
                        formatter_class=argparse.RawTextHelpFormatter,
                                     description='''
    Display alerts

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
    parser.add_argument('-s', dest='status', required=False,
                        choices=['Active', 'Cleared'],
                        help='''
    Alerts with given alert state will be returned.  State values include
    Active and Cleared''')
    parser.add_argument('-v', dest='severity', required=False,
                        choices=['Unknown', 'OK', 'Disabled', 'Warning',
                                 'Critical'],
                        help='''
    Alerts with given severity will be returned.''')
    parser.add_argument('-t', dest='category', required=False,
                        choices=['Appliance', 'ConnectionInstance',
                                 'DeviceBay', 'Enclosure', 'Fan',
                                 'fc-device-managers', 'Firmware', 'Host',
                                 'Instance', 'interconnect', 'InterconnectBay',
                                 'licenses', 'logical-interconnect',
                                 'LogicalSwitch', 'Logs',
                                 'ManagementProcessor', 'Memory', 'Network',
                                 'None', 'Operational', 'Power', 'Processor',
                                 'RemoteSupport', 'Storage', 'Thermal',
                                 'Unknown'],
                        help='''
    Alerts with given health category will be returned.''')

    args = parser.parse_args()
    credential = {'userName': args.user, 'password': args.passwd}

    con = hpov.connection(args.host)
    act = hpov.activity(con)

    if args.proxy:
        con.set_proxy(args.proxy.split(':')[0], args.proxy.split(':')[1])
    if args.cert:
        con.set_trusted_ssl_bundle(args.cert)

    login(con, credential)
    acceptEULA(con)

    get_alerts(act, args.status, args.severity, args.category)


if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
