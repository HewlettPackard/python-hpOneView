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


class StoragePools(object):
    """
    Storage Pools API client.

    """
    URI = '/rest/storage-pools'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a list of storage pools. Returns a list of storage pools based on optional sorting and filtering, and
        constrained by start and count parameters. The following storage pool attributes can be used with filtering and
        sorting operation: name, domain, deviceType, deviceSpeed, supportedRAIDLevel, status, and state.

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
            list: A list of storage pools.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def add(self, resource, timeout=-1):
        """
        Adds storage pool for management by the appliance.

        Args:
            resource (dict):
                Object to create
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Created storage pool.

        """
        return self._client.create(resource, timeout=timeout)

    def get(self, id_or_uri):
        """
        Gets the specified storage pool resource by ID or by URI.

        Args:
            id_or_uri: Can be either the storage pool id or the storage pool uri.

        Returns:
            dict: The storage pool.
        """
        return self._client.get(id_or_uri)

    def remove(self, resource, force=False, timeout=-1):
        """
        Removes an imported storage pool from OneView.

        Args:
            resource (dict):
                Object to remove.
            force (bool):
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Details of associated resource.

        """
        return self._client.delete(resource, force=force, timeout=timeout)

    def get_by(self, field, value):
        """
        Gets all storage pools that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of storage pools.
        """
        return self._client.get_by(field, value)

    def get_reachable_storage_pools(self, start=0, count=-1, filter='', query='', sort='', networks=[]):
        """
        Gets the storage pools that are connected on the specified networks
        based on the storage system port's expected network connectivity.

        Returns:
            list: Reachable Storage Pools List.
        """
        uri = self.URI + "/reachable-storage-pools"

        if networks:
            elements = "\'"
            for n in networks:
                elements += n + ','
            elements = elements[:-1] + "\'"
            uri = uri + "?networks=" + elements

        return self._client.get(self._client.build_query_uri(start=start, count=count, filter=filter, query=query,
                                                             sort=sort, uri=uri))

    def update(self, resource, timeout=-1):
        """
        Updates a storage pool.
        It can be used to manage/unmanage a storage pool, update attributes or to request a refresh.
        To manage or unmanage a storage pool: Set the isManaged attribute true to manage or false to unmanage.
        Attempting to unmanage a StoreVirtual pool is not allowed and the attempt will return a task error.
        To request a refresh set the "requestingRefresh" attribute to true. No other attribute update can be performed
        while also requesting a refresh of the pool.

        Args:
            resource (dict):
                Object to update.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated storage system.
        """
        return self._client.update(resource, timeout=timeout)
