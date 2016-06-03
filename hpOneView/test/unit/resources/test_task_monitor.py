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
from hpOneView.resources.task_monitor import TaskMonitor, MSG_UNKNOWN_OBJECT_TYPE, MSG_TASK_TYPE_UNRECONIZED, \
    MSG_TIMEOUT, MSG_UNKNOWN_EXCEPTION
from hpOneView.exceptions import HPOneViewUnknownType, HPOneViewInvalidResource, HPOneViewTimeout, HPOneViewTaskError


class TaskMonitorTest(unittest.TestCase):
    URI = "/rest/testuri"

    def setUp(self):
        super(TaskMonitorTest, self).setUp()
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self.task_monitor = TaskMonitor(self.connection)

    @mock.patch.object(connection, 'get')
    def test_get_associated_resource_with_task(self, mock_get):

        task = {
            "category": "tasks",
            "type": "TaskResourceV2",
            "associatedResource": {
                "resourceUri": "/rest/associatedresourceuri"
            }}

        mock_get.return_value = {"resource": "resource1"}

        ret_task, entity = self.task_monitor.get_associated_resource(task.copy())

        self.assertEqual(entity, {"resource": "resource1"})
        self.assertEqual(ret_task, task)
        mock_get.assert_called_once_with("/rest/associatedresourceuri")

    @mock.patch.object(connection, 'get')
    def test_get_associated_resource_with_backup(self, mock_get):
        backup = {
            "category": "backups",
            "type": "BACKUP",
            "taskUri": "/rest/taskuri",
        }

        task = {
            "category": "TaskResourceV2",
            "type": "tasks",
            "uri": "/rest/justuri",
        }

        def inner_get(uri):
            if uri == "/rest/taskuri":
                return task.copy()
            else:
                return {"resource": "resource1"}

        mock_get.side_effect = inner_get
        mock_get.return_value = task.copy()

        ret_task, entity = self.task_monitor.get_associated_resource(backup.copy())

        self.assertEqual(entity, {"resource": "resource1"})
        self.assertEqual(ret_task, task)

    def test_get_associated_resource_with_task_empty(self):

        task, entity = self.task_monitor.get_associated_resource({})
        self.assertFalse(task)
        self.assertFalse(entity)

    def test_get_associated_resource_with_invalid_task(self):
        try:
            self.task_monitor.get_associated_resource({"category": "networking"})
        except HPOneViewUnknownType as e:
            self.assertEqual(MSG_UNKNOWN_OBJECT_TYPE, e.msg)
        else:
            self.fail()

    def test_get_associated_resource_with_invalid_type(self):
        try:
            self.task_monitor.get_associated_resource({"category": "tasks",
                                                       "type": "TaskResource"})
        except HPOneViewInvalidResource as e:
            self.assertEqual(MSG_TASK_TYPE_UNRECONIZED % "TaskResource", e.msg)
        else:
            self.fail()

    @mock.patch.object(TaskMonitor, 'get')
    def test_task_is_running(self, mock_get):

        mock_get.return_value = {"uri": "uri",
                                 "taskState": "Pending"}

        self.assertTrue(self.task_monitor.task_is_running({"uri": "uri"}))

    @mock.patch.object(TaskMonitor, 'get')
    def test_task_is_running_false(self, mock_get):
        mock_get.return_value = {"uri": "uri",
                                 "taskState": "Warning"}

        self.assertFalse(self.task_monitor.task_is_running({"uri": "uri"}))

    @mock.patch.object(TaskMonitor, 'task_is_running')
    def test_wait_for_task_timeout(self, mock_is_running):

        mock_is_running.return_value = True
        timeout = 2

        try:
            self.task_monitor.wait_for_task({"uri": "uri"}, timeout)
        except HPOneViewTimeout as e:
            self.assertEqual(MSG_TIMEOUT % timeout, e.msg)
        else:
            self.fail()

    @mock.patch.object(TaskMonitor, 'task_is_running')
    @mock.patch.object(TaskMonitor, 'get')
    def test_wait_for_task_with_error_message(self, mock_get, mock_is_running):

        task = {"uri": "uri",
                "taskState": "Error",
                "taskErrors": [{"message": "Error Message"}]}

        mock_is_running.return_value = False
        mock_get.return_value = task

        try:
            self.task_monitor.wait_for_task(task.copy())
        except HPOneViewTaskError as e:
            self.assertEqual("Error Message", e.msg)
        else:
            self.fail()

    def test_wait_for_task_empty(self):
        self.assertFalse(self.task_monitor.wait_for_task({}))

    @mock.patch.object(TaskMonitor, 'task_is_running')
    @mock.patch.object(TaskMonitor, 'get')
    def test_wait_for_task_with_error_empty(self, mock_get, mock_is_running):

        task = {"uri": "uri",
                "taskState": "Error",
                "taskStatus": "Failed",
                }

        mock_is_running.return_value = False
        mock_get.return_value = task

        try:
            self.task_monitor.wait_for_task(task.copy())
        except HPOneViewTaskError as e:
            self.assertEqual("Failed", e.msg)
        else:
            self.fail()

    @mock.patch.object(TaskMonitor, 'task_is_running')
    @mock.patch.object(TaskMonitor, 'get')
    def test_wait_for_task_with_error_unknown(self, mock_get, mock_is_running):

        task = {"uri": "uri",
                "taskState": "Error",
                }

        mock_is_running.return_value = False
        mock_get.return_value = task

        try:
            self.task_monitor.wait_for_task(task.copy())
        except HPOneViewTaskError as e:
            self.assertEqual(MSG_UNKNOWN_EXCEPTION, e.msg)
        else:
            self.fail()

    @mock.patch.object(TaskMonitor, 'get_associated_resource')
    @mock.patch.object(TaskMonitor, 'task_is_running')
    @mock.patch.object(TaskMonitor, 'get')
    def test_wait_for_task(self, mock_get, mock_is_running, mock_assoc_res):
        task = {"uri": "uri",
                "type": "TaskResourceV2",
                "name": "update",
                "taskState": "Completed",
                }

        mock_is_running.return_value = False
        mock_get.return_value = task
        mock_assoc_res.return_value = task.copy(), {"resource", "resource1"}

        ret_entity = self.task_monitor.wait_for_task(task.copy())

        self.assertEqual(ret_entity, {"resource", "resource1"})

    @mock.patch.object(TaskMonitor, 'get_associated_resource')
    @mock.patch.object(TaskMonitor, 'task_is_running')
    @mock.patch.object(TaskMonitor, 'get')
    def test_wait_for_task_delete(self, mock_get, mock_is_running, mock_assoc_res):
        task = {"uri": "uri",
                "type": "TaskResourceV2",
                "name": "Delete",
                "taskState": "Completed",
                }

        mock_is_running.return_value = False
        mock_get.return_value = task
        mock_assoc_res.return_value = task.copy(), {"resource", "resource1"}

        ret_dict = self.task_monitor.wait_for_task(task.copy())

        self.assertEqual(ret_dict, task)

    @mock.patch.object(connection, 'get')
    def test_get(self, mock_get):
        self.task_monitor.get({"uri": "an uri"})
        mock_get.assert_called_once_with("an uri")
