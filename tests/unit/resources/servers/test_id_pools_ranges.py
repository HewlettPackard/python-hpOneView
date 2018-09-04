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

from hpOneView import HPOneViewValueError
from hpOneView.connection import connection
from hpOneView.resources.resource import Resource
from hpOneView.resources.servers.id_pools_ranges import IdPoolsRanges
import unittest


class TestIdPoolsRanges(unittest.TestCase):
    resource_info = {'type': 'Range',
                     'name': 'No name'}

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self.id_pool_name = 'vsn'
        self.client = IdPoolsRanges(self.id_pool_name, self.connection)
        self.client.data = {'uri': "/rest/id-pools/" + self.id_pool_name + "/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"}
        self.example_uri = "/rest/id-pools/" + self.id_pool_name + "/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"

    @mock.patch.object(Resource, '__init__')
    def test_id_pools_ranges_constructor_with_type_vsn(self, mock_rclient):
        mock_rclient.return_value = None
        IdPoolsRanges(type='vsn', connection=self.connection)
        mock_rclient.assert_called_once_with(self.connection, None)

    @mock.patch.object(Resource, '__init__')
    def test_id_pools_ranges_constructor_with_type_vwwn(self, mock_rclient):
        mock_rclient.return_value = None
        IdPoolsRanges('vwwn', self.connection)
        mock_rclient.assert_called_once_with(self.connection, None)

    @mock.patch.object(Resource, '__init__')
    def test_id_pools_ranges_constructor_with_type_vmac(self, mock_rclient):
        mock_rclient.return_value = None
        IdPoolsRanges('vmac', self.connection)
        mock_rclient.assert_called_once_with(self.connection, None)

    @mock.patch.object(Resource, '__init__')
    def test_id_pools_ranges_constructor_with_invalid_type(self, mock_rclient):
        mock_rclient.return_value = None
        self.assertRaises(HPOneViewValueError, IdPoolsRanges, 'invalid', self.connection)

    @mock.patch.object(Resource, 'create')
    def test_create_called_once(self, mock_create):
        self.client.create(self.resource_info)
        mock_create.assert_called_once_with(self.resource_info)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_by_id_called_once(self, mock_get_by_uri):
        id_pools_range_id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self.client.get_by_uri(id_pools_range_id)
        mock_get_by_uri.assert_called_once_with(id_pools_range_id)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_by_uri_called_once(self, mock_get_by_uri):
        self.client.get_by_uri(self.example_uri)
        mock_get_by_uri.assert_called_once_with(self.example_uri)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'update')
    def test_enable_called_once(self, mock_update, load_resource):
        self.client.enable(self.resource_info.copy())
        mock_update.assert_called_once_with(self.resource_info.copy(), timeout=-1)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'get_collection')
    def test_get_allocated_fragments_called_once_with_defaults(self, mock_get, load_resource):
        self.client.get_allocated_fragments()
        mock_get.assert_called_once_with("/allocated-fragments?start=0&count=-1")

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'get_collection')
    def test_get_allocated_fragments_called_once(self, mock_get, load_resource):
        self.client.get_allocated_fragments(5, 2)
        mock_get.assert_called_once_with("/allocated-fragments?start=2&count=5")

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'get_collection')
    def test_get_free_fragments_called_once_with_defaults(self, mock_get, load_resource):
        self.client.get_free_fragments()
        mock_get.assert_called_once_with("/free-fragments?start=0&count=-1")

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'get_collection')
    def test_get_free_fragments_called_once(self, mock_get, load_resource):
        self.client.get_free_fragments(5, 3)
        mock_get.assert_called_once_with("/free-fragments?start=3&count=5")

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'delete')
    def test_delete_called_once(self, mock_delete, load_resource):
        self.client.delete(force=True, timeout=50)
        mock_delete.assert_called_once_with(force=True, timeout=50)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'delete')
    def test_delete_called_once_with_defaults(self, mock_delete, load_resource):
        self.client.delete()
        mock_delete.assert_called_once_with()

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'do_put')
    def test_allocate_called_once(self, mock_put, load_resource):
        self.client.allocate(self.resource_info.copy())
        mock_put.assert_called_once_with(self.example_uri + '/allocator', self.resource_info.copy(), timeout=-1)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'do_put')
    def test_collect_called_once(self, mock_put, load_resource):
        self.client.collect(self.resource_info.copy())
        mock_put.assert_called_once_with(self.example_uri + '/collector', self.resource_info.copy(), timeout=-1)
