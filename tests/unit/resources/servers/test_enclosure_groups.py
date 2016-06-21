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
from hpOneView.resources.servers.enclosure_groups import EnclosureGroups
from hpOneView.resources.resource import ResourceClient


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

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self.client.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self.client.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self.client.get(id)
        mock_get.assert_called_once_with(id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        uri = "/rest/enclosure-groups/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self.client.get(uri)
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_script_by_id_called_once(self, mock_get):
        id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self.client.get_script(id)
        mock_get.assert_called_once_with("/rest/enclosure-groups/f0a0a113-ec97-41b4-83ce-d7c92b900e7c/script")

    @mock.patch.object(ResourceClient, 'get')
    def test_get_script_by_uri_called_once(self, mock_get):
        uri = "/rest/enclosure-groups/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self.client.get_script(uri)
        mock_get.assert_called_once_with(uri + "/script")

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self.client.get_by("name", "test name")
        mock_get_by.assert_called_once_with("name", "test name")

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        eg_initial = self.MINIMAL_DATA_FOR_EG_CREATION.copy()

        self.client.create(eg_initial)

        eg_expected = self.MINIMAL_DATA_FOR_EG_CREATION.copy()
        eg_expected["type"] = "EnclosureGroupV200"

        mock_create.assert_called_once_with(eg_expected, timeout=-1)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        self.client.delete({"an_entity": ""})

        mock_delete.assert_called_once_with({"an_entity": ""}, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_update):
        eg_initial = self.MINIMAL_DATA_FOR_EG_CREATION.copy()

        self.client.update(eg_initial)

        eg_expected = self.MINIMAL_DATA_FOR_EG_CREATION.copy()
        eg_expected["type"] = "EnclosureGroupV200"

        mock_update.assert_called_once_with(eg_expected, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_script_by_uri_called_once(self, mock_update):
        uri = "/rest/enclosure-groups/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        script_body = "#TEST COMMAND"
        self.client.update_script(uri, script_body)
        mock_update.assert_called_once_with(script_body, uri=uri + "/script")
