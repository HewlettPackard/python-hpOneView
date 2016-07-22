# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
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
    def test_create_snapshot_should_use_default_values(self, mock_create):
        volume_id = '280FF951-F007-478F-AC29-E4655FC'
        uri = '/rest/storage-volumes/280FF951-F007-478F-AC29-E4655FC/snapshots/'
        resource = {
            'name': 'OneViewSDK Test Snapshot',
        }
        resource_with_default_values = {
            'name': 'OneViewSDK Test Snapshot',
            'type': 'Snapshot',
        }

        self._volumes.create_snapshot(volume_id, resource)
        mock_create.assert_called_once_with(resource_with_default_values, uri=uri, timeout=-1)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_snapshot_should_use_given_values(self, mock_create):
        volume_id = '280FF951-F007-478F-AC29-E4655FC'
        uri = '/rest/storage-volumes/280FF951-F007-478F-AC29-E4655FC/snapshots/'
        resource = {
            'name': 'OneViewSDK Test Snapshot',
            'type': 'SnapshotV3',
        }

        self._volumes.create_snapshot(volume_id, resource)
        mock_create.assert_called_once_with(resource, uri=uri, timeout=-1)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        resource = {
            'name': 'OneViewSDK Test Snapshot',
            'type': 'SnapshotV3',
            'uri': '/rest/storage-volumes/280FF951-F007-478F-AC29-E4655FC/snapshots/78216B75-3CC4-4444-B5B-13046'
        }
        self._volumes.delete_snapshot(resource, force=True, timeout=50)

        mock_delete.assert_called_once_with(resource, force=True, timeout=50)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once_with_defaults(self, mock_delete):
        resource = {
            'name': 'OneViewSDK Test Snapshot',
            'type': 'SnapshotV3',
            'uri': '/rest/storage-volumes/280FF951-F007-478F-AC29-E4655FC/snapshots/78216B75-3CC4-4444-B5B-13046'
        }
        self._volumes.delete_snapshot(resource)

        mock_delete.assert_called_once_with(resource, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_snapshot_by_called_once(self, mock_get_by):
        volume_id = '280FF951-F007-478F-AC29-E4655FC'
        volume_uri = '/rest/storage-volumes/280FF951-F007-478F-AC29-E4655FC/snapshots/'
        self._volumes.get_snapshot_by(volume_id, "name", "test name")

        mock_get_by.assert_called_once_with("name", "test name", uri=volume_uri)
