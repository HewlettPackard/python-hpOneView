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

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()

from copy import deepcopy

from hpOneView.resources.resource import Resource, ensure_resource_client


class ServerProfileTemplate(Resource):
    """
    The server profile template resource provides methods to create, retrieve, modify, and delete server
    profile templates.

    A server profile template serves as a structural reference when creating a server profile.
    All of the configuration constructs of a server profile are present in the server profile template.
    The server profile template serves as the initial and ongoing reference for the structure of a server profile.
    The server profile template defines the centralized source for the configuration of firmware, connections,
    local storage, SAN storage, boot, BIOS, profile affinity and hide unused flexNICs.

    After being created from a server profile template, the server profile continues to maintain an association to its
    server profile template. Any drift in configuration consistency between the server profile template and server
    profile(s) is monitored and made visible on both the server profile template and the associated server profile(s).

    """

    URI = '/rest/server-profile-templates'
    TRANSFORMATION_PATH = "/transformation/?serverHardwareTypeUri={server_hardware_type_uri}" + \
                          "&enclosureGroupUri={enclosure_group_uri}"

    DEFAULT_VALUES = {
        '200': {'type': 'ServerProfileTemplateV1'},
        '300': {'type': 'ServerProfileTemplateV2'},
        '500': {'type': 'ServerProfileTemplateV3'},
        '600': {'type': 'ServerProfileTemplateV4'},
        '800': {'type': 'ServerProfileTemplateV5'}
    }

    def __init__(self, connection, data=None):
        super(ServerProfileTemplate, self).__init__(connection, data)

    def get_all(self, start=0, count=-1, filter='', sort='', scope_uris=''):
        """
        Gets a list of server profile templates based on optional sorting and filtering and is constrained by start and
        count parameters.

        Args:
            start: The first item to return, using 0-based indexing. If not specified, the default
                is 0 - start with the first available item.
            count: The number of resources to return. Providing a -1 for the count parameter will restrict
                the result set size to 64 server profile templates. The maximum number of profile templates
                is restricted to 256, that is, if user requests more than 256, this will be internally limited to 256.
                The actual number of items in the response might differ from the
                requested count if the sum of start and count exceeds the total number of items, or if returning the
                requested number of items would take too long.
            filter (list or str): A general filter/query string to narrow the list of items returned. The default is no filter; all
                resources are returned. Filters are supported for the name, description, affinity, macType, wwnType,
                serialNumberType, status, serverHardwareTypeUri, enclosureGroupUri, and firmware.firmwareBaselineUri attributes.
            sort: The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.
            scope_uris: An expression to restrict the resources returned according to the scopes to which they are assigned.

        Returns:
            list: A list of server profile templates.

        """
        return self._helper.get_all(start=start, count=count, filter=filter, sort=sort, scope_uris=scope_uris)

    def create(self, data=None, uri=None, timeout=-1, force=True):
        """Makes a POST request to create a resource when a request body is required.

        Args:
            data: Additional fields can be passed to create the resource.
            uri: Resouce uri
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

        resource_data = self._helper.create(data, uri, timeout, force=force)
        new_resource = self.new(self._connection, resource_data)

        return new_resource

    @ensure_resource_client(update_data=True)
    def update(self, data=None, timeout=-1, force=True):
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

        self.data = self._helper.update(resource, uri, force, timeout)

        return self

    @ensure_resource_client
    def get_new_profile(self):
        """
        A profile object will be returned with the configuration based on this template. Specify the profile name and
        server hardware to assign. If template has any fiber channel connection (which is specified as bootable) but no
        boot target was defined, that connection will be instantiated as a non-bootable connection. So modify that
        connection to change it to bootable and to specify the boot target.

        Returns:
            dict: The server profile resource.
        """
        uri = "{}/new-profile".format(self.data["uri"])
        return self._helper.do_get(uri)

    @ensure_resource_client
    def get_transformation(self, server_hardware_type_uri, enclosure_group_uri):
        """
        Transforms an existing profile template by supplying a new server hardware type and enclosure group or both.
        A profile template will be returned with a new configuration based on the capabilities of the supplied
        server hardware type and/or enclosure group. All configured connections will have their port assignments
        set to 'Auto.'
        The new profile template can subsequently be used in the update method, but is not guaranteed to pass
        validation. Any incompatibilities will be flagged when the transformed server profile template is submitted.

        Note:
            This method is available for API version 300 or later.

        Args:
            server_hardware_type_uri: The URI of the new server hardware type.
            enclosure_group_uri: The URI of the new enclosure group.

        Returns:
            dict: The server profile template resource.
        """
        query_params = self.TRANSFORMATION_PATH.format(**locals())
        uri = "{}{}".format(self.data["uri"], query_params)
        return self._helper.do_get(uri)

    def get_available_networks(self, **kwargs):
        """
        Retrieves the list of Ethernet networks, Fibre Channel networks and network sets that are available
        to a server profile template along with their respective ports. The scopeUris, serverHardwareTypeUri and
        enclosureGroupUri parameters should be specified to get the available networks for a new server profile template.
        The serverHardwareTypeUri, enclosureGroupUri, and profileTemplateUri should be specified to get available
        networks for an existing server profile template.
        The scopeUris parameter is ignored when the profileTemplateUri is specified.

        Args:
            enclosureGroupUri: The URI of the enclosure group is required when the serverHardwareTypeUri
                specifies a blade server.
            profileTemplateUri: If the URI of the server profile template is provided the list of available
                networks will include only networks that share a scope with the server profile template.
            scopeUris: An expression to restrict the resources returned according to the scopes
                to which they are assigned.
            serverHardwareTypeUri: If the server hardware type specifies a rack server, the list of
                available network includes all networks that are applicable for the specified server hardware type.
                If the server hardware type specifies a blade server, the enclosureGroupUri parameter must be
                specified, and the list of available networks includes all networks that are applicable for the
                specified server hardware type and all empty bays within the enclosure group that can support
                the specified server hardware type.
            view: The FunctionType (Ethernet or FibreChannel) to filter the list of networks returned.

        Returns:
            dict: Dictionary with available networks details.
        """
        query_string = '&'.join('{}={}'.format(key, value)
                                for key, value in kwargs.items() if value)
        uri = self.URI + "{}?{}".format("/available-networks", query_string)

        return self._helper.do_get(uri)
