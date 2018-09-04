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
from hpOneView import HPOneViewValueError


class IdPoolsRanges(Resource):
    """
    Base class for Id Pools Ranges API client.

    Has common function used by: vMAC, vSN, vWWN
    """

    def __init__(self, type, connection, options=None):
        uri = ""
        if type == 'vmac':
            uri = '/rest/id-pools/vmac/ranges'
        elif type == 'vsn':
            uri = '/rest/id-pools/vsn/ranges'
        elif type == 'vwwn':
            uri = '/rest/id-pools/vwwn/ranges'
        else:
            raise HPOneViewValueError("Invalid type: {0}, types allowed: vmac, vsn, vwwn, ".format(type))

        self.URI = uri
        super(IdPoolsRanges, self).__init__(connection, options)

    @ensure_resource_client
    def enable(self, information, timeout=-1):
        """
        Enables or disables a range.

        Args:
            information (dict): Information to update.
            id_or_uri: ID or URI of range.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated resource.
        """

        return self.update(information, timeout=timeout)

    @ensure_resource_client
    def get_allocated_fragments(self, count=-1, start=0):
        """
        Gets all fragments that have been allocated in range.

        Args:
            count:
                 The number of resources to return. A count of -1 requests all items. The actual number of items in
                 the response may differ from the requested count if the sum of start and count exceed the total number
                 of items.
            start:
                The first item to return, using 0-based indexing. If not specified, the default is 0 - start with the
                first available item.

        Returns:
            list: A list with the allocated fragements.
        """
        path = "/allocated-fragments?start={0}&count={1}".format(start, count)
        return self.get_collection(path)

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
            dict: Allocator
        """
        uri = self.data['uri'] + "/allocator"

        return self.do_put(uri, information, timeout=timeout)

    @ensure_resource_client
    def collect(self, information, timeout=-1):
        """
        Collects a set of IDs back to range.

        The collector returned contains the list of IDs successfully collected.

        Args:
            information (dict):
                The list of IDs to be collected
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Collector containing list of collected IDs successfully collected.
        """
        uri = self.data['uri'] + "/collector"

        return self.do_put(uri, information, timeout=timeout)

    @ensure_resource_client
    def get_free_fragments(self, count=-1, start=0):
        """
        Gets all free fragments in a vSN range.

        Args:
            count:
                 The number of resources to return. A count of -1 requests all items. The actual number of items in
                 the response may differ from the requested count if the sum of start and count exceed the total number
                 of items.
            start:
                The first item to return, using 0-based indexing. If not specified, the default is 0 - start with the
                first available item.

        Returns:
            list: A list with the free fragments.
        """
        path = "/free-fragments?start={0}&count={1}".format(start, count)
        return self.get_collection(path)
