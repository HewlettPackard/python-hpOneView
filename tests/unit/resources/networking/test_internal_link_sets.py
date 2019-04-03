# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2019) Hewlett Packard Enterprise Development LP
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
from hpOneView.resources.networking.internal_link_sets import InternalLinkSets
from hpOneView.resources.resource import ResourceHelper

INTERNAL_LINK_SETS = [
    {'name': 'OneViewSDK Test Internal Link Set'},
    {'name': 'test'},
    {'name': 'OneViewSDK Test Internal Link Set'},
    {'name': 'abc'},
]


class InternalLinkSetsTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._client = InternalLinkSets(self.connection)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        query = 'teste'
        fields = 'a,b,c'
        view = 'teste'

        self._client.get_all(2, 500, filter, query, sort, view, fields)

        mock_get_all.assert_called_once_with(start=2, count=500, filter=filter, sort=sort, query=query, fields=fields,
                                             view=view)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_without_parameters(self, mock_get_all):
        self._client.get_all()
        mock_get_all.assert_called_once_with(start=0, count=-1, filter='', sort='', query='', fields='', view='')

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_called_once(self, mock_get_all):
        mock_get_all.return_value = INTERNAL_LINK_SETS
        expected_result = [
            {'name': 'OneViewSDK Test Internal Link Set'},
            {'name': 'OneViewSDK Test Internal Link Set'},
        ]

        result = self._client.get_by('name', 'OneViewSDK Test Internal Link Set')

        self.assertEqual(result, expected_result)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_should_return_empty_list_when_not_match(self, mock_get_all):
        mock_get_all.return_value = INTERNAL_LINK_SETS
        expected_result = []

        result = self._client.get_by('name', 'Testing')

        self.assertEqual(result, expected_result)
