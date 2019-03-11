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


from hpOneView.resources.resource import Resource, ensure_resource_client
from hpOneView.resources.networking.ethernet_networks import EthernetNetworks
from builtins import isinstance


class UplinkSets(Resource):
    """
    Uplink Sets API client.

    """
    URI = '/rest/uplink-sets'

    DEFAULT_VALUES = {
        '200': {"type": "uplink-setV3"},
        '300': {"type": "uplink-setV300"},
        '500': {"type": "uplink-setV300"},
        '600': {"type": "uplink-setV4"},
        '800': {"type": "uplink-setV4"}
    }

    def __init__(self, connection, data=None):
        super(UplinkSets, self).__init__(connection, data)
        self._ethernet_network = EthernetNetworks(connection)

    @ensure_resource_client
    def get_ethernet_networks(self):
        """
        Gets a list of associated ethernet networks of an uplink set.

        Args:
            id_or_uri: Can be either the uplink set id or the uplink set uri.

        Returns:
            list: Associated ethernet networks.
        """
        network_uris = self.data.get('networkUris')
        networks = []
        if network_uris:
            for uri in network_uris:
                networks.append(self._ethernet_network.get_by_uri(uri))
        return networks

    @ensure_resource_client
    def add_ethernet_networks(self, ethernet_id_or_uris):
        """
        Adds existing ethernet networks to an uplink set.

        Args:
            id_or_uri:
                Can be either the uplink set id or the uplink set uri.
            ethernet_id_or_uris:
                Could be either one or more ethernet network id or ethernet network uri.

        Returns:
            dict: The updated uplink set.
        """
        return self.__set_ethernet_uris(ethernet_id_or_uris, operation="add")

    @ensure_resource_client
    def remove_ethernet_networks(self, ethernet_id_or_uris):
        """
        Remove existing ethernet networks of an uplink set.

        Args:
            id_or_uri:
                Can be either the uplink set id or the uplink set uri.
            ethernet_id_or_uris:
                Could be either one or more ethernet network id or ethernet network uri.

        Returns:
            dict: The updated uplink set.
        """
        return self.__set_ethernet_uris(id_or_uri, ethernet_id_or_uris, operation="remove")

    def __set_ethernet_uris(self, ethernet_id_or_uris, operation="add"):
        if not isinstance(ethernet_id_or_uris, list):
            ethernet_id_or_uris = [ethernet_id_or_uris]

        associated_enets = self.data.get('networkUris', [])

        for i, enet in enumerate(ethernet_id_or_uris):
            ethernet_id_or_uris[i] = enet if '/' in enet else self._ethernet_network.URI + '/' + enet

        if operation == "remove":
            enets_to_update = sorted(list(set(associated_enets) - set(ethernet_id_or_uris)))
        elif operation == "add":
            enets_to_update = sorted(list(set(associated_enets).union(set(ethernet_id_or_uris))))
        else:
            raise ValueError("Value {} is not supported as operation. The supported values are: ['add', 'remove']")

        if set(enets_to_update) != set(associated_enets):
            updated_network = {'networkUris': enets_to_update}
            return self.update(updated_network)
        else:
            return uplink
