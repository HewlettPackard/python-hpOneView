# -*- coding: utf-8 -*-

"""
activity.py
~~~~~~~~~~~~

This module implements the Activity HP OneView REST API
"""

__title__ = 'activity'
__version__ = "0.0.1"
__copyright__ = "(C) Copyright 2012-2013 Hewlett-Packard Development " \
                " Company, L.P."
__license__ = "MIT"
__status__ = "Development"

###
# (C) Copyright 2013 Hewlett-Packard Development Company, L.P.
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


from hpOneView.common import *
from hpOneView.connection import *
from hpOneView.exceptions import *
import time  # For sleep
import sys  # For verbose


TaskCompletedStates = ['Error', 'Warning', 'Completed', 'Terminated', 'Killed']
TaskPendingStates = ['New', 'Starting', 'Running', 'Suspended', 'Stopping']


class activity(object):
    def __init__(self, con):
        self._con = con

    ###########################################################################
    # Tasks
    ###########################################################################
    #
    def get_task_assocaited_resource(self, task):
        if not task:
            return {}
        if task['type'] == "TaskResource":
            obj = self._con.get(task['associatedResourceUri'])
            tmp = {'resourceName': obj['name'],
                   'associationType': None,
                   'resourceCategory': None,
                   'resourceUri': obj['uri']}
        elif task['type'] == "TaskResourceV2":
            tmp = task['associatedResource']
        else:
            raise HPOneViewInvalidResource("Task resource is not a recognized"
                                    " version")
        return tmp

    def make_task_entity_tuple(self, obj):
        task = {}
        entity = {}
        if obj:
            if obj['category'] == "tasks":
                # it is an error if type is not in obj, so let the except flow
                uri = ''
                if obj['type'] == "TaskResource":
                    task = obj
                    uri = obj['associatedResourceUri']
                elif obj['type'] == "TaskResourceV2":
                    task = obj
                    uri = obj['associatedResource']['resourceUri']
                else:
                    raise HPOneViewInvalidResource("Task resource is not a"
                                            " recognized version")
                if uri:
                    try:
                        entity = self._con.get(uri)
                    except HPOneViewException:
                        raise
                else:
                    entity = obj
        return task, entity

    def get_task_state(self, task_uri):
        if not task_uri:
            return False
        task = self._con.get(task_uri)
        return task['taskState']
        info = self.get_task_assocaited_resource(task)
        progress_string = ("Resource = %s: Progress=%s%%: State=%s"
                           % (info['resourceName'],
                              task['percentComplete'],
                              task['taskState']))
        return progress_string

    def is_task_running(self, task):
        global TaskPendingStates
        if not task:
            return False
        if isinstance(task, dict):
            task_uri = task['uri']
        else:
            task_uri = task
        return self.get_task_state(task_uri) in TaskPendingStates

    def wait4task(self, task, tout=60, verbose=False):
        count = 0
        while self.is_task_running(task):
            if verbose:
                    sys.stdout.write("Task still running after %d seconds   \r"
                                     % (count))
                    sys.stdout.flush()
            time.sleep(1)
            count = count + 1
            if count > tout:
                raise HPOneViewTimeout("Waited " + str(tout) +
                            " seconds for task to complete, aborting")
        if verbose is True:
            print()

    def wait4tasks(self, tasks, tout=60, verbose=False):
        running = list(filter(self.is_task_running, tasks[:]))
        count = 0
        while running:
            if verbose:
                    print(("Tasks still running after %s seconds", count))
                    print(running)
            time.sleep(1)
            count = count + 1
            running = list(filter(self.is_task_running, running))
            if count > tout:
                raise HPOneViewTimeout("Waited 60 seconds for task to complete"
                                ", aborting")

    ###########################################################################
    # Alerts
    ###########################################################################
    def get_alerts(self, AlertState='All'):
        global uri
        if AlertState == 'All':
            return(get_members(self._con.get(uri['alerts'])))
        else:
            return(self._con.get_entities_byfield(uri['alerts'],
                                        'alertState',
                                        AlertState))

    def delete_alert(self, alert):
        self._con.delete(alert['uri'])

    def update_alert(self, alert, alertMap):
        moddedAlert = self._con.put(alert['uri'], alertMap)
        return moddedAlert

    ###########################################################################
    # Audit Logs
    ###########################################################################
    def get_audit_logs(self, query=""):
        global uri
        body = self._con.get(uri['audit-logs'] + "?" + query)
        return(get_members(body))

    def create_audit_log(self, auditLogRecord):
        global uri
        self._con.post(uri['audit-logs'], auditLogRecord)
        return

    ###########################################################################
    # Events
    ###########################################################################
    def get_events(self, query=""):
        global uri
        body = self._con.get(uri['events'] + "?" + query)
        return(get_members(body))

    def create_event(self, eventRecord):
        global uri
        self._con.post(uri['events'], eventRecord)
        return
