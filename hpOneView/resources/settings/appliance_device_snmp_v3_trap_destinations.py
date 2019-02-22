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


class ApplianceDeviceSNMPv3TrapDestinations(object):
    """
    ApplianceDeviceSNMPv3TrapDestinations API client.
    The appliance has the ability to forward events received from monitored or managed server hardware to the specified destinations as SNMPv3 traps.
    """
    URI = '/rest/appliance/snmpv3-trap-forwarding/destinations'

    def __init__(self, con):
        self._client = ResourceClient(con, self.URI)

    def create(self, resource, timeout=-1):
        """
        Adds the specified trap forwarding destination.
        The trap destination associated with the specified id will be created if trap destination with that id does not exists.
        The id can only be an integer greater than 0.

        Args:
            resource (dict): Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Created resource.

        """
        return self._client.create(resource, timeout=timeout)

    def get(self, id_or_uri):
        """
        Returns the SNMPv3 trap forwarding destination with the specified ID, if it exists.

        Args:
            id_or_uri: ID or URI of SNMPv3 trap destination.

        Returns:
            dict: Appliance SNMPv3 trap destination.
        """
        return self._client.get(id_or_uri)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Retrieves all SNMPv3 trap forwarding destinations.

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
            list: A list of SNMPv3 Trap Destionations.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def get_by(self, field, value):
        """
        Gets all SNMPv3 trap forwarding destinations that match the filter.
        The search is case-insensitive.

        Args:
            field: field name to filter
            value: value to filter

        Returns:
            list: A list of SNMPv3 Trap Destionations.
        """
        return self._client.get_by(field, value)

    def delete(self, id_or_uri, timeout=-1):
        """
        Deletes SNMPv3 trap forwarding destination based on {Id} only if no User is assigned to it.

        Args:
            id_or_uri: dict object to delete
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            bool: Indicates if the resource was successfully deleted.

        """
        return self._client.delete(id_or_uri, timeout=timeout)

    def update(self, resource, timeout=-1):
        """
        Updates SNMPv3 trap forwarding destination based on Id.

        Args:
            resource: dict object with changes.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Updated appliance SNMPv3 trap destinations.
        """
        return self._client.update(resource, timeout=timeout)
