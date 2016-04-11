#!/usr/bin/env python
###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
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

PYTHON_VERSION = sys.version_info[:3]
PY2 = (PYTHON_VERSION[0] == 2)
if PY2:
    if PYTHON_VERSION < (2, 7, 9):
        raise Exception('Must use Python 2.7.9 or later')
elif PYTHON_VERSION < (3, 4):
    raise Exception('Must use Python 3.4 or later')

import hpOneView as hpov
from pprint import pprint
import json
from hpOneView.common import uri


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
    # Login with given credentials
    try:
        con.login(credential)
    except:
        print('Login failed')


def get_eg_from_arg(srv, name):
    if srv and name:
        if name.startswith('/rest') and uri['enclosureGroups'] in name:
            return name
        else:
            egs = srv.get_enclosure_groups()
            for eg in egs:
                if eg['name'] == name:
                    return eg['uri']
    return None


def get_sht_from_arg(srv, name):    
    if srv and name:
        if name.startswith('/rest') and uri['server-hardware-types'] in name:
            return name
        else:
            shts = srv.get_server_hardware_types()
            for sht in shts:
                if sht['name'] == name:
                    return sht['uri']
    return None


def define_profile_template(
                            srv,
                            name,
                            desc,
                            sp_desc,
                            server_hwt,
                            enc_group,
                            affinity,
                            hide_flexnics,
                            conn_list):
    
    if conn_list:
        # read connection list from file
        conn = json.loads(open(conn_list).read())
    else:
        conn = []
       
    profile_template = srv.create_server_profile_template(
                                              name=name,
                                              description=desc,
                                              serverProfileDescription=sp_desc,
                                              serverHardwareTypeUri=server_hwt,
                                              enclosureGroupUri=enc_group,
                                              affinity=affinity,
                                              hideUnusedFlexNics=hide_flexnics,
                                              profileConnectionV4=conn)

    if 'serialNumberType' in profile_template:
        print('\n\nName:                ', profile_template['name'])
        print('Type:                ', profile_template['type'])
        print('Description:         ', profile_template['description'])        
        print('serialNumberType:    ', profile_template['serialNumberType'])
        print('Connections:')
        for connection in profile_template['connections']:
            print('  name:          ', connection['name'])
            print('  functionType:  ', connection['functionType'])
            print('  networkUri:    ', connection['networkUri'])
        print('Firmware:')
        print('  manageFirmware:       ', profile_template['firmware']['manageFirmware'])
        print('  forceInstallFirmware: ', profile_template['firmware']['forceInstallFirmware'])
        print('  firmwareBaselineUri:  ', profile_template['firmware']['firmwareBaselineUri'])
        print('Bios:')
        print('  manageBios:         ', profile_template['bios']['manageBios'])
        print('  overriddenSettings: ', profile_template['bios']['overriddenSettings'])
        print('Boot:')
        print('  manageBoot:         ', profile_template['boot']['manageBoot'])
        print('  order:              ', profile_template['boot']['order'], '\n')
    else:
        pprint(profile_template)


def main():
    parser = argparse.ArgumentParser(add_help=True,
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description='''
    Define a server profile template''')
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
    parser.add_argument('-n', dest='name',
                        required=True,
                        help='''
    Name of the profile template''')
    parser.add_argument('-d', dest='desc',
                        required=False,
                        help='''
    Description for the server profile template''')
    parser.add_argument('-spd', dest='sp_desc',
                        required=False,
                        help='''
    Server profile description''')
    parser.add_argument('-sht', dest='server_hwt', required=True,
                        help='''
    Server hardware type is required for defining an unassigned profile. Note
    the Server Hardware Type must be present in the HP OneView appliance
    before it can be used. For example, a single server with the specific server
    hardware type must have been added to OneView for that hardware type to
    be used. The example script get-server-hardware-types.py with the -l
    argument can be used to get a list of server hardware types that have
    been imported into the OneView appliance''')
    parser.add_argument('-eg', dest='enc_group', required=True,
                        help='''
    Identifies the enclosure group for which the Server Profile Template
    was designed. The enclosureGroupUri is determined when the profile
    template is created and cannot be modified
                        ''')
    parser.add_argument('-af', dest='affinity',
                        required=False, choices=['Bay', 'BayAndServer'],
                        default='Bay',
                        help='''
    This identifies the behavior of the server profile when the server
    hardware is removed or replaced.

        . Bay:  This profile remains with the device bay when the server
                hardware is removed or replaced.

        . BayAndServer This profile is pinned to both the device bay and
          specific server hardware.''')
    parser.add_argument('-hn', dest='hide_flexnics',
                        required=False, choices=['true', 'false'],
                        help='''
    This setting controls the enumeration of physical functions that do not
    correspond to connections in a profile. Using this flag will SHOW unused
    FlexNICs to the Operating System. Changing this setting may alter the order
    of network interfaces in the Operating System. This option sets the 'Hide
    Unused FlexNICs' to disabled, eight FlexNICs will be enumerated in the
    Operating System as network interfaces for each Flex-10 or FlexFabric
    adapter.  Configuring Fibre Channel connections on a FlexFabric adapter may
    enumerate two storage interfaces, reducing the number of network interfaces
    to six. The default (this option is not selected) enables 'Hide Unused
    FlexNICs' and may suppress enumeration of FlexNICs that do not correspond
    to profile connections. FlexNICs are hidden in pairs, starting with the 4th
    pair. For instance, if the 4th FlexNIC on either physical port corresponds
    to a profile connection, all eight physical functions are enumerated. If a
    profile connection corresponds to the 2nd FlexNIC on either physical port,
    but no connection corresponds to the 3rd or 4th FlexNIC on either physical
    port, only the 1st and 2nd physical functions are enumerated in the
    Operating System.''')
    parser.add_argument('-cl', dest='conn_list',
                        required=False,
                        help='''
    File with list of connections for this profile in JSON format. This file
    can be created with multiple calls to define-connection-list.py''')
    
    args = parser.parse_args()
    credential = {'userName': args.user, 'password': args.passwd}

    con = hpov.connection(args.host)
    srv = hpov.servers(con)

    if args.proxy:
        con.set_proxy(args.proxy.split(':')[0], args.proxy.split(':')[1])
    if args.cert:
        con.set_trusted_ssl_bundle(args.cert)

    login(con, credential)
    acceptEULA(con)

    eg = get_eg_from_arg(srv, args.enc_group)
                
    sht = get_sht_from_arg(srv, args.server_hwt)

    define_profile_template(
                            srv,
                            args.name,
                            args.desc,
                            args.sp_desc,
                            sht,
                            eg,
                            args.affinity,
                            args.hide_flexnics,
                            args.conn_list)


if __name__ == '__main__':
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
