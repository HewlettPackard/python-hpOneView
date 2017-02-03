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


class IdPools(object):
    """
    Class for Id Pools API client.
    """
    URI = '/rest/id-pools'

    def __init__(self, con):
        self._client = ResourceClient(con, self.URI)

    def get(self, id_or_uri):
        """
        Gets a pool.

        Args:
            id_or_uri: Can be either the range ID or URI.

        Returns:
            dict: Pool resource.
        """
        return self._client.get(id_or_uri)

    def enable(self, information, id_or_uri, timeout=-1):
        """
        Enables or disables a pool.

        Args:
            information (dict): Information to update.
            id_or_uri: ID or URI of range.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated resource.
        """

        uri = self._client.build_uri(id_or_uri)
        return self._client.update(information, uri, timeout=timeout)

    def validate_id_pool(self, id_or_uri, ids_pools):
        """
        Validates an ID pool.

        Args:
            id_or_uri:
                ID or URI of range.
            ids_pools (list):
                List of Id Pools.

        Returns:
            dict: A dict containing a list with IDs.
        """
        uri = self._client.build_uri(id_or_uri) + "/validate?idList=" + "&idList=".join(ids_pools)
        return self._client.get(uri)

    def validate(self, information, id_or_uri, timeout=-1):
        """
        Validates a set of user specified IDs to reserve in the pool.

        This API can be used to check if the specified IDs can be allocated.

        Args:
            information (dict):
                Information to update. Can result in system specified IDs or the system reserving user-specified IDs.
            id_or_uri:
                ID or URI of vSN range.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: A dict containing a list with IDs.
        """
        uri = self._client.build_uri(id_or_uri) + "/validate"
        return self._client.update(information, uri, timeout=timeout)

    def allocate(self, information, id_or_uri, timeout=-1):
        """
        Allocates a set of IDs from range.

        The allocator returned contains the list of IDs successfully allocated.

        Args:
            information (dict):
                Information to update. Can result in system specified IDs or the system reserving user-specified IDs.
            id_or_uri:
                ID or URI of vSN range.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: A dict containing a list with IDs.
        """
        uri = self._client.build_uri(id_or_uri) + "/allocator"

        return self._client.update(information, uri, timeout=timeout)

    def collect(self, information, id_or_uri, timeout=-1):
        """
        Collects one or more IDs to be returned to a pool.

        Args:
            information (dict):
                The list of IDs to be collected
            id_or_uri:
                ID or URI of range
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Collector containing list of collected IDs successfully collected.
        """
        uri = self._client.build_uri(id_or_uri) + "/collector"

        return self._client.update(information, uri, timeout=timeout)

    def get_check_range_availability(self, id_or_uri, ids_pools):
        """
        Checks the range availability in the ID pool.

        Args:
            id_or_uri:
                ID or URI of range.
            ids_pools (list):
                List of Id Pools.

        Returns:
            dict: A dict containing a list with IDs.
        """

        uri = self._client.build_uri(id_or_uri) + "/checkrangeavailability?idList=" + "&idList=".join(ids_pools)
        return self._client.get(uri)

    def generate(self, id_or_uri):
        """
        Generates and returns a random range.

        Args:
            id_or_uri:
                ID or URI of range.

        Returns:
            dict: A dict containing a list with IDs.
        """
        uri = self._client.build_uri(id_or_uri) + "/generate"
        return self._client.get(uri)
