# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2017) Hewlett Packard Enterprise Development LP
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

from unittest import TestCase

import mock

from hpOneView.connection import connection
from hpOneView.resources.resource import ResourceClient
from hpOneView.resources.settings.firmware_drivers import FirmwareDrivers

ALL_FIRMWARE_DRIVERS = [
    {
        'name': 'Supplemental Update',
        'uri': '/rest/firmware-drivers/hp-firmware-hdd-a1b08f8a6b-HPGH-1_1_x86_64',
        'fwComponents': [{'fileName': 'hp-firmware-hdd-a1b08f8a6b-HPGH-1.1.x86_64.rpm'}]
    },
    {
        'name': 'Service Pack for ProLiant.iso',
        'uri': '/rest/firmware-drivers/spp_gen9_snap6_add-on_bundle',
        'fwComponents': [{'fileName': 'spp_gen9_snap6_add-on_bundle.zip'}]
    }
]


class FirmwareDriversTest(TestCase):
    DEFAULT_HOST = '127.0.0.1'

    def setUp(self):
        oneview_connection = connection(self.DEFAULT_HOST)
        self.resource = FirmwareDrivers(oneview_connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all(self, mock_get_all):
        filter_by = 'name=TestName'
        sort = 'name:ascending'

        self.resource.get_all(2, 500, filter_by, sort)
        mock_get_all.assert_called_once_with(2, 500, filter=filter_by, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_by(self, mock_get_all):
        property_name = 'name'
        firmware_name = 'Service Pack for ProLiant.iso'
        expected_result = [ALL_FIRMWARE_DRIVERS[1]]
        mock_get_all.return_value = ALL_FIRMWARE_DRIVERS

        result = self.resource.get_by(property_name, firmware_name)
        self.assertEqual(expected_result, result)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_by_without_match(self, mock_get_all):
        property_name = 'name'
        firmware_name = 'Service Pack for ProLiant X64'
        mock_get_all.return_value = ALL_FIRMWARE_DRIVERS

        result = self.resource.get_by(property_name, firmware_name)
        self.assertEqual(0, len(result))

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_by_when_there_are_not_any_firmware(self, mock_get_all):
        property_name = 'name'
        firmware_name = 'Service Pack for ProLiant X64'
        mock_get_all.return_value = []

        result = self.resource.get_by(property_name, firmware_name)
        self.assertEqual(0, len(result))

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id(self, mock_get):
        firmware_id = "SPP2012080.2012_0713.57"

        self.resource.get(firmware_id)
        mock_get.assert_called_once_with(firmware_id)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_should_use_given_values(self, mock_create):
        resource = {
            'customBaselineName': 'FirmwareDriver1_Example',
            'baselineUri': '/rest/fakespp',
            'hotfixUris': ['/rest/fakehotfix']
        }
        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self.resource.create(resource, 30)
        mock_create.assert_called_once_with(resource_rest_call, timeout=30)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove(self, mock_delete):
        fake_firmware = dict(name='Service Pack for ProLiant.iso')

        self.resource.delete(fake_firmware)
        mock_delete.assert_called_once_with(fake_firmware, force=False, timeout=-1)
