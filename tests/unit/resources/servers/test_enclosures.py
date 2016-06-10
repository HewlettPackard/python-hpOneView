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
from hpOneView.resources.servers.enclosures import Enclosures
from hpOneView.resources.resource import ResourceClient


class EnclosuresTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._enclosures = Enclosures(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._enclosures.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default_values(self, mock_get_all):
        self._enclosures.get_all()

        mock_get_all.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._enclosures.get_by('name', 'OneViewSDK-Test-Enclosure')

        mock_get_by.assert_called_once_with('name', 'OneViewSDK-Test-Enclosure')

    @mock.patch.object(ResourceClient, 'create')
    def test_add_called_once(self, mock_create):
        information = {
            'enclosureGroupUri': '/rest/enclosure-groups/id-enclosure-group'
        }
        mock_create.return_value = {}

        self._enclosures.add(information)
        mock_create.assert_called_once_with(information.copy())

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._enclosures.get('3518be0e-17c1-4189-8f81-83f3724f6155')

        mock_get.assert_called_once_with('3518be0e-17c1-4189-8f81-83f3724f6155')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/enclosures/3518be0e-17c1-4189-8f81-83f3724f6155'
        self._enclosures.get(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'patch')
    def test_patch_should_use_user_defined_values(self, mock_patch):
        mock_patch.return_value = {}

        self._enclosures.patch('123a53cz', 'replace', '/name', 'new_name', False)
        mock_patch.assert_called_once_with('123a53cz', 'replace', '/name', 'new_name', blocking=False)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._enclosures.remove(id, force=False)

        mock_delete.assert_called_once_with(id, force=False)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove_called_once_with_force(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._enclosures.remove(id, force=True)

        mock_delete.assert_called_once_with(id, force=True)

    @mock.patch.object(ResourceClient, 'get_utilization')
    def test_get_utilization_with_all_args(self, mock_get_utilization):
        self._enclosures.get_utilization('09USE7335NW3', fields='AmbientTemperature,AveragePower,PeakPower',
                                         filter='startDate=2016-05-30T03:29:42.361Z',
                                         refresh=True, view='day')

        mock_get_utilization.assert_called_once_with('09USE7335NW3', fields='AmbientTemperature,AveragePower,PeakPower',
                                                     filter='startDate=2016-05-30T03:29:42.361Z',
                                                     refresh=True, view='day')

    @mock.patch.object(ResourceClient, 'get_utilization')
    def test_get_utilization_with_defaults(self, mock_get):
        self._enclosures.get_utilization('09USE7335NW3')

        mock_get.assert_called_once_with('09USE7335NW3', fields=None, filter=None, refresh=False, view=None)
