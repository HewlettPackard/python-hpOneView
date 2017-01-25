# -*- coding: utf-8 -*-

"""
profile.py
~~~~~~~~~~~~
This module implements some common helper functions for building a server profile
and server profile template in OneView.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import json
import re
from future import standard_library
from hpOneView.common import (make_FirmwareSettingsV3, make_LogicalDriveV3, make_LocalStorageEmbeddedController,
                              make_LocalStorageSettingsV3, make_BootModeSetting, make_BootSettings)
from hpOneView.exceptions import HPOneViewInvalidResource, HPOneViewException

standard_library.install_aliases()


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
def make_firmware_dict(settings, baseline):
    """
    Create a firmware settings dictionary for use in defining either a server
    profile or server profile template.
    """
    uri = ''

    if baseline:
        # The OneView appliance converts '.' in the filename to '_', except for
        # the final one
        baseline = baseline.replace('.', '_').replace('_iso', '.iso')

        spps = settings.get_spps()
        for spp in spps:
            if spp['isoFileName'] == baseline:
                uri = spp['uri']
        if not uri:
            message = 'ERROR: Locating Firmware Baseline SPP\n Baseline: "%s" can not be located' % baseline
            raise HPOneViewInvalidResource(message)

    if uri:
        fw_settings = make_FirmwareSettingsV3(uri, 'FirmwareOnly', True, False)
    else:
        fw_settings = None

    return fw_settings


def make_local_storage_dict(sht, raidlevel, lboot, init_storage, num, drive_name):
    """
    Create a local storage dictionary for use in defining either a server
    profile or server profile template.
    """
    if 'model' in sht:
        model = sht['model']
    else:
        raise HPOneViewInvalidResource('Error, can not retrieve server model')

    if raidlevel or init_storage:
        p = re.compile('.*DL\d.*', re.IGNORECASE)
        match = p.match(model)
        if match:
            raise HPOneViewInvalidResource('Local storage management is not supported on DL servers')

        # FIXME -- Add a test to verify that the number of physical drives
        # is consistent with the RAID level and the number of drives in the
        # server hardware type

        drives = []
        drives.append(make_LogicalDriveV3(bootable=lboot,
                                          driveName=drive_name,
                                          driveTechnology=None,
                                          numPhysicalDrives=num,
                                          raidLevel=raidlevel))

        controllers = []
        controllers.append(make_LocalStorageEmbeddedController(importConfiguration=True,
                                                               initialize=init_storage,
                                                               LogicalDrives=drives,
                                                               managed=True,
                                                               mode='RAID'))
        local_storage = make_LocalStorageSettingsV3(controllers)

        return local_storage
    return None


def __get_boot_settings_dict_capabilities(sht):
    if 'capabilities' in sht and 'bootCapabilities' in sht:
        if 'ManageBootOrder' not in sht['capabilities']:
            raise HPOneViewInvalidResource('Error, server does not support managed  boot order')
        allowed_boot = sht['bootCapabilities']
        return allowed_boot
    else:
        raise HPOneViewInvalidResource('Error, can not retrieve server boot capabilities')


def __get_boot_settings_dict_mode(sht):
    if 'model' in sht:
        model = sht['model']
        return model
    else:
        raise HPOneViewInvalidResource('Error: Can not identify server hardware type model')


def __validate_allowed_boot(allowed_boot, boot_order):
    # The FibreChannelHba boot option is not exposed to the user
    if 'FibreChannelHba' in allowed_boot:
        allowed_boot.remove('FibreChannelHba')

    if len(boot_order) != len(allowed_boot):
        message = 'Error: All supported boot options are required. The supported options are: ' + \
                  ('; '.join(allowed_boot))
        raise HPOneViewInvalidResource(message)

    # Error if the users submitted and boot option that is
    # not supported by the server hardware type
    diff = set(boot_order).difference(set(allowed_boot))
    if diff:
        message = 'Error: "' + ', '.join(diff) + '" are not supported boot options for this server hardware ' \
                                                 'type. The supported options are: ' + '; '.join(allowed_boot)
        raise HPOneViewInvalidResource(message)


def __get_boot_settings_dict_boot_mode(gen9, boot_mode, pxe):
    # bootmode can not be set for Gen 7 & 8
    bootmode = None
    if gen9:
        if boot_mode == 'BIOS':
            bootmode = make_BootModeSetting(True, boot_mode, None)
        else:
            bootmode = make_BootModeSetting(True, boot_mode, pxe)
    return bootmode


def add_connection(srv_profile, id, name, function_type, network_uri, port_id,
                   requested_mbps, boot, mac=None, requested_vfs='Auto', wwnn=None, wwpn=None):
    """
    Adds a connection to a server profile resource (dict only).

    Args:
        srv_profile (dict): Server profile resource to update.
        id (int): A unique identifier for this connection.
        name (str): A string used to identify the respective connection.
        function_type (str): Type of function required for the connection.
        network_uri (str): Identifies the network or network set to be connected.
        port_id: Identifies the port (FlexNIC) used for this connection.
        requested_mbps: The transmit throughput (mbps) that should be allocated to this connection.
        boot (dict): Indicates that the server will attempt to boot from this connection.
        mac (str): The MAC address that is currently programmed on the FlexNic.
        requested_vfs: This value can be "Auto" or 0.
        wwnn: The node WWN address that is currently programmed on the FlexNIC.
        wwpn: The port WWN address that is currently programmed on the FlexNIC.

    Examples:

        >>> profile.add_connection(server_profile_dict,
        >>>                        id=2,
        >>>                        port_id=None,
        >>>                        name="Network name",
        >>>                        function_type='Ethernet',
        >>>                        requested_mbps=2500,
        >>>                        network_uri='/rest/ethernet-networks/2f2bf8e2-3e1a-42a8-9aff-64b04314bf3c',
        >>>                        boot={
        >>>                            "priority": "NotBootable"
        >>>                        })

    """

    connections = srv_profile.get('connections')

    new_connection = {
        "id": id,
        "name": name,
        "functionType": function_type,
        "portId": port_id,
        "requestedMbps": requested_mbps,
        "networkUri": network_uri,
        "boot": boot,
        'mac': mac,
        'requestedVFs': requested_vfs,
        'wwnn': wwnn,
        'wwpn': wwpn
    }

    updated = False
    for connection in connections:
        if connection['name'] == name:
            raise HPOneViewException("The connection name is already used by another connection within the profile.")

        if connection['id'] == id:
            connection.clear()
            connection.update(new_connection)
            updated = True

    if not updated:
        connections.append(new_connection)


def remove_connection(srv_profile, connection_name):
    """
    Removes a connection from the server profile resource (dict only).

    Args:
        srv_profile: Server profile resource to update.
        connection_name (str): The connection name to delete.

    Examples:
        >>> profile.remove_connection(server_profile_dict, "Connection name")

    """
    connections = srv_profile.get('connections')
    srv_profile['connections'] = [item for item in connections if item['name'] != connection_name]


def make_boot_settings_dict(srv, sht, disable_manage_boot, boot_order, boot_mode, pxe):
    """
    Create boot settings and boot mode dictionaries for use in defining either a server
    profile or server profile template.
    """
    gen9 = False
    # Get the bootCapabilites from the Server Hardware Type
    allowed_boot = __get_boot_settings_dict_capabilities(sht)

    model = __get_boot_settings_dict_mode(sht)

    regx = re.compile('.*Gen9.*', re.IGNORECASE)
    gen_match = regx.match(model)

    if gen_match:
        gen9 = True

    # Managed Boot Enable with Boot Options specified
    if boot_order:
        __validate_allowed_boot(allowed_boot, boot_order)

        bootmode = __get_boot_settings_dict_boot_mode(gen9, boot_mode, pxe)
        boot = make_BootSettings(boot_order, manageBoot=True)

    # Managed Boot Default value WITHOUT Boot Options specified
    # Setting boot to None uses the default from the appliance which is
    # boot.manageBoot = True.
    elif not disable_manage_boot:
        bootmode = __get_boot_settings_dict_boot_mode(gen9, boot_mode, pxe)
        boot = None

    # Managed Boot explicitly disabled
    elif disable_manage_boot:
        # For a Gen 9 BL server hardware "boot.manageBoot" cannot be set to
        # true unless "bootMode" is specified and "bootMode.manageMode" is set
        # to 'true'.
        p = re.compile('.*BL\d.*', re.IGNORECASE)
        match = p.match(model)
        if match:
            raise HPOneViewInvalidResource('Error: bootMode cannot be disabled on BL servers')
        else:  # bootmode can not be set for Gen 7 & 8
            bootmode = None

        boot = make_BootSettings([], manageBoot=False)

    else:
        raise HPOneViewInvalidResource('Error: Unknown boot mode case')

    return boot, bootmode


def make_bios_dict(bios_list):
    '''
    Create a bios dictionary for use in defining either a server
    profile or server profile template.
    '''
    if bios_list:
        try:
            bios = json.loads(open(bios_list).read())

            overriddenSettings = []
            overriddenBios = {}
            for b in bios:
                overriddenSetting = {}
                overriddenSetting['id'] = b['id']
                if 'options' in b and len(b['options']) > 0:
                    overriddenSetting['value'] = b['options'][0]['id']
                overriddenSettings.append(overriddenSetting)

            overriddenBios['manageBios'] = True
            overriddenBios['overriddenSettings'] = overriddenSettings
            return overriddenBios
        except ValueError:
            raise ValueError('Error: Cannot parse BIOS JSON file. JSON must be well-formed.')
