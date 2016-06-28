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
from hpOneView.resources.servers.logical_enclosures import LogicalEnclosures
from hpOneView.resources.resource import ResourceClient


class LogicalEnclosuresTest(TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._logical_enclosures = LogicalEnclosures(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._logical_enclosures.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default_values(self, mock_get_all):
        self._logical_enclosures.get_all()

        mock_get_all.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._logical_enclosures.get_by(
            'name', 'OneViewSDK-Test-Logical-Enclosure')

        mock_get_by.assert_called_once_with(
            'name', 'OneViewSDK-Test-Logical-Enclosure')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_id_called_once(self, mock_get):
        logical_enclosure_id = '3518be0e-17c1-4189-8f81-83f3724f6155'
        self._logical_enclosures.get(logical_enclosure_id)

        mock_get.assert_called_once_with(logical_enclosure_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        logical_enclosure_uri = '/rest/enclosures/3518be0e-17c1-4189-8f81-83f3724f6155'
        self._logical_enclosures.get(logical_enclosure_uri)

        mock_get.assert_called_once_with(logical_enclosure_uri)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once_with_defaults(self, mock_update):
        logical_enclosure = {
            "name": "one_enclosure_le",
        }
        self._logical_enclosures.update(logical_enclosure)
        mock_update.assert_called_once_with(logical_enclosure, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_update):
        logical_enclosure = {
            "name": "one_enclosure_le",
        }
        self._logical_enclosures.update(logical_enclosure, 70)
        mock_update.assert_called_once_with(logical_enclosure, timeout=70)

    @mock.patch.object(ResourceClient, 'patch')
    def test_patch_should_use_user_defined_values(self, mock_patch):
        mock_patch.return_value = {}

        self._logical_enclosures.patch(
            '123a53cz', 'replace', '/name', 'new_name', 1)
        mock_patch.assert_called_once_with(
            '123a53cz', 'replace', '/name', 'new_name', timeout=1)

    @mock.patch.object(ResourceClient, 'update_with_zero_body')
    def test_update_configuration_by_uri(self, mock_update_with_zero_body):
        logical_enclosure_uri = '/rest/logical-enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32/configuration'

        self._logical_enclosures.update_configuration(logical_enclosure_uri)

        mock_update_with_zero_body.assert_called_once_with(
            uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceClient, 'update_with_zero_body')
    def test_update_configuration_by_id(self, mock_update_with_zero_body):
        logical_enclosure_id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32/configuration'

        self._logical_enclosures.update_configuration(logical_enclosure_id)

        mock_update_with_zero_body.assert_called_once_with(
            uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_script_by_uri(self, mock_get):
        logical_enclosure_uri = '/rest/logical-enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32/script'

        self._logical_enclosures.get_script(
            logical_enclosure_uri)

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_script_by_id(self, mock_get):
        logical_enclosure_id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32/script'

        self._logical_enclosures.get_script(
            logical_enclosure_id)

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_script_by_uri(self, mock_update):
        logical_enclosure_uri = '/rest/logical-enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32/script'
        information = {"#TEST COMMAND"}
        configuration_rest_call = information.copy()

        self._logical_enclosures.update_script(
            logical_enclosure_uri, information)

        mock_update.assert_called_once_with(
            configuration_rest_call, uri=uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_script_by_id(self, mock_update):
        logical_enclosure_id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32/script'
        information = {"#TEST COMMAND"}
        configuration_rest_call = information.copy()

        self._logical_enclosures.update_script(
            logical_enclosure_id, information)

        mock_update.assert_called_once_with(
            configuration_rest_call, uri=uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceClient, 'create')
    def test_support_dump_called_once(self, mock_create):
        information = {
            "errorCode": "MyDump16",
            "encrypt": True,
            "excludeApplianceDump": False
        }
        logical_enclosure_uri = '/rest/logical-enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32/support-dumps'

        mock_create.return_value = {}

        self._logical_enclosures.generate_support_dump(
            information, logical_enclosure_uri)
        mock_create.assert_called_once_with(
            information.copy(), uri=uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceClient, 'update_with_zero_body')
    def test_update_from_group_by_uri(self, mock_update_with_zero_body):
        logical_enclosure_uri = '/rest/logical-enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32/updateFromGroup'

        self._logical_enclosures.update_from_group(logical_enclosure_uri)

        mock_update_with_zero_body.assert_called_once_with(
            uri=uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceClient, 'update_with_zero_body')
    def test_update_from_group_by_id(self, mock_update_with_zero_body):
        logical_enclosure_id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32/updateFromGroup'

        self._logical_enclosures.update_from_group(logical_enclosure_id, -1)

        mock_update_with_zero_body.assert_called_once_with(
            uri=uri_rest_call, timeout=-1)
