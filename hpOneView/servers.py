# -*- coding: utf-8 -*-

"""
servers.py
~~~~~~~~~~~~

This module implements servers HP OneView REST API
"""

__title__ = 'servers'
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
from hpOneView.activity import *
from hpOneView.exceptions import *


class servers(object):
    def __init__(self, con):
        self._con = con
        self._activity = activity(con)

    def get_enclosures(self):
        body = self._con.get(uri['enclosures'])
        return get_members(body)

    ###########################################################################
    # Server Hardware
    ###########################################################################
    def get_server_by_bay(self, baynum):
        servers = get_members(self._con.get(uri['servers']))
        for server in servers:
            if server['position'] == baynum:
                return server

    def get_server_by_name(self, name):
        servers = get_members(self._con.get(uri['servers']))
        for server in servers:
            if server['shortModel'] == name:
                return server

    def get_servers(self):
        return get_members(self._con.get(uri['servers']))

    def set_server_powerstate(self, server, state, force=False):
        if state == 'Off' and force is True:
            powerRequest = make_powerstate_dict('Off', 'PressAndHold')
        elif state == 'Off' and force is False:
            powerRequest = make_powerstate_dict('Off', 'MomentaryPress')
        elif state == 'On':
            powerRequest = make_powerstate_dict('On', 'MomentaryPress')
        elif state == 'Reset':
            powerRequest = make_powerstate_dict('On', 'Reset')
        self._con.put(server['uri'] + '/powerState', powerRequest)
        return

    def delete_server(self, server, blocking=True, verbose=False):
        task = self._con.delete(server['uri'])
        if blocking is True:
            self._activity.wait4task(task, tout=600, verbose=verbose)
        return

    def update_server(self, server):
        body = self._con.put(server['uri'], server)
        return body

    def add_server(self, server, blocking=True, verbose=False):
        global uri
        task = self._con.post(uri['servers'], server)
        if blocking is True:
            self._activity.wait4task(task, tout=600, verbose=verbose)
        serverResource = self._activity.get_task_assocaited_resource(task)
        if serverResource['resourceUri'] is not None:
            server = self._con.get(serverResource['resourceUri'])
            return server
        else:
            raise HPOneViewException('Server not added')

    ###########################################################################
    # Server Profiles
    ###########################################################################
    def create_server_profile(self, profile, blocking=True, verbose=False):
        # Creating a profile returns a task with no resource uri
        task = self._con.post(uri['profiles'], profile)
        if blocking is True:
            try:
                if profile['firmware']['firmwareBaselineUri'] is None:
                    tout = 600
                else:
                    tout = 3600
            except Exception:
                tout = 600
            self._activity.wait4task(task, tout=tout, verbose=verbose)
            # Update the task to get the associated resource uri
            task = self._con.get(task['uri'])
        profileResource = self._activity.get_task_assocaited_resource(task)
        profile = self._con.get(profileResource['resourceUri'])
        return profile

    def remove_server_profile(self, profile, blocking=True, verbose=False):
        task = self._con.delete(profile['uri'])
        if blocking is True:
            self._activity.wait4task(task, tout=600, verbose=verbose)
        return

    def get_server_profiles(self):
        body = self._con.get(uri['profiles'])
        return get_members(body)

    def update_server_profile(self, profile, blocking=True, verbose=False):
        task = self._con.put(profile['uri'], profile)
        if blocking is True:
            try:
                if profile['firmware']['firmwareBaselineUri'] is None:
                    tout = 600
                else:
                    tout = 3600
            except Exception:
                tout = 600
            self._activity.wait4task(task, tout=tout, verbose=verbose)
            # Update the task to get the associated resource uri
            task = self._con.get(task['uri'])
        profileResource = self._activity.get_task_assocaited_resource(task)
        profile = self._con.get(profileResource['resourceUri'])
        return profile

    ###########################################################################
    # Enclosures
    ###########################################################################
#    def get_enclosures(self):
#        body = get_members(self._con.get(uri['enclosures']))
#        return body

    def add_enclosure(self, enclosure, blocking=True, verbose=False):
        task = self._con.post(uri['enclosures'], enclosure)
        if blocking is True:
            try:
                if enclosure['firmwareBaselineUri'] is None:
                    self._activity.wait4task(task, tout=600, verbose=verbose)
                else:
                    self._activity.wait4task(task, tout=3600, verbose=verbose)
            except:
                self._activity.wait4task(task, tout=600, verbose=verbose)
        task = self._con.get(task['uri'])
        entity = self._activity.get_task_assocaited_resource(task)
        enclosure = self._con.get(entity['resourceUri'])
        return enclosure

    def remove_enclosure(self, enclosure, blocking=True, verbose=False):
        task = self._con.delete(enclosure['uri'])
        if blocking is True:
            self._activity.wait4task(task, tout=600, verbose=verbose)
        return

    ###########################################################################
    # Enclosure Groups
    ###########################################################################
    def create_enclosure_group(self, egroup):
        # Creating an Enclosure Group returns the group, NOT a task
        body = self._con.post(uri['enclosureGroups'], egroup)
        return body

    def delete_enclosure_group(self, egroup):
        self._con.delete(egroup['uri'])

    def get_enclosure_groups(self):
        return get_members(self._con.get(uri['enclosureGroups']))

    def update_enclosure_group(self, enclosuregroup):
        body = self._con.put(enclosuregroup['uri'], enclosuregroup)
        return body

    ###########################################################################
    # ID Pools
    ###########################################################################
    def get_pool(self, pooltype):
        body = self._con.get(uri['idpool'] + '/' + pooltype)
        return body

    def get_vmac_pool(self):
        body = self._con.get(uri['vmac-pool'])
        return body

    def get_vwwn_pool(self):
        body = self._con.get(uri['vwwn-pool'])
        return body

    def get_vsn_pool(self):
        body = self._con.get(uri['vsn-pool'])
        return body

    # TODO put pool
    def allocate_pool_ids(self, url, count):
        allocatorUrl = "%s/allocator" % url
        allocatorBody = {'count': count}
        body = self._con.put(allocatorUrl, allocatorBody)
        return body

    def release_pool_ids(self, url, idList):
        collectorUrl = "%s/collector" % url
        collectorBody = {'idList': idList}
        body = self._con.put(collectorUrl, collectorBody)
        return body

    def allocate_range_ids(self, allocatorUrl, count):
        body = self._con.put(allocatorUrl, {'count': count})
        return body

    def release_range_ids(self, collectorUrl, idList):
        body = self._con.put(collectorUrl, {'idList': idList})
        return body

    # TODO POST Range
    def enable_range(self, url):
        prange = self._con.get(url)
        prange['enabled'] = True
        body = self._con.put(url, prange)
        return body

    def disable_range(self, url):
        prange = self._con.get(url)
        prange['enabled'] = False
        body = self._con.put(url, prange)
        return body

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
