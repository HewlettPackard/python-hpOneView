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
from hpOneView.resources.resource import ResourceClient
from hpOneView.resources.servers.id_pools_vsn_ranges import IdPoolsVsnRanges
import unittest


class TestIdPoolsRangesVsn(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._id_pools_vsn_ranges = IdPoolsVsnRanges(self.connection)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        vsn_range = {
            "type": "Range",
            "name": "VSN",
            "prefix": None,
            "enabled": True,
            "startAddress": "VCGS5EI000",
            "endAddress": "VCGS5EIZZZ",
            "rangeCategory": "Generated",
            "totalCount": 46656,
            "freeIdCount": 46656,
            "allocatedIdCount": 0,
            "defaultRange": True,
            "allocatorUri":
                "/rest/id-pools/vsn/ranges/ae2df099-5570-4f9e-9503-16531324d9a4/allocator",
            "collectorUri":
                "/rest/id-pools/vsn/ranges/ae2df099-5570-4f9e-9503-16531324d9a4/collector",
            "reservedIdCount": 0,
            "freeFragmentUri":
                "/rest/id-pools/vsn/ranges/ae2df099-5570-4f9e-9503-16531324d9a4/free-fragments?start=0&count=-1",
            "allocatedFragmentUri":
                "/rest/id-pools/vsn/ranges/ae2df099-5570-4f9e-9503-16531324d9a4/allocated-fragments?start=0&count=-1",
            "category": "id-range-VSN",
            "uri":
                "/rest/id-pools/vsn/ranges/ae2df099-5570-4f9e-9503-16531324d9a4",
            "eTag": None,
            "created": "2013-04-08 18:11:17.862",
            "modified": "2013-04-08 18:11:17.862"
        }
        self._id_pools_vsn_ranges.create(vsn_range, 70)
        mock_create.assert_called_once_with(vsn_range, timeout=70)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        id_pools_vsn_range_id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._id_pools_vsn_ranges.get(id_pools_vsn_range_id)
        mock_get.assert_called_once_with(id_pools_vsn_range_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        id_pools_vsn_range_uri = "/rest/id-pools/vsn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._id_pools_vsn_ranges.get(id_pools_vsn_range_uri)
        mock_get.assert_called_once_with(id_pools_vsn_range_uri)

    @mock.patch.object(ResourceClient, 'update')
    def test_enable_called_once(self, update):
        information = {
            "type": "Range",
            "enabled": True
        }
        id_pools_vsn_range_uri = "/rest/id-pools/vsn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._id_pools_vsn_ranges.enable(information, id_pools_vsn_range_uri)
        update.assert_called_once_with(
            information, id_pools_vsn_range_uri, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_allocated_fragments_called_once_with_defaults(self, mock_get):
        id_pools_vsn_range = {
            "uri": "/rest/id-pools/vsn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c",
        }

        self._id_pools_vsn_ranges.get_allocated_fragments(id_pools_vsn_range)
        uri = "/rest/id-pools/vsn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c/allocated-fragments?start=0&count=-1"
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_allocated_fragments_called_once(self, mock_get):
        id_pools_vsn_range = {
            "uri": "/rest/id-pools/vsn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c",
        }

        self._id_pools_vsn_ranges.get_allocated_fragments(
            id_pools_vsn_range, 5, 2)
        uri = "/rest/id-pools/vsn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c/allocated-fragments?start=2&count=5"
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_free_fragments_called_once_with_defaults(self, mock_get):
        id_pools_vsn_range = {
            "uri": "/rest/id-pools/vsn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c",
        }

        self._id_pools_vsn_ranges.get_free_fragments(id_pools_vsn_range)
        uri = "/rest/id-pools/vsn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c/free-fragments?start=0&count=-1"
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_free_fragments_called_once(self, mock_get):
        id_pools_vsn_range = {
            "uri": "/rest/id-pools/vsn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c",
        }

        self._id_pools_vsn_ranges.get_free_fragments(
            id_pools_vsn_range, 5, 2)
        uri = "/rest/id-pools/vsn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c/free-fragments?start=2&count=5"
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._id_pools_vsn_ranges.delete(id, force=True, timeout=50)

        mock_delete.assert_called_once_with(id, force=True, timeout=50)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once_with_defaults(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._id_pools_vsn_ranges.delete(id)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_allocate_called_once(self, update):
        information = {
            "count": 5
        }
        id_pools_vsn_range_uri = "/rest/id-pools/vsn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._id_pools_vsn_ranges.allocate(
            information, id_pools_vsn_range_uri)
        update.assert_called_once_with(
            information, id_pools_vsn_range_uri + "/allocator", timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_collect_called_once(self, update):
        information = {
            "idList": [
                "VCG434R000",
                "VCG434R001"
            ]
        }
        id_pools_vsn_range_uri = "/rest/id-pools/vsn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._id_pools_vsn_ranges.collect(
            information, id_pools_vsn_range_uri)
        update.assert_called_once_with(
            information, id_pools_vsn_range_uri + "/collector", timeout=-1)
