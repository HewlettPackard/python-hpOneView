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


class Datacenters(object):
    """
    Datacenters API client.

    """
    URI = '/rest/datacenters'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', query='', sort=''):
        """
        Gets a set of data center resources according to the specified parameters. Filters can be used to get a specific
        set of data centers.

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
            query:
                 A general query string to narrow the list of resources returned. The default
                 is no query - all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.

        Returns:
            list: List of data centers.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort, query=query)

    def get(self, id_or_uri):
        """
        Gets a single data center resource based upon its ID or URI.

        Args:
            id_or_uri:
                Can be either the data center id or the data center uri.

        Returns:
            dict: The data center.
        """
        return self._client.get(id_or_uri)

    def get_visual_content(self, id_or_uri):
        """
        Gets a list of visual content objects describing each rack within the data center. The response aggregates data
        center and rack data with a specified metric (peak24HourTemp) to provide simplified access to display data for
        the data center.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.

        Return:
            list: List of visual content objects.
        """
        uri = self._client.build_uri(id_or_uri) + "/visualContent"
        return self._client.get(uri)

    def get_by(self, field, value):
        """
        Gets all data centers that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: List of data centers.

        """
        return self._client.get_by(field, value)

    def remove(self, resource, force=False, timeout=-1):
        """
        Deletes the resource specified.

        Args:
            resource (dict): Object to remove.
            force:
                 If set to true, the operation completes despite any problems with network connectivity or errors on the
                 resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns: Result status.
        """
        return self._client.delete(resource, force=force, timeout=timeout)

    def add(self, information, timeout=-1):
        """
        Adds a data center resource based upon the attributes specified.

        Args:
            information: Data center information
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Added data center.
        """
        return self._client.create(information, timeout=timeout)

    def update(self, resource, timeout=-1):
        """
        Updates the specified data center resource.

        Args:
            resource (dict): Object to update.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated data center.
        """
        return self._client.update(resource, timeout=timeout)

    def remove_all(self, filter, force=False, timeout=-1):
        """
        Deletes the set of datacenters according to the specified parameters. A filter is required to identify the set
        of resources to be deleted.

        Args:
            filter:
                 A general filter/query string to narrow the list of items that will be removed.
            force:
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                 Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                 in OneView; it just stops waiting for its completion.

        Returns:
             bool: operation success
        """
        return self._client.delete_all(filter=filter, force=force, timeout=timeout)
