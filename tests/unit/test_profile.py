# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###
import json
import unittest

import mock

import hpOneView.profile as profile
from hpOneView.connection import connection
from hpOneView.exceptions import HPOneViewInvalidResource
from hpOneView.servers import servers
from hpOneView.settings import settings
from tests.test_utils import mock_builtin


class ProfilesTest(unittest.TestCase):

    def setUp(self):
        super(ProfilesTest, self).setUp()
        self.host = 'http://1.2.3.4'
        self.connection = connection(self.host)
        self.settings = settings(self.connection)
        self.servers = servers(self.connection)
        self.profile = profile

    @mock.patch.object(settings, 'get_spps')
    def test_make_firmware_exists(self, mock_get_spps):
        baseline = 'SPP2016020_2015_1204_63.iso'

        # build a FW response dictionary
        fw_driver = self.build_get_spp_response()

        # return the FW response when get_spps() is called
        mock_get_spps.return_value = [fw_driver]

        firmware = self.profile.make_firmware_dict(settings, baseline)

        self.assertIsNotNone(firmware)
        self.assertEqual(
            {'manageFirmware': True, 'firmwareBaselineUri': '/rest/firmware-drivers/SPP2016020_2015_1204_63',
             'forceInstallFirmware': False}, firmware)

    @mock.patch.object(settings, 'get_spps')
    def test_make_firmware_does_not_exist(self, mock_get_spps):
        baseline = 'SPP20160201_2015_1204_63.iso'

        # build a FW response dictionary
        fw_driver = self.build_get_spp_response()

        # return the FW response when get_spps() is called
        mock_get_spps.return_value = [fw_driver]

        try:
            self.profile.make_firmware_dict(settings, baseline)
        except HPOneViewInvalidResource as hp_exception:
            self.assertEqual(hp_exception.args[0], 'ERROR: Locating Firmware Baseline SPP\n Baseline: '
                                                   '"SPP20160201_2015_1204_63.iso" can not be located')
        else:
            self.fail("Expected Exception")

    def test_make_local_storage_with_bl(self):
        sht = self.build_gen8_bl_sht()
        local_storage = self.profile.make_local_storage_dict(
            sht, 'RAID0', False, False, 2, 'Operating System')
        self.assertIsNotNone(local_storage)
        self.assertEqual(
            {'controllers': [{'slotNumber': '0', 'logicalDrives': [
                             {'driveTechnology': None, 'driveName': 'Operating System', 'raidLevel': 'RAID0',
                              'bootable': False, 'numPhysicalDrives': 2}], 'importConfiguration': True,
                'mode': 'RAID', 'initialize': False, 'managed': True}]},
            local_storage)

    def test_make_local_storage_with_dl(self):
        sht = self.build_dl_sht()
        try:
            self.profile.make_local_storage_dict(
                sht, 'RAID0', False, False, 2, 'Operating System')
        except HPOneViewInvalidResource as hp_exception:
            self.assertEqual(
                hp_exception.args[0], 'Local storage management is not supported on DL servers')
        else:
            self.fail("Expected Exception")

    def test_make_local_storage_no_model(self):
        sht = self.build_gen8_bl_sht()
        sht.pop('model', None)
        try:
            self.profile.make_local_storage_dict(
                sht, 'RAID0', False, False, 2, 'Operating System')
        except HPOneViewInvalidResource as hp_exception:
            self.assertEqual(
                hp_exception.args[0], 'Error, can not retrieve server model')
        else:
            self.fail("Expected Exception")

    def test_make_boot_gen8_bl(self):
        sht = self.build_gen8_bl_sht()
        boot_order = ['CD', 'Floppy', 'USB', 'HardDisk', 'PXE']
        boot, boot_mode = self.profile.make_boot_settings_dict(
            servers, sht, False, boot_order, 'BIOS', 'Auto')
        self.assertEqual(
            {'manageBoot': True, 'order': ['CD', 'Floppy', 'USB', 'HardDisk', 'PXE']}, boot)
        self.assertIsNone(boot_mode)

    def test_make_boot_gen8_bl_disable_boot(self):
        sht = self.build_gen8_bl_sht()
        boot_order = []
        try:
            self.profile.make_boot_settings_dict(
                servers, sht, True, boot_order, 'BIOS', 'Auto')
        except HPOneViewInvalidResource as hp_exception:
            self.assertEqual(
                hp_exception.msg, 'Error: bootMode cannot be disabled on BL servers')
        else:
            self.fail("Expected Exception")

    def test_make_boot_gen9_bl(self):
        sht = self.build_gen9_bl_sht()
        boot_order = ['CD', 'USB', 'HardDisk', 'PXE']
        boot, boot_mode = self.profile.make_boot_settings_dict(
            servers, sht, False, boot_order, 'UEFI', 'Auto')
        self.assertEqual(
            {'order': ['CD', 'USB', 'HardDisk', 'PXE'], 'manageBoot': True}, boot)
        self.assertEqual(
            {'manageMode': True, 'mode': 'UEFI', 'pxeBootPolicy': 'Auto'}, boot_mode)

    def test_make_boot_gen9_bl_missing_order_options(self):
        sht = self.build_gen9_bl_sht()
        boot_order = ['CD', 'USB', 'HardDisk']
        try:
            self.profile.make_boot_settings_dict(
                servers, sht, False, boot_order, 'UEFI', 'Auto')
        except HPOneViewInvalidResource as hp_exception:
            self.assertEqual(hp_exception.args[0], 'Error: All supported boot options are required. The supported '
                                                   'options are: CD; USB; HardDisk; PXE')
        else:
            self.fail("Expected Exception")

    def test_make_boot_gen9_bl_mismatch_order_options(self):
        sht = self.build_gen9_bl_sht()
        boot_order = ['CD', 'USB', 'HardDisk', 'Floppy']
        try:
            self.profile.make_boot_settings_dict(
                servers, sht, False, boot_order, 'UEFI', 'Auto')
        except HPOneViewInvalidResource as hp_exception:
            self.assertEqual(hp_exception.args[0], 'Error: "Floppy" are not supported boot options for this server '
                                                   'hardware type. The supported options are: CD; USB; HardDisk; PXE')
        else:
            self.fail("Expected Exception")

    @mock.patch(mock_builtin('open'))
    def test_make_bios(self, mock_open):
        filename = 'bios_list'
        mock_file = mock.Mock()
        mock_file.read.return_value = self.build_bios_list()
        mock_open.return_value = mock_file
        bios = self.profile.make_bios_dict(filename)
        self.assertIsNotNone(bios)
        self.assertEqual(
            {'manageBios': True, 'overriddenSettings': [{'value': '2', 'id': '134'}]}, bios)

    @mock.patch(mock_builtin('open'))
    def test_make_bios_with_defaukt_options(self, mock_open):
        filename = 'bios_list'
        mock_file = mock.Mock()
        mock_file.read.return_value = self.build_bios_list_without_options()
        mock_open.return_value = mock_file
        bios = self.profile.make_bios_dict(filename)
        self.assertIsNotNone(bios)
        self.assertEqual(
            {'manageBios': True, 'overriddenSettings': [{'id': '134'}]}, bios)

    @mock.patch(mock_builtin('open'))
    def test_make_bios_invalid_json(self, mock_open):
        filename = 'bios_list'
        mock_file = mock.Mock()
        mock_file.read.return_value = 'adfadsf'
        mock_open.return_value = mock_file
        try:
            self.profile.make_bios_dict(filename)
        except ValueError as value_error:
            self.assertEqual(value_error.args[
                             0], "Error: Cannot parse BIOS JSON file. JSON must be well-formed.")
        else:
            self.fail("Expected Exception")

    # helper functions
    def build_dl_sht(self):
        return {
            'type': 'server-hardware-type-4',
            'category': 'server-hardware-types',
            'name': 'DL360p Gen8 1',
            'description': None,
            'uri': '/rest/server-hardware-types/F8DDCB66-2EA3-4A29-BA8A-337DD121B',
            'model': 'ProLiant DL360p Gen8',
            'formFactor': '1U',
            'biosSettings': [],
            'storageCapabilities': {
                'raidLevels': ['RAID0', 'RAID1', 'RAID1ADM', 'RAID10', 'RAID5', 'RAID6'],
                'controllerModes': ['RAID'],
                'driveTechnologies': ['SasHdd', 'SataHdd', 'SasSsd', 'SataSsd'],
                'maximumDrives': 10
            },
            'pxeBootPolicies': ['IPv4'],
            'bootModes': ['BIOS'],
            'adapters': [],
            'bootCapabilities': ['CD', 'Floppy', 'USB', 'HardDisk', 'PXE'],
            'capabilities': ['ManageBIOS', 'ManageLocalStorage', 'ManageBootOrder', 'FirmwareUpdate']
        }

    def build_gen8_bl_sht(self):
        return {
            'type': 'server-hardware-type-4',
            'category': 'server-hardware-types',
            'name': 'BL460c Gen8 1',
            'description': None,
            'uri': '/rest/server-hardware-types/E322DD37-2ED3-4FFE-8C20-2F0D3BA559',
            'model': 'ProLiant BL460c Gen8',
            'formFactor': 'HalfHeight',
            'biosSettings': [],
            'storageCapabilities': {
                'raidLevels': ['RAID0', 'RAID1'],
                'controllerModes': ['RAID'],
                'driveTechnologies': ['SasHdd', 'SataHdd', 'SasSsd', 'SataSsd'],
                'maximumDrives': 2
            },
            'pxeBootPolicies': ['IPv4'],
            'bootModes': ['BIOS'],
            'adapters': [],
            'bootCapabilities': ['CD', 'Floppy', 'USB', 'HardDisk', 'FibreChannelHba', 'PXE'],
            'capabilities': ['ManageBIOS', 'VirtualUUID', 'ManageLocalStorage', 'VirtualWWN', 'ManageBootOrder',
                             'VCConnections', 'VirtualMAC', 'FirmwareUpdate']
        }

    def build_gen9_bl_sht(self):
        return {
            'type': 'server-hardware-type-4',
            'category': 'server-hardware-types',
            'name': 'BL460c Gen9 1',
            'description': None,
            'uri': '/rest/server-hardware-types/0D2A55D6-F261-445A-BB24-9508E257',
            'model': 'ProLiant BL460c Gen9',
            'formFactor': 'HalfHeight',
            'biosSettings': [],
            'storageCapabilities': {
                'raidLevels': ['RAID0', 'RAID1'],
                'controllerModes': ['RAID', 'HBA'],
                'driveTechnologies': ['SasHdd', 'SataHdd', 'SasSsd', 'SataSsd'],
                'maximumDrives': 2
            },
            'pxeBootPolicies': ['Auto', 'IPv6ThenIPv4', 'IPv4', 'IPv4ThenIPv6', 'IPv6'],
            'bootModes': ['UEFIOptimized', 'BIOS', 'UEFI'],
            'adapters': [],
            'bootCapabilities': ['CD', 'USB', 'HardDisk', 'FibreChannelHba', 'PXE'],
            'capabilities': ['ManageBIOS', 'VirtualUUID', 'ManageLocalStorage', 'VirtualWWN', 'ManageBootOrder',
                             'VCConnections', 'VirtualMAC', 'FirmwareUpdate']
        }

    def build_get_spp_response(self):
        return {
            'type': 'firmware-baselines',
            'bundleType': 'SPP',
            'resourceId': 'SPP2016020_2015_1204_63',
            'uuid': 'SPP2016020_2015_1204_63',
            'xmlKeyName': 'bp002524',
            'isoFileName': 'SPP2016020_2015_1204_63.iso',
            'baselineShortName': 'SPP 2016.02.0',
            'bundleSize': 5821517824,
            'version': '2016.02.0',
            'releaseDate': '2015-12-04T11:24:27.773Z',
            'supportedOSList': ['Microsoft Windows Server 2008 R2'],
            'supportedLanguages': 'English (US), Japanese, Chinese (Simplified)',
            'fwComponents': [],
            'swPackagesFullPath': '/mnt/fwbundles/SPP2016020_2015_1204_63/hp/swpackages/',
            'state': 'Created',
            'lastTaskUri': '',
            'hpsumVersion': '750_b42',
            'description': 'The Service Pack for ProLiant (SPP) is a comprehensive systems software and firmware update'
                           'solution, which is delivered as a single ISO image.',
            'name': 'Service Pack for ProLiant',
            'status': 'OK',
            'category': 'firmware-drivers',
            'uri': '/rest/firmware-drivers/SPP2016020_2015_1204_63'
        }

    def build_bios_list(self):
        return json.dumps([{
            'id': '134',
            'help': 'Controls the Virtual Install Disk. The Virtual\nInstall Disk may contain drivers specific to this'
                    'server\nthat an OS may use during installation.',
            'name': 'Virtual Install Disk',
            'options': [
                {
                    'id': '2',
                    'name': 'Disabled'
                }
            ]
        }])

    def build_bios_list_without_options(self):
        return json.dumps([{
            'id': '134',
            'help': 'Controls the Virtual Install Disk.',
            'name': 'Virtual Install Disk'
        }])


if __name__ == '__main__':
    unittest.main()
