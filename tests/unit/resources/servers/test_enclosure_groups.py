# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2019 Hewlett Packard Enterprise Development LP
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
from hpOneView.resources.servers.enclosure_groups import EnclosureGroups
from hpOneView.resources.resource import Resource, ResourceHelper


class EnclosureGroupsTest(unittest.TestCase):
    MINIMAL_DATA_FOR_EG_CREATION = {
        "name": "Enclosure Group 1",
        "stackingMode": "Enclosure",
        "interconnectBayMappings":
            [
                {
                    "interconnectBay": 1,
                },
                {
                    "interconnectBay": 2,
                },
                {
                    "interconnectBay": 3,
                },
                {
                    "interconnectBay": 4,
                },
                {
                    "interconnectBay": 5,
                },
                {
                    "interconnectBay": 6,
                },
                {
                    "interconnectBay": 7,
                },
                {
                    "interconnectBay": 8,
                }
            ]
    }

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self.client = EnclosureGroups(self.connection)
        self.uri = "/rest/enclosure-groups/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self.client.data = {"uri": self.uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        scope_uris = 'rest/scopes/cd237b60-09e2-45c4-829e-082e318a6d2a'
        self.client.get_all(2, 500, filter, sort, scope_uris)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort, scope_uris=scope_uris)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self.client.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='', scope_uris='')

    @mock.patch.object(ResourceHelper, 'create')
    def test_create_called_once(self, mock_create):
        eg_initial = self.MINIMAL_DATA_FOR_EG_CREATION.copy()

        self.client.create(eg_initial)
        default_values = self.client._get_default_values()
        eg_expected = self.MINIMAL_DATA_FOR_EG_CREATION.copy()
        eg_expected.update(default_values)

        mock_create.assert_called_once_with(eg_expected, None, -1, None, False)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete_called_once(self, mock_delete):
        self.client.delete()

        mock_delete.assert_called_once_with(self.client.data["uri"], custom_headers=None, force=False, timeout=-1)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update_called_once(self, mock_update, mock_ensure_client):
        eg_initial = self.MINIMAL_DATA_FOR_EG_CREATION.copy()

        self.client.update(eg_initial)

        eg_expected = self.MINIMAL_DATA_FOR_EG_CREATION.copy()
        eg_expected["uri"] = self.uri

        mock_update.assert_called_once_with(eg_expected, self.uri, False, -1, None)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_script_by_uri_called_once(self, mock_update):
        script_body = "#TEST COMMAND"
        self.client.update_script(script_body)
        mock_update.assert_called_once_with(script_body, uri=self.uri + "/script")
