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
from hpOneView.resources.servers.id_pools import IdPools


class TestIdPools(unittest.TestCase):
    resource_info = {'type': 'Range',
                     'name': 'No name'}
    example_uri = "/rest/id-pools/ipv4"

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self.client = IdPools(self.connection)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once_by_id(self, mock_get):
        id_pools_range_id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self.client.get(id_pools_range_id)
        mock_get.assert_called_once_with(id_pools_range_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once_by_uri(self, mock_get):
        self.client.get(self.example_uri)
        mock_get.assert_called_once_with(self.example_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_generate_called_once(self, mock_get):
        self.client.generate(self.example_uri)
        mock_get.assert_called_once_with(self.example_uri + '/generate')

    @mock.patch.object(ResourceClient, 'get')
    def test_validate_id_pool_called_once(self, mock_get):
        self.client.validate_id_pool(self.example_uri, ['VCGYOAA023',
                                                        'VCGYOAA024'])
        mock_get.assert_called_once_with(self.example_uri + "/validate?idList=VCGYOAA023&idList=VCGYOAA024")

    @mock.patch.object(ResourceClient, 'update')
    def test_validate_called_once(self, update):
        self.client.validate(self.resource_info.copy(), self.example_uri)
        update.assert_called_once_with(self.resource_info.copy(), self.example_uri + "/validate", timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_enable_called_once(self, update):
        self.client.enable(self.resource_info.copy(), self.example_uri)
        update.assert_called_once_with(self.resource_info.copy(), self.example_uri, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_check_range_availability_called_once_with_defaults(self, mock_get):
        self.client.get_check_range_availability(self.example_uri, ['VCGYOAA023',
                                                                    'VCGYOAA024'])
        mock_get.assert_called_once_with(
            self.example_uri + "/checkrangeavailability?idList=VCGYOAA023&idList=VCGYOAA024")

    @mock.patch.object(ResourceClient, 'update')
    def test_allocate_called_once(self, mock_update):
        self.client.allocate(self.resource_info.copy(), self.example_uri)
        mock_update.assert_called_once_with(self.resource_info.copy(), self.example_uri + "/allocator", timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_collect_called_once(self, update):
        self.client.collect(self.resource_info.copy(), self.example_uri)
        update.assert_called_once_with(self.resource_info.copy(), self.example_uri + "/collector", timeout=-1)
