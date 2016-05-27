# -*- coding: utf-8 -*-

"""
facilities.py
~~~~~~~~~~~~

This module implements settings HPE OneView REST API
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

__title__ = 'facilities'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright 2012-2015 Hewlett Packard Enterprise' \
                ' Development LP'
__license__ = 'MIT'
__status__ = 'Development'

###
# (C) Copyright (2012-2015) Hewlett Packard Enterprise Development LP
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

from hpOneView.common import uri
from hpOneView.activity import activity


class facilities(object):
    def __init__(self, con):
        self._con = con
        self._activity = activity(con)

    def get_datacenters(self):
        body = self._con.get(uri['datacenters'])
        return body

    def get_powerdevices(self):
        body = self._con.get(uri['powerDevices'])
        return body

    def get_racks(self):
        body = self._con.get(uri['racks'])
        return body

    def delete_datacenter(self, datacenter, force=False, blocking=True,
                          verbose=False):
        if force:
            task, body = self._con.delete(datacenter['uri'] + '?force=True')
        else:
            task, body = self._con.delete(datacenter['uri'])
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        return task

    def delete_rack(self, rack, force=False, blocking=True,
                    verbose=False):
        if force:
            task, body = self._con.delete(rack['uri'] + '?force=True')
        else:
            task, body = self._con.delete(rack['uri'])
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        return task

    def delete_powerdevice(self, powerdevice, force=False, blocking=True,
                           verbose=False):
        if force:
            task, body = self._con.delete(powerdevice['uri'] + '?force=True')
        else:
            task, body = self._con.delete(powerdevice['uri'])
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        return task

    def add_datacenter(self, datacenter, blocking=True, verbose=False):
        task, body = self._con.post(uri['datacenters'], datacenter)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            if task:
                if 'type' in task and task['type'].startswith('Task'):
                    entity = self._activity.get_task_associated_resource(task)
                    datacenter = self._con.get(entity['resourceUri'])
                    return datacenter
            return body
        return task

    def add_rack(self, rack, blocking=True, verbose=False):
        task, body = self._con.post(uri['racks'], rack)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            if task:
                if 'type' in task and task['type'].startswith('Task'):
                    entity = self._activity.get_task_associated_resource(task)
                    rack = self._con.get(entity['resourceUri'])
                    return rack
            return body
        return task

    def add_powerdevice(self, powerdevice, blocking=True, verbose=False):
        task, body = self._con.post(uri['powerDevices'], powerdevice)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            if task:
                if 'type' in task and task['type'].startswith('Task'):
                    entity = self._activity.get_task_associated_resource(task)
                    powerdevice = self._con.get(entity['resourceUri'])
                    return powerdevice
            return body
        return task

    def add_iPDU(self, host, user, passwd, blocking=True, verbose=False):
        request = {'hostname': host,
                   'username': user,
                   'password': passwd}
        task, body = self._con.post(uri['powerDevicesDiscover'], request)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            if task:
                if 'type' in task and task['type'].startswith('Task'):
                    entity = self._activity.get_task_associated_resource(task)
                    powerdevice = self._con.get(entity['resourceUri'])
                    return powerdevice
            return body
        return task

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
