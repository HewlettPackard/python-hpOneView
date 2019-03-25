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
from hpOneView.resources.networking.interconnect_types import InterconnectTypes
from hpOneView.resources.resource import Resource, ResourceHelper


class InterconnectTypesTest(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._interconnect_types = InterconnectTypes(self.connection)

    @mock.patch.object(ResourceHelper, 'do_requests_to_getall')
    def test_get_all_called_once(self, mock_do_get):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._interconnect_types.get_all(2, 500, filter=filter, sort=sort)

        mock_do_get.assert_called_once_with('/rest/interconnect-types?start=2&count=500&filter=name%3DTestName&sort=name%3Aascending', 500)

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._interconnect_types.get_by_name('HP VC Flex-10 Enet Module')

        mock_get_by.assert_called_once_with(
            'name', 'HP VC Flex-10 Enet Module')
