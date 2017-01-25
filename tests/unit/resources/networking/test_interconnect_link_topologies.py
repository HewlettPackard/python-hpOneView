# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2017) Hewlett Packard Enterprise Development LP
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
from hpOneView.resources.networking.interconnect_link_topologies import InterconnectLinkTopologies
from hpOneView.resources.resource import ResourceClient


class InterconnectLinkTopologiesTest(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._interconnect_link_topologies = InterconnectLinkTopologies(self.connection)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once_by_id(self, mock_get):
        ilt_id = 'c6f4e705-2bb5-430a-b7a1-a35b2f7aa9b9'
        self._interconnect_link_topologies.get(ilt_id)

        mock_get.assert_called_once_with(ilt_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once_by_uri(self, mock_get):
        ilt_uri = '/rest/interconnect-link-topologies/c6f4e705-2bb5-430a-b7a1-a35b2f7aa9b9'
        self._interconnect_link_topologies.get(ilt_uri)

        mock_get.assert_called_once_with(ilt_uri)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._interconnect_link_topologies.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._interconnect_link_topologies.get_by('name', 'sample name')

        mock_get_by.assert_called_once_with(
            'name', 'sample name')
