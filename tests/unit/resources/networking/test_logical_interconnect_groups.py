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

from hpOneView.connection import connection
from hpOneView.resources.networking.logical_interconnect_groups import LogicalInterconnectGroups
from hpOneView.resources.resource import Resource, ResourceHelper, ResourcePatchMixin


class LogicalInterconnectGroupsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._lig = LogicalInterconnectGroups(self.connection)
        self.uri = "/rest/logical-interconnect-groups/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._lig.data = {"uri": self.uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        scope_uris = 'TestScope'

        self._lig.get_all(2, 500, filter, sort, scope_uris)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort, scope_uris=scope_uris)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._lig.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='', scope_uris='')

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_default_settings_called_once(self, mock_get):
        lig_settings_uri = "/rest/logical-interconnect-groups/defaultSettings"
        self._lig.get_default_settings()
        mock_get.assert_called_once_with(lig_settings_uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_settings_called_once_when_lig_uri_provided(self, mock_get):
        lig_settings_uri = "{}/settings".format(self.uri)
        self._lig.get_settings()
        mock_get.assert_called_once_with(lig_settings_uri)

    @mock.patch.object(ResourceHelper, 'create')
    def test_create_called_once(self, mock_create):
        lig = {
            "type": "logical-interconnect-groupV3",
            "name": "OneView Test Logical Interconnect Group",
            "interconnectMapTemplate": {
                "interconnectMapEntryTemplates": []
            },
            "uplinkSets": [],
            "enclosureType": "C7000",
        }
        self._lig.create(lig, timeout=70)
        mock_create.assert_called_once_with(lig, None, 70, None, False)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_called_once(self, mock_update, mock_ensure_client):
        lig = {
            "type": "logical-interconnect-groupV3",
            "name": "OneView Test Logical Interconnect Group",
            "interconnectMapTemplate": {
                "interconnectMapEntryTemplates": []
            },
            "uplinkSets": [],
            "enclosureType": "C7000",
        }
        self._lig.update(lig, timeout=70)

        lig["uri"] = self.uri

        mock_update.assert_called_once_with(lig, self.uri, False, 70, None)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._lig.delete(force=True, timeout=50)

        mock_delete.assert_called_once_with(self.uri, custom_headers=None,
                                            force=True, timeout=50)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once_with_defaults(self, mock_delete):
        self._lig.delete()

        mock_delete.assert_called_once_with(self.uri, custom_headers=None,
                                            force=False, timeout=-1)

    @mock.patch.object(ResourcePatchMixin, 'patch_request')
    def test_patch_should_use_user_defined_values(self, mock_patch):
        mock_patch.return_value = {}

        self._lig.patch('replace',
                        '/scopeUris',
                        ['rest/fake/scope123'],
                        timeout=-1)

        mock_patch.assert_called_once_with(self.uri,
                                           body=[{'path': '/scopeUris',
                                                  'value': ['rest/fake/scope123'],
                                                  'op': 'replace'}],
                                           custom_headers=None,
                                           timeout=-1)
