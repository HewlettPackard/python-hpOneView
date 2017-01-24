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


class Racks(object):
    """
    Racks API client.

    """
    URI = '/rest/racks'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', query='', sort=''):
        """
        Gets a set of rack resources according to the specified parameters. Filters can be used to get a specific set
        of racks. With no filters specified, the API returns a potentially paginated list of all the racks subject
        to start/count/sort parameters.

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
            list: List of racks.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort, query=query)

    def get(self, id_or_uri):
        """
        Gets a rack with the specified ID or URI.

        Args:
            id_or_uri:
                Can be either the rack id or the rack uri.

        Returns:
            dict: The rack.
        """
        return self._client.get(id_or_uri)

    def get_device_topology(self, id_or_uri):
        """
        Retrieves the topology information for the rack resource specified by ID or URI.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.

        Return:
            dict: Device topology.
        """
        uri = self._client.build_uri(id_or_uri) + "/deviceTopology"
        return self._client.get(uri)

    def get_by(self, field, value):
        """
        Gets all racks that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: List of racks.

        """
        return self._client.get_by(field, value)

    def remove(self, resource, force=False, timeout=-1):
        """
        Removes the specified rack.

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
        Adds a rack resource based upon the attributes specified. All attributes without default values must be
        specified in the POST body. The response contains the rack resource as added to the appliance with default and
        assigned properties expanded. The id and uri are assigned by the management appliance and are used to uniquely
        identify this particular resource.

        Args:
            information: Rack information
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Added rack.

        """
        return self._client.create(information, timeout=timeout)

    def update(self, resource, timeout=-1):
        """
        Updates the specified rack resource. The properties that are omitted (not included as part of the request body)
        are reset to their respective default values. The id and uuid properties are required and cannot be changed.
        To update existing racks first perform a get() request to retrieve the current properties, update the desired
        properties, and then update() the request body containing the new representation of the resource.

        Args:
            resource (dict): Object to update.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated rack.

        """
        return self._client.update(resource, timeout=timeout)
