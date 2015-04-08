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
import json


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


def get_server(srv, server_name, server_ip, forcePowerOff):
    if server_name:
        server_id = server_name
    else:
        server_id = server_ip

    # Get handle for named server and power off in necessary
    servers = srv.get_servers()
    located_server = None
    for server in servers:
        if server['name'] == server_name or server_ip == server['mpIpAddress']:
            located_server = server
            if server['state'] != 'NoProfileApplied':
                print('\nError: server', server_id, 'already has a profile '
                      'defined\n')
                sys.exit(1)
            if server['powerState'] == 'On':
                if forcePowerOff:
                    srv.set_server_powerstate(server, 'Off', force=True)
                else:
                    print('Error: Server', server_id,
                          ' needs to be powered off')
                    sys.exit(1)
            break
    if not located_server:
        print('Server ', server_id, ' not found')
        sys.exit(1)

    return located_server


def get_fw_settings(sts, baseline):
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

    if uri:
        fw_settings = hpov.common.make_firmware_settings_dict(uri)
    else:
        fw_settings = None

    return fw_settings


def validate_boot_settings(con, srv, server, manage_boot, boot_order):

    # Get the bootCapabilites from the Server Hardwer Type
    sht = con.get(server['serverHardwareTypeUri'])
    if 'capabilities' in sht and 'bootCapabilities' in sht:
        if 'ManageBootOrder' not in sht['capabilities']:
            print('Error, server does not support managed  boot order')
            sys.exit()
        allowed_boot = sht['bootCapabilities']
    else:
        print('Error, can not retreive server boot capabilities')
        sys.exit()

    if boot_order:
        # The FibreChannelHba boot option is not exposed to the user
        if 'FibreChannelHba' in allowed_boot:
            allowed_boot.remove('FibreChannelHba')

        if len(boot_order) != len(allowed_boot):
            print('Error: All supported boot options are required')
            print('The supported options are:')
            print('\t-bo', end=' ')
            for item in allowed_boot:
                print(item, end=' ')
            print()
            sys.exit()

        # Error if the users submitted and boot option that is
        # not supported by the server hardware type
        diff = set(boot_order).difference(set(allowed_boot))
        if diff:
            print('Error:"', diff, '"are not supported boot options for this'
                  'server hardware type')
            print('The supported options are:')
            print('\t-bo', end=' ')
            for item in allowed_boot:
                print(item, end=' ')
            print()
            sys.exit()

        boot = hpov.common.make_boot_settings_dict(boot_order, manageBoot=True)

    elif manage_boot:
        boot = hpov.common.make_boot_settings_dict([], manageBoot=True)

    else:
        boot = None

    return boot


def define_profile(con, srv, profileName, desc, server, boot, fw, conn_list):

    if conn_list:
        # read connection list from file
        conn = json.loads(open(conn_list).read())
    else:
        conn = []

    profile_dict = hpov.common.make_profile_dict(profileName, server, desc, fw,
                                                boot, conn)

    profile = srv.create_server_profile(profile_dict)
    if 'serialNumberType' in profile:
        print('\n\nName:                ', profile['name'])
        print('Description:         ', profile['description'])
        print('Type:                ', profile['type'])
        print('wwnType:             ', profile['wwnType'])
        print('macType:             ', profile['macType'])
        print('serialNumberType:    ', profile['serialNumberType'])
        print('Firmware:')
        print('  manageFirmware:       ', profile['firmware']['manageFirmware'])
        print('  forceInstallFirmware: ', profile['firmware']['forceInstallFirmware'])
        print('  firmwareBaselineUri:  ', profile['firmware']['firmwareBaselineUri'])
        print('Bios:')
        print('  manageBios:         ', profile['bios']['manageBios'])
        print('  overriddenSettings: ', profile['bios']['overriddenSettings'])
        print('Boot:')
        print('  manageBoot:         ', profile['boot']['manageBoot'])
        print('  order:              ', profile['boot']['order'], '\n')
    else:
        pprint(profile_dict)


def main():
    parser = argparse.ArgumentParser(add_help=True,
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description='''
    Define a server profile''')
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
    Name of the profile''')
    parser.add_argument('-d', dest='desc',
                        required=False,
                        help='''
    Description for the server profile''')
    parser.add_argument('-f', dest='forcePowerOff',
                        required=False,
                        action='store_true',
                        help='''
    When set, forces power off of target server.
    Avoids error exit if server is up''')
    parser.add_argument('-s', dest='baseline', required=False,
                        help='''
    SPP Baseline file name. e.g. SPP2013090_2013_0830_30.iso''')
    parser.add_argument('-mb', dest='manage_boot',
                       action='store_true',
                       help='''
    Enable Boot Order Management. Required for Connection boot
    enablement.  If this optoin is disabled, then  PXE and FC BfS settings
    are disabled within the entire Server Profile.''')
    parser.add_argument('-bo', dest='boot_order', required=False,
                        nargs='+',
                        help='''
    Defines the order in which boot will be attempted on the available
    devices. Please NOTE the supported boot order is server hardware type
    specific. For Gen7 and Gen8 server hardware the possible values are 'CD',
    'Floppy', 'USB', 'HardDisk', and 'PXE'. For Gen9 BL server hardware in
    Legacy BIOS boot mode, the possible values are 'CD', 'USB', 'HardDisk',
    and 'PXE'. For Gen9 BL server hardware in UEFI or UEFI Optimized boot
    mode, only one value is allowed and must be either 'HardDisk' or 'PXE'.
    For Gen9 DL server hardware in Legacy BIOS boot mode, the possible
    values are 'CD', 'USB', 'HardDisk', and 'PXE'. For Gen9 DL server
    hardware in UEFI or UEFI Optimized boot mode, boot order configuration
    is not supported.

    Server boot order defined as a list seperatedby spaces. For example:

    Gen7/8 BIOS Default Boot Order:
                            -bo CD Floppy USB HardDisk PXE
    Gen9 Legacy BIOS Boot Order:
                            -bo CD USB HardDisk PXE
    Gen9 UEFI Default Boot Order:
                            -bo HardDisk
    ''')
    parser.add_argument('-cl', dest='conn_list',
                        required=False,
                        help='''
    File with list of connections for this profile in JSON format. This file
    can be created with multiple calls to define-connection-list.py''')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-sn', dest='server_name',
                       help='''
    Name of the standalone server hardware which this profile is for''')
    group.add_argument('-si', dest='server_ip',
                       help='''
    IP address of the standalone server iLO''')

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

    if args.boot_order and not args.manage_boot:
        print('Error: Managed Boot must be enabled to define a boot order')
        sys.exit()

    server = get_server(srv, args.server_name, args.server_ip,
                        args.forcePowerOff)
    boot = validate_boot_settings(con, srv, server, args.manage_boot,
                                  args.boot_order)
    fw_settings = get_fw_settings(sts, args.baseline)
    define_profile(con, srv, args.name, args.desc, server, boot, fw_settings,
                   args.conn_list)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
