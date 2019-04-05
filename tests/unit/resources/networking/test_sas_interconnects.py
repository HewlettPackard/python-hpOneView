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

from hpOneView.resources.networking.sas_interconnects import SasInterconnects
from hpOneView.resources.resource import ResourceHelper, ResourcePatchMixin


class SasInterconnectsTest(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self._sas_interconnects = SasInterconnects(None)
        self.uri = '/rest/sas-interconnects/3518be0e-17c1-4189-8f81-83f3724f6155'
        self._sas_interconnects.data = {"uri": self.uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._sas_interconnects.get_all(2, 500, filter=filter, sort=sort)
        mock_get_all.assert_called_once_with(start=2, count=500, filter=filter, sort=sort, query='', view='', fields='')

    @mock.patch.object(ResourcePatchMixin, 'patch_request')
    def test_patch_called_once(self, mock_patch_request):
        args = dict(
            operation='replace',
            path='/deviceResetState',
            value='Reset',
        )

        self._sas_interconnects.patch(**args)
        mock_patch_request.assert_called_once_with(self.uri,
                                                   body=[{'path': '/deviceResetState',
                                                          'op': 'replace',
                                                          'value': 'Reset'}],
                                                   custom_headers=None, timeout=-1)

    @mock.patch.object(ResourceHelper, 'update')
    def test_refresh_state_called_once(self, mock_update):
        configuration = dict(refreshState="RefreshPending")
        expected_uri = "{}/refreshState".format(self.uri)

        self._sas_interconnects.refresh_state(configuration=configuration)

        mock_update.assert_called_once_with(resource=configuration, uri=expected_uri)
