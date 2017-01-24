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
from hpOneView.resources.resource import ResourceClient
from hpOneView.resources.storage.sas_logical_jbods import SasLogicalJbods


class SasLogicalJbodsTest(unittest.TestCase):

    SAS_LOGICAL_JBOD_ID = 'c8ed5329-f9c1-492c-aa46-b78665ee7734'
    SAS_LOGICAL_JBOD_URI = '/rest/sas-logical-jbods/' + SAS_LOGICAL_JBOD_ID

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._resource = SasLogicalJbods(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        args = dict(
            start=2,
            count=500,
            filter='name=TestName',
            sort='name:ascending'
        )

        self._resource.get_all(**args)
        mock_get_all.assert_called_once_with(**args)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._resource.get(id_or_uri=self.SAS_LOGICAL_JBOD_ID)
        mock_get.assert_called_once_with(id_or_uri=self.SAS_LOGICAL_JBOD_ID)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._resource.get_by('name', 'SAS Logical JBOD Name')

        mock_get_by.assert_called_once_with('name', 'SAS Logical JBOD Name')

    @mock.patch.object(ResourceClient, 'build_uri')
    @mock.patch.object(ResourceClient, 'get')
    def test_get_drives_called_once(self, mock_get, mock_build_uri):
        mock_build_uri.return_value = self.SAS_LOGICAL_JBOD_URI
        self._resource.get_drives(id_or_uri=self.SAS_LOGICAL_JBOD_ID)

        expected_uri = self.SAS_LOGICAL_JBOD_URI + SasLogicalJbods.DRIVES_PATH
        mock_build_uri.assert_called_once_with(id_or_uri=self.SAS_LOGICAL_JBOD_ID)
        mock_get.assert_called_once_with(id_or_uri=expected_uri)
