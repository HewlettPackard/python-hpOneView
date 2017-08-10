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
from hpOneView.resources.storage.volumes import INVALID_VOLUME_URI
from hpOneView.resources.storage.volumes import Volumes


class VolumesTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._volumes = Volumes(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._volumes.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._volumes.get_by('name', 'Test Volume')

        mock_get_by.assert_called_once_with('name', 'Test Volume')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        self._volumes.get('3518be0e-17c1-4189-8f81-83f3724f6155')

        mock_get.assert_called_once_with('3518be0e-17c1-4189-8f81-83f3724f6155')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        self._volumes.get('/rest/storage-volumes/3518be0e-17c1-4189-8f81-83f3724f6155')

        mock_get.assert_called_once_with('/rest/storage-volumes/3518be0e-17c1-4189-8f81-83f3724f6155')

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        resource = {
            'name': 'ONEVIEW_SDK_TEST_VOLUME_TYPE_1'
        }
        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self._volumes.create(resource)
        mock_create.assert_called_once_with(resource_rest_call, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_update):
        resource = {
            'uri': '/rest/storage-volumes/3518be0e-17c1-4189-8f81-83f3724f6155',
            'name': 'ONEVIEW_SDK_TEST_VOLUME_TYPE_1'
        }
        resource_rest_call = resource.copy()

        self._volumes.update(resource)

        mock_update.assert_called_once_with(resource_rest_call, timeout=-1, force=False)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once_with_force(self, mock_update):
        resource = {
            'uri': '/rest/storage-volumes/3518be0e-17c1-4189-8f81-83f3724f6155',
            'name': 'ONEVIEW_SDK_TEST_VOLUME_TYPE_1'
        }
        resource_rest_call = resource.copy()

        self._volumes.update(resource, force=True)

        mock_update.assert_called_once_with(resource_rest_call, timeout=mock.ANY, force=True)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_by_id_called_once(self, mock_delete):
        id = 'fake'
        uri = '/rest/storage-volumes/fake'
        self._volumes.delete(id, force=False, timeout=-1)

        expected_headers = {"If-Match": '*'}
        mock_delete.assert_called_once_with(uri, force=False, timeout=-1, custom_headers=expected_headers)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_with_force_called_once(self, mock_delete):
        uri = '/rest/storage-volumes/fake'
        self._volumes.delete(uri, force=True)

        mock_delete.assert_called_once_with(mock.ANY, force=True, timeout=mock.ANY, custom_headers=mock.ANY)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_only_from_oneview_called_once_api300(self, mock_delete):
        uri = '/rest/storage-volumes/fake'
        self._volumes.delete(uri, export_only=True)

        expected_headers = {'If-Match': '*', "exportOnly": True}
        mock_delete.assert_called_once_with(uri, force=mock.ANY, timeout=mock.ANY, custom_headers=expected_headers)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_only_from_oneview_called_once_api500(self, mock_delete):
        uri = '/rest/storage-volumes/fake'
        extended_uri = '/rest/storage-volumes/fake?suppressDeviceUpdates=true'
        self._volumes.delete(uri, suppress_device_updates=True)

        expected_headers = {'If-Match': '*'}
        mock_delete.assert_called_once_with(extended_uri, force=mock.ANY,
                                            timeout=mock.ANY, custom_headers=expected_headers)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_snapshots_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        volume_id = '280FF951-F007-478F-AC29-E4655FC76DDC'
        uri = '/rest/storage-volumes/280FF951-F007-478F-AC29-E4655FC76DDC/snapshots/'

        self._volumes.get_snapshots(volume_id, 2, 500, filter, sort)
        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort, uri=uri)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_snapshots_called_once_with_default(self, mock_get_all):
        volume_id = '280FF951-F007-478F-AC29-E4655FC76DDC'
        uri = '/rest/storage-volumes/280FF951-F007-478F-AC29-E4655FC76DDC/snapshots/'
        self._volumes.get_snapshots(volume_id)
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='', uri=uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_snapshot_by_id_called_once(self, mock_get):
        volume_id = '280FF951-F007-478F-AC29-E4655FC76DDC'
        snapshot_id = '78216B75-3CC4-4444-BB5B-13C7504675'
        uri = '/rest/storage-volumes/280FF951-F007-478F-AC29-E4655FC76DDC/snapshots/78216B75-3CC4-4444-BB5B-13C7504675'
        self._volumes.get_snapshot(snapshot_id, volume_id)
        mock_get.assert_called_once_with(uri)

    def test_get_snapshot_by_id_without_volume_id_should_fail(self):
        snapshot_id = '78216B75-3CC4-4444-BB5B-13C7504675'
        try:
            self._volumes.get_snapshot(snapshot_id)
        except ValueError as e:
            self.assertEqual(INVALID_VOLUME_URI, e.args[0])
        else:
            self.fail("Expected exception was not raised")

    @mock.patch.object(ResourceClient, 'get')
    def test_get_get_snapshot_by_uri_called_once(self, mock_get):
        snapshot_uri = '/rest/storage-volumes/280FF951-F007-478F-AC29-E4655FC/snapshots/78216B75-3CC4-4444-B5B-13046'
        self._volumes.get_snapshot(snapshot_uri)
        mock_get.assert_called_once_with(snapshot_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_get_snapshot_by_uri_and_volume_id_called_once(self, mock_get):
        snapshot_uri = '/rest/storage-volumes/280FF951-F007-478F-AC29-E4655FC/snapshots/78216B75-3CC4-4444-B5B-13046'
        volume_id = '280FF951-F007-478F-AC29-E4655FC'
        self._volumes.get_snapshot(snapshot_uri, volume_id)
        mock_get.assert_called_once_with(snapshot_uri)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_snapshot_should_be_called_once(self, mock_create):
        volume_id = '280FF951-F007-478F-AC29-E4655FC'
        uri = '/rest/storage-volumes/280FF951-F007-478F-AC29-E4655FC/snapshots/'
        resource = {
            'name': 'OneViewSDK Test Snapshot',
        }

        self._volumes.create_snapshot(volume_id, resource, 20)
        mock_create.assert_called_once_with(resource, uri=uri, timeout=20,
                                            default_values=self._volumes.DEFAULT_VALUES_SNAPSHOT)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_snapshot_called_once(self, mock_delete):
        resource = {
            'name': 'OneViewSDK Test Snapshot',
            'type': 'SnapshotV3',
            'uri': '/rest/storage-volumes/280FF951-F007-478F-AC29-E4655FC/snapshots/78216B75-3CC4-4444-B5B-13046'
        }
        expected_headers = {"If-Match": '*'}
        self._volumes.delete_snapshot(resource, force=True, timeout=50)

        mock_delete.assert_called_once_with(resource, force=True, timeout=50, custom_headers=expected_headers)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_snapshot_called_once_with_defaults(self, mock_delete):
        resource = {
            'name': 'OneViewSDK Test Snapshot',
            'type': 'SnapshotV3',
            'uri': '/rest/storage-volumes/280FF951-F007-478F-AC29-E4655FC/snapshots/78216B75-3CC4-4444-B5B-13046'
        }
        expected_headers = {"If-Match": '*'}

        self._volumes.delete_snapshot(resource)

        mock_delete.assert_called_once_with(resource, force=False, timeout=-1, custom_headers=expected_headers)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_snapshot_by_called_once(self, mock_get_by):
        volume_id = '280FF951-F007-478F-AC29-E4655FC'
        volume_uri = '/rest/storage-volumes/280FF951-F007-478F-AC29-E4655FC/snapshots/'
        self._volumes.get_snapshot_by(volume_id, "name", "test name")

        mock_get_by.assert_called_once_with("name", "test name", uri=volume_uri)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_extra_managed_storage_volume_paths_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._volumes.get_extra_managed_storage_volume_paths(2, 500, filter, sort)

        expected_uri = '/rest/storage-volumes/repair?alertFixType=ExtraManagedStorageVolumePaths'
        mock_get_all.assert_called_once_with(2, 500, uri=expected_uri, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'create')
    def test_repair_by_id_called_once(self, mock_create):
        volume_id = '280FF951-F007-478F-AC29-E4655FC'
        data = {
            'resourceUri': '/rest/storage-volumes/280FF951-F007-478F-AC29-E4655FC',
            'type': 'ExtraManagedStorageVolumePaths'
        }
        self._volumes.repair(volume_id)

        custom_headers = {u'Accept-Language': u'en_US'}
        mock_create.assert_called_once_with(data, uri='/rest/storage-volumes/repair', timeout=-1,
                                            custom_headers=custom_headers)

    @mock.patch.object(ResourceClient, 'create')
    def test_repair_by_uri_called_once(self, mock_create):
        volume_id = '/rest/storage-volumes/280FF951-F007-478F-AC29-E4655FC'
        data = {
            'resourceUri': '/rest/storage-volumes/280FF951-F007-478F-AC29-E4655FC',
            'type': 'ExtraManagedStorageVolumePaths'
        }
        self._volumes.repair(volume_id)

        custom_headers = {u'Accept-Language': u'en_US'}
        mock_create.assert_called_once_with(data, uri='/rest/storage-volumes/repair', timeout=-1,
                                            custom_headers=custom_headers)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_attachable_volumes_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        query = 'availableNetworks IN [/rest/fc-networks/123-45-67,/rest/fc-networks/111-222-333]'

        self._volumes.get_attachable_volumes(2, 500, filter, query, sort)

        expected_uri = '/rest/storage-volumes/attachable-volumes'
        mock_get_all.assert_called_once_with(2, 500, uri=expected_uri, filter=filter, query=query, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_attachable_volumes_called_with_default_values(self, mock_get_all):
        self._volumes.get_attachable_volumes()

        expected_uri = '/rest/storage-volumes/attachable-volumes'
        mock_get_all.assert_called_once_with(0, -1, uri=expected_uri, filter='', query='', sort='')

    @mock.patch.object(ResourceClient, 'create')
    def test_create_from_snapshot_called_once(self, mock_create):
        data = {
            'fake': 'data'
        }
        self._volumes.create_from_snapshot(data)
        mock_create.assert_called_once_with(data, uri='/rest/storage-volumes/from-snapshot', timeout=-1)

    @mock.patch.object(ResourceClient, 'create')
    def test_add_from_existing_called_once(self, mock_create):
        data = {
            'fake': 'data'
        }
        self._volumes.add_from_existing(data)
        mock_create.assert_called_once_with(data, uri='/rest/storage-volumes/from-existing', timeout=-1)
