# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2019) Hewlett Packard Enterprise Development LP
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
import unittest
import mock

from hpOneView.connection import connection
from hpOneView.resources.networking.sas_logical_interconnects import SasLogicalInterconnects
from hpOneView.resources.resource import ResourceHelper


class SasLogicalInterconnectsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._client = SasLogicalInterconnects(self.connection)
        self.uri = "/rest/sas-logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32"
        self._client.data = {"uri": self.uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._client.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(count=500, fields='name=TestName', filter='name:ascending', query='',
                                             sort='', start=2, view='')

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._client.get_all()
        mock_get_all.assert_called_once_with(count=-1, fields='', filter='', query='', sort='', start=0, view='')

    @mock.patch.object(ResourceHelper, 'do_get')
    @mock.patch.object(ResourceHelper, 'create')
    def test_replace_drive_enclosure_called_once(self, mock_create, mock_get):
        drive_replacement = {
            "oldSerialNumber": "SN1100",
            "newSerialNumber": "SN1101"
        }
        self._client.replace_drive_enclosure(drive_replacement)

        mock_create.assert_called_once_with(
            drive_replacement.copy(),
            '{}/replaceDriveEnclosure'.format(self.uri))

    @mock.patch.object(ResourceHelper, 'do_get')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_compliance_all_called_once(self, mock_update, mock_get):
        compliance_uris = {
            "uris": [
                "/rest/sas-logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32"
            ]}

        self._client.update_compliance_all(compliance_uris)

        mock_update.assert_called_once_with(compliance_uris.copy(),
                                            '/rest/sas-logical-interconnects/compliance',
                                            timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_compliance(self, mock_update, mock_get):
        self._client.update_compliance()

        mock_update.assert_called_once_with({}, '{}/compliance'.format(self.uri), timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_configuration(self, mock_update, mock_get):
        self._client.update_configuration()

        mock_update.assert_called_once_with({}, '{}/configuration'.format(self.uri))

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_firmware(self, mock_get):
        expected_uri = self.uri + "/firmware"

        self._client.get_firmware()
        mock_get.assert_called_once_with(expected_uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_firmware(self, mock_update, mock_get):
        fake_firmware = dict(
            command="Update",
            sppUri="/rest/firmware-drivers/Service_0Pack_0for_0ProLiant"
        )

        expected_uri = self.uri + "/firmware"

        self._client.update_firmware(fake_firmware)
        mock_update.assert_called_once_with(fake_firmware, expected_uri, force=False)
