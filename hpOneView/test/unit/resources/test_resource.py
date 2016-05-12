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

import mock
import unittest

from hpOneView.oneview_client import OneViewClient
from hpOneView.connection import connection
from hpOneView.activity import activity
from hpOneView.resources.networking.fc_networks import FcNetworks
from hpOneView.resources.resource import ResourceClient


class ResourceTest(unittest.TestCase):
    URI = "this/is/a/test/uri"

    def setUp(self):
        super(ResourceTest, self).setUp()
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self.resource_client = ResourceClient(self.connection, self.URI)

    @mock.patch.object(ResourceClient, 'get_members')
    def test_get_all_called_once(self, mock_get_members):
        filter = 'name=TestName'
        sort = 'name:ascending'
        self.resource_client.get_all(1, 500, filter, sort)
        uri = self.URI + "?start=1&count=500&filter=name=TestName&sort=name:ascending"
        mock_get_members.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get_members')
    def test_get_all_with_defaults(self, mock_get_members):
        self.resource_client.get_all()
        uri = self.URI + "?start=0&count=9999999"
        mock_get_members.assert_called_once_with(uri)

    @mock.patch.object(connection, 'delete')
    @mock.patch.object(activity, 'wait4task')
    def test_delete_by_id_called_once(self, mock_wait4task, mock_delete):
        task = {"task": "task"}
        body = {"body": "body"}

        mock_delete.return_value = task, body
        mock_wait4task.return_value = task

        delete_task = self.resource_client.delete('1', True, True)

        self.assertEqual(task, delete_task)
        mock_delete.assert_called_once_with(self.URI + "/1")

    @mock.patch.object(connection, 'delete')
    @mock.patch.object(activity, 'wait4task')
    def test_delete_dict_called_once(self, mock_wait4task, mock_delete):
        dict_to_delete = {"task": "task",
                          "uri": "a_uri"}
        task = {"task": "task"}
        body = {"body": "body"}

        mock_delete.return_value = task, body
        mock_wait4task.return_value = task

        delete_task = self.resource_client.delete(dict_to_delete, False, False)

        self.assertEqual(task, delete_task)
        mock_delete.assert_called_once_with("a_uri")

    @mock.patch.object(connection, 'get')
    def test_get_schema_uri(self, mock_get):
        self.resource_client.get_schema()
        mock_get.assert_called_once_with(self.URI + "/schema")

    @mock.patch.object(connection, 'get')
    def test_get_by_id_uri(self, mock_get):
        self.resource_client.get('12345')
        mock_get.assert_called_once_with(self.URI + "/12345")

    @mock.patch.object(connection, 'put')
    @mock.patch.object(activity, 'wait4task')
    def test_update_uri(self, mock_wait4task, mock_update):
        dict_to_update = {"resource_data": "resource_data",
                          "uri": "a_uri"}
        task = {"task": "task"}
        body = {"body": "body"}

        mock_update.return_value = task, body
        mock_wait4task.return_value = task
        update_task = self.resource_client.update("456444", dict_to_update, True, True)

        self.assertEqual(task, update_task)
        mock_update.assert_called_once_with(self.URI + "/456444", dict_to_update)
