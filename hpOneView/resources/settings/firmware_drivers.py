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


class FirmwareDrivers(object):
    """
    Firmware Drivers API client.

    """
    URI = '/rest/firmware-drivers'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a paginated collection of Firmware Drivers. The collection is based on optional sorting and filtering, and
        constrained by start and count parameters.

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
            list: list of firmware baseline resources.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def get_by(self, field, value):
        """
        Gets the list of firmware baseline resources managed by the appliance. Optional parameters can be used to
        filter the list of resources returned.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: List of firmware baseline resources.
        """
        firmwares = self.get_all()
        matches = []
        for item in firmwares:
            if item.get(field) == value:
                matches.append(item)
        return matches

    def get(self, id_or_uri):
        """
        Gets the individual firmware baseline resource for the given URI.

        Args:
            id: ID or URI of firmware baseline resource.

        Returns:
            dict: Firmware baseline resource.
        """
        return self._client.get(id_or_uri)

    def create(self, resource, timeout=-1):
        """
        Creates a custom SPP (Service Pack for ProLiant) from an existing SPP and one or more hotfixes that have already
        been added to the system.

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
        Delete the firmware baseline resource with the specified ID. If force is set to true, the firmware baseline
        resource will be deleted even if it is assigned to devices.

        Args:
            resource (dict): Object to delete
            force: If set to true, the operation completes despite any problems with
                network connectivity or errors on the resource itself. The default is false.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates if the resource was successfully deleted.
        """
        return self._client.delete(resource, force=force, timeout=timeout)
