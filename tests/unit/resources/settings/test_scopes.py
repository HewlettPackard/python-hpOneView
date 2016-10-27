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

from unittest import TestCase

import mock

from hpOneView.connection import connection
from hpOneView.resources.resource import ResourceClient
from hpOneView.resources.settings.scopes import Scopes


class ScopesTest(TestCase):
    DEFAULT_HOST = '127.0.0.1'

    def setUp(self):
        oneview_connection = connection(self.DEFAULT_HOST)
        self.resource = Scopes(oneview_connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all(self, mock_get_all):
        filter_by = 'name=TestName'
        sort = 'name:ascending'

        self.resource.get_all(2, 500, filter_by, sort)
        mock_get_all.assert_called_once_with(2, 500, filter=filter_by, sort=sort)

    @mock.patch.object(ResourceClient, 'patch_request')
    def test_update_resource_assignments_called_once(self, mock_patch_request):
        uri = '/rest/scopes/11c466d1-0ade-4aae-8317-2fb20b6ef3f2'

        information = {
            "addedResourceUris": ["/rest/ethernet-networks/e801b73f-b4e8-4b32-b042-36f5bac2d60f"],
            "removedResourceUris": ["/rest/ethernet-networks/390bc9f9-cdd5-4c70-b38f-cf04e64f5c72"]
        }
        self.resource.update_resource_assignments(uri, information)

        mock_patch_request.assert_called_once_with(
            '/rest/scopes/11c466d1-0ade-4aae-8317-2fb20b6ef3f2/resource-assignments',
            information.copy(),
            custom_headers={'Content-Type': 'application/json'},
            timeout=-1)
