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

from hpOneView.resources.networking.sas_interconnects import SasInterconnects
from hpOneView.resources.resource import ResourceClient


class SasInterconnectsTest(unittest.TestCase):

    SAS_INTERCONNECT_URI = '/rest/sas-interconnects/3518be0e-17c1-4189-8f81-83f3724f6155'

    def setUp(self):
        self.host = '127.0.0.1'
        self._sas_interconnects = SasInterconnects(None)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._sas_interconnects.get_all(2, 500, filter=filter, sort=sort)
        mock_get_all.assert_called_once_with(start=2, count=500, filter=filter, sort=sort, query='', view='', fields='')

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        sas_interconnect_name = "0000A66103, interconnect 4"
        self._sas_interconnects.get_by('name', sas_interconnect_name)
        mock_get_by.assert_called_once_with('name', sas_interconnect_name)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        sas_interconnect_id = '3518be0e-17c1-4189-8f81-83f3724f6155'
        self._sas_interconnects.get(id_or_uri=sas_interconnect_id)
        mock_get.assert_called_once_with(sas_interconnect_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        self._sas_interconnects.get(id_or_uri=self.SAS_INTERCONNECT_URI)
        mock_get.assert_called_once_with(self.SAS_INTERCONNECT_URI)

    @mock.patch.object(ResourceClient, 'patch')
    def test_patch_called_once(self, mock_patch):
        args = dict(
            id_or_uri=self.SAS_INTERCONNECT_URI,
            operation='replace',
            path='/deviceResetState',
            value='Reset',
        )

        self._sas_interconnects.patch(**args)
        mock_patch.assert_called_once_with(timeout=-1, **args)

    @mock.patch.object(ResourceClient, 'build_uri')
    @mock.patch.object(ResourceClient, 'update')
    def test_refresh_state_called_once(self, mock_update, mock_build_uri):
        configuration = dict(refreshState="RefreshPending")
        expected_uri = self.SAS_INTERCONNECT_URI + "/refreshState"

        mock_build_uri.return_value = self.SAS_INTERCONNECT_URI
        self._sas_interconnects.refresh_state(id_or_uri=self.SAS_INTERCONNECT_URI, configuration=configuration)

        mock_build_uri.assert_called_once_with(self.SAS_INTERCONNECT_URI)
        mock_update.assert_called_once_with(uri=expected_uri, resource=configuration)
