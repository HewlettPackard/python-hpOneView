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


class LogicalSwitches(object):
    """
    Logical Switches API client.

    Note:
        This resource is only available on C7000 enclosures.

    """
    URI = '/rest/logical-switches'

    SWITCH_DEFAULT_VALUES = {
        '200': {"type": "logical-switch"},
        '300': {"type": "logical-switchV300"},
        '500': {"type": "logical-switchV300"},
        '600': {"type": "logical-switchV4"}
    }

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a paginated collection of Logical Switches. The collection is based on optional
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
            list: A list of Logical Switches.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def delete(self, resource, force=False, timeout=-1):
        """
        Deletes a Logical Switch.

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
        Gets the Logical Switch with the specified ID.

        Args:
            id_or_uri: Can be either the Logical Switch ID or URI

        Returns:
            dict: Logical Switch.
        """
        return self._client.get(id_or_uri)

    def create(self, resource, timeout=-1):
        """
        Creates a Logical Switch.

        Args:
            resource (dict): Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Created resource.
        """
        self.__set_default_values(resource)
        return self._client.create(resource, timeout=timeout)

    def update(self, resource, timeout=-1):
        """
        Updates a Logical Switch.

        Args:
            resource (dict): Object to update.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Updated resource.
        """
        self.__set_default_values(resource)
        uri = self._client.build_uri(resource['logicalSwitch']['uri'])
        return self._client.update(resource, uri=uri, timeout=timeout)

    def get_by(self, field, value):
        """
        Gets all Logical Switches that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of Logical Switches.
        """
        return self._client.get_by(field, value)

    def refresh(self, id_or_uri, timeout=-1):
        """
        The Refresh action reclaims the top-of-rack switches in a logical switch.

        Args:
            id_or_uri:
                Can be either the Logical Switch ID or URI
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: The Logical Switch
        """
        uri = self._client.build_uri(id_or_uri) + "/refresh"
        return self._client.update_with_zero_body(uri, timeout=timeout)

    def patch(self, id_or_uri, operation, path, value, timeout=-1):
        """
        Uses the PATCH to update a resource for a given logical switch group.

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

    def __set_default_values(self, resource):
        if 'logicalSwitch' in resource:
            resource['logicalSwitch'] = self._client.merge_default_values(resource['logicalSwitch'],
                                                                          self.SWITCH_DEFAULT_VALUES)
