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

from hpOneView.connection import connection
from hpOneView.activity import activity
from hpOneView.resources.resource import ResourceClient
from hpOneView.exceptions import HPOneViewUnknownType


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
        query = "name NE 'WrongName'"
        view = '"{view-name}"'
        self.resource_client.get_all(1, 500, filter, query, sort, view)

        uri = self.URI
        uri += '?start=1&count=500&filter=name=TestName&query=name NE \'WrongName\'&sort=name:ascending&view="{view-name}"'

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

        delete_task = self.resource_client.delete('1', force=True, blocking=True, verbose=True)

        self.assertEqual(task, delete_task)
        mock_delete.assert_called_once_with(self.URI + "/1?force=True")

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

    def test_delete_dict_invalid_uri(self):
        dict_to_delete = {"task": "task",
                          "uri": ""}
        try:
            self.resource_client.delete(dict_to_delete, False, False)
        except HPOneViewUnknownType as e:
            self.assertEqual("Unknown object type", e.args[0])
        else:
            self.fail()

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
        update_task = self.resource_client.update(dict_to_update, False)

        self.assertEqual(task, update_task)
        mock_update.assert_called_once_with("a_uri", dict_to_update)

    @mock.patch.object(connection, 'put')
    def test_update_return_task_when_not_blocking(self, mock_put):
        dict_to_update = {
            "resource_name": "a name",
            "uri": "a_uri",
        }
        task = {"task": "task"}

        mock_put.return_value = task, dict_to_update

        result = self.resource_client.update(dict_to_update, False)

        self.assertEqual(result, task)

    @mock.patch.object(connection, 'put')
    @mock.patch.object(connection, 'get')
    @mock.patch.object(activity, 'wait4task')
    @mock.patch.object(activity, 'get_task_associated_resource')
    def test_update_return_entity_when_blocking(self, mock_get_task_associated_resource, mock_wait4task,
                                                mock_get, mock_put):
        dict_to_update = {
            "resource_name": "a name",
            "uri": "a_uri",
        }
        task = {"task": "task"}

        mock_put.return_value = task, {}
        mock_wait4task.return_value = {"type": "TaskBlaBla"}
        mock_get_task_associated_resource.return_value = {"resourceUri": self.URI + "path/ID"}
        mock_get.return_value = dict_to_update

        result = self.resource_client.update(dict_to_update, True)

        self.assertEqual(result, dict_to_update)

    @mock.patch.object(connection, 'post')
    @mock.patch.object(activity, 'make_task_entity_tuple')
    def test_create_uri(self, mock_make_task_entity_tuple, mock_post):
        dict_to_create = {
            "resource_name": "a name",
        }
        mock_post.return_value = {}, {}

        self.resource_client.create(dict_to_create, False)

        mock_post.assert_called_once_with(self.URI, dict_to_create)

    @mock.patch.object(connection, 'post')
    def test_create_return_task_when_not_blocking(self, mock_post):
        dict_to_create = {
            "resource_name": "a name",
        }
        created_resource = {
            "resource_id": "123",
            "resource_name": "a name",
        }
        task = {"task": "task"}

        mock_post.return_value = task, created_resource

        result = self.resource_client.create(dict_to_create, False)

        self.assertEqual(result, task)

    @mock.patch.object(connection, 'post')
    @mock.patch.object(connection, 'get')
    @mock.patch.object(activity, 'wait4task')
    @mock.patch.object(activity, 'get_task_associated_resource')
    def test_create_return_entity_when_blocking(self, mock_get_task_associated_resource, mock_wait4task,
                                                mock_get, mock_post):
        dict_to_create = {
            "resource_name": "a name",
        }
        created_resource = {
            "resource_id": "123",
            "resource_name": "a name",
        }
        task = {"task": "task"}

        mock_post.return_value = task, {}
        mock_wait4task.return_value = {"type": "TaskBlaBla"}
        mock_get_task_associated_resource.return_value = {"resourceUri": self.URI + "path/ID"}
        mock_get.return_value = created_resource

        result = self.resource_client.create(dict_to_create, True)

        self.assertEqual(result, created_resource)

    @mock.patch.object(connection, 'post')
    @mock.patch.object(activity, 'wait4task')
    @mock.patch.object(activity, 'make_task_entity_tuple')
    def test_wait_for_activity_on_create(self, mock_make_task_entity_tuple, mock_wait4task, mock_post):
        task = {"task": "task"}
        mock_post.return_value = task, {}
        mock_make_task_entity_tuple.return_value = task, {}
        mock_wait4task.return_value = task

        self.resource_client.create({}, True)

        mock_wait4task.assert_called_once_with({"task": "task"}, tout=60, verbose=False)

    @mock.patch.object(connection, 'post')
    @mock.patch.object(activity, 'wait4task')
    @mock.patch.object(activity, 'make_task_entity_tuple')
    def test_not_wait_for_activity_on_create(self, mock_make_task_entity_tuple, mock_wait4task, mock_post):
        task = {"task": "task"}
        mock_post.return_value = task, {}
        mock_make_task_entity_tuple.return_value = task, {}
        mock_wait4task.return_value = task

        self.resource_client.create({}, False)

        mock_wait4task.assert_not_called()
