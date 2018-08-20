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

from hpOneView.resources.resource import Resource, ensure_resource_client


class IdPools(Resource):
    """
    Class for Id Pools API client.
    """
    URI = '/rest/id-pools'

    def __init__(self, connection, options=None):
        super(IdPools, self).__init__(connection, options)

    def get_by_name(self, name):
        """
        Retrieve a id pool
        """
        uri = '{}/{}'.format(self.URI, name)
        self.data = self.do_get(uri)
        return self

    def get_by_uri(self, uri):
        """
        Retrieve a id pool
        """
        self.data = self.do_get(uri)
        return self

    def enable(self, information, timeout=-1):
        """
        Enables or disables a pool.

        Args:
            information (dict): Information to update.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated resource.
        """

        return self.update(information, timeout=timeout)

    @ensure_resource_client
    def validate_id_pool(self, ids_pools):
        """
        Validates an ID pool.

        Args:
            ids_pools (list):
                List of Id Pools.

        Returns:
            dict: A dict containing a list with IDs.
        """

        uri = self.data['uri'] + "/validate?idList=" + "&idList=".join(ids_pools)
        return self.do_get(uri)

    @ensure_resource_client
    def validate(self, information, timeout=-1):
        """
        Validates a set of user specified IDs to reserve in the pool.

        This API can be used to check if the specified IDs can be allocated.

        Args:
            information (dict):
                Information to update. Can result in system specified IDs or the system reserving user-specified IDs.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: A dict containing a list with IDs.
        """

        uri = '{}/validate'.format(self.data['uri'])
        return self.do_put(uri, information, timeout=timeout)

    @ensure_resource_client
    def allocate(self, information, timeout=-1):
        """
        Allocates a set of IDs from range.

        The allocator returned contains the list of IDs successfully allocated.

        Args:
            information (dict):
                Information to update. Can result in system specified IDs or the system reserving user-specified IDs.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: A dict containing a list with IDs.
        """

        uri = '{}/allocator'.format(self.data['uri'])
        return self.do_put(uri, information, timeout=timeout)

    @ensure_resource_client
    def collect(self, information, timeout=-1):
        """
        Collects one or more IDs to be returned to a pool.

        Args:
            information (dict):
                The list of IDs to be collected
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Collector containing list of collected IDs successfully collected.
        """

        uri = '{}/collector'.format(self.data['uri'])
        return self.do_put(uri, information, timeout=timeout)

    @ensure_resource_client
    def get_check_range_availability(self, ids_pools):
        """
        Checks the range availability in the ID pool.

        Args:
            ids_pools (list):
                List of Id Pools.

        Returns:
            dict: A dict containing a list with IDs.
        """

        uri = self.data['uri'] + "/checkrangeavailability?idList=" + "&idList=".join(ids_pools)
        return self.do_get(uri)

    @ensure_resource_client
    def generate(self):
        """
        Generates and returns a random range.

        Args:
            None

        Returns:
            dict: A dict containing a list with IDs.
        """

        uri = '{}/generate'.format(self.data['uri'])
        return self.do_get(uri)
