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


class LogicalInterconnectGroups(object):
    """
    Logical Interconnect Groups API client.

    """
    URI = '/rest/logical-interconnect-groups'

    DEFAULT_VALUES = {
        '200': {"type": "logical-interconnect-groupV3"},
        '300': {"type": "logical-interconnect-groupV300"},
        '500': {"type": "logical-interconnect-groupV300"},
        '600': {"type": "logical-interconnect-groupV4"}
    }

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort='', scope_uris=''):
        """
        Gets a list of logical interconnect groups based on optional sorting and filtering and is constrained by start
        and count parameters.

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
            scope_uris:
                An expression to restrict the resources returned according to the scopes to
                which they are assigned.

        Returns:
            list: A list of logical interconnect groups.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort, scope_uris=scope_uris)

    def get(self, id_or_uri):
        """
        Gets a logical interconnect group by ID or by URI.

        Args:
            id_or_uri: Can be either the logical interconnect group id or the logical interconnect group uri.

        Returns:
            dict: The logical interconnect group.
        """
        return self._client.get(id_or_uri)

    def get_default_settings(self):
        """
        Gets the default interconnect settings for a logical interconnect group.

        Returns:
            dict: Interconnect Settings.
        """
        uri = self.URI + "/defaultSettings"
        return self._client.get(uri)

    def get_settings(self, id_or_uri):
        """
        Gets the interconnect settings for a logical interconnect group.

        Args:
            id_or_uri: Can be either the logical interconnect group id or the logical interconnect group uri.

        Returns:
            dict: Interconnect Settings.
        """
        uri = self._client.build_uri(id_or_uri) + "/settings"
        return self._client.get(uri)

    def create(self, resource, timeout=-1):
        """
        Creates a logical interconnect group.

        Args:
            resource (dict): Object to create
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Created logical interconnect group.

        """
        return self._client.create(resource, timeout=timeout, default_values=self.DEFAULT_VALUES)

    def update(self, resource, timeout=-1):
        """
        Updates a logical interconnect group.

        Args:
            resource (dict): Object to update
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated logical interconnect group.

        """
        return self._client.update(resource, timeout=timeout, default_values=self.DEFAULT_VALUES)

    def delete(self, resource, force=False, timeout=-1):
        """
        Deletes a logical interconnect group.

        Args:
            resource (dict): Object to delete.
            force (bool):
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates if the resource was successfully deleted.
        """
        return self._client.delete(resource, force=force, timeout=timeout)

    def get_by(self, field, value):
        """
        Gets all Logical interconnect groups that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of Logical interconnect groups.
        """
        return self._client.get_by(field, value)

    def patch(self, id_or_uri, operation, path, value, timeout=-1):
        """
        Uses the PATCH to update a resource for a given logical interconnect group.

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
