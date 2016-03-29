#!/usr/bin/env python
#
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
#
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
import re


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


def get_server(con, srv, server_id, forcePowerOff, name):
    sht = None

    if server_id.upper() == 'UNASSIGNED':
        profiles = srv.get_server_profiles()
        for profile in profiles:
            if profile['name'] == name:
                sht = con.get(profile['serverHardwareTypeUri'])
                return None, sht

        if sht is None:
            print('Error, server hardware type not found')
            sys.exit(1)

    # Get handle for named server and power off in necessary
    servers = srv.get_servers()
    located_server = None
    for server in servers:
        ips = server['mpHostInfo']['mpIpAddresses']
        for ip in ips:
            if server_id == server['name'] or server_id == ip['address']:
                located_server = server
                if server['state'] != 'NoProfileApplied':
                    print('\nError: server', server_id, 'already has a profile '
                          'defined or is being monitored\n')
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

    sht = con.get(located_server['serverHardwareTypeUri'])
    if not sht:
        print('Error, server hardware type not found')
        sys.exit()

    return located_server, sht


def increment_name(name):
    p = re.compile(r'\([0-9]+\)$')
    s = p.search(name)
    # if name ends in ([digit]) then increment the digit
    if s:
        num = int(s.group().strip('()'))
        inc = '(' + str(num + 1) + ')'
        dest_name = re.sub(r'\([0-9]+\)$', inc, name)
    else:
        dest_name = name + ' (1)'

    return dest_name


def san_vol_copy_name(sto, name):
    dest_name = increment_name(name)

    volumes = sto.get_storage_volumes()
    invalid = True
    while invalid:
        invalid = False
        for vol in volumes['members']:
            if vol['name'] == dest_name:
                dest_name = increment_name(dest_name)
                invalid = True

    return dest_name


def fix_san(con, sto, san):
    attachments = san['volumeAttachments']
    volumes = []
    for vols in attachments:
        vol = con.get_by_uri(vols['volumeUri'])
        if 'shareable' in vol:
            if not vol['shareable']:
                dest_name = san_vol_copy_name(sto, vol['name'])
                print(('\tCopying Volume %s to %s' % (vol['name'], dest_name)))
                ret = sto.copy_storage_volume(vol, dest_name)
                paths = vols['storagePaths']
                for path in paths:
                    if 'storageTargets' in path:
                        path['storageTargets'] = []
                    if 'status' in path:
                        del path['status']
                volumes.append(hpov.common.make_VolumeAttachmentV2(lun=None,
                                                                   lunType='Auto',
                                                                   volumeUri=ret['uri'],
                                                                   volumeStoragePoolUri=ret['storagePoolUri'],
                                                                   volumeStorageSystemUri=ret['storageSystemUri'],
                                                                   storagePaths=paths))
            else:
                print(('\tMapping  Volume %s' % vol['name']))
                paths = vols['storagePaths']
                for path in paths:
                    if 'storageTargets' in path:
                        path['storageTargets'] = []
                    if 'status' in path:
                        del path['status']
                volumes.append(hpov.common.make_VolumeAttachmentV2(lun=None,
                                                                   lunType='Auto',
                                                                   volumeUri=vol['uri'],
                                                                   volumeStoragePoolUri=vol['storagePoolUri'],
                                                                   volumeStorageSystemUri=vol['storageSystemUri'],
                                                                   storagePaths=paths))

    san_storage = hpov.common.make_SanStorageV3(san['hostOSType'], True, None)
    san_storage['volumeAttachments'] = volumes
    return san_storage


def copy_profile(con, srv, sto, name, dest, server, sht):
    profiles = srv.get_server_profiles()
    for profile in profiles:
        if profile['name'] == dest:
            print('Error: profile with name', dest, 'already exsists')
            sys.exit()

    for profile in profiles:
        if profile['name'] == name:
            print(('Copying Profile %s' % profile['name']))
            profile['name'] = dest
            if 'serverHardwareUri' in profile:
                if server is not None:
                    profile['serverHardwareUri'] = server['uri']
                else:
                    del profile['serverHardwareUri']
            if 'uri' in sht:
                profile['serverHardwareTypeUri'] = sht['uri']
            if 'created' in profile:
                del profile['created']
            if 'serialNumber' in profile:
                del profile['serialNumber']
            if 'taskUri' in profile:
                del profile['taskUri']
            if 'uri' in profile:
                del profile['uri']
            if 'uuid' in profile:
                del profile['uuid']
            if 'enclosureBay' in profile:
                del profile['enclosureBay']
            if 'enclosureUri' in profile:
                del profile['enclosureUri']
            if 'connections' in profile:
                connections = profile['connections']
                for conn in connections:
                    if 'interconnectUri' in conn:
                        del conn['interconnectUri']
                    if 'allocatedMbps' in conn:
                        del conn['allocatedMbps']
                    if 'deploymentStatus' in conn:
                        del conn['deploymentStatus']
                    if 'macType' in conn:
                        if conn['macType'] == 'Virtual':
                            if 'mac' in conn:
                                del conn['mac']
                            if 'wwpnType' in conn:
                                if conn['wwpnType'] == 'Virtual':
                                    if 'wwnn' in conn:
                                        del conn['wwnn']
                                    if 'wwpn' in conn:
                                        del conn['wwpn']
            if 'sanStorage' in profile:
                if profile['sanStorage']['manageSanStorage'] is True:
                    san_storage = fix_san(con, sto, profile['sanStorage'])
                    profile['sanStorage'] = san_storage

            ret = srv.post_server_profile(profile)

            if 'serialNumberType' in ret:
                print('\n\nName:                ', ret['name'])
                print('Description:         ', ret['description'])
                print('Type:                ', ret['type'])
                print('wwnType:             ', ret['wwnType'])
                print('macType:             ', ret['macType'])
                print('serialNumberType:    ', ret['serialNumberType'])
                print('Firmware:')
                print('  manageFirmware:       ',
                      ret['firmware']['manageFirmware'])
                print('  forceInstallFirmware: ', ret[
                    'firmware']['forceInstallFirmware'])
                print('  firmwareBaselineUri:  ', ret[
                    'firmware']['firmwareBaselineUri'])
                print('Bios:')
                print('  manageBios:         ', ret['bios']['manageBios'])
                print('  overriddenSettings: ',
                      ret['bios']['overriddenSettings'])
                print('Boot:')
                print('  manageBoot:         ', ret['boot']['manageBoot'])
                print('  order:              ', ret['boot']['order'], '\n')
            else:
                pprint(ret)

            sys.exit(0)

    print(('Can not locate profile: %s' % name))

def main():
    parser = argparse.ArgumentParser(add_help=True,
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description='''
   Copy Server Profile

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
    Trusted SSL Certificate Bundle in PEM (Base64 EncodedDER) Format''')
    parser.add_argument('-y', dest='proxy', required=False,
                        help='''
    Proxy (host:port format''')
    parser.add_argument('-j', dest='domain', required=False,
                        default='Local',
                        help='''
    HP OneView Authorized Login Domain''')
    parser.add_argument('-n', dest='name', required=True,
                        help='''
    Name of the source server profile''')
    parser.add_argument('-d', dest='dest', required=True,
                        help='''
    Name of the destination  server profile''')
    parser.add_argument('-f', dest='forcePowerOff',
                        required=False,
                        action='store_true',
                        help='''
    When set, forces power off of target server.
    Avoids error exit if server is up''')
    parser.add_argument('-s', dest='server_id', required=True,
                        help='''
    Destination  Server identification. There are multiple ways to specify
    the server id:

    . Hostname or IP address of the stand-alone server iLO
    . Server Hardware name of a server than has already been imported
      into HP OneView and is listed under Server Hardware
    . "UNASSIGNED" for creating an unassigned Server Profile''')
    args = parser.parse_args()
    credential = {'authLoginDomain': args.domain.upper(), 'userName': args.user, 'password': args.passwd}

    con = hpov.connection(args.host)
    srv = hpov.servers(con)
    sto = hpov.storage(con)

    if args.proxy:
        con.set_proxy(args.proxy.split(':')[0], args.proxy.split(':')[1])
        if args.cert:
            con.set_trusted_ssl_bundle(args.cert)

    login(con, credential)
    acceptEULA(con)

    server, sht = get_server(con, srv, args.server_id, args.forcePowerOff,
                             args.name)
    copy_profile(con, srv, sto, args.name, args.dest, server, sht)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
