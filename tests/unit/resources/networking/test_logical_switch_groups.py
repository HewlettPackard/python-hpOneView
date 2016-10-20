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
from hpOneView.resources.networking.logical_switch_groups import LogicalSwitchGroups
from hpOneView.resources.resource import ResourceClient


class LogicalSwitchGroupsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._lsg = LogicalSwitchGroups(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._lsg.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._lsg.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        lsg_id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._lsg.get(lsg_id)
        mock_get.assert_called_once_with(lsg_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        lsg_uri = "/rest/logical-switch-groups/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._lsg.get(lsg_uri)
        mock_get.assert_called_once_with(lsg_uri)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        lsg = {
            "name": "OneView Test Logical Switch Group",
            "switchMapTemplate": {
                "switchMapEntryTemplates": [{
                    "logicalLocation": {
                        "locationEntries": [{
                            "relativeValue": 1,
                            "type": "StackingMemberId"
                        }]
                    },
                    "permittedSwitchTypeUri": "/rest/switch-types/46d7ffad-4424-4e36-acf3-b379c3116206"
                }]
            }
        }
        self._lsg.create(lsg, 70)
        mock_create.assert_called_once_with(lsg, timeout=70, default_values=self._lsg.DEFAULT_VALUES)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_update):
        lsg = {
            "name": "Updated name",
            "switchMapTemplate": {
                "switchMapEntryTemplates": [{
                    "logicalLocation": {
                        "locationEntries": [{
                            "relativeValue": 1,
                            "type": "StackingMemberId"
                        }]
                    },
                    "permittedSwitchTypeUri": "/rest/switch-types/46d7ffad-4424-4e36-acf3-b379c3116206"
                }],
                "uri": "/rest/logical-switch-groups/dce3fc90-873e-48f7-8340-cc927d625b16"
            }
        }
        self._lsg.update(lsg, 70)
        mock_update.assert_called_once_with(lsg, timeout=70, default_values=self._lsg.DEFAULT_VALUES)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._lsg.delete(id, force=True, timeout=50)

        mock_delete.assert_called_once_with(id, force=True, timeout=50)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once_with_defaults(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._lsg.delete(id)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._lsg.get_by("name", "test name")

        mock_get_by.assert_called_once_with("name", "test name")
