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


class EnclosureGroups(object):
    """
    Enclosure Groups API client.

    """
    URI = '/rest/enclosure-groups'

    DEFAULT_VALUES = {
        '200': {"type": "EnclosureGroupV200"},
        '300': {"type": "EnclosureGroupV300"},
        '500': {"type": "EnclosureGroupV400"}
    }

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort='', scope_uris=''):
        """
        Gets a list of enclosure groups.

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
            list: A list of enclosure groups.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort, scope_uris=scope_uris)

    def get(self, id_or_uri):
        """
        Gets an enclosure group by ID or by URI.

        Args:
            id_or_uri: Can be either the enclosure group ID or the enclosure group URI.

        Returns:
            dict: Enclosure group.
        """
        return self._client.get(id_or_uri)

    def get_script(self, id_or_uri):
        """
        Gets the configuration script of the enclosure-group resource with the specified URI.

        Returns:
            dict: Configuration script.
        """

        uri = self._client.build_uri(id_or_uri) + "/script"

        return self._client.get(uri)

    def get_by(self, field, value):
        """
        Gets all enclosure groups that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of enclosure groups.
        """
        return self._client.get_by(field, value)

    def create(self, resource, timeout=-1):
        """
        Creates an enclosure group. An interconnect bay mapping must be provided for each
        of the interconnect bays in the enclosure. For this release, the same logical
        interconnect group must be provided for each interconnect bay mapping.

        Args:
            resource (dict): Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Created enclosure group.
        """
        return self._client.create(resource, timeout=timeout, default_values=self.DEFAULT_VALUES)

    def delete(self, resource, timeout=-1):
        """
        Deletes an enclosure group. An enclosure group cannot be deleted if any enclosures
        are currently part of that enclosure group.

        Args:
            resource (dict): Object to delete.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates if the resource was successfully deleted.

        """
        return self._client.delete(resource, timeout=timeout)

    def update(self, resource, timeout=-1):
        """
        Updates an enclosure group with new attributes.

        Args:
            resource (dict): Object to update
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated enclosure group

        """
        return self._client.update(resource, timeout=timeout, default_values=self.DEFAULT_VALUES)

    def update_script(self, id_or_uri, script_body):
        """
        Updates the configuration script of the enclosure-group with the specified URI.

        Args:
            id_or_uri: Resource id or resource uri.
            script_body:  Configuration script.

        Returns:
            dict: Updated enclosure group.
        """
        uri = self._client.build_uri(id_or_uri) + "/script"

        return self._client.update(script_body, uri=uri)
