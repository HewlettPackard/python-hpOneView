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
from hpOneView.resources.settings.backups import Backups
from hpOneView.resources.resource import ResourceClient


class BackupsTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._client = Backups(self.connection)

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_all_called_once(self, mock_get_collection):
        self._client.get_all()

        mock_get_collection.assert_called_once_with('/rest/backups')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._client.get('appliance_backup_2017-04-20_180138')

        mock_get.assert_called_once_with('appliance_backup_2017-04-20_180138')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/backups/appliance_backup_2017-04-20_180138'

        self._client.get(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'create_with_zero_body')
    def test_create_called_once(self, mock_create):
        mock_create.return_value = {}

        self._client.create()

        mock_create.assert_called_once_with(timeout=-1)

    @mock.patch.object(ResourceClient, 'download')
    def test_download_called_once_by_id(self, mock_download):
        download_uri = '/rest/backups/archive/appliance_backup_2017-04-20_182809'
        destination = 'appliance_backup_2017-04-20_180138.bkp'

        self._client.download(download_uri, destination)

        mock_download.assert_called_once_with('/rest/backups/archive/appliance_backup_2017-04-20_182809', destination)

    @mock.patch.object(ResourceClient, 'upload')
    def test_upload_artifact_bundle_called_once(self, mock_upload):
        filepath = "appliance_backup_2017-04-20_182809.bkp"

        self._client.upload(filepath)

        mock_upload.assert_called_once_with(filepath)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_config_called_once(self, mock_get):
        self._client.get_config()

        mock_get.assert_called_once_with('config')

    @mock.patch.object(ResourceClient, 'update')
    def test_update_config_called_once(self, mock_update):
        options = {"enabled": False}

        self._client.update_config(options, timeout=30)

        mock_update.assert_called_once_with(options, uri='/rest/backups/config', timeout=30)

    @mock.patch.object(ResourceClient, 'update_with_zero_body')
    def test_update_remote_archive_called_once(self, mock_update):
        save_uri = '/rest/backups/remotearchive/appliance_backup_2017-04-20_182809'

        self._client.update_remote_archive(save_uri, timeout=30)

        mock_update.update_with_zero_body(uri=save_uri, timeout=30)
