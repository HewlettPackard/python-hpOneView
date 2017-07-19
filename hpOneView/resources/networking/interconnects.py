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
from hpOneView.resources.resource import merge_default_values


class Interconnects(object):
    """
    Interconnects API client.

    """

    URI = '/rest/interconnects'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a paginated collection of interconnects that includes the ports.

        To avoid a timeout on busy systems, the recommended maximum value of count is 2.

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all items.
                The actual number of items in the response might differ from the requested
                count if the sum of start and count exceeds the total number of items.
            filter (list or str):
                A general filter/query string to narrow the list of items returned. The
                default is no filter; all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.

        Returns:
            list: A list of interconnects.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def get_statistics(self, id_or_uri, port_name=''):
        """
        Gets the statistics from an interconnect.

        Args:
            id_or_uri:  Can be either the interconnect id or the interconnect uri.
            port_name (str): A specific port name of an interconnect.

        Returns:
             dict: The statistics for the interconnect that matches id.
        """
        uri = self._client.build_uri(id_or_uri) + "/statistics"

        if port_name:
            uri = uri + "/" + port_name

        return self._client.get(uri)

    def get_subport_statistics(self, id_or_uri, port_name, subport_number):
        """
        Gets the subport statistics on an interconnect.

        Args:
            id_or_uri:  Can be either the interconnect id or the interconnect uri.
            port_name (str): A specific port name of an interconnect.
            subport_number (int): The subport.

        Returns:
             dict: The statistics for the interconnect that matches id, port_name, and subport_number.
        """
        uri = self._client.build_uri(id_or_uri) + "/statistics/{0}/subport/{1}".format(port_name, subport_number)
        return self._client.get(uri)

    def get_name_servers(self, id_or_uri):
        """
        Gets the named servers for an interconnect.

        Args:
            id_or_uri:  Can be either the interconnect id or the interconnect uri.

        Returns:
             dict: the name servers for an interconnect.
        """

        uri = self._client.build_uri(id_or_uri) + "/nameServers"
        return self._client.get(uri)

    def get(self, id_or_uri):
        """
        Gets the Interconnect by ID or by URI.

        Args:
            id_or_uri: Can be either the interconnect id or the interconnect uri.

        Returns:
            dict
        """
        return self._client.get(id_or_uri)

    def get_by(self, field, value):
        """
        Gets all interconnects that match the filter
        The search is case-insensitive

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of interconnects.
        """
        return self._client.get_by(field, value)

    def get_by_name(self, name):
        """
        Retrieve an Interconnect by its name.

        Args:
            name: Interconnect name.

        Returns:
            dict: Interconnect.
        """
        return self._client.get_by_name(name)

    def patch(self, id_or_uri, operation, path, value, timeout=-1):
        """
        Performs a specific patch operation for the given interconnect.

        There is a limited set of interconnect properties which might be changed.
        They are: 'powerState', 'uidState', and 'deviceResetState'.

        If the interconnect supports the operation, the operation is performed and
        a task is returned through which the results are reported.

        Args:
            id_or_uri:
                Can be either the interconnect id or the interconnect uri
            operation:
                The type of operation: one of "add", "copy", "move", "remove", "replace", or "test".
            path:
                The JSON path the operation is to use. The exact meaning depends on the type of operation.
            value:
                The value to add or replace for "add" and "replace" operations or the value to compare against
                for a "test" operation. Not used by "copy", "move", or "remove".

        Returns:
            dict
        """
        return self._client.patch(id_or_uri, operation, path, value, timeout)

    def update_port(self, port_information, id_or_uri, timeout=-1):
        """
        Updates an interconnect port.

        Args:
            id_or_uri: Can be either the interconnect id or the interconnect uri.
            port_information (dict): object to update
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: The interconnect.

        """
        uri = self._client.build_uri(id_or_uri) + "/ports"
        return self._client.update(port_information, uri, timeout)

    def update_ports(self, ports, id_or_uri, timeout=-1):
        """
        Updates the interconnect ports.

        Args:
            id_or_uri: Can be either the interconnect id or the interconnect uri.
            ports (list): Ports to update.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: The interconnect.

        """
        resources = merge_default_values(ports, {'type': 'port'})

        uri = self._client.build_uri(id_or_uri) + "/update-ports"
        return self._client.update(resources, uri, timeout)

    def reset_port_protection(self, id_or_uri, timeout=-1):
        """
        Triggers a reset of port protection.

        Cause port protection to be reset on all the interconnects of the logical interconnect that matches ID.

        Args:
            id_or_uri: Can be either the interconnect id or the interconnect uri.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: The interconnect.

        """
        uri = self._client.build_uri(id_or_uri) + "/resetportprotection"
        return self._client.update_with_zero_body(uri, timeout)

    def get_ports(self, id_or_uri, start=0, count=-1):
        """
        Gets all interconnect ports.

        Args:
            id_or_uri: Can be either the interconnect id or the interconnect uri.
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all items.
                The actual number of items in the response might differ from the requested
                count if the sum of start and count exceeds the total number of items.

        Returns:
            list: All interconnect ports.
        """
        uri = self._client.build_subresource_uri(resource_id_or_uri=id_or_uri, subresource_path="ports")
        return self._client.get_all(start, count, uri=uri)

    def get_port(self, id_or_uri, port_id_or_uri):
        """
        Gets an interconnect port.

        Args:
            id_or_uri: Can be either the interconnect id or uri.
            port_id_or_uri: The interconnect port id or uri.

        Returns:
            dict: The interconnect port.
        """
        uri = self._client.build_subresource_uri(id_or_uri, port_id_or_uri, "ports")
        return self._client.get(uri)

    def get_pluggable_module_information(self, id_or_uri):
        """
        Gets all the pluggable module information.

        Args:
            id_or_uri: Can be either the interconnect id or uri.

        Returns:
            array: dicts of the pluggable module information.
        """
        uri = self._client.build_uri(id_or_uri) + "/pluggableModuleInformation"
        return self._client.get(uri)

    def update_configuration(self, id_or_uri, timeout=-1):
        """
        Reapplies the appliance's configuration on the interconnect. This includes running the same configure steps
        that were performed as part of the interconnect add by the enclosure.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            Interconnect
        """
        uri = self._client.build_uri(id_or_uri) + "/configuration"
        return self._client.update_with_zero_body(uri, timeout=timeout)
