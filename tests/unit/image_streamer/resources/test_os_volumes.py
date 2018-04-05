# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2017) Hewlett Packard Enterprise Development LP
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
from hpOneView.image_streamer.resources.os_volumes import OsVolumes
from hpOneView.resources.resource import ResourceClient


class OsVolumesTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._client = OsVolumes(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._client.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default_values(self, mock_get_all):
        self._client.get_all()

        mock_get_all.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._client.get('57f2d803-9c11-4f9a-bc02-71804a0fcc3e')

        mock_get.assert_called_once_with(
            '57f2d803-9c11-4f9a-bc02-71804a0fcc3e')

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._client.get_by('name', 'OSVolume-5')

        mock_get_by.assert_called_once_with(
            'name', 'OSVolume-5')

    @mock.patch.object(ResourceClient, 'get_by_name')
    def test_get_by_name_called_once(self, mock_get_by):
        self._client.get_by_name('OSVolume-5')

        mock_get_by.assert_called_once_with('OSVolume-5')

    @mock.patch.object(ResourceClient, 'download')
    def test_download_archive_called_once_with_id(self, mock_download):
        id = '3518be0e-17c1-4189-8f81-83f3724f6155'

        self._client.download_archive(id, "~/archive.log")

        mock_download.assert_called_once_with('/rest/os-volumes/archive/3518be0e-17c1-4189-8f81-83f3724f6155',
                                              '~/archive.log')

    @mock.patch.object(ResourceClient, 'download')
    def test_download_archive_called_once_with_uri(self, mock_download):
        uri = '/rest/os-volumes/archive/3518be0e-17c1-4189-8f81-83f3724f6155'

        self._client.download_archive(uri, "~/archive.log")

        mock_download.assert_called_once_with('/rest/os-volumes/archive/3518be0e-17c1-4189-8f81-83f3724f6155',
                                              '~/archive.log')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_storage(self, mock_download):
        uri = '/rest/os-volumes/3518be0e-17c1-4189-8f81-83f3724f6155/storage'
        self._client.get(uri)
        mock_download.assert_called_once_with('/rest/os-volumes/3518be0e-17c1-4189-8f81-83f3724f6155/storage')
