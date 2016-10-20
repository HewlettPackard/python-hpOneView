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
from hpOneView.resources.storage.drive_enclosures import DriveEnclosures
from hpOneView.resources.resource import ResourceClient


class DriveEnclosuresTest(unittest.TestCase):

    DRIVE_ENCLOSURE_ID = "SN123101"
    DRIVE_ENCLOSURE_URI = "/rest/drive-enclosures/" + DRIVE_ENCLOSURE_ID

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._drive_enclosures = DriveEnclosures(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._drive_enclosures.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(start=2, count=500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._drive_enclosures.get_all()
        mock_get_all.assert_called_once_with(start=0, count=-1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        self._drive_enclosures.get(self.DRIVE_ENCLOSURE_ID)
        mock_get.assert_called_once_with(id_or_uri=self.DRIVE_ENCLOSURE_ID)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        field = 'serialNumber'
        value = 'SN123101'

        self._drive_enclosures.get_by(field, value)
        mock_get_by.assert_called_once_with(field=field, value=value)

    @mock.patch.object(ResourceClient, 'build_uri')
    @mock.patch.object(ResourceClient, 'get')
    def test_get_port_map_called_once(self, mock_get, mock_build_uri):
        mock_build_uri.return_value = self.DRIVE_ENCLOSURE_URI
        self._drive_enclosures.get_port_map(self.DRIVE_ENCLOSURE_ID)

        expected_uri = self.DRIVE_ENCLOSURE_URI + DriveEnclosures.PORT_MAP_PATH
        mock_get.assert_called_once_with(id_or_uri=expected_uri)

    @mock.patch.object(ResourceClient, 'build_uri')
    @mock.patch.object(ResourceClient, 'update')
    def test_refresh_state_called_once(self, mock_update, mock_build_uri):
        refresh_config = dict(refreshState="RefreshPending")
        mock_build_uri.return_value = self.DRIVE_ENCLOSURE_URI
        self._drive_enclosures.refresh_state(id_or_uri=self.DRIVE_ENCLOSURE_ID, configuration=refresh_config)

        expected_uri = self.DRIVE_ENCLOSURE_URI + DriveEnclosures.REFRESH_STATE_PATH
        mock_update.assert_called_once_with(uri=expected_uri, resource=refresh_config, timeout=-1)

    @mock.patch.object(ResourceClient, 'patch')
    def test_patch_called_once(self, mock_patch):
        patch_config = dict(
            id_or_uri=self.DRIVE_ENCLOSURE_URI,
            operation="replace",
            path="/powerState",
            value="Off"
        )

        self._drive_enclosures.patch(**patch_config)
        mock_patch.assert_called_once_with(timeout=-1, **patch_config)
