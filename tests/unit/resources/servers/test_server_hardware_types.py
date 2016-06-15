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
import mock

from hpOneView.connection import connection
from hpOneView.resources.servers.server_hardware_types import ServerHardwareTypes
from hpOneView.resources.resource import ResourceClient
import unittest


class ServerHardwareTypesTest(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._server_hardware_types = ServerHardwareTypes(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._server_hardware_types.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_conce(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._server_hardware_types.get_all(2, 500, filter, sort)
        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        server_hardware_type_id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._server_hardware_types.get(server_hardware_type_id)
        mock_get.assert_called_once_with(server_hardware_type_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        server_hardware_type_uri = "/rest/server-hardware-types/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._server_hardware_types.get(server_hardware_type_uri)
        mock_get.assert_called_once_with(server_hardware_type_uri)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once_with_defaults(self, update):
        server_hardware_type = {
            "name": "New Server Type Name",
            "description": "New Description"
        }
        self._server_hardware_types.update(server_hardware_type)
        update.assert_called_once_with(
            server_hardware_type, None, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, update):
        server_hardware_type = {
            "name": "New Server Type Name",
            "description": "New Description"
        }
        self._server_hardware_types.update(server_hardware_type, None, 70)
        update.assert_called_once_with(
            server_hardware_type, None, timeout=70)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._server_hardware_types.delete(id, force=True, timeout=50)

        mock_delete.assert_called_once_with(id, force=True, timeout=50)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once_with_defaults(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._server_hardware_types.delete(id)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._server_hardware_types.get_by("name", "test name")

        mock_get_by.assert_called_once_with("name", "test name")
