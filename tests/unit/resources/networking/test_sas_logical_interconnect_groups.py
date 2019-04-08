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
from hpOneView.resources.networking.sas_logical_interconnect_groups import SasLogicalInterconnectGroups
from hpOneView.resources.resource import Resource, ResourceHelper


class SasLogicalInterconnectGroupsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._resource = SasLogicalInterconnectGroups(self.connection)
        self.uri = "/rest/sas-logical-interconnect-groups/3518be0e-17c1-4189-8f81-83f3724f6155"
        self._resource.data = {"uri": self.uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        scope_uris = 'TestScope'
        query = 'test'

        self._resource.get_all(2, 500, filter, sort, scope_uris, query=query)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort, scope_uris=scope_uris, query=query)

    @mock.patch.object(ResourceHelper, 'create')
    def test_create_called_once(self, mock_create):
        resource = {'name': 'Test SAS Logical Interconnect Group'}

        self._resource.create(resource, timeout=30)

        mock_create.assert_called_once_with(resource, None, 30, None, False)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_called_once(self, mock_update, mock_ensure_client):
        resource = {'name': 'Test SAS Logical Interconnect Group'}

        self._resource.update(resource, timeout=60)
        resource["uri"] = self.uri
        mock_update.assert_called_once_with(resource, self.uri, False, 60, None)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._resource.delete(force=False, timeout=-1)

        mock_delete.assert_called_once_with(self.uri, custom_headers=None, force=False, timeout=-1)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once_with_force(self, mock_delete):
        self._resource.delete(force=True, timeout=-1)

        mock_delete.assert_called_once_with(self.uri, custom_headers=None, force=True, timeout=-1)
