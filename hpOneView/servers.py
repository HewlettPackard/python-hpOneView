# -*- coding: utf-8 -*-

"""
servers.py
~~~~~~~~~~~~

This module implements servers HP OneView REST API
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from pprint import pprint

__title__ = 'servers'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2015) Hewlett Packard Enterprise ' \
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

from hpOneView.common import *
from hpOneView.connection import *
from hpOneView.activity import *
from hpOneView.exceptions import *

class servers(object):

    def __init__(self, con):
        self._con = con
        self._activity = activity(con)

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
            if server['name'] == name:
                return server

    def get_available_servers(self, server_hardware_type=None,
                              enclosure_group=None, server_profile=None):
        filters = []
        if server_hardware_type:
            filters.append('serverHardwareTypeUri=' + server_hardware_type['uri'])
        if enclosure_group:
            filters.append('enclosureGroupUri=' + enclosure_group['uri'])
        if server_profile:
            filters.append('serverProfileUri=' + server_profile['uri'])

        query_string = ''
        if filters:
            query_string = '?' + '&'.join(filters)

        return self._con.get(uri['profile-available-targets'] + query_string)

    def get_servers(self):
        return get_members(self._con.get(uri['servers']))

    def get_server_hardware_types(self):
        body = self._con.get(uri['server-hardware-types'])
        return get_members(body)

    def set_server_powerstate(self, server, state, force=False, blocking=True,
                              verbose=False):
        if state == 'Off' and force is True:
            powerRequest = make_powerstate_dict('Off', 'PressAndHold')
        elif state == 'Off' and force is False:
            powerRequest = make_powerstate_dict('Off', 'MomentaryPress')
        elif state == 'On':
            powerRequest = make_powerstate_dict('On', 'MomentaryPress')
        elif state == 'Reset':
            powerRequest = make_powerstate_dict('On', 'Reset')
        task, body = self._con.put(server['uri'] + '/powerState', powerRequest)
        if blocking is True:
            task = self._activity.wait4task(task, tout=60, verbose=verbose)
        return task

    def delete_server(self, server, force=False, blocking=True, verbose=False):
        if force:
            task, body = self._con.delete(server['uri'] + '?force=True')
        else:
            task, body = self._con.delete(server['uri'])
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        return task

    def update_server(self, server):
        task, body = self._con.put(server['uri'], server)
        return body

    def add_server(self, server, blocking=True, verbose=False):
        task, body = self._con.post(uri['servers'], server)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            if 'type' in task and task['type'].startswith('Task'):
                entity = self._activity.get_task_associated_resource(task)
                server = self._con.get(entity['resourceUri'])
                return server
        return task

    ###########################################################################
    # Server Profiles
    ###########################################################################
    def create_server_profile(self,
                              affinity='Bay',
                              biosSettings=None,
                              bootSettings=None,
                              bootModeSetting=None,
                              profileConnectionV4=None,
                              description=None,
                              firmwareSettingsV3=None,
                              hideUnusedFlexNics=True,
                              localStorageSettingsV3=None,
                              macType='Virtual',
                              name=None,
                              sanStorageV3=None,
                              serialNumber=None,
                              serialNumberType='Physical',
                              serverHardwareTypeUri=None,
                              serverHardwareUri=None,
                              serverProfileTemplateUri=None,
                              uuid=None,
                              wwnType='Virtual',
                              blocking=True, verbose=False):
        """ Create a ServerProfileV5 profile for use with the V200 API

        Args:
            affinity:
                This identifies the behavior of the server profile when the server
                hardware is removed or replaced. This can be set to 'Bay' or
                'BayAndServer'.
            biosSettings:
                Dictionary that describes Server BIOS settings
            bootSettings:
                Dictionary that indicates that the server will attempt to boot from
                this connection. This object can only be specified if
                "boot.manageBoot" is set to 'true'
            bootModeSetting:
                Dictionary that describes the boot mode settings to be confiured on
                Gen9 and newer servers.
            profileConnectionV4:
                Array of ProfileConnectionV3
            description:
                Description of the Server Profile
            firmwareSettingsV3:
                FirmwareSettingsV3 disctionary that defines the firmware baseline
                and managemnt
            hideUnusedFlexNics:
                This setting controls the enumeration of physical functions that do
                not correspond to connections in a profile.
            localStorageSettingsV3:
                Disctionary that describes the local storage settings.
            macType:
                Specifies the type of MAC address to be programmed into the IO
                devices. The value can be 'Virtual', 'Physical' or 'UserDefined'.
            name:
                Unique name of the Server Profile
            sanStorageV3:
                Dictionary that describes teh san storage settings.
            serialNumber:
                A 10-byte value that is exposed to the Operating System as the
                server hardware's Serial Number. The value can be a virtual serial
                number, user defined serial number or physical serial number read
                from the server's ROM. It cannot be modified after the profile is
                created.
            serialNumberType:
                 Specifies the type of Serial Number and UUID to be programmed into
                 the server ROM. The value can be 'Virtual', 'UserDefined', or
                 'Physical'. The serialNumberType defaults to 'Virtual' when
                 serialNumber or uuid are not specified. It cannot be modified
                 after the profile is created.
            serverHardwareTypeUri:
                Identifies the server hardware type for which the Server Profile
                was designed. The serverHardwareTypeUri is determined when the
                profile is created.
            serverHardwareUri:
                 Identifies the server hardware to which the server profile is
                 currently assigned, if applicable
            serverProfileTemplateUri:
                Identifies the Server profile template the Server Profile is based
                on.
            uuid:
                A 36-byte value that is exposed to the Operating System as the
                server hardware's UUID. The value can be a virtual uuid, user
                defined uuid or physical uuid read from the server's ROM. It
                cannot be modified after the profile is created.
            wwnType:
                 Specifies the type of WWN address to be programmed into the IO
                 devices. The value can be 'Virtual', 'Physical' or 'UserDefined'.
                 It cannot be modified after the profile is created.

        Returns: server profile or task
        """

        # Creating a profile returns a task with no resource uri
        profile = make_ServerProfileV5(affinity, biosSettings, bootSettings,
                                       bootModeSetting, profileConnectionV4,
                                       description, firmwareSettingsV3,
                                       hideUnusedFlexNics,
                                       localStorageSettingsV3, macType, name,
                                       sanStorageV3, serialNumber,
                                       serialNumberType, serverHardwareTypeUri,
                                       serverHardwareUri,
                                       serverProfileTemplateUri, uuid, wwnType)
        task, body = self._con.post(uri['profiles'], profile)
        if profile['firmware'] is None:
            tout = 600
        else:
            tout = 3600
        if blocking is True:
            task = self._activity.wait4task(task, tout, verbose=verbose)
            if 'type' in task and task['type'].startswith('Task'):
                entity = self._activity.get_task_associated_resource(task)
                profile = self._con.get(entity['resourceUri'])
                return profile
        return task


    def post_server_profile(self, profile, blocking=True, verbose=False):
        """ POST a ServerProfileV5 profile for use with the V200 API

        Args:
            profile:
                ServerProfileV5

        Returns: server profile or task
        """

        task, body = self._con.post(uri['profiles'], profile)
        if profile['firmware'] is None:
            tout = 600
        else:
            tout = 3600
        if blocking is True:
            task = self._activity.wait4task(task, tout, verbose=verbose)
            if 'type' in task and task['type'].startswith('Task'):
                entity = self._activity.get_task_associated_resource(task)
                profile = self._con.get(entity['resourceUri'])
                return profile
        return task


    def remove_server_profile(self, profile, force=False, blocking=True, verbose=False):
        if force:
            task, body = self._con.delete(profile['uri'] + '?force=True')
        else:
            task, body = self._con.delete(profile['uri'])
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        return task

    def get_server_profiles(self):
        body = self._con.get(uri['profiles'])
        return get_members(body)

    def update_server_profile(self, profile, blocking=True, verbose=False):
        task, body = self._con.put(profile['uri'], profile)
        try:
            if profile['firmware']['firmwareBaselineUri'] is None:
                tout = 600
            else:
                tout = 3600
        except Exception:
            tout = 600
        # Update the task to get the associated resource uri
        if blocking is True:
            task = self._activity.wait4task(task, tout=tout, verbose=verbose)
        profileResource = self._activity.get_task_associated_resource(task)
        profile = self._con.get(profileResource['resourceUri'])
        return profile

    def update_server_profile_from_template(self, profile, blocking=True, verbose=False):
        patch_request = [{'op':'replace', 'path':'/templateCompliance', 'value':'Compliant'}]
        task, body = self._con.patch(profile['uri'], patch_request)
        try:
            if profile['firmware']['firmwareBaselineUri'] is None:
                tout = 600
            else:
                tout = 3600
        except Exception:
            tout = 600
            # Update the task to get the associated resource uri
            if blocking is True:
                task = self._activity.wait4task(task, tout=tout, verbose=verbose)
            profileResource = self._activity.get_task_associated_resource(task)
            profile = self._con.get(profileResource['resourceUri'])
            return profile

    def get_server_profile_by_name(self, name):
        body = self._con.get_entity_byfield(uri['profiles'], 'name', name)
        return body


    ###########################################################################
    # Server Profile Templates
    ###########################################################################
    def create_server_profile_template(
                                       self, 
                                       name=None, 
                                       description=None, 
                                       serverProfileDescription=None, 
                                       serverHardwareTypeUri=None, 
                                       enclosureGroupUri=None,
                                       affinity=None,
                                       hideUnusedFlexNics=None, 
                                       blocking=True, 
                                       verbose=False):
        """
        Create a ServerProfileTemplateV1 dictionary for use with the V200 API
        Args:
            name:
                Unique name of the Server Profile Template
            description:
                Description of the Server Profile Template
            serverProfileDescription:
                The description of the server profiles created from this template.
            serverHardwareTypeUri:
                Identifies the server hardware type for which the Server Profile
                was designed. The serverHardwareTypeUri is determined when the
                profile is created.
            enclosureGroupUri:
                 Identifies the enclosure group for which the Server Profile Template
                 was designed. The enclosureGroupUri is determined when the profile
                 template is created and cannot be modified.
            affinity:
                This identifies the behavior of the server profile when the server
                hardware is removed or replaced. This can be set to 'Bay' or
                'BayAndServer'.        
            hideUnusedFlexNics:
                This setting controls the enumeration of physical functions that do
                not correspond to connections in a profile.        
    
        Returns: dict
        """       
        profile_template = make_ServerProfileTemplateV1(
                                                        name, 
                                                        description, 
                                                        serverProfileDescription,
                                                        serverHardwareTypeUri,
                                                        enclosureGroupUri,
                                                        affinity,
                                                        hideUnusedFlexNics)

        task, body = self._con.post(uri['profile-templates'], profile_template)
        tout = 600
        if blocking is True:
            task = self._activity.wait4task(task, tout, verbose=verbose)
            if 'type' in task and task['type'].startswith('Task'):
                entity = self._activity.get_task_associated_resource(task)
                profile_template = self._con.get(entity['resourceUri'])
                return profile_template
        return task

    def remove_server_profile_template(self, profile_template, blocking=True, verbose=False):
        task, body = self._con.delete(profile_template['uri'])
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            return task
        return body

    def get_server_profile_templates(self):
        body = self._con.get(uri['profile-templates'])
        return get_members(body)

    def get_server_profile_template_by_name(self, name):
        body = self._con.get_entity_byfield(uri['profile-templates'], 'name', name)
        return body

    def update_server_profile_template(self, profile_template, blocking=True, verbose=False):
        task, body = self._con.put(profile_template['uri'], profile_template)
        tout = 600
        # Update the task to get the associated resource uri
        if blocking is True:
            task = self._activity.wait4task(task, tout=tout, verbose=verbose)
        profileTemplateResource = self._activity.get_task_associated_resource(task)
        profile = self._con.get(profileTemplateResource['resourceUri'])
        return profile_template

    def get_server_profile_from_template(self, profile_template):
        profile = self._con.get(profile_template['uri']+'/new-profile')
        return profile

    ###########################################################################
    # Enclosures
    ###########################################################################
    def get_enclosures(self):
        body = self._con.get(uri['enclosures'])
        return get_members(body)

    def add_enclosure(self, enclosure, blocking=True, verbose=False):
        task, body = self._con.post(uri['enclosures'], enclosure)
        if enclosure['state'] is 'Monitored':
            tout = 600
        elif enclosure['firmwareBaselineUri'] is None:
            tout = 600
        else:
            tout = 3600

        if blocking is True:
            task = self._activity.wait4task(task, tout, verbose=verbose)
            if 'type' in task and task['type'].startswith('Task'):
                entity = self._activity.get_task_associated_resource(task)
                enclosure = self._con.get(entity['resourceUri'])
                return enclosure
        return task

    def remove_enclosure(self, enclosure, force=False, blocking=True,
                         verbose=False):
        if force:
            task, body = self._con.delete(enclosure['uri'] + '?force=True')
        else:
            task, body = self._con.delete(enclosure['uri'])
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        return task

    ###########################################################################
    # Enclosure Groups
    ###########################################################################
    def create_enclosure_group(self, associatedLIGs, name,
                               powerMode='RedundantPowerSupply'):
        """ Create an EnclosureGroupV200 dictionary

        Args:
            associatedLIGs:
                A sorted list of logical interconnect group URIs associated with
                the enclosure group.
            name:
                The name of the enclosure group.
            powerMode:
                Power mode of the enclosure group. Values are 'RedundantPowerFeed'
                or 'RedundantPowerSupply'.

        Returns: enclosure group
        """
        egroup = make_EnclosureGroupV200(associatedLIGs, name, powerMode)
        # Creating an Enclosure Group returns the group, NOT a task
        task, body = self._con.post(uri['enclosureGroups'], egroup)
        return body

    def delete_enclosure_group(self, egroup):
        self._con.delete(egroup['uri'])

    def get_enclosure_groups(self):
        return get_members(self._con.get(uri['enclosureGroups']))

    def update_enclosure_group(self, enclosuregroup):
        task, body = self._con.put(enclosuregroup['uri'], enclosuregroup)
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

    def get_profile_networks(self):
        body = self._con.get(uri['profile-networks'])
        return body

    def get_profile_available_servers(self):
        body = self._con.get(uri['profile-available-servers'])
        return body

    def get_profile_available_storage_systems(self):
        body = self._con.get(uri['profile-available-storage-systems'])
        return body

    def get_profile_ports(self):
        body = self._con.get(uri['profile-ports'])
        return body

    # TODO put pool
    def allocate_pool_ids(self, url, count):
        allocatorUrl = '%s/allocator' % url
        allocatorBody = {'count': count}
        task, body = self._con.put(allocatorUrl, allocatorBody)
        return body

    def release_pool_ids(self, url, idList):
        collectorUrl = '%s/collector' % url
        collectorBody = {'idList': idList}
        task, body = self._con.put(collectorUrl, collectorBody)
        return body

    def allocate_range_ids(self, allocatorUrl, count):
        task, body = self._con.put(allocatorUrl, {'count': count})
        return body

    def release_range_ids(self, collectorUrl, idList):
        task, body = self._con.put(collectorUrl, {'idList': idList})
        return body

    # TODO POST Range
    def enable_range(self, url):
        prange = self._con.get(url)
        prange['enabled'] = True
        task, body = self._con.put(url, prange)
        return body

    def disable_range(self, url):
        prange = self._con.get(url)
        prange['enabled'] = False
        task, body = self._con.put(url, prange)
        return body

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
