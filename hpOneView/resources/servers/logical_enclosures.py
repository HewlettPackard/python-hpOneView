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


class LogicalEnclosures(object):
    """
    The logical enclosure resource provides methods for managing one or more enclosures that are
    linked or stacked with stacking links.

    """
    URI = '/rest/logical-enclosures'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def create(self, resource, timeout=-1):
        """
        Creates a logical enclosure.

        Note:
            This method is only available on HPE Synergy.

        Args:
            resource (dict): Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Created resource.
        """
        return self._client.create(resource, timeout=timeout)

    def delete(self, resource, force=False, timeout=-1):
        """
        Deletes a logical enclosure.

        Note:
            This method is only available on HPE Synergy.

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

    def get_all(self, start=0, count=-1, filter='', sort='', scope_uris=''):
        """
        Returns a list of logical enclosures matching the specified filter. A maximum of 40 logical enclosures are
        returned to the caller. Additional calls can be made to retrieve any other logical enclosures matching the
        filter. Valid filter parameters include attributes of a Logical Enclosure resource.

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
            list: A list of logical enclosures.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort, scope_uris=scope_uris)

    def get_by(self, field, value):
        """
        Gets all logical enclosures that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of logical enclosures.
        """
        return self._client.get_by(field, value)

    def get_by_name(self, name):
        """
        Retrieves a resource by its name.

        Args:
            name: Resource name.

        Returns:
            dict: Logical enclosure.
        """
        return self._client.get_by_name(name=name)

    def get(self, id_or_uri):
        """
        Returns the logical enclosure, if it exists, with the specified ID.

        Args:
            id_or_uri: ID or URI of logical enclosure.

        Returns:
            dict: Logical enclosure.
        """
        return self._client.get(id_or_uri)

    def update(self, resource, timeout=-1):
        """
        Updates the given logical enclosure that is passed in. The fields that can be updated on the logical enclosure
        itself include name and configuration script. When the script is updated on the logical enclosure, the
        configuration script runs on all enclosures in the logical enclosure.

        Args:
            resource (dict): Object to update
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns: (dict) Updated logical enclosure.

        """
        return self._client.update(resource, timeout=timeout)

    def patch(self, id_or_uri, operation, path, value, timeout=-1, custom_headers=None):
        """
        Updates the given logical enclosure's attributes that are passed in the parameters. The PATCH operation
        partially updates the resource. The support operation in this context is the firmware update.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            operation: Patch operation
            path: Path
            value: Value
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
            custom_headers: Dictionary with custom headers.

        Returns:
            dict: Updated logical enclosure.
        """
        return self._client.patch(id_or_uri, operation, path, value, timeout=timeout,
                                  custom_headers=custom_headers)

    def update_configuration(self, id_or_uri, timeout=-1):
        """
        Reapplies the appliance's configuration on enclosures for the logical enclosure by ID or URI. This includes
        running the same configure steps that were performed as part of the enclosure add.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Logical enclosure.
        """
        uri = self._client.build_uri(id_or_uri) + "/configuration"
        return self._client.update_with_zero_body(uri, timeout=timeout)

    def get_script(self, id_or_uri):
        """
        Gets the configuration script of the logical enclosure by ID or URI.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.

        Return:
            str: Configuration script.
        """
        uri = self._client.build_uri(id_or_uri) + "/script"
        return self._client.get(uri)

    def update_script(self, id_or_uri, information, timeout=-1):
        """
        Updates the configuration script of the logical enclosure and on all enclosures in the logical enclosure with
        the specified ID.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            information: Updated script.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Return:
            Configuration script.
        """
        uri = self._client.build_uri(id_or_uri) + "/script"
        return self._client.update(information, uri=uri, timeout=timeout)

    def generate_support_dump(self, information, id_or_uri, timeout=-1):
        """
        Generates a support dump for the logical enclosure with the specified ID. A logical enclosure support dump
        includes content for logical interconnects associated with that logical enclosure. By default, it also contains
        appliance support dump content.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            information (dict): Information to generate support dump.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Support dump.
        """
        uri = self._client.build_uri(id_or_uri) + "/support-dumps"
        return self._client.create(information, uri=uri, timeout=timeout)

    def update_from_group(self, id_or_uri, timeout=-1):
        """
        Use this action to make a logical enclosure consistent with the enclosure group when the logical enclosure is
        in the Inconsistent state.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Logical enclosure.
        """
        uri = self._client.build_uri(id_or_uri) + "/updateFromGroup"
        return self._client.update_with_zero_body(uri=uri, timeout=timeout)
