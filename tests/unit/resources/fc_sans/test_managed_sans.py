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
from hpOneView.resources.resource import ResourceClient
from hpOneView.resources.fc_sans.managed_sans import ManagedSANs

TIMEOUT = -1


class SanManagersTest(TestCase):
    def setUp(self):
        host = '127.0.0.1'
        http_connection = connection(host)
        self._resource = ManagedSANs(http_connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all(self, mock_get_all):
        query_filter = "name EQ 'TestName'"
        sort = 'name:ascending'

        self._resource.get_all(start=2, count=500, query=query_filter, sort=sort)
        mock_get_all.assert_called_once_with(start=2, count=500, query=query_filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_by_name_should_return_san_manager_when_found(self, mock_get_all):
        mock_get_all.return_value = [
            {"name": "SAN1_0", "uri": "/rest/fc-sans/managed-sans/d1d"},
            {"name": "SAN1_1", "uri": "/rest/fc-sans/managed-sans/sc5"}
        ]
        managed_san = self._resource.get_by_name("SAN1_1")

        expected_result = {"name": "SAN1_1", "uri": "/rest/fc-sans/managed-sans/sc5"}
        self.assertEqual(managed_san, expected_result)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_by_name_should_return_null_when_not_found(self, mock_get_all):
        mock_get_all.return_value = [
            {"name": "SAN1_0", "uri": "/rest/fc-sans/managed-sans/d1d"},
            {"name": "SAN1_1", "uri": "/rest/fc-sans/managed-sans/sc5"}
        ]
        managed_san = self._resource.get_by_name("SAN1_3")

        self.assertIsNone(managed_san)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id(self, mock_get):
        id = "6fee02f3-b7c7-42bd-a528-04341e16bad6"

        self._resource.get(id)
        mock_get.assert_called_once_with(id_or_uri=id)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_with_uri(self, mock_update):
        uri = "/rest/fc-sans/managed-sans/d1d"
        data = {"attributes": "values"}

        self._resource.update(uri, data)

        mock_update.assert_called_once_with(data, timeout=-1, uri=uri)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_with_id(self, mock_update):
        uri = "/rest/fc-sans/managed-sans/d1d"
        data = {"attributes": "values"}

        self._resource.update("d1d", data)

        mock_update.assert_called_once_with(data, timeout=-1, uri=uri)
