# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2019) Hewlett Packard Enterprise Development LP
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

from copy import deepcopy

from hpOneView.resources.resource import (Resource, ResourcePatchMixin,
                                          ResourceSchemaMixin, ensure_resource_client)


class ServerProfiles(ResourcePatchMixin, ResourceSchemaMixin, Resource):
    """
    Server Profile API client.

    """
    URI = '/rest/server-profiles'

    DEFAULT_VALUES = {
        '200': {"type": "ServerProfileV5"},
        '300': {"type": "ServerProfileV6"},
        '500': {"type": "ServerProfileV7"},
        '600': {"type": "ServerProfileV8"},
        '800': {"type": "ServerProfileV9"}
    }

    def __init__(self, connection, data=None):
        super(ServerProfiles, self).__init__(connection, data)

    def create(self, data=None, timeout=-1, force=''):
        """Makes a POST request to create a resource when a request body is required.

        Args:
            data: Additional fields can be passed to create the resource.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
            force: Flag to force the operation
        Returns:
            Created resource.
        """
        if not data:
            data = {}

        default_values = self._get_default_values()
        for key, value in default_values.items():
            if not data.get(key):
                data[key] = value

        resource_data = self._helper.create(data, timeout=timeout, force=force)
        new_resource = self.new(self._connection, resource_data)

        return new_resource

    @ensure_resource_client(update_data=True)
    def update(self, data=None, timeout=-1, force=''):
        """Updates server profile template.

        Args:
            data: Data to update the resource.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
            force: Force the update operation.

        Returns:
            A dict with the updated resource data.
        """
        uri = self.data['uri']

        resource = deepcopy(self.data)
        resource.update(data)

        # Removes related fields to serverHardware in case of unassign
        if resource.get('serverHardwareUri') is None:
            resource.pop('enclosureBay', None)
            resource.pop('enclosureUri', None)

        self.data = self._helper.update(resource, uri, force, timeout)

        return self

    def delete_all(self, filter, timeout=-1, force=False):
        """
        Deletes all Server Profile objects from the appliance that match the provided filter.
        Filters are supported only for the following profile attributes:  name, description, serialnumber, uuid,
        mactype, wwntype, serialnumbertype, status, and state.


        Examples:
            >>> server_profile_client.delete_all(filter="name='Exchange Server'")
            # Remove all profiles that match the name "Exchange Server"

            >>> server_profile_client.delete_all(filter="name matches'%25Database%25'")
            # Remove all profiles that have the word "Database" in its name

        The filter function here operates similarly to the function defined for GET Server Profiles. It allows
        for both actual and partial matches of data in the profile. Any requests that use a wildcard match
        must include a %25 as illustrated in the previous example. This is how you encode that character for
        transmission to the appliance.

        Args:
            filter (dict): Object to delete.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates whether the server profile was successfully deleted.
        """
        return self._helper.delete_all(filter=filter, force=force, timeout=timeout)

    @ensure_resource_client
    def get_compliance_preview(self):
        """
        Gets the preview of manual and automatic updates required to make the server profile
        consistent with its template.

        Returns:
            dict: Server profile compliance preview.
        """
        uri = '{}/compliance-preview'.format(self.data["uri"])
        return self._helper.do_get(uri)

    def get_profile_ports(self, **kwargs):
        """
        Retrieves the port model associated with a server or server hardware type and enclosure group.

        Args:
            enclosureGroupUri (str):
                The URI of the enclosure group associated with the resource.
            serverHardwareTypeUri (str):
                The URI of the server hardware type associated with the resource.
            serverHardwareUri (str):
                The URI of the server hardware associated with the resource.

        Returns:
            dict: Profile port.
        """
        uri = self._helper.build_uri_with_query_string(kwargs, '/profile-ports')
        return self._helper.do_get(uri)

    @ensure_resource_client
    def get_messages(self):
        """
        Retrieves the error or status messages associated with the specified profile.

        Returns:
            dict: Server Profile Health.
        """
        uri = '{}/messages'.format(self.data["uri"])
        return self._helper.do_get(uri)

    @ensure_resource_client
    def get_transformation(self, **kwargs):
        """

        Transforms an existing profile by supplying a new server hardware type or enclosure group or both.
        A profile will be returned with a new configuration based on the capabilities of the supplied server hardware
        type or enclosure group or both. The port assignment for all deployed connections will be set to Auto.
        Re-selection of the server hardware may also be required. The new profile can subsequently be used for updating
        the server profile, but passing validation is not guaranteed. Any incompatibilities will be flagged when the
        transformed server profile is submitted.

        Args:
            enclosureGroupUri (str):
                The URI of the enclosure group associated with the resource.
            serverHardwareTypeUri (str):
                The URI of the server hardware type associated with the resource.
            serverHardwareUri (str):
                The URI of the server hardware associated with the resource.

        Returns:
            dict: Server Profile.
        """
        uri = self._helper.build_uri_with_query_string(kwargs,
                                                       '/transformation',
                                                       self.data["uri"])
        return self._helper.do_get(uri)

    def get_available_networks(self, **kwargs):
        """
        Retrieves the list of Ethernet networks, Fiber Channel networks, and network sets that are available to a
        server profile, along with their respective ports.

        Args:
           enclosureGroupUri (str): The URI of the enclosure group associated with the resource.
           functionType (str): The FunctionType (Ethernet or FibreChannel) to filter the list of networks returned.
           serverHardwareTypeUri (str): The URI of the server hardware type associated with the resource.
           serverHardwareUri (str): The URI of the server hardware associated with the resource.
           view (str): Returns a specific subset of the attributes of the resource or collection, by
               specifying the name of a predefined view. The default view is expand (show all attributes
               of the resource and all elements of collections of resources).

               Values:
                   Ethernet
                       Specifies that the connection is to an Ethernet network or a network set.
                   FibreChannel
                       Specifies that the connection is to a Fibre Channel network.
           profileUri (str): If the URI of the server profile is provided the list of available networks will
               include only networks that share a scope with the server profile.
           scopeUris (str): An expression to restrict the resources returned according to the scopes
               to which they are assigned

        Returns:
            list: Available networks.
        """
        uri = self._helper.build_uri_with_query_string(kwargs, '/available-networks')
        return self._helper.do_get(uri)

    def get_available_servers(self, **kwargs):
        """
        Retrieves the list of available servers.

        Args:
           enclosureGroupUri (str): The URI of the enclosure group associated with the resource.
           serverHardwareTypeUri (str): The URI of the server hardware type associated with the resource.
           profileUri (str): The URI of the server profile resource.
           scopeUris (str): An expression to restrict the resources returned according to
               the scopes to which they are assigned.
           filter (list or str): A general filter/query string to narrow the list of items returned.
               The default is no filter, all resources are returned.
        Returns:
            list: Available servers.
        """
        uri = self._helper.build_uri_with_query_string(kwargs, '/available-servers')
        return self._helper.do_get(uri)

    def get_available_storage_system(self, **kwargs):
        """
        Retrieves a specific storage system and its associated volumes available to the server profile based
        on the given server hardware type and enclosure group.

        Args:
           enclosureGroupUri (str):
               The URI of the enclosure group associated with the resource.
           serverHardwareTypeUri (str):
               The URI of the server hardware type associated with the resource.
           storageSystemId (str):
               The storage system ID associated with the resource.

        Returns:
            dict: Available storage system.
        """
        uri = self._helper.build_uri_with_query_string(kwargs, '/available-storage-system')
        return self._helper.do_get(uri)

    def get_available_storage_systems(self, start=0, count=-1, filter='', sort='', **kwargs):
        """
        Retrieves the list of the storage systems and their associated volumes available to the server profile
        based on the given server hardware type and enclosure group.

        Args:
           count:
               The number of resources to return. A count of -1 requests all items. The actual number of items in
               the response may differ from the requested count if the sum of start and count exceed the total
               number of items.
           start:
               The first item to return, using 0-based indexing. If not specified, the default is 0 - start with the
               first available item.
           filter (list or str):
               A general filter/query string to narrow the list of items returned. The default is no filter; all
               resources are returned.
           sort:
               The sort order of the returned data set. By default, the sort order is based on create time, with the
               oldest entry first.
           enclosureGroupUri (str):
               The URI of the enclosure group associated with the resource.
           serverHardwareTypeUri (str):
               The URI of the server hardware type associated with the resource.

        Returns:
            list: Available storage systems.
        """
        uri = self._helper.build_uri_with_query_string(kwargs, '/available-storage-systems')
        return self._helper.get_all(start=start, count=count, filter=filter, sort=sort, uri=uri)

    def get_available_targets(self, **kwargs):
        """
        Retrieves a list of the target servers and empty device bays that are available for assignment to the server
        profile.

        Args:
           enclosureGroupUri (str): The URI of the enclosure group associated with the resource.
           serverHardwareTypeUri (str): The URI of the server hardware type associated with the resource.
           profileUri (str): The URI of the server profile associated with the resource.
           scopeUris (str): An expression to restrict the resources returned according to
               the scopes to which they are assigned.
           filter (list or str): A general filter/query string to narrow the list of items returned.
               The default is no filter, all resources are returned.

        Returns:
            list: List of available servers and bays.
        """
        uri = self._helper.build_uri_with_query_string(kwargs, '/available-targets')
        return self._helper.do_get(uri)

    @ensure_resource_client
    def get_new_profile_template(self):
        """
        Retrieves the profile template for a given server profile.

        Returns:
            dict: Server profile template.
        """
        uri = '{}/new-profile-template'.format(self.data["uri"])
        return self._helper.do_get(uri)
