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


class SasLogicalInterconnectGroups(object):
    """
    SAS Logical Interconnect Groups API client.

    Note:
        This resource is only available on HPE Synergy.

    """
    URI = '/rest/sas-logical-interconnect-groups'

    DEFAULT_VALUES = {
        '300': {'type': 'sas-logical-interconnect-group'},
        '500': {'type': 'sas-logical-interconnect-group'},
        '600': {'type': 'sas-logical-interconnect-groupV2'},
    }

    def __init__(self, con):
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort='', scope_uris=''):
        """
        Gets a paginated collection of SAS logical interconnect groups. The collection is based
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
            scope_uris:
                An expression to restrict the resources returned according to the scopes to
                which they are assigned.


        Returns:
            list: A list of SAS logical interconnect groups.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort, scope_uris=scope_uris)

    def get(self, id_or_uri):
        """
        Gets the SAS logical interconnect group.

        Args:
            id_or_uri: ID or URI of a SAS logical interconnect group.

        Returns:
            dict: SAS logical interconnect group.
        """
        return self._client.get(id_or_uri)

    def get_by(self, field, value):
        """
        Gets all SAS logical interconnect groups that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of SAS logical interconnect groups.
        """
        return self._client.get_by(field, value)

    def create(self, resource, timeout=-1):
        """
        Creates a SAS logical interconnect group.

        Args:
            resource (dict): Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Created resource.

        """
        return self._client.create(resource, timeout=timeout, default_values=self.DEFAULT_VALUES)

    def update(self, resource, timeout=-1):
        """
        Updates a SAS logical interconnect group.

        Args:
            resource (dict): Object to update.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Updated resource.

        """
        return self._client.update(resource, timeout=timeout, default_values=self.DEFAULT_VALUES)

    def delete(self, resource, force=False, timeout=-1):
        """
        Removes a SAS logical interconnect group. You cannot delete a SAS logical interconnect group when a
        corresponding SAS logical interconnect is still referencing it. Delete the logical enclosure before
        attempting to delete the SAS logical interconnect it uses.

        Args:
            resource: object to delete
            force:
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates if the resource was deleted successfully.

        """
        return self._client.delete(resource, force=force, timeout=timeout)
