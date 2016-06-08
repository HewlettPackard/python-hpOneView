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
from hpOneView.exceptions import HPOneViewUnknownType
from hpOneView.resources.resource import ResourceClient, RESOURCE_CLIENT_INVALID_ID, TaskMonitor


class FakeResource(object):
    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, "/rest/fake/resource")

    def get_fake(self, uri):
        return self._client.get(uri)


class ResourceTest(unittest.TestCase):
    URI = "/rest/testuri"

    def setUp(self):
        super(ResourceTest, self).setUp()
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self.resource_client = ResourceClient(self.connection, self.URI)

    @mock.patch.object(ResourceClient, 'get_members')
    def test_get_all_called_once(self, mock_get_members):
        filter = "'name'='OneViewSDK \"Test FC Network'"
        sort = 'name:ascending'
        query = "name NE 'WrongName'"
        view = '"{view-name}"'

        self.resource_client.get_all(1, 500, filter, query, sort, view, 'name,owner,modified')

        uri = self.URI
        uri += '?start=1' \
               '&count=500' \
               '&filter=%27name%27%3D%27OneViewSDK%20%22Test%20FC%20Network%27' \
               '&query=name%20NE%20%27WrongName%27' \
               '&sort=name%3Aascending' \
               '&view=%22%7Bview-name%7D%22' \
               '&fields=name%2Cowner%2Cmodified'

        mock_get_members.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get_members')
    def test_get_all_with_defaults(self, mock_get_members):
        self.resource_client.get_all()
        uri = self.URI + "?start=0&count=-1"
        mock_get_members.assert_called_once_with(uri)

    @mock.patch.object(connection, 'delete')
    @mock.patch.object(TaskMonitor, 'wait_for_task')
    def test_delete_by_id_called_once(self, mock_wait4task, mock_delete):
        task = {"task": "task"}
        body = {"body": "body"}

        mock_delete.return_value = task, body
        mock_wait4task.return_value = task

        delete_task = self.resource_client.delete('1', force=True, blocking=True, verbose=True)

        self.assertEqual(task, delete_task)
        mock_delete.assert_called_once_with(self.URI + "/1?force=True")

    @mock.patch.object(connection, 'delete')
    def test_delete_dict_called_once_non_blocking(self, mock_delete):
        dict_to_delete = {"task": "task",
                          "uri": "a_uri"}
        task = {"task": "task"}
        body = {"body": "body"}

        mock_delete.return_value = task, body

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

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_by_uri(self, mock_get_all):
        self.resource_client.get_by('name', 'MyFibreNetwork')
        mock_get_all.assert_called_once_with(filter="\"'name'='MyFibreNetwork'\"")

    @mock.patch.object(connection, 'put')
    def test_update_with_uri_called_once(self, mock_put):
        dict_to_update = {"name": "test"}
        uri = "/rest/resource/test"
        task = None
        body = {"body": "body"}

        mock_put.return_value = task, body

        response = self.resource_client.update(dict_to_update, uri=uri)

        self.assertEqual(body, response)
        mock_put.assert_called_once_with(uri, dict_to_update)

    @mock.patch.object(connection, 'put')
    @mock.patch.object(TaskMonitor, 'wait_for_task')
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
    @mock.patch.object(TaskMonitor, 'wait_for_task')
    def test_update_return_task_when_not_blocking(self, mock_wait_for_task, mock_put):
        dict_to_update = {
            "resource_name": "a name",
            "uri": "a_uri",
        }
        task = {"task": "task"}

        mock_put.return_value = task, dict_to_update
        mock_wait_for_task.return_value = dict_to_update

        result = self.resource_client.update(dict_to_update, blocking=False)

        self.assertEqual(result, task)

    @mock.patch.object(connection, 'put')
    @mock.patch.object(TaskMonitor, 'wait_for_task')
    def test_update_return_entity_when_blocking(self, mock_wait4task, mock_put):
        dict_to_update = {
            "resource_name": "a name",
            "uri": "a_uri",
        }
        task = {"task": "task"}

        mock_put.return_value = task, {}
        mock_wait4task.return_value = dict_to_update

        result = self.resource_client.update(dict_to_update, blocking=True)

        self.assertEqual(result, dict_to_update)

    @mock.patch.object(connection, 'post')
    def test_create_uri(self, mock_post):
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
    @mock.patch.object(TaskMonitor, 'wait_for_task')
    def test_create_return_entity_when_blocking(self, mock_wait4task, mock_post):
        dict_to_create = {
            "resource_name": "a name",
        }
        created_resource = {
            "resource_id": "123",
            "resource_name": "a name",
        }
        task = {"task": "task"}

        mock_post.return_value = task, {}
        mock_wait4task.return_value = created_resource

        result = self.resource_client.create(dict_to_create, True)

        self.assertEqual(result, created_resource)

    @mock.patch.object(connection, 'post')
    @mock.patch.object(TaskMonitor, 'wait_for_task')
    def test_wait_for_activity_on_create(self, mock_wait4task, mock_post):
        task = {"task": "task"}
        mock_post.return_value = task, {}
        mock_wait4task.return_value = task

        self.resource_client.create({"test", "test"}, True)

        mock_wait4task.assert_called_once_with({"task": "task"}, 60)

    @mock.patch.object(connection, 'post')
    @mock.patch.object(TaskMonitor, 'wait_for_task')
    def test_not_wait_for_activity_on_create(self, mock_wait4task, mock_post):
        task = {"task": "task"}
        mock_post.return_value = task, {}
        mock_wait4task.return_value = task

        self.resource_client.create({"test", "test"}, False)

        mock_wait4task.assert_not_called()

    @mock.patch.object(connection, 'patch')
    def test_patch_request_uri_and_body_when_id_is_provided(self, mock_patch):
        request_body = [{
            'op': 'replace',
            'path': '/name',
            'value': 'new_name',
        }]
        mock_patch.return_value = {}, {}

        self.resource_client.patch('123a53cz', 'replace', '/name', 'new_name', False)

        mock_patch.assert_called_once_with('/rest/testuri/123a53cz', request_body)

    @mock.patch.object(connection, 'patch')
    def test_patch_request_uri_and_body_when_uri_is_provided(self, mock_patch):
        request_body = [{
            'op': 'replace',
            'path': '/name',
            'value': 'new_name',
        }]
        mock_patch.return_value = {}, {}

        self.resource_client.patch('/rest/testuri/123a53cz', 'replace', '/name', 'new_name', False)

        mock_patch.assert_called_once_with('/rest/testuri/123a53cz', request_body)

    @mock.patch.object(connection, 'patch')
    def test_patch_return_task_when_not_blocking(self, mock_patch):
        task = {"task": "task"}
        entity = {"resource_id": "123a53cz"}
        mock_patch.return_value = task, entity

        result = self.resource_client.patch('123a53cz', 'replace', '/name', 'new_name', False)

        self.assertEqual(result, task)

    @mock.patch.object(connection, 'patch')
    @mock.patch.object(TaskMonitor, 'wait_for_task')
    def test_patch_return_entity_when_blocking(self, mock_wait4task, mock_patch):
        task = {"task": "task"}
        entity = {"resource_id": "123a53cz"}
        mock_patch.return_value = task, task
        mock_wait4task.return_value = entity

        result = self.resource_client.patch('123a53cz', 'replace', '/name', 'new_name', True)

        self.assertEqual(result, entity)

    @mock.patch.object(connection, 'patch')
    @mock.patch.object(TaskMonitor, 'wait_for_task')
    def test_wait_for_activity_on_patch(self, mock_wait4task, mock_patch):
        task = {"task": "task"}
        entity = {"resource_id": "123a53cz"}
        mock_patch.return_value = task, task
        mock_wait4task.return_value = entity

        self.resource_client.patch('123a53cz', 'replace', '/name', 'new_name', True)

        mock_wait4task.assert_called_once_with({"task": "task"}, mock.ANY)

    @mock.patch.object(connection, 'patch')
    @mock.patch.object(TaskMonitor, 'wait_for_task')
    def test_not_wait_for_activity_on_patch(self, mock_wait4task, mock_patch):
        task = {"task": "task"}
        entity = {"resource_id": "123a53cz"}
        mock_patch.return_value = task, task
        mock_wait4task.return_value = entity

        self.resource_client.patch('123a53cz', 'replace', '/name', 'new_name', False)

        mock_wait4task.assert_not_called()

    def test_delete_with_none(self):
        try:
            self.resource_client.delete(None)
        except ValueError as e:
            self.assertTrue("Resource" in e.args[0])
        else:
            self.fail()

    def test_delete_with_empty_dict(self):
        try:
            self.resource_client.delete({})
        except ValueError as e:
            self.assertTrue("Resource" in e.args[0])
        else:
            self.fail()

    def test_get_with_none(self):
        try:
            self.resource_client.get(None)
        except ValueError as e:
            self.assertTrue("id" in e.args[0])
        else:
            self.fail()

    def test_create_with_none(self):
        try:
            self.resource_client.create(None)
        except ValueError as e:
            self.assertTrue("Resource" in e.args[0])
        else:
            self.fail()

    def test_create_with_empty_dict(self):
        try:
            self.resource_client.create({})
        except ValueError as e:
            self.assertTrue("Resource" in e.args[0])
        else:
            self.fail()

    def test_update_with_none(self):
        try:
            self.resource_client.update(None)
        except ValueError as e:
            self.assertTrue("Resource" in e.args[0])
        else:
            self.fail()

    def test_update_with_empty_dict(self):
        try:
            self.resource_client.update({})
        except ValueError as e:
            self.assertTrue("Resource" in e.args[0])
        else:
            self.fail()

    def test_get_by_with_name_none(self):
        try:
            self.resource_client.get_by(None, None)
        except ValueError as e:
            self.assertTrue("field" in e.args[0])
        else:
            self.fail()

    @mock.patch.object(connection, 'get')
    def test_get_with_uri_should_work(self, mock_get):
        mock_get.return_value = {}
        uri = self.URI + "/ad28cf21-8b15-4f92-bdcf-51cb2042db32"
        self.resource_client.get(uri)

        mock_get.assert_called_once_with(uri)

    def test_get_with_uri_with_incompatible_url_shoud_fail(self):
        message = "Unrecognized URI for this resource"
        uri = "/rest/interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32"
        try:
            self.resource_client.get(uri)
        except HPOneViewUnknownType as exception:
            self.assertEqual(message, exception.args[0])
        else:
            self.fail("Expected Exception was not raised")

    def test_get_with_uri_from_another_resource_with_incompatible_url_shoud_fail(self):
        message = "Unrecognized URI for this resource"
        uri = "/rest/interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32"
        fake_resource = FakeResource(None)
        try:
            fake_resource.get_fake(uri)
        except HPOneViewUnknownType as exception:
            self.assertEqual(message, exception.args[0])
        else:
            self.fail("Expected Exception was not raised")

    @mock.patch.object(connection, 'get')
    def test_get_utilization_with_args(self, mock_get):
        self.resource_client.get_utilization('09USE7335NW3', fields='AmbientTemperature,AveragePower,PeakPower',
                                             filter='startDate=2016-05-30T03:29:42.361Z',
                                             refresh=True, view='day')

        expected_uri = '/rest/testuri/09USE7335NW3/utilization' \
                       '?filter=startDate%3D2016-05-30T03%3A29%3A42.361Z' \
                       '&fields=AmbientTemperature%2CAveragePower%2CPeakPower' \
                       '&refresh=true' \
                       '&view=day'

        mock_get.assert_called_once_with(expected_uri)

    @mock.patch.object(connection, 'get')
    def test_get_utilization_with_multiple_filters(self, mock_get):
        self.resource_client.get_utilization(
            '09USE7335NW3',
            fields='AmbientTemperature,AveragePower,PeakPower',
            filter='startDate=2016-05-30T03:29:42.361Z,endDate=2016-05-31T03:29:42.361Z',
            refresh=True, view='day')

        expected_uri = '/rest/testuri/09USE7335NW3/utilization' \
                       '?filter=startDate%3D2016-05-30T03%3A29%3A42.361Z' \
                       '&filter=endDate%3D2016-05-31T03%3A29%3A42.361Z' \
                       '&fields=AmbientTemperature%2CAveragePower%2CPeakPower' \
                       '&refresh=true' \
                       '&view=day'

        mock_get.assert_called_once_with(expected_uri)

    @mock.patch.object(connection, 'get')
    def test_get_utilization_with_defaults(self, mock_get):
        self.resource_client.get_utilization('09USE7335NW3')

        expected_uri = '/rest/testuri/09USE7335NW3/utilization'

        mock_get.assert_called_once_with(expected_uri)

    def test_get_utilization_with_empty(self):

        try:
            self.resource_client.get_utilization('')
        except ValueError as exception:
            self.assertEqual(RESOURCE_CLIENT_INVALID_ID, exception.args[0])
        else:
            self.fail("Expected Exception was not raised")
