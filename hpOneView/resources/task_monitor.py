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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

__title__ = 'TaskMonitor'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2016) Hewlett Packard Enterprise ' \
                ' Development LP'
__license__ = 'MIT'
__status__ = 'Development'

import logging
import time
from hpOneView.exceptions import HPOneViewInvalidResource, HPOneViewTimeout, HPOneViewTaskError, HPOneViewUnknownType

TASK_PENDING_STATES = ['New', 'Starting', 'Pending', 'Running', 'Suspended', 'Stopping']
TASK_ERROR_STATES = ['Error', 'Warning', 'Terminated', 'Killed']
TASK_COMPLETED_STATES = ['Error', 'Warning', 'Completed', 'Terminated', 'Killed']

MSG_UNKNOWN_OBJECT_TYPE = 'Unknown object type'
MSG_TASK_TYPE_UNRECONIZED = "Task type: '%s' resource is not a recognized version"
MSG_UNKNOWN_EXCEPTION = 'Unknown Exception'
MSG_TIMEOUT = 'Waited %s seconds for task to complete, aborting'
MSG_INVALID_TASK = 'Invalid task was provided'

logger = logging.getLogger(__name__)


class TaskMonitor(object):
    def __init__(self, con):
        self._connection = con

    @staticmethod
    def get_current_seconds():
        return int(time.time())

    def wait_for_task(self, task, timeout=60):
        """
        Wait for task execution and return associated resource
        Args:
            task: task dict
            timeout: timeout in seconds

        Returns: associated resource when creating or updating; True when deleting
        """
        if not task:
            raise HPOneViewUnknownType(MSG_INVALID_TASK)

        logger.debug('Waiting for task')

        # gets current cpu second for timeout
        start_time = self.get_current_seconds()

        i = 0
        while self.is_task_running(task):
            # wait 1 to 10 seconds
            # the value increases to avoid flooding server with requests
            i = i + 1 if i < 10 else 10

            time.sleep(i)
            if start_time + timeout < self.get_current_seconds():
                raise HPOneViewTimeout(MSG_TIMEOUT % str(timeout))

        task_response = self.__get_task_response(task)
        logger.debug('Task completed')
        return task_response

    def __get_task_response(self, task):
        task = self.get(task)
        if task['taskState'] in TASK_ERROR_STATES and task['taskState'] != 'Warning':
            msg = None
            if 'taskErrors' in task and len(task['taskErrors']) > 0:
                err = task['taskErrors'][0]
                if 'message' in err:
                    msg = err['message']

            if msg:
                raise HPOneViewTaskError(msg)
            elif 'taskStatus' in task and task['taskStatus']:
                raise HPOneViewTaskError(task['taskStatus'])
            else:
                raise HPOneViewTaskError(MSG_UNKNOWN_EXCEPTION)

        deleted_resource = (task['name'] == 'Delete' or task['name'] == 'Remove')

        if 'type' in task and task['type'].startswith('Task') and 'name' in task and not deleted_resource:
            # get associated resource when is not a delete task
            task, entity = self.get_associated_resource(task)
            return entity

        if 'name' in task and task['name'] == 'Delete':
            # delete task return true
            return True

        logger.warning('Task completed, unknown response: ' + str(task))
        return task

    def is_task_running(self, task):
        """
            Check if a task is running according: TASK_PENDING_STATES ['New', 'Starting',
            'Pending', 'Running', 'Suspended', 'Stopping']

        Args:
            task: task dict

        Returns:
            True when is in TASK_PENDING_STATES; False when not

        """
        if 'uri' in task:
            task = self.get(task)
            if 'taskState' in task and task['taskState'] in TASK_PENDING_STATES:
                return True
        return False

    def get(self, task):
        """
        Retrieve a task by its uri

        Args:
            task: task dict, must have 'uri' key

        Returns:
            task dict

        """

        task = self._connection.get(task['uri'])
        return task

    def get_associated_resource(self, task):
        """
        Retrieve a resource associated to a task

        Args:
            task: task dict

        Returns:
            tuple: task (updated), the entity found (dict)
        """

        if not task:
            raise HPOneViewUnknownType(MSG_INVALID_TASK)

        if task['category'] != 'tasks' and task['category'] != 'backups':
            # it is an error if type is not in obj, so let the except flow
            raise HPOneViewUnknownType(MSG_UNKNOWN_OBJECT_TYPE)

        if task['type'] == 'TaskResourceV2':
            resource_uri = task['associatedResource']['resourceUri']
        elif task['type'] == 'BACKUP':
            task = self._connection.get(task['taskUri'])
            resource_uri = task['uri']
        else:
            raise HPOneViewInvalidResource(MSG_TASK_TYPE_UNRECONIZED % task['type'])

        entity = {}

        if resource_uri:
            entity = self._connection.get(resource_uri)

        return task, entity
