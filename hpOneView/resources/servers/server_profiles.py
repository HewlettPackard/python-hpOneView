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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()


from hpOneView.resources.resource import ResourceClient


class ServerProfiles(object):
    """
    Server Profile API client.

    """
    URI = '/rest/server-profiles'

    DEFAULT_VALUES = {
        '200': {"type": "ServerProfileV5"},
        '300': {"type": "ServerProfileV6"},
        '500': {"type": "ServerProfileV7"},
        '600': {"type": "ServerProfileV8"},

    }

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def create(self, resource, timeout=-1, force=''):
        """
        Creates a server profile using the information provided in the resource parameter.

        Args:
            resource (dict): Object to create.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.
            force: Comma separated list of flags for ignoring specific warning.

        Returns:
            dict: Created server profile.
        """
        uri = self.__build_uri_with_query_string({"force": force})
        return self._client.create(resource=resource, uri=uri, timeout=timeout, default_values=self.DEFAULT_VALUES)

    def update(self, resource, id_or_uri, force=''):
        """
        Allows the configuration of a server profile object to be modified.

        Args:
            id_or_uri: Can be either the server profile id or the server profile uri.
            resource (dict): Object to update.
            force: Comma separated list of flags for ignoring specific warning.

        Returns:
            dict: The server profile resource.
        """
        # Removes related fields to serverHardware in case of unassign
        if resource.get('serverHardwareUri') is None:
            resource.pop('enclosureBay', None)
            resource.pop('enclosureUri', None)

        uri = self. __build_uri_with_query_string({'force': force}, id_or_uri=id_or_uri)
        return self._client.update(resource=resource, uri=uri, default_values=self.DEFAULT_VALUES)

    def patch(self, id_or_uri, operation, path, value, timeout=-1):
        """
        Performs a specific patch operation for the given server profile.

        The supported operation:
            Updates the server profile from the server profile template.
                Operation: replace | Path: /templateCompliance | Value: Compliant

        Args:
            id_or_uri:
                Can be either the server profile id or the server profile uri
            operation:
                The type of operation: one of "add", "copy", "move", "remove", "replace", or "test".
            path:
                The JSON path the operation is to use. The exact meaning depends on the type of operation.
            value:
                The value to add or replace for "add" and "replace" operations, or the value to compare against
                for a "test" operation. Not used by "copy", "move", or "remove".

        Returns:
            dict: Server profile resource.
        """
        return self._client.patch(id_or_uri, operation, path, value, timeout)

    def delete(self, resource, timeout=-1):
        """
        Deletes a server profile object from the appliance based on its server profile UUID.

        Args:
            resource (dict): Object to delete.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates whether the server profile was successfully deleted.
        """
        return self._client.delete(resource=resource, timeout=timeout)

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
        return self._client.delete_all(filter=filter, force=force, timeout=timeout)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a list of server profiles based on optional sorting and filtering and is constrained by start and
        count parameters.

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return.
                Providing a -1 for the count parameter will restrict the result set size to 64 server profile
                templates. The maximum number of profile templates is restricted to 256, that is, if user requests more
                than 256, this will be internally limited to 256.
                The actual number of items in the response might differ from the
                requested count if the sum of start and count exceeds the total number of items, or if returning the
                requested number of items would take too long.
            filter (list or str):
                A general filter/query string to narrow the list of items returned. The
                default is no filter; all resources are returned.
                Filters are supported for the name, description, serialNumber, uuid, affinity, macType, wwnType,
                serialNumberType, serverProfileTemplateUri, templateCompliance, status, and state attributes.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.

        Returns:
            list: A list of server profiles.
        """
        return self._client.get_all(start=start, count=count, filter=filter, sort=sort)

    def get(self, id_or_uri):
        """
        Retrieves a server profile managed by the appliance by ID or by URI.

        Args:
            id_or_uri: Can be either the server profile resource ID or URI.

        Returns:
            dict: The server profile resource.
        """
        return self._client.get(id_or_uri=id_or_uri)

    def get_by(self, field, value):
        """
        Gets all server profiles that match a specified filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of server profiles.
        """
        return self._client.get_by(field, value)

    def get_by_name(self, name):
        """
        Gets a server profile by name.

        Args:
            name: Name of the server profile.

        Returns:
            dict: The server profile resource.
        """
        return self._client.get_by_name(name)

    def get_schema(self):
        """
        Generates the Server Profile schema.

        Returns:
            dict: The server profile schema.
        """
        return self._client.get_schema()

    def get_compliance_preview(self, id_or_uri):
        """
        Gets the preview of manual and automatic updates required to make the server profile
        consistent with its template.

        Args:
            id_or_uri: Can be either the server profile resource ID or URI.

        Returns:
            dict: Server profile compliance preview.
        """
        uri = self._client.build_uri(id_or_uri) + '/compliance-preview'
        return self._client.get(uri)

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
        uri = self.__build_uri_with_query_string(kwargs, '/profile-ports')
        return self._client.get(uri)

    def get_messages(self, id_or_uri):
        """
        Retrieves the error or status messages associated with the specified profile.

        Args:
            id_or_uri: Can be either the server profile resource ID or URI.

        Returns:
            dict: Server Profile Health.
        """
        uri = self._client.build_uri(id_or_uri) + '/messages'
        return self._client.get(uri)

    def get_transformation(self, id_or_uri, **kwargs):
        """

        Transforms an existing profile by supplying a new server hardware type or enclosure group or both.
        A profile will be returned with a new configuration based on the capabilities of the supplied server hardware
        type or enclosure group or both. The port assignment for all deployed connections will be set to Auto.
        Re-selection of the server hardware may also be required. The new profile can subsequently be used for updating
        the server profile, but passing validation is not guaranteed. Any incompatibilities will be flagged when the
        transformed server profile is submitted.

        Args:
            id_or_uri:
                Can be either the server profile resource ID or URI.
            enclosureGroupUri (str):
                The URI of the enclosure group associated with the resource.
            serverHardwareTypeUri (str):
                The URI of the server hardware type associated with the resource.
            serverHardwareUri (str):
                The URI of the server hardware associated with the resource.

        Returns:
            dict: Server Profile.
        """
        uri = self.__build_uri_with_query_string(kwargs, '/transformation', id_or_uri)
        return self._client.get(uri)

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
        uri = self.__build_uri_with_query_string(kwargs, '/available-networks')
        return self._client.get(uri)

    def get_available_servers(self, **kwargs):
        """
        Retrieves the list of available servers.

        Args:
           enclosureGroupUri (str): The URI of the enclosure group associated with the resource.
           serverHardwareTypeUri (str): The URI of the server hardware type associated with the resource.
           profileUri (str): The URI of the server profile resource.
           scopeUris (str): An expression to restrict the resources returned according to
               the scopes to which they are assigned.

        Returns:
            list: Available servers.
        """
        uri = self.__build_uri_with_query_string(kwargs, '/available-servers')
        return self._client.get(uri)

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
        uri = self.__build_uri_with_query_string(kwargs, '/available-storage-system')
        return self._client.get(uri)

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
        uri = self.__build_uri_with_query_string(kwargs, '/available-storage-systems')
        return self._client.get_all(start=start, count=count, filter=filter, sort=sort, uri=uri)

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

        Returns:
            list: List of available servers and bays.
        """
        uri = self.__build_uri_with_query_string(kwargs, '/available-targets')
        return self._client.get(uri)

    def __build_uri_with_query_string(self, kwargs, sufix_path='', id_or_uri=None):
        uri = self.URI
        if id_or_uri:
            uri = self._client.build_uri(id_or_uri)

        query_string = '&'.join('{}={}'.format(key, kwargs[key]) for key in sorted(kwargs))
        return uri + sufix_path + '?' + query_string

    def get_new_profile_template(self, id_or_uri):
        """
        Retrieves the profile template for a given server profile.

        Args:
            id_or_uri: Can be either the server profile resource ID or URI.

        Returns:
            dict: Server profile template.
        """
        uri = self._client.build_uri(id_or_uri) + '/new-profile-template'
        return self._client.get(uri)
