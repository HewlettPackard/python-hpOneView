# -*- coding: utf-8 -*-

"""
networking.py
~~~~~~~~~~~~

This module implements Settings HP OneView REST API
"""

__title__ = 'networking'
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


class networking(object):
    def __init__(self, con):
        self._con = con
        self._activity = activity(con)

    ###########################################################################
    # Logical Interconnect Group
    ###########################################################################
    def update_settings_from_default(self, settings={}):
        global uri
        if not settings:
            settings = make_enet_settings('__NoName__')
        default = self._con.get('%s/defaultSettings')
        return default

        for key in list(settings.keys()):
            if key != 'name':
                settings[key] = default[key]
        return settings

    def create_lig(self, lig, blocking=True, verbose=False):
        global uri
        body = self._con.post(uri['lig'], lig)
        task, entity = self._activity.make_task_entity_tuple(body)
        if blocking is True:
            self._activity.wait4task(task, verbose=verbose)
        return entity

    def update_lig(self, lig):
        global uri
        return self._activity.make_task_entity_tuple(self._con.put(uri['lig'],
                                                        lig))

    def delete_lig(self, lig, blocking=True, verbose=False):
        global uri
        task = self._con.delete(lig['uri'])
        if blocking is True:
            self._activity.wait4task(task, verbose=verbose)
        return

    def get_ligs(self):
        global uri
        return get_members(self._con.get(uri['lig']))

    ###########################################################################
    # Connection Templates
    ###########################################################################
    def update_net_ctvalues(self, xnet, bw={}):
        if not bw:
            return
        if not xnet:
            raise HPOneViewInvalidResource('Missing Network')
        defaultCT = self._con.get(xnet['connectionTemplateUri'])
        defaultCT['bandwidth']['maximumBandwidth'] = bw['maximumBandwidth']
        defaultCT['bandwidth']['typicalBandwidth'] = bw['typicalBandwidth']
        body = self._con.put(defaultCT['uri'], defaultCT)
        return self._activity.make_task_entity_tuple(body)

    ###########################################################################
    # NetworkSets
    ###########################################################################
    def create_networkset(self, name, nets=[], bw={},
                                blocking=True, verbose=False):
        global uri
        nset = make_netset_dict(name, nets)
        body = self._con.conditional_post(uri['nset'], nset)
        task, entity = self._activity.make_task_entity_tuple(body)
        if not task and not entity:
            # contitional_post returned an already existing resource
            return body
        else:
            # assume we can update CT even if network create task is not cmpelt
            self.update_net_ctvalues(entity, bw)
            if blocking is True:
                self._activity.wait4task(task, tout=60, verbose=verbose)
            return entity

    def delete_networkset(self, networkset, blocking=True, verbose=False):
        task = self._con.delete(networkset['uri'])
        if blocking is True:
            self._activity.wait4task(task, verbose=verbose)
        return

    def get_networksets(self):
        global uri
        return get_members(self._con.get(uri['nset']))

    ###########################################################################
    # Networks
    ###########################################################################
    def create_enet_networks(self, prefix, vid_start, vid_count):
        enet_list = []
        try:
            for vid in range(vid_start, vid_start + vid_count):
                enet_name = "%s%s" % (prefix, vid)
                enet_list.append(self.create_enet_network(enet_name, vid))
        except http.client.HTTPException:
            # All or nothing
            for enet in enet_list:
                try:
                    self._con.delete(enet['uri'])
                except http.client.HTTPException:
                    pass
            raise HPOneViewException("Could not create one or more networks")
        return enet_list

    def create_enet_network(self, name, vid,
                            smartLink=True,
                            privateNetwork=False,
                            bw={},
                            blocking=True,
                            verbose=False):
        global uri
        xnet = make_enet_dict(name, vid,
                              smartLink=smartLink,
                              privateNetwork=privateNetwork)
        return self.create_network(uri['enet'], xnet, bw, blocking=blocking,
                                    verbose=verbose)

    def create_fc_network(self, name, attach="FabricAttach", bw={},
                            blocking=True, verbose=False):
        global uri
        xnet = make_fc_dict(name, attach)
        return self.create_network(uri['fcnet'], xnet, bw, blocking=blocking,
                                    verbose=verbose)

    def create_network(self, uri, xnet, bw={}, blocking=True, verbose=False):
        # throws an exception if there is an error
        body = self._con.conditional_post(uri, xnet)
        task, entity = self._activity.make_task_entity_tuple(body)
        if not task and not entity:
            # contitional_post returned an already existing resource
            return body
        else:
            # assume we can update CT even if network create task is not cmpelt
            self.update_net_ctvalues(entity, bw)
            if blocking is True:
                self._activity.wait4task(task, tout=60, verbose=verbose)
            return entity

    def update_network(self, xnet):
        return self._activity.make_task_entity_tuple(self._con.put(xnet['uri'],
                                                        xnet))

    def delete_network(self, xnet, blocking=True, verbose=False):
        task = self._con.delete(xnet["uri"])
        if blocking is True:
            self._activity.wait4task(task, verbose=verbose)
        return

    def get_enet_networks(self):
        global uri
        return get_members(self._con.get(uri['enet']))

    def get_fc_networks(self):
        global uri
        return get_members(self._con.get(uri['fcnet']))

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
