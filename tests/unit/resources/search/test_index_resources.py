# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2018) Hewlett Packard Enterprise Development LP
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
from hpOneView.resources.search.index_resources import IndexResources
from hpOneView.resources.resource import ResourceClient


class IndexResourcesTest(unittest.TestCase):

    INDEX_RESOURCE = dict(
        uri="/rest/index/resources/rest/resource/uri",
        resourceUri="/rest/resource/uri",
        type="IndexResourceV300",
        category="the-resource-category",
        created="2014-03-31T02:08:27.884Z",
        modified="2014-03-31T02:08:27.884Z",
        eTag=None,
        members=[{'name': 'sh1'}, {'name': 'sh2'}]
    )

    def return_index(self):
        return self.INDEX_RESOURCE

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._resource = IndexResources(self.connection)

    @mock.patch.object(ResourceClient, 'get_all', return_value=dict(members='test'))
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        expected_uri = '/rest/index/resources?filter=name=TestName&sort=name:ascending'

        self._resource.get_all(start=2, count=500, filter=filter, sort=sort)
        mock_get_all.assert_called_once_with(start=2, count=500, uri=expected_uri)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_without_results(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        expected_uri = '/rest/index/resources?filter=name=TestName&sort=name:ascending'
        self._resource.get_all(start=2, count=500, filter=filter, sort=sort)
        mock_get_all.assert_called_once_with(start=2, count=500, uri=expected_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        index_uri = "/rest/server-hardwares/fake"
        expected_call_uri = "/rest/index/resources/rest/server-hardwares/fake"
        self._resource.get(index_uri)
        mock_get.assert_called_once_with(expected_call_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_aggregated_called_once(self, mock_get_aggregated):

        expected_uri = '/rest/index/resources/aggregated?attribute=Model&attribute=State&category=server-hardware&childLimit=6'

        self._resource.get_aggregated(['Model', 'State'], 'server-hardware')
        mock_get_aggregated.assert_called_once_with(expected_uri)


if __name__ == '__main__':
    unittest.main()
