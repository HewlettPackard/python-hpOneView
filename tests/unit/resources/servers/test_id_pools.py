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
from hpOneView.resources.servers.id_pools import IdPools


class TestIdPools(unittest.TestCase):
    resource_info = {'type': 'Range',
                     'name': 'No name'}
    example_uri = "/rest/id-pools/ipv4"

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._id_pools = IdPools(self.connection)
        self._id_pools.data = {'uri': '/rest/id-pools/ipv4'}

    @mock.patch.object(Resource, 'do_get')
    def test_get_called_once_by_name(self, mock_do_get):
        id_pools_range_id = "ipv4"
        self._id_pools.get_by_name(id_pools_range_id)
        mock_do_get.assert_called_once_with(self.example_uri)

    @mock.patch.object(Resource, 'do_get')
    def test_get_called_once_by_uri(self, mock_do_get):
        self._id_pools.get_by_uri(self.example_uri)
        mock_do_get.assert_called_once_with(self.example_uri)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'do_get')
    def test_generate_called_once(self, mock_do_get, load_resource):
        self._id_pools.generate()
        mock_do_get.assert_called_once_with(self.example_uri + '/generate')

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'do_get')
    def test_validate_id_pool_called_once(self, mock_do_get, load_resource):
        self._id_pools.validate_id_pool(['VCGYOAA023', 'VCGYOAA024'])
        mock_do_get.assert_called_once_with(self.example_uri + "/validate?idList=VCGYOAA023&idList=VCGYOAA024")

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'do_put')
    def test_validate_called_once(self, mock_do_put, load_resource):
        self._id_pools.validate(self.resource_info.copy())
        mock_do_put.assert_called_once_with(self.example_uri + "/validate", self.resource_info.copy(), timeout=-1)

    @mock.patch.object(Resource, 'update')
    def test_enable_called_once(self, update):
        self._id_pools.enable(self.resource_info.copy())
        update.assert_called_once_with(self.resource_info.copy(), timeout=-1)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'do_get')
    def test_get_check_range_availability_called_once_with_defaults(self, mock_do_get, load_resource):
        self._id_pools.get_check_range_availability(['VCGYOAA023', 'VCGYOAA024'])
        mock_do_get.assert_called_once_with(
            self.example_uri + "/checkrangeavailability?idList=VCGYOAA023&idList=VCGYOAA024")

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'do_put')
    def test_allocate_called_once(self, mock_do_put, load_resource):
        self._id_pools.allocate(self.resource_info.copy())
        mock_do_put.assert_called_once_with(self.example_uri + "/allocator", self.resource_info.copy(), timeout=-1)

    @mock.patch.object(Resource, 'load_resource')
    @mock.patch.object(Resource, 'do_put')
    def test_collect_called_once(self, mock_do_put, load_resource):
        self._id_pools.collect(self.resource_info.copy())
        mock_do_put.assert_called_once_with(self.example_uri + "/collector", self.resource_info.copy(), timeout=-1)
