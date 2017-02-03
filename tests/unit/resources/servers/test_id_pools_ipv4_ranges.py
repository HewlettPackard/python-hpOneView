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
import mock
import unittest

from hpOneView.connection import connection
from hpOneView.resources.resource import ResourceClient
from hpOneView.resources.servers.id_pools_ipv4_ranges import IdPoolsIpv4Ranges


class TestIdPoolsIpv4Ranges(unittest.TestCase):
    resource_info = {'type': 'Range',
                     'name': 'No name'}
    example_uri = "/rest/id-pools/ipv4/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self.client = IdPoolsIpv4Ranges(self.connection)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        self.client.create(self.resource_info)
        mock_create.assert_called_once_with(self.resource_info, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        id_pools_range_id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self.client.get(id_pools_range_id)
        mock_get.assert_called_once_with(id_pools_range_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        self.client.get(self.example_uri)
        mock_get.assert_called_once_with(self.example_uri)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, update):
        self.client.update(self.resource_info.copy())
        update.assert_called_once_with(self.resource_info.copy(), timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_enable_called_once(self, update):
        self.client.enable(self.resource_info.copy(), self.example_uri)
        update.assert_called_once_with(self.resource_info.copy(), self.example_uri, timeout=-1)

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_allocated_fragments_called_once_with_defaults(self, mock_get):
        self.client.get_allocated_fragments(self.example_uri)
        mock_get.assert_called_once_with(self.example_uri + "/allocated-fragments?start=0&count=-1")

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_allocated_fragments_called_once(self, mock_get):
        self.client.get_allocated_fragments(self.example_uri, 5, 2)
        mock_get.assert_called_once_with(self.example_uri + "/allocated-fragments?start=2&count=5")

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_free_fragments_called_once_with_defaults(self, mock_get):
        self.client.get_free_fragments(self.example_uri)
        mock_get.assert_called_once_with(self.example_uri + "/free-fragments?start=0&count=-1")

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_free_fragments_called_once(self, mock_get):
        self.client.get_free_fragments(self.example_uri, 5, 3)
        mock_get.assert_called_once_with(self.example_uri + "/free-fragments?start=3&count=5")

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        self.client.delete({'uri': '/rest/uri'}, force=True, timeout=50)
        mock_delete.assert_called_once_with({'uri': '/rest/uri'}, force=True, timeout=50)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once_with_defaults(self, mock_delete):
        self.client.delete({'uri': '/rest/uri'})
        mock_delete.assert_called_once_with({'uri': '/rest/uri'}, force=False, timeout=-1)
