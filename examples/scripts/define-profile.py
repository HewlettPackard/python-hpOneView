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
import re
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


def boot_settings(con, srv, server, disable_manage_boot, boot_order, boot_mode, pxe,
                  conn_list):

    gen9 = False
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

    if 'model' in sht:
        model = sht['model']
    else:
        print('Error: Can not identify server hardware type model')
        sys.exit()

    regx = re.compile('.*Gen9.*', re.IGNORECASE)
    gen_match = regx.match(model)

    if gen_match:
        gen9 = True

    # Managed Boot Enable with Boot Options specified
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

        if gen9:
            if boot_mode == 'BIOS':
                bootmode = hpov.common.make_bootmode_settings_dict(True,
                                                                   boot_mode,
                                                                   None)
            else:
                bootmode = hpov.common.make_bootmode_settings_dict(True,
                                                                   boot_mode,
                                                                   pxe)
        else:  # bootmode can not be set for Gen 7 & 8
            bootmode = None

        boot = hpov.common.make_boot_settings_dict(boot_order, manageBoot=True)

    # Managed Boot Default value WITHOUT Boot Options specified
    # Setting boot to None uses the default from the appliance which is
    # boot.manageBoot = True.
    elif not disable_manage_boot:
        if gen9:
            if boot_mode == 'BIOS':
                bootmode = hpov.common.make_bootmode_settings_dict(True,
                                                                   boot_mode,
                                                                   None)
            else:
                bootmode = hpov.common.make_bootmode_settings_dict(True,
                                                                   boot_mode,
                                                                   pxe)

        else:  # bootmode can not be set for Gen 7 & 8
            bootmode = None

        boot = None

    # Managed Boot explicity disabled
    elif disable_manage_boot:
        # For a Gen 9 BL server hardware "boot.manageBoot" cannot be set to
        # true unless "bootMode" is specified and "bootMode.manageMode" is set
        # to 'true'.
        p = re.compile('.*BL\d.*', re.IGNORECASE)
        match = p.match(model)
        if match:
            print('Error: bootMode cannot be disabled on BL servers')
            sys.exit()
        else:  # bootmode can not be set for Gen 7 & 8
            bootmode = None

        boot = hpov.common.make_boot_settings_dict([], manageBoot=False)

    else:
        print('Error: Unknown boot mode case')
        sys.exit()

    return boot, bootmode


def define_profile(con, srv, profileName, desc, server, boot, bootmode, fw,
                   conn_list):

    if conn_list:
        # read connection list from file
        conn = json.loads(open(conn_list).read())
    else:
        conn = []

    profile_dict = hpov.common.make_profile_dict(profileName, server, desc, fw,
                                                boot, bootmode, conn)

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
    parser.add_argument('-mb', dest='disable_manage_boot',
                        action='store_true',
                        help='''
    Explicitly DISABLE Boot Order Management. This value is enabled by
    default and required for Connection boot enablement. If this optoin is
    disabled, then  PXE and FC BfS settings are disabled within the entire
    Server Profile.''')
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
    parser.add_argument('-bm', dest='boot_mode', required=False,
                        choices=['UEFI', 'UEFIOptimized', 'BIOS'],
                        default='BIOS',
                        help='''
    Specify the Gen9 Boot Envrionment.

    Sets the boot mode as one of the following:

        . UEFI
        . UEFIOptimized
        . BIOS

    If you select UEFI or UEFI optimized for an HP ProLiant DL Gen9 rack
    mount server, the remaining boot setting available is the PXE boot policy.

    For the UEFI or UEFI optimized boot mode options, the boot mode choice
    should be based on the expected OS and required boot features for the
    server hardware. UEFI optimized boot mode reduces the time the system
    spends in POST(Video driver initialization). In order to select the
    appropriate boot mode, consider the following:

        . If a secure boot is required, the boot mode must be set to UEFI
          or UEFI optimized .
        . For operating systems that do not support UEFI (such as DOS, or
          older versions of Windows and Linux), the boot mode must be set
          to BIOS.
        . When booting in UEFI mode, Windows 7, Server 2008, or 2008 R2
          should not be set to UEFIOptimized.''')
    parser.add_argument('-px', dest='pxe', required=False,
                        choices=['Auto', 'IPv4', 'IPv6',
                                 'IPv4ThenIPv6', 'IPv6ThenIPv4'],
                        default='IPv4',
                        help='''
    Controls the ordering of the network modes available to the Flexible
    LOM (FLB); for example, IPv4 and IPv6.

    Select from the following policies:

        . Auto
        . IPv4 only
        . IPv6 only
        . IPv4 then IPv6
        . IPv6 then IPv4

    Setting the policy to Auto means the order of the existing network boot
    targets in the UEFI Boot Order list will not be modified, and any new
    network boot targets will be added to the end of the list using the
    System ROM's default policy.''')
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

    if args.boot_order and args.disable_manage_boot:
        print('Error: Managed Boot must be enabled to define a boot order')
        sys.exit()

    server = get_server(srv, args.server_name, args.server_ip,
                        args.forcePowerOff)
    boot, bootmode = boot_settings(con, srv, server, args.disable_manage_boot,
                                   args.boot_order, args.boot_mode, args.pxe,
                                   args.conn_list)
    fw_settings = get_fw_settings(sts, args.baseline)
    define_profile(con, srv, args.name, args.desc, server, boot, bootmode,
                   fw_settings, args.conn_list)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
