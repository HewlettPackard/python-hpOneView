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
from hpOneView.resources.servers.id_pools_vwwn_ranges import IdPoolsVwwnRanges
import unittest


class TestIdPoolsRangesVwwn(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._id_pools_vwwn_ranges = IdPoolsVwwnRanges(self.connection)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        vwwn_range = {
            "type": "Range",
            "name": "VWWN",
            "prefix": None,
            "enabled": True,
            "startAddress": "10:00:38:9d:30:60:00:00",
            "endAddress": "10:00:38:9d:30:6f:ff:ff",
            "rangeCategory": "Generated",
            "totalCount": 1048576,
            "freeIdCount": 1048576,
            "allocatedIdCount": 0,
            "defaultRange": True,
            "allocatorUri":
                "/rest/id-pools/vwwn/ranges/daa36872-03b1-463b-aaf7-09d58b650142/allocator",
            "collectorUri":
                "/rest/id-pools/vwwn/ranges/daa36872-03b1-463b-aaf7-09d58b650142/collector",
            "reservedIdCount": 0,
            "freeFragmentUri":
                "/rest/id-pools/vwwn/ranges/daa36872-03b1-463b-aaf7-09d58b650142/free-fragments?start=0&count=-1",
            "allocatedFragmentUri":
                "/rest/id-pools/vwwn/ranges/daa36872-03b1-463b-aaf7-09d58b650142/allocated-fragments?start=0&count=-1",
            "category": "id-range-VWWN",
            "uri":
                "/rest/id-pools/vwwn/ranges/daa36872-03b1-463b-aaf7-09d58b650142",
            "eTag": None,
            "created": "2013-04-08 18:11:18.049",
            "modified": "2013-04-08 18:11:18.049"
        }
        self._id_pools_vwwn_ranges.create(vwwn_range, 70)
        mock_create.assert_called_once_with(vwwn_range, timeout=70)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        id_pools_vwwn_range_id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._id_pools_vwwn_ranges.get(id_pools_vwwn_range_id)
        mock_get.assert_called_once_with(id_pools_vwwn_range_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        id_pools_vwwn_range_uri = "/rest/id-pools/vwwn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._id_pools_vwwn_ranges.get(id_pools_vwwn_range_uri)
        mock_get.assert_called_once_with(id_pools_vwwn_range_uri)

    @mock.patch.object(ResourceClient, 'update')
    def test_enable_called_once(self, update):
        information = {
            "type": "Range",
            "enabled": True
        }
        id_pools_vwwn_range_uri = "/rest/id-pools/vwwn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._id_pools_vwwn_ranges.enable(information, id_pools_vwwn_range_uri)
        update.assert_called_once_with(
            information, id_pools_vwwn_range_uri, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_allocated_fragments_called_once_with_defaults(self, mock_get):
        id_pools_vwwn_range = {
            "uri": "/rest/id-pools/vwwn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c",
        }

        self._id_pools_vwwn_ranges.get_allocated_fragments(
            id_pools_vwwn_range['uri'])
        uri = "/rest/id-pools/vwwn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c/allocated-fragments?start=0&count=-1"
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_allocated_fragments_called_once(self, mock_get):
        id_pools_vwwn_range = {
            "uri": "/rest/id-pools/vwwn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c",
        }

        self._id_pools_vwwn_ranges.get_allocated_fragments(
            id_pools_vwwn_range['uri'], 5, 2)
        uri = "/rest/id-pools/vwwn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c/allocated-fragments?start=2&count=5"
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_free_fragments_called_once_with_defaults(self, mock_get):
        id_pools_vwwn_range = {
            "uri": "/rest/id-pools/vwwn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c",
        }

        self._id_pools_vwwn_ranges.get_free_fragments(
            id_pools_vwwn_range['uri'])
        uri = "/rest/id-pools/vwwn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c/free-fragments?start=0&count=-1"
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_free_fragments_called_once(self, mock_get):
        id_pools_vwwn_range = {
            "uri": "/rest/id-pools/vwwn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c",
        }

        self._id_pools_vwwn_ranges.get_free_fragments(
            id_pools_vwwn_range['uri'], 5, 2)
        uri = "/rest/id-pools/vwwn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c/free-fragments?start=2&count=5"
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._id_pools_vwwn_ranges.delete(id, force=True, timeout=50)

        mock_delete.assert_called_once_with(id, force=True, timeout=50)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once_with_defaults(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._id_pools_vwwn_ranges.delete(id)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_allocate_called_once(self, update):
        information = {
            "count": 5
        }
        id_pools_vwwn_range_uri = "/rest/id-pools/vwwn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._id_pools_vwwn_ranges.allocate(
            information, id_pools_vwwn_range_uri)
        update.assert_called_once_with(
            information, id_pools_vwwn_range_uri + "/allocator", timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_collect_called_once(self, update):
        information = {
            "idList": [
                "VCG434R000",
                "VCG434R001"
            ]
        }
        id_pools_vwwn_range_uri = "/rest/id-pools/vwwn/ranges/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._id_pools_vwwn_ranges.collect(
            information, id_pools_vwwn_range_uri)
        update.assert_called_once_with(
            information, id_pools_vwwn_range_uri + "/collector", timeout=-1)
