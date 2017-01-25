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
from hpOneView.resources.storage.storage_volume_attachments import StorageVolumeAttachments
from hpOneView.resources.resource import ResourceClient


class StorageVolumeAttachmentsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._storage_volume_attachments = StorageVolumeAttachments(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._storage_volume_attachments.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._storage_volume_attachments.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        storage_volume_attachments_id = "4C259D33-0195-4374-9DA9-51FE443E2408"
        self._storage_volume_attachments.get(storage_volume_attachments_id)
        mock_get.assert_called_once_with(storage_volume_attachments_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        storage_volume_attachments_uri = "/rest/storage-volume-attachments/4C259D33-0195-4374-9DA9-51FE443E2408"
        self._storage_volume_attachments.get(storage_volume_attachments_uri)
        mock_get.assert_called_once_with(storage_volume_attachments_uri)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_extra_unmanaged_storage_volumes_called_once(self, mock_get):
        storage_volume_attachments_host_types_uri = \
            "/rest/storage-volume-attachments/repair?alertFixType=ExtraUnmanagedStorageVolumes"
        self._storage_volume_attachments.get_extra_unmanaged_storage_volumes()
        mock_get.assert_called_once_with(start=0, count=-1, filter='', sort='',
                                         uri=storage_volume_attachments_host_types_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_paths_called_once_with_uri(self, mock_get):
        storage_volume_attachments_uri = "/rest/storage-volume-attachments/4C259D33-0195-4374-9DA9-51FE443E2408"
        storage_volume_attachments_paths_uri = \
            "/rest/storage-volume-attachments/4C259D33-0195-4374-9DA9-51FE443E2408/paths"
        self._storage_volume_attachments.get_paths(storage_volume_attachments_uri)
        mock_get.assert_called_once_with(storage_volume_attachments_paths_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_paths_called_once_with_id(self, mock_get):
        storage_volume_attachments_id = "4C259D33-0195-4374-9DA9-51FE443E2408"
        storage_volume_attachments_paths_uri = \
            "/rest/storage-volume-attachments/4C259D33-0195-4374-9DA9-51FE443E2408/paths"
        self._storage_volume_attachments.get_paths(storage_volume_attachments_id)
        mock_get.assert_called_once_with(storage_volume_attachments_paths_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_paths_called_once_with_uri_and_path_id(self, mock_get):
        storage_volume_attachments_uri = "/rest/storage-volume-attachments/4C259D33-0195-4374-9DA9-51FE443E2408"
        path_id = "C862833E-907C-4124-8841-BDC75444CF76"
        storage_volume_attachments_paths_uri = "/rest/storage-volume-attachments/4C259D33-0195-4374-9DA9-51FE443E2408" \
                                               "/paths/C862833E-907C-4124-8841-BDC75444CF76"
        self._storage_volume_attachments.get_paths(storage_volume_attachments_uri, path_id)
        mock_get.assert_called_once_with(storage_volume_attachments_paths_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_paths_called_once_with_id_and_path_id(self, mock_get):
        storage_volume_attachments_id = "4C259D33-0195-4374-9DA9-51FE443E2408"
        path_id = "C862833E-907C-4124-8841-BDC75444CF76"
        storage_volume_attachments_paths_uri = "/rest/storage-volume-attachments/4C259D33-0195-4374-9DA9-51FE443E2408" \
                                               "/paths/C862833E-907C-4124-8841-BDC75444CF76"
        self._storage_volume_attachments.get_paths(storage_volume_attachments_id, path_id)
        mock_get.assert_called_once_with(storage_volume_attachments_paths_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_paths_called_once_with_uri_and_path_uri(self, mock_get):
        storage_volume_attachments_uri = "/rest/storage-volume-attachments/4C259D33-0195-4374-9DA9-51FE443E2408"
        path_uri = "/rest/storage-volume-attachments/4C259D33-0195-4374-9DA9-51FE443E2408" \
                   "/paths/C862833E-907C-4124-8841-BDC75444CF76"
        storage_volume_attachments_paths_uri = "/rest/storage-volume-attachments/4C259D33-0195-4374-9DA9-51FE443E2408" \
                                               "/paths/C862833E-907C-4124-8841-BDC75444CF76"
        self._storage_volume_attachments.get_paths(storage_volume_attachments_uri, path_uri)
        mock_get.assert_called_once_with(storage_volume_attachments_paths_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_paths_called_once_with_id_and_path_uri(self, mock_get):
        storage_volume_attachments_id = "4C259D33-0195-4374-9DA9-51FE443E2408"
        path_uri = "/rest/storage-volume-attachments/4C259D33-0195-4374-9DA9-51FE443E2408/paths/" \
                   "C862833E-907C-4124-8841-BDC75444CF76"
        storage_volume_attachments_paths_uri = "/rest/storage-volume-attachments/4C259D33-0195-4374-9DA9-51FE443E2408" \
                                               "/paths/C862833E-907C-4124-8841-BDC75444CF76"
        self._storage_volume_attachments.get_paths(storage_volume_attachments_id, path_uri)
        mock_get.assert_called_once_with(storage_volume_attachments_paths_uri)

    @mock.patch.object(ResourceClient, 'create')
    def test_remove_extra_presentations_called_once_with_defaults(self, mock_create):
        info = {
            "type": "ExtraUnmanagedStorageVolumes",
            "resourceUri": "/rest/server-profiles/123-45-67-89-124"
        }
        self._storage_volume_attachments.remove_extra_presentations(info)
        mock_create.assert_called_once_with(
            info, uri='/rest/storage-volume-attachments/repair', timeout=-1,
            custom_headers={'Accept-Language': 'en_US'})

    @mock.patch.object(ResourceClient, 'create')
    def test_remove_extra_presentations_called_once(self, mock_create):
        info = {
            "type": "ExtraUnmanagedStorageVolumes",
            "resourceUri": "/rest/server-profiles/123-45-67-89-124"
        }
        self._storage_volume_attachments.remove_extra_presentations(info, 70)
        mock_create.assert_called_once_with(
            info, uri='/rest/storage-volume-attachments/repair', timeout=70,
            custom_headers={'Accept-Language': 'en_US'})

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._storage_volume_attachments.get_by("name", "test name")
        mock_get_by.assert_called_once_with("name", "test name")
