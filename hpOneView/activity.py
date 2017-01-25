# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2017) Hewlett Packard Enterprise Development LP
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
"""
This module implements the Activity HPE OneView REST API.

It has been deprecated and will be removed soon. We strongly recommend to use the OneViewClient class instead.
See more details at: https://github.com/HewlettPackard/python-hpOneView/tree/master/hpOneView/README.md
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import filter
from future import standard_library

standard_library.install_aliases()


import sys  # For verbose
import time  # For sleep
from hpOneView.common import uri, get_members
from hpOneView.exceptions import HPOneViewInvalidResource, HPOneViewException, HPOneViewUnknownType, \
    HPOneViewTaskError, HPOneViewTimeout
from warnings import warn


def deprecated(func):
    def wrapper(*args, **kwargs):
        warn("Module activity is deprecated, use OneViewClient class instead", DeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)

    return wrapper


TaskErrorStates = ['Error', 'Warning', 'Terminated', 'Killed']
TaskCompletedStates = ['Error', 'Warning', 'Completed', 'Terminated', 'Killed']
TaskPendingStates = ['New', 'Starting', 'Pending', 'Running', 'Suspended', 'Stopping']


class activity(object):
    def __init__(self, con):
        self._con = con

    ###########################################################################
    # Tasks
    ###########################################################################
    #
    @deprecated
    def get_task_associated_resource(self, task):
        if not task:
            return {}
        if task['type'] == 'TaskResource':
            obj = self._con.get(task['associatedResourceUri'])
            tmp = {
                'resourceName': obj['name'],
                'associationType': None,
                'resourceCategory': None,
                'resourceUri': obj['uri']}
        elif task['type'] == 'TaskResourceV2':
            tmp = task['associatedResource']
        else:
            raise HPOneViewInvalidResource('Task resource is not a recognized'
                                           ' version')
        return tmp

    @deprecated
    def make_task_entity_tuple(self, obj):
        task = {}
        entity = {}
        if obj:
            if obj['category'] == 'tasks' or obj['category'] == 'backups':
                # it is an error if type is not in obj, so let the except flow
                uri = ''
                if obj['type'] == 'TaskResource':
                    task = obj
                    uri = obj['associatedResourceUri']
                elif obj['type'] == 'TaskResourceV2':
                    task = obj
                    uri = obj['associatedResource']['resourceUri']
                elif obj['type'] == 'BACKUP':
                    task = self._con.get(obj['taskUri'])
                    uri = obj['uri']
                else:
                    raise HPOneViewInvalidResource('Task resource is not a'
                                                   ' recognized version')
                if uri:
                    try:
                        entity = self._con.get(uri)
                    except HPOneViewException:
                        raise
                else:
                    entity = obj
            else:
                raise HPOneViewUnknownType('Unknown object type')

        return task, entity

    @deprecated
    def is_task_running(self, task):
        global TaskPendingStates
        if 'uri' in task:
            task = self._con.get(task['uri'])
            if 'taskState' in task and task['taskState'] in TaskPendingStates:
                return True
        return False

    @deprecated
    def wait4task(self, task, tout=60, verbose=False):
        count = 0
        if task is None:
            return None
        while self.is_task_running(task):
            if verbose:
                sys.stdout.write('Task still running after %d seconds   \r'
                                 % count)
                sys.stdout.flush()
            time.sleep(1)
            count += 1
            if count > tout:
                raise HPOneViewTimeout('Waited ' + str(tout) +
                                       ' seconds for task to complete, aborting')
        task = self._con.get(task['uri'])
        if task['taskState'] in TaskErrorStates and task['taskState'] != 'Warning':
            err = task['taskErrors'][0]
            msg = err['message']
            if msg is not None:
                raise HPOneViewTaskError(msg)
            elif task['taskStatus'] is not None:
                raise HPOneViewTaskError(task['taskStatus'])
            else:
                raise HPOneViewTaskError('Unknown Exception')
        return task

    @deprecated
    def wait4tasks(self, tasks, tout=60, verbose=False):
        running = list(filter(self.is_task_running, tasks[:]))
        count = 0
        while running:
            if verbose:
                print(('Tasks still running after %s seconds', count))
                print(running)
            time.sleep(1)
            count += 1
            running = list(filter(self.is_task_running, running))
            if count > tout:
                raise HPOneViewTimeout('Waited 60 seconds for task to complete'
                                       ', aborting')

    @deprecated
    def get_tasks(self):
        return get_members(self._con.get(uri['task']))

    ###########################################################################
    # Alerts
    ###########################################################################
    @deprecated
    def get_alerts(self, AlertState='All'):
        if AlertState == 'All':
            # TODO remove the evil use/hack of the large count default. The OneView
            # API documents that count=-1 should return everything but it is not
            # universally honored, where the extremely large count number is.
            return get_members(self._con.get(uri['alerts'] +
                                             '?start=0&count=9999999'))
        else:
            return (self._con.get_entities_byfield(uri['alerts'],
                                                   'alertState',
                                                   AlertState, count=9999999))

    @deprecated
    def delete_alert(self, alert):
        self._con.delete(alert['uri'])

    @deprecated
    def delete_alerts(self):
        self._con.delete(uri['alerts'])

    @deprecated
    def update_alert(self, alert, alertMap):
        task, moddedAlert = self._con.put(alert['uri'], alertMap)
        return moddedAlert

    ###########################################################################
    # Audit Logs
    ###########################################################################
    @deprecated
    def get_audit_logs(self, query=''):
        body = self._con.get(uri['audit-logs'] + '?' + query)
        return get_members(body)

    @deprecated
    def create_audit_log(self, auditLogRecord):
        self._con.post(uri['audit-logs'], auditLogRecord)
        return

    @deprecated
    def download_audit_logs(self, filename):
        body = self._con.get(uri['audit-logs-download'])
        f = open(filename, 'wb')
        f.write(body)
        f.close()
        return

    ###########################################################################
    # Events
    ###########################################################################
    @deprecated
    def get_events(self, query=''):
        body = self._con.get(uri['events'] + '?' + query)
        return get_members(body)

    @deprecated
    def create_event(self, eventRecord):
        self._con.post(uri['events'], eventRecord)
        return
