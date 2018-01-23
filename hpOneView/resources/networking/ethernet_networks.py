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


class EthernetNetworks(object):
    """
    Ethernet Networks API client.

    """
    URI = '/rest/ethernet-networks'

    DEFAULT_VALUES = {
        '200': {"type": "ethernet-networkV3"},
        '300': {"type": "ethernet-networkV300"},
        '500': {"type": "ethernet-networkV300"},
        '600': {"type": "ethernet-networkV4"}
    }
    BULK_DEFAULT_VALUES = {
        '200': {"type": "bulk-ethernet-network"},
        '300': {"type": "bulk-ethernet-network"},
        '500': {"type": "bulk-ethernet-network"},
        '600': {"type": "bulk-ethernet-networkV1"}
    }

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a paginated collection of Ethernet networks. The collection is based on optional sorting and filtering
        and is constrained by start and count parameters.

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
            list: A list of ethernet networks.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def delete(self, resource, force=False, timeout=-1):
        """
        Deletes an Ethernet network.

        Any deployed connections that are using the network are placed in the 'Failed' state.

        Args:
            resource: dict object to delete
            force:
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates if the resource was successfully deleted.

        """
        return self._client.delete(resource, force=force, timeout=timeout)

    def get(self, id_or_uri):
        """
        Gets the Ethernet network.

        Args:
            id_or_uri: ID or URI of Ethernet network.

        Returns:
            dict: The ethernet network.
        """
        return self._client.get(id_or_uri)

    def create(self, resource, timeout=-1):
        """
        Creates an Ethernet network.

        Args:
            resource (dict): Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Created resource.

        """
        return self._client.create(resource, timeout=timeout, default_values=self.DEFAULT_VALUES)

    def create_bulk(self, resource, timeout=-1):
        """
        Creates bulk Ethernet networks.

        Args:
            resource (dict): Specifications to create in bulk.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            list: List of created Ethernet Networks.

        """
        uri = self.URI + '/bulk'
        self._client.create(resource, uri=uri, timeout=timeout, default_values=self.BULK_DEFAULT_VALUES)

        return self.get_range(resource['namePrefix'], resource['vlanIdRange'])

    def get_range(self, name_prefix, vlan_id_range):
        """
        Gets a list of Ethernet Networks that match the 'given name_prefix' and the 'vlan_id_range'.

        Examples:
            >>> enet.get_range('Enet_name', '1-2,5')
                # The result contains the ethernet network with names:
                ['Enet_name_1', 'Enet_name_2', 'Enet_name_5']

            >>> enet.get_range('Enet_name', '2')
                # The result contains the ethernet network with names:
                ['Enet_name_1', 'Enet_name_2']

        Args:
            name_prefix: The Ethernet Network prefix
            vlan_id_range: A combination of values or ranges to be retrieved. For example, '1-10,50,51,500-700'.

        Returns:
            list: A list of Ethernet Networks.

        """
        filter = '"\'name\' matches \'{}\_%\'"'.format(name_prefix)
        ethernet_networks = self.get_all(filter=filter, sort='vlanId:ascending')

        vlan_ids = self.dissociate_values_or_ranges(vlan_id_range)

        for net in ethernet_networks[:]:
            if int(net['vlanId']) not in vlan_ids:
                ethernet_networks.remove(net)
        return ethernet_networks

    def dissociate_values_or_ranges(self, vlan_id_range):
        """
        Build a list of vlan ids given a combination of ranges and/or values

        Examples:
            >>> enet.dissociate_values_or_ranges('1-2,5')
                [1, 2, 5]

            >>> enet.dissociate_values_or_ranges('5')
                [1, 2, 3, 4, 5]

            >>> enet.dissociate_values_or_ranges('4-5,7-8')
                [4, 5, 7, 8]

        Args:
            vlan_id_range: A combination of values or ranges. For example, '1-10,50,51,500-700'.

        Returns:
            list: vlan ids
        """
        values_or_ranges = vlan_id_range.split(',')
        vlan_ids = []
        # The expected result is different if the vlan_id_range contains only one value
        if len(values_or_ranges) == 1 and '-' not in values_or_ranges[0]:
            vlan_ids = list(range(1, int(values_or_ranges[0]) + 1))
        else:
            for value_or_range in values_or_ranges:
                value_or_range.strip()
                if '-' not in value_or_range:
                    vlan_ids.append(int(value_or_range))
                else:
                    start, end = value_or_range.split('-')
                    range_ids = range(int(start), int(end) + 1)
                    vlan_ids.extend(range_ids)

        return vlan_ids

    def update(self, resource, timeout=-1):
        """
        Updates an Ethernet network.

        Args:
            resource: dict object to update
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns: Updated resource.

        """
        return self._client.update(resource, timeout=timeout, default_values=self.DEFAULT_VALUES)

    def get_by(self, field, value):
        """
        Gets all Ethernet networks that match the filter.
        The search is case-insensitive.

        Args:
            field: field name to filter
            value: value to filter

        Returns:
            list: A list of ethernet networks.
        """
        return self._client.get_by(field, value)

    def get_associated_profiles(self, id_or_uri):
        """
        Gets the URIs of profiles which are using an Ethernet network.

        Args:
            id_or_uri: Can be either the logical interconnect group id or the logical interconnect group uri

        Returns:
            list: URIs of the associated profiles.

        """
        uri = self._client.build_uri(id_or_uri) + "/associatedProfiles"
        return self._client.get(uri)

    def get_associated_uplink_groups(self, id_or_uri):
        """
        Gets the uplink sets which are using an Ethernet network.

        Args:
            id_or_uri: Can be either the logical interconnect group id or the logical interconnect group uri

        Returns:
            list: URIs of the associated uplink sets.

        """
        uri = self._client.build_uri(id_or_uri) + "/associatedUplinkGroups"
        return self._client.get(uri)

    def patch(self, id_or_uri, operation, path, value, timeout=-1):
        """
        Uses the PATCH to update the given resource.

        Only one operation can be performed in each PATCH call.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            operation: Patch operation
            path: Path
            value: Value
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated resource.
        """
        return self._client.patch(id_or_uri, operation, path, value, timeout=timeout)
