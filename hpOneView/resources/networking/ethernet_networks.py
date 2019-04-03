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


from hpOneView.resources.resource import (Resource, ResourcePatchMixin,
                                          ensure_resource_client)


class EthernetNetworks(ResourcePatchMixin, Resource):
    """
    Ethernet Networks API client.

    """
    URI = '/rest/ethernet-networks'

    DEFAULT_VALUES = {
        '200': {"type": "ethernet-networkV3"},
        '300': {"type": "ethernet-networkV300"},
        '500': {"type": "ethernet-networkV300"},
        '600': {"type": "ethernet-networkV4"},
        '800': {"type": "ethernet-networkV4"}
    }
    BULK_DEFAULT_VALUES = {
        '200': {"type": "bulk-ethernet-network"},
        '300': {"type": "bulk-ethernet-network"},
        '500': {"type": "bulk-ethernet-network"},
        '600': {"type": "bulk-ethernet-networkV1"},
        '800': {"type": "bulk-ethernet-networkV1"},
    }

    def __init__(self, connection, data=None):
        super(EthernetNetworks, self).__init__(connection, data)

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
        default_values = self._get_default_values(self.BULK_DEFAULT_VALUES)
        updated_data = self._helper.update_resource_fields(resource, default_values)

        self._helper.create(updated_data, uri=uri, timeout=timeout)

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

    @ensure_resource_client
    def get_associated_profiles(self):
        """
        Gets the URIs of profiles which are using an Ethernet network.

        Args:
            id_or_uri: Can be either the logical interconnect group id or the logical interconnect group uri

        Returns:
            list: URIs of the associated profiles.

        """
        uri = "{}/associatedProfiles".format(self.data['uri'])
        return self._helper.do_get(uri)

    @ensure_resource_client
    def get_associated_uplink_groups(self):
        """
        Gets the uplink sets which are using an Ethernet network.

        Returns:
            list: URIs of the associated uplink sets.

        """
        uri = "{}/associatedUplinkGroups".format(self.data['uri'])
        return self._helper.do_get(uri)
