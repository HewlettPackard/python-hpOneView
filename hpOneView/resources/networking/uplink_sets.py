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
from hpOneView.resources.networking.ethernet_networks import EthernetNetworks
from builtins import isinstance


class UplinkSets(object):
    """
    Uplink Sets API client.

    """
    URI = '/rest/uplink-sets'

    DEFAULT_VALUES = {
        '200': {"type": "uplink-setV3"},
        '300': {"type": "uplink-setV300"},
        '500': {"type": "uplink-setV300"},
        '600': {"type": "uplink-setV4"}
    }

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)
        self._ethernet_network = EthernetNetworks(con)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a paginated list of uplink sets based on optional sorting and filtering and is constrained by start and
        count parameters.

        Filters can be used in the URL to control the number of uplink sets that are returned.
        With no filters specified, the API returns all uplink sets.

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
            list: A list of uplink sets.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def get(self, id_or_uri):
        """
        Gets an uplink set with the specified ID.

        Args:
            id_or_uri: Can be either the uplink set id or the uplink set uri.

        Returns:
            dict: The uplink set.
        """
        return self._client.get(id_or_uri)

    def get_by(self, field, value):
        """
        Gets all uplink sets that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: Uplink sets

        """
        return self._client.get_by(field, value)

    def create(self, resource, timeout=-1):
        """
        Creates an uplink set.

        Args:
            resource (dict): Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        Returns:
            dict: Created resource.
        """
        return self._client.create(resource, timeout=timeout, default_values=self.DEFAULT_VALUES)

    def update(self, resource, timeout=-1):
        """
        Updates an uplink set.

        Args:
            resource (dict): Resource to update.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        Returns:
            dict: Updated resource.
        """
        return self._client.update(resource, timeout=timeout, default_values=self.DEFAULT_VALUES)

    def delete(self, resource, force=False, timeout=-1):
        """
        Deletes an uplink set. If the uplink set was carrying a Fibre Channel (FC) network, any connections which are
        deployed and using the FC network will be placed into a 'Failed' state.

        Args:
            resource: Resource to delete or the resource ID.
            force:
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

            Returns:
                bool: True if successfully deleted.
        """
        return self._client.delete(resource, force=force, timeout=timeout)

    def get_ethernet_networks(self, id_or_uri):
        """
        Gets a list of associated ethernet networks of an uplink set.

        Args:
            id_or_uri: Can be either the uplink set id or the uplink set uri.

        Returns:
            list: Associated ethernet networks.
        """
        uplink = self.get(id_or_uri)
        network_uris = uplink.get('networkUris')
        networks = []
        if network_uris:
            for uri in network_uris:
                networks.append(self._ethernet_network.get(uri))
        return networks

    def add_ethernet_networks(self, id_or_uri, ethernet_id_or_uris):
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
        return self.__set_ethernet_uris(id_or_uri, ethernet_id_or_uris, operation="add")

    def remove_ethernet_networks(self, id_or_uri, ethernet_id_or_uris):
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

    def __set_ethernet_uris(self, id_or_uri, ethernet_id_or_uris, operation="add"):
        if not isinstance(ethernet_id_or_uris, list):
            ethernet_id_or_uris = [ethernet_id_or_uris]

        uplink = self.get(id_or_uri)

        associated_enets = uplink.get('networkUris', [])

        for i, enet in enumerate(ethernet_id_or_uris):
            ethernet_id_or_uris[i] = enet if '/' in enet else self._ethernet_network.URI + '/' + enet

        if operation == "remove":
            enets_to_update = sorted(list(set(associated_enets) - set(ethernet_id_or_uris)))
        elif operation == "add":
            enets_to_update = sorted(list(set(associated_enets).union(set(ethernet_id_or_uris))))
        else:
            raise ValueError("Value {} is not supported as operation. The supported values are: ['add', 'remove']")

        if set(enets_to_update) != set(associated_enets):
            uplink['networkUris'] = enets_to_update
            return self.update(uplink)
        else:
            return uplink
