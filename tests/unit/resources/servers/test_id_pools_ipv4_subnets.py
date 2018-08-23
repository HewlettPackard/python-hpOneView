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
from hpOneView.resources.resource import Resource
from hpOneView.resources.servers.id_pools_ipv4_subnets import IdPoolsIpv4Subnets


class TestIdPoolsIpv4Subnets(unittest.TestCase):
    resource_info = {'type': 'Range',
                     'name': 'No name'}
    example_uri = "/rest/id-pools/ipv4/subnets/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self.client = IdPoolsIpv4Subnets(self.connection)
        self.client.data = {'uri': "/rest/id-pools/ipv4/subnets/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"}

    @mock.patch.object(Resource, 'create')
    def test_create_called_once(self, mock_create):
        self.client.create(self.resource_info)
        mock_create.assert_called_once_with(self.resource_info)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_by_id_called_once(self, mock_get_by_uri, load_resource):
        id_pools_subnet_id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self.client.get_by_uri(id_pools_subnet_id)
        mock_get_by_uri.assert_called_once_with(id_pools_subnet_id)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_by_uri_called_once(self, mock_get_by_uri, load_resource):
        self.client.get_by_uri(self.example_uri)
        mock_get_by_uri.assert_called_once_with(self.example_uri)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'update')
    def test_enable_called_once(self, update, load_resource):
        self.client.update(self.resource_info.copy())
        update.assert_called_once_with(self.resource_info.copy())

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'get_all')
    def test_get_allocated_fragments_called_once_with_defaults(self, mock_get, load_resource):
        self.client.get_all(self.example_uri)
        mock_get.assert_called_once_with(self.example_uri)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'delete')
    def test_delete_called_once(self, mock_delete, load_resource):
        self.client.delete({'uri': '/rest/uri'}, force=True, timeout=50)
        mock_delete.assert_called_once_with({'uri': '/rest/uri'}, force=True, timeout=50)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'delete')
    def test_delete_called_once_with_defaults(self, mock_delete, load_resource):
        self.client.delete({'uri': '/rest/uri'})
        mock_delete.assert_called_once_with({'uri': '/rest/uri'})
