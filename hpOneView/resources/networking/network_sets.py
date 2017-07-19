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

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()


from hpOneView.resources.resource import ResourceClient


class NetworkSets(object):
    """
    Network Sets API client.

    """
    URI = '/rest/network-sets'

    DEFAULT_VALUES = {
        '200': {"type": "network-set"},
        '300': {"type": "network-setV300"},
        '500': {"type": "network-setV300"}
    }

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a paginated collection of network sets. The collection is based on optional
        sorting and filtering and is constrained by start and count parameters.

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
            list: A list of Network sets.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def delete(self, resource, force=False, timeout=-1):
        """
        Deletes a network set.

        Any deployed connections that are using the network are placed in the 'Failed' state.

        Args:
            resource: dict object to delete
            force:
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates if the resource was successfully deleted.
        """
        return self._client.delete(resource, force=force, timeout=timeout)

    def get(self, id_or_uri):
        """
        Gets the network set with the specified ID.

        Args:
            id_or_uri: ID or URI of network set.

        Returns:
            dict: Network set.
        """
        return self._client.get(id_or_uri)

    def create(self, resource, timeout=-1):
        """
        Creates a network set.

        Args:
            resource (dict): Object to create.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns: Created resource.
        """
        return self._client.create(resource, timeout=timeout, default_values=self.DEFAULT_VALUES)

    def update(self, resource, timeout=-1):
        """
        Updates a network set.

        Args:
            resource (dict): Object to update.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated resource.
        """
        return self._client.update(resource, timeout=timeout, default_values=self.DEFAULT_VALUES)

    def get_by(self, field, value):
        """
        Gets all network sets that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of Network sets.
        """
        return self._client.get_by(field, value)

    def get_all_without_ethernet(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a paginated collection of network sets without ethernet. The collection is based
        on optional sorting and filtering and is constrained by start and count parameters.

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
            list: List of network sets, excluding Ethernet networks.
        """
        without_ethernet_client = ResourceClient(
            self._connection, "/rest/network-sets/withoutEthernet")
        return without_ethernet_client.get_all(start, count, filter=filter, sort=sort)

    def get_without_ethernet(self, id_or_uri):
        """
        Gets the network set with the specified ID or URI without ethernet.

        Args:
            id_or_uri: Can be either the Network Set ID or URI.

        Returns:
            dict: Network set excluding Ethernet networks.
        """
        uri = self._client.build_uri(id_or_uri) + "/withoutEthernet"
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
