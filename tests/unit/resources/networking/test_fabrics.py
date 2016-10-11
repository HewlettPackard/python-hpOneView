# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
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
from hpOneView.resources.networking.fabrics import Fabrics
from hpOneView.resources.resource import ResourceClient


class FabricsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._fabrics = Fabrics(self.connection)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._fabrics.get('7a9f7d09-3c24-4efe-928f-50a1af411120')

        mock_get.assert_called_once_with(
            '7a9f7d09-3c24-4efe-928f-50a1af411120')

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._fabrics.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._fabrics.get_by('name', 'DefaultFabric')

        mock_get_by.assert_called_once_with('name', 'DefaultFabric')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_reserved_vlan_range(self, mock_get):
        uri = '/rest/fabrics/123/reserved-vlan-range'
        self._fabrics.get_reserved_vlan_range('123')

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_reserved_vlan_range(self, mock_update):
        uri = '/rest/fabrics/123/reserved-vlan-range'
        data_to_update = {
            "start": 100,
            "length": 100
        }

        self._fabrics.update_reserved_vlan_range('123', data_to_update)

        mock_update.assert_called_once_with(
            resource=data_to_update,
            uri=uri,
            force=False,
            default_values=Fabrics.DEFAULT_VALUES
        )
