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

from unittest import TestCase

import mock

from hpOneView.connection import connection
from hpOneView.resources.settings.firmware_drivers import FirmwareDrivers
from hpOneView.resources.resource import ResourceClient


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

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get(self, mock_get_by):
        property_name = 'name'
        firmware_name = 'Service Pack for ProLiant.iso'

        self.resource.get_by(property_name, firmware_name)
        mock_get_by.assert_called_once_with(property_name, firmware_name)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id(self, mock_get):
        firmware_id = "SPP2012080.2012_0713.57"

        self.resource.get(firmware_id)
        mock_get.assert_called_once_with(firmware_id)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove(self, mock_delete):
        fake_firmware = dict(name='Service Pack for ProLiant.iso')

        self.resource.delete(fake_firmware)
        mock_delete.assert_called_once_with(fake_firmware, force=False, timeout=-1)
