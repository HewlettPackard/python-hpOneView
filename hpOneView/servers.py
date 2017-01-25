# -*- coding: utf-8 -*-

"""
servers.py
~~~~~~~~~~~~

This module implements servers HPE OneView REST API.

It has been deprecated and will be removed soon. We strongly recommend to use the OneViewClient class instead.
See more details at: https://github.com/HewlettPackard/python-hpOneView/tree/master/hpOneView/README.md
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()


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

from hpOneView.activity import activity
from hpOneView.common import get_members, uri, make_powerstate_dict, make_server_type_dict, make_ServerProfileV5, \
    make_EnclosureGroupV200, make_ServerProfileTemplateV1
from warnings import warn


def deprecated(func):
    def wrapper(*args, **kwargs):
        warn("Module servers is deprecated, use OneViewClient class instead", DeprecationWarning)
        return func(*args, **kwargs)
    return wrapper


class servers(object):
    def __init__(self, con):
        self._con = con
        self._activity = activity(con)

    ###########################################################################
    # Connections
    ###########################################################################
    @deprecated
    def get_connections(self, filter=''):
        """ List all the active connections

            Args:
                filter:
                    A general filter/query string that narrows the list of
                    resources returned by a multi-resource GET (read) request and
                    DELETE (delete) request. The default is no filter
                    (all resources are returned). The filter parameter specifies
                    a general filter/query string. This query string narrows the
                    selection of resources returned from a GET request that
                    returns a list of resources. The following example shows how to
                    retrieve only the first 10 connections:

            Returns: all the connections, filtered or not.
            """
        return get_members(self._con.get(uri['conn'] + filter))

    @deprecated
    def get_connection(self, server):
        """ List a specific connection

            Args:
                server:
                    Connection id

            Returns: all the connections, filtered or not.
        """
        body = self._con.get(server['uri'])
        return body

    ###########################################################################
    # Server Hardware
    ###########################################################################
    @deprecated
    def get_server_by_bay(self, baynum):
        servers = get_members(self._con.get(uri['servers']))
        for server in servers:
            if server['position'] == baynum:
                return server

    @deprecated
    def get_server_by_name(self, name):
        servers = get_members(self._con.get(uri['servers']))
        for server in servers:
            if server['name'] == name:
                return server

    @deprecated
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

    @deprecated
    def get_servers(self):
        return get_members(self._con.get(uri['servers']))

    @deprecated
    def get_utilization(self, server):
        """Retrieves historical utilization data for the specified resource, metrics, and time span. """
        body = self._con.get(server['uri'] + '/utilization')
        return body

    @deprecated
    def get_env_conf(self, server):
        """Gets the settings that describe the environmental configuration of the server hardware resource. """
        body = self._con.get(server['uri'] + '/environmentalConfiguration')
        return body

    @deprecated
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

    @deprecated
    def delete_server(self, server, force=False, blocking=True, verbose=False):
        if force:
            task, body = self._con.delete(server['uri'] + '?force=True')
        else:
            task, body = self._con.delete(server['uri'])
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        return task

    @deprecated
    def update_server(self, server):
        task, body = self._con.put(server['uri'], server)
        return body

    @deprecated
    def add_server(self, server, blocking=True, verbose=False):
        task, body = self._con.post(uri['servers'], server)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            if 'type' in task and task['type'].startswith('Task'):
                entity = self._activity.get_task_associated_resource(task)
                server = self._con.get(entity['resourceUri'])
                return server
        return task

    @deprecated
    def get_server_schema(self):
        """ Gets the JSON schema of the server hardware resource."""
        return self._con.get(uri['servers'] + '/schema')

    @deprecated
    def get_bios(self, server):
        """ Gets the list of BIOS/UEFI values currently set on the physical server."""
        return self._con.get(server['uri'] + '/bios')

    @deprecated
    def get_ilo_sso_url(self, server):
        """ Retrieves the URL to launch a Single Sign-On (SSO) session for the iLO web interface."""
        return self._con.get(server['uri'] + '/iloSsoUrl')

    @deprecated
    def get_java_remote_console_url(self, server):
        """ Generates a Single Sign-On (SSO) session for the iLO Java Applet console and returns
        the URL to launch it. """
        return self._con.get(server['uri'] + '/javaRemoteConsoleUrl')

    @deprecated
    def get_remote_console_url(self, server):
        """ Generates a Single Sign-On (SSO) session for the iLO Integrated Remote Console Application
        (IRC) and returns the URL to launch it."""
        return self._con.get(server['uri'] + '/remoteConsoleUrl')

    ###########################################################################
    # Server Hardware Types
    ###########################################################################
    @deprecated
    def get_server_hardware_types(self):
        """ Get the list of server hardware type resources defined on the appliance."""
        body = self._con.get(uri['server-hardware-types'])
        return get_members(body)

    @deprecated
    def remove_server_hardware_type(self, server_hardware_type, force=False, blocking=True, verbose=False):
        """ Remove the server hardware type with the specified URI. A server hardware type cannot be deleted
         if it is associated with a server hardware or server profile resource. """
        if force:
            task, body = self._con.delete(server_hardware_type['uri'] + '?force=True')
        else:
            task, body = self._con.delete(server_hardware_type['uri'])
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        return task

    @deprecated
    def get_server_type_schema(self):
        """ Get the JSON schema of the server hardware types resource."""
        return self._con.get(uri['server-hardware-types'] + '/schema')

    @deprecated
    def get_server_hardware_type(self, server_type):
        """ Get the server hardware type resource with the specified ID."""
        return self._con.get(server_type['uri'])

    @deprecated
    def set_server_hardware_type(self, server_hardware_type, name, description):
        """ Updates one or more attributes for a server hardware type resource.

        Args:
            name:
                 The localized name that describes a BIOS/UEFI setting.
            description:
                 Brief description of the server hardware type.
                    Maximum Length: 255
                    Minimum Length: 0
        """
        request = make_server_type_dict(name, description)
        task, body = self._con.put(server_hardware_type['uri'], request)
        return task

    ###########################################################################
    # Server Profiles
    ###########################################################################
    @deprecated
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
                Dictionary that describes the boot mode settings to be configured on
                Gen9 and newer servers.
            profileConnectionV4:
                Array of ProfileConnectionV3
            description:
                Description of the Server Profile
            firmwareSettingsV3:
                FirmwareSettingsV3 dictionary that defines the firmware baseline
                and management
            hideUnusedFlexNics:
                This setting controls the enumeration of physical functions that do
                not correspond to connections in a profile.
            localStorageSettingsV3:
                Dictionary that describes the local storage settings.
            macType:
                Specifies the type of MAC address to be programmed into the IO
                devices. The value can be 'Virtual', 'Physical' or 'UserDefined'.
            name:
                Unique name of the Server Profile
            sanStorageV3:
                Dictionary that describes the SAN storage settings.
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

        # missing required field: enclousure group
        # E.g.: profile['enclosureGroupUri'] =  "/rest/enclosure-groups/a0f1c07b-f811-4c85-8e38-ac5ec34ea2f4"
        return self.create_server_profile_from_dict(profile, blocking, verbose)

    @deprecated
    def create_server_profile_from_dict(self, profile, blocking=True, verbose=False):
        # Creating a profile returns a task with no resource uri
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

    @deprecated
    def get_server_profile_compliance(self, server_profile):
        compliance_preview = self._con.get(server_profile['uri'] + '/compliance-preview')
        return compliance_preview

    @deprecated
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

    @deprecated
    def remove_server_profile(self, profile, force=False, blocking=True, verbose=False):
        if force:
            task, body = self._con.delete(profile['uri'] + '?force=True')
        else:
            task, body = self._con.delete(profile['uri'])
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        return task

    @deprecated
    def get_server_profiles(self):
        body = self._con.get(uri['profiles'])
        return get_members(body)

    @deprecated
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

    @deprecated
    def update_server_profile_from_template(self, profile, blocking=True, verbose=False):
        patch_request = [{'op': 'replace', 'path': '/templateCompliance', 'value': 'Compliant'}]
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

    @deprecated
    def get_server_profile_by_name(self, name):
        body = self._con.get_entity_byfield(uri['profiles'], 'name', name)
        return body

    @deprecated
    def get_profile_message(self, profile):
        """ Retrieve the error or status messages associated with the specified profile. """
        message = self._con.get(profile['uri'] + '/messages')
        return message

    @deprecated
    def get_profile_compliance_preview(self, profile):
        """ Gets the preview of manual and automatic updates required to make the
        server profile consistent with its template. """
        return self._con.get(profile['uri'] + '/compliance-preview')

    ###########################################################################
    # Server Profile Templates
    ###########################################################################
    @deprecated
    def create_server_profile_template(self, name=None, description=None,
                                       serverProfileDescription=None, serverHardwareTypeUri=None,
                                       enclosureGroupUri=None, affinity=None, hideUnusedFlexNics=None,
                                       profileConnectionV4=None, firmwareSettingsV3=None, bootSettings=None,
                                       bootModeSetting=None, sanStorageV3=None, blocking=True, verbose=False):
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
            profileConnectionV4:
                An array of profileConnectionV4
            firmwareSettingsV3:
                FirmwareSettingsV3 dictionary that defines the firmware baseline
                and management.
            bootSettings:
                Dictionary that indicates that the server will attempt to boot from
                this connection. This object can only be specified if
                "boot.manageBoot" is set to 'true'
            bootModeSetting:
                Dictionary that describes the boot mode settings to be configured on
                Gen9 and newer servers.
            sanStorageV3:
                Dictionary that describes the SAN storage settings.

        Returns: dict
        """
        profile_template = make_ServerProfileTemplateV1(name,
                                                        description,
                                                        serverProfileDescription,
                                                        serverHardwareTypeUri,
                                                        enclosureGroupUri,
                                                        affinity,
                                                        hideUnusedFlexNics,
                                                        profileConnectionV4,
                                                        firmwareSettingsV3,
                                                        bootSettings,
                                                        bootModeSetting,
                                                        sanStorageV3)

        task, body = self._con.post(uri['profile-templates'], profile_template)
        tout = 600
        if blocking is True:
            task = self._activity.wait4task(task, tout, verbose=verbose)
            if 'type' in task and task['type'].startswith('Task'):
                entity = self._activity.get_task_associated_resource(task)
                profile_template = self._con.get(entity['resourceUri'])
                return profile_template
        return task

    @deprecated
    def remove_server_profile_template(self, profile_template, blocking=True, verbose=False):
        task, body = self._con.delete(profile_template['uri'])
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            return task
        return body

    @deprecated
    def get_server_profile_templates(self):
        body = self._con.get(uri['profile-templates'])
        return get_members(body)

    @deprecated
    def get_server_profile_template_by_name(self, name):
        body = self._con.get_entity_byfield(uri['profile-templates'], 'name', name)
        return body

    @deprecated
    def update_server_profile_template(self, profile_template, blocking=True, verbose=False):
        task, body = self._con.put(profile_template['uri'], profile_template)
        tout = 600
        # Update the task to get the associated resource uri
        if blocking is True:
            task = self._activity.wait4task(task, tout=tout, verbose=verbose)
        profileTemplateResource = self._activity.get_task_associated_resource(task)
        self._con.get(profileTemplateResource['resourceUri'])
        return profile_template

    @deprecated
    def get_server_profile_from_template(self, profile_template):
        profile = self._con.get(profile_template['uri'] + '/new-profile')
        return profile

    ###########################################################################
    # Enclosures
    ###########################################################################
    @deprecated
    def get_enclosures(self):
        body = self._con.get(uri['enclosures'])
        return get_members(body)

    @deprecated
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

    @deprecated
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
    @deprecated
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

    @deprecated
    def delete_enclosure_group(self, egroup):
        self._con.delete(egroup['uri'])

    @deprecated
    def get_enclosure_groups(self):
        return get_members(self._con.get(uri['enclosureGroups']))

    @deprecated
    def update_enclosure_group(self, enclosuregroup):
        task, body = self._con.put(enclosuregroup['uri'], enclosuregroup)
        return body

    ###########################################################################
    # ID Pools
    ###########################################################################
    @deprecated
    def get_pool(self, pooltype):
        body = self._con.get(uri['idpool'] + '/' + pooltype)
        return body

    @deprecated
    def get_vmac_pool(self):
        body = self._con.get(uri['vmac-pool'])
        return body

    @deprecated
    def get_vwwn_pool(self):
        body = self._con.get(uri['vwwn-pool'])
        return body

    @deprecated
    def get_vsn_pool(self):
        body = self._con.get(uri['vsn-pool'])
        return body

    @deprecated
    def get_profile_networks(self):
        body = self._con.get(uri['profile-networks'])
        return body

    @deprecated
    def get_profile_schema(self):
        return self._con.get(uri['profile-networks-schema'])

    @deprecated
    def get_profile_available_servers(self):
        body = self._con.get(uri['profile-available-servers'])
        return body

    @deprecated
    def get_profile_available_storage_systems(self):
        body = self._con.get(uri['profile-available-storage-systems'])
        return body

    @deprecated
    def get_profile_ports(self):
        body = self._con.get(uri['profile-ports'])
        return body

    # TODO put pool
    @deprecated
    def allocate_pool_ids(self, url, count):
        allocatorUrl = '%s/allocator' % url
        allocatorBody = {'count': count}
        task, body = self._con.put(allocatorUrl, allocatorBody)
        return body

    @deprecated
    def release_pool_ids(self, url, idList):
        collectorUrl = '%s/collector' % url
        collectorBody = {'idList': idList}
        task, body = self._con.put(collectorUrl, collectorBody)
        return body

    @deprecated
    def allocate_range_ids(self, allocatorUrl, count):
        task, body = self._con.put(allocatorUrl, {'count': count})
        return body

    @deprecated
    def release_range_ids(self, collectorUrl, idList):
        task, body = self._con.put(collectorUrl, {'idList': idList})
        return body

    # TODO POST Range
    @deprecated
    def enable_range(self, url):
        prange = self._con.get(url)
        prange['enabled'] = True
        task, body = self._con.put(url, prange)
        return body

    @deprecated
    def disable_range(self, url):
        prange = self._con.get(url)
        prange['enabled'] = False
        task, body = self._con.put(url, prange)
        return body

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
