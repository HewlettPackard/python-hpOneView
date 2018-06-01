# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2018) Hewlett Packard Enterprise Development LP
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
from hpOneView.resources.settings.licenses import Licenses


class LicensesTest(TestCase):
    DEFAULT_HOST = '127.0.0.1'

    def setUp(self):
        oneview_connection = connection(self.DEFAULT_HOST)
        self.resource = Licenses(oneview_connection)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        data = {
            'key': 'ASD8 JKL7 UYT9',
            'type': 'LicenseListV500'
        }
        self.resource.create(data)
        mock_create.assert_called_once_with(data, timeout=-1, default_values=self.resource.DEFAULT_VALUES)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = '54'
        self.resource.delete(id)
        mock_delete.assert_called_once_with(id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get_by_id):
        id = '/rest/licenses/54'
        self.resource.get_by_id(id)
        mock_get_by_id.assert_called_once_with(id)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        self.resource.get_all(2, 500, filter, sort)
        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)
