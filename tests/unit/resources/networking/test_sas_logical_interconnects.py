# -*- coding: utf-8 -*-
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
import unittest
import mock

from hpOneView.connection import connection
from hpOneView.resources.networking.sas_logical_interconnects import SasLogicalInterconnects
from hpOneView.resources.resource import ResourceClient


class SasLogicalInterconnectsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._client = SasLogicalInterconnects(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._client.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(count=500, fields='name=TestName', filter='name:ascending', query='',
                                             sort='', start=2, view='')

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._client.get_all()
        mock_get_all.assert_called_once_with(count=-1, fields='', filter='', query='', sort='', start=0, view='')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        logical_interconnect_id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._client.get(logical_interconnect_id)
        mock_get.assert_called_once_with(logical_interconnect_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        logical_interconnect_uri = "/rest/sas-logical-interconnects/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._client.get(logical_interconnect_uri)
        mock_get.assert_called_once_with(logical_interconnect_uri)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get):
        self._client.get_by("name", "value")
        mock_get.assert_called_once_with("name", "value")

    @mock.patch.object(ResourceClient, 'create')
    def test_replace_drive_enclosure_called_once(self, mock_create):
        drive_replacement = {
            "oldSerialNumber": "SN1100",
            "newSerialNumber": "SN1101"
        }
        self._client.replace_drive_enclosure(drive_replacement, "ad28cf21-8b15-4f92-bdcf-51cb2042db32")

        mock_create.assert_called_once_with(
            drive_replacement.copy(),
            '/rest/sas-logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/replaceDriveEnclosure')

    @mock.patch.object(ResourceClient, 'update')
    def test_update_compliance_all_called_once(self, mock_update):
        compliance_uris = {
            "uris": [
                "/rest/sas-logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32"
            ]}

        self._client.update_compliance_all(compliance_uris)

        mock_update.assert_called_once_with(compliance_uris.copy(),
                                            '/rest/sas-logical-interconnects/compliance',
                                            timeout=-1)

    @mock.patch.object(ResourceClient, 'update_with_zero_body')
    def test_update_compliance_by_uri(self, mock_update_with_zero_body):
        logical_interconnect_uri = '/rest/sas-logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._client.update_compliance(logical_interconnect_uri)

        mock_update_with_zero_body.assert_called_once_with(
            '/rest/sas-logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/compliance', timeout=-1)

    @mock.patch.object(ResourceClient, 'update_with_zero_body')
    def test_update_compliance_by_id(self, mock_update_with_zero_body):
        mock_update_with_zero_body.return_value = {}
        logical_interconnect_id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'

        self._client.update_compliance(logical_interconnect_id)

        mock_update_with_zero_body.assert_called_once_with(
            '/rest/sas-logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/compliance', timeout=-1)

    @mock.patch.object(ResourceClient, 'update_with_zero_body')
    def test_update_configuration_by_uri(self, mock_update_with_zero_body):
        logical_interconnect_uri = '/rest/sas-logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32'

        self._client.update_configuration(logical_interconnect_uri)

        mock_update_with_zero_body.assert_called_once_with(
            '/rest/sas-logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/configuration')

    @mock.patch.object(ResourceClient, 'update_with_zero_body')
    def test_update_configuration_by_id(self, mock_update_with_zero_body):
        logical_interconnect_id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'

        self._client.update_configuration(logical_interconnect_id)

        mock_update_with_zero_body.assert_called_once_with(
            '/rest/sas-logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/configuration')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_firmware(self, mock_get):
        logical_interconnect_id = '3518be0e-17c1-4189-8f81-83f3724f6155'

        logical_interconnect_uri = "/rest/sas-logical-interconnects/" + logical_interconnect_id

        expected_uri = logical_interconnect_uri + "/firmware"

        self._client.get_firmware(logical_interconnect_id)
        mock_get.assert_called_once_with(expected_uri)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_firmware(self, mock_update):
        logical_interconnect_id = '3518be0e-17c1-4189-8f81-83f3724f6155'

        fake_firmware = dict(
            command="Update",
            sppUri="/rest/firmware-drivers/Service_0Pack_0for_0ProLiant"
        )

        logical_interconnect_uri = "/rest/sas-logical-interconnects/" + logical_interconnect_id

        expected_uri = logical_interconnect_uri + "/firmware"

        self._client.update_firmware(fake_firmware, logical_interconnect_id)
        mock_update.assert_called_once_with(fake_firmware, expected_uri)
