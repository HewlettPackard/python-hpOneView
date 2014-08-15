# -*- coding: utf-8 -*-

"""
storage.py
~~~~~~~~~~~~

This module implements settings HP OneView REST API
"""

__title__ = 'storage'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright 2012-2014 Hewlett-Packard Development ' \
                ' Company, L.P.'
__license__ = 'MIT'
__status__ = 'Development'

###
# (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
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
from hpOneView.activity import *
from hpOneView.exceptions import *
from pprint import pprint


class storage(object):

    def __init__(self, con):
        self._con = con
        self._activity = activity(con)

    def add_storage_system(self, host, user, passwd, blocking=True,
                           verbose=False):
        request = {'ip_hostname': host,
                   'username': user,
                   'password': passwd}
        task, body = self._con.post(uri['storage-systems'], request)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        return body

    def update_storage_system(self, StorageSystem):
        task, body = self._con.put(StorageSystem['uri'], StorageSystem)
        return body

    def remove_storage_system(self, system, blocking=True, verbose=False):
        task, body = self._con.delete(system['uri'])
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        return task

    def get_storage_systems(self):
        global uri
        body = get_members(self._con.get(uri['storage-systems']))
        return body

    def get_storage_pools(self):
        global uri
        body = self._con.get(uri['storage-pools'])
        return body

    def add_storage_pool(self, name, storageSystemUri):
        request = [{'storageSystemUri': storageSystemUri,
                   'poolName': name}]
        task, body = self._con.post(uri['storage-pools'] +
                                    '?multiResource=true', request)
        return body

    # TODO - this method seems to causes an UNEXPECTED_EXCEPTION
    # Even taking the payload directly from a working capture
    # and useing it directly.
    def add_storage_volume_template(self, volTemplate, blocking=True):
        request = {'name': 'Prod Volumes',
                   'description': 'Production Volumes',
                   'type': 'StorageVolumeTemplate',
                   'provisioning': { 'storagePoolUri': '/rest/storage-pools/88CCD985-FECB-4B63-8CE0-D22391449FF5/',
                                      'capacity': '10737418240',
                                      'provisionType': 'Thin',
                                      'shareable': False}
                  }
        task, body = self._con.post(uri['vol-templates'], request)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        return task

    def remove_storage_volume_template(self, volTemplate, blocking=True,
                                       verbose=False):
        task, body = self._con.delete(volTemplate['uri'])
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        return task

    def get_storage_volume_templates(self):
        global uri
        body = self._con.get(uri['vol-templates'])
        return body

    def add_storage_volume(self, volume, blocking=True,
                           verbose=False):
        task, body = self._con.post(uri['storage-volumes'], volume)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        return body

    def remove_storage_volume(self, volume, blocking=True,
                              verbose=False):
        task, body = self._con.delete(volume['uri'])
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        return task

    def get_storage_volumes(self):
        global uri
        body = self._con.get(uri['storage-volumes'])
        return body

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
