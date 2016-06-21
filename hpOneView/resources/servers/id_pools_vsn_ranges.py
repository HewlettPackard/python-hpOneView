# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
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

__title__ = 'id-pools-vsn-ranges'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP'
__license__ = 'MIT'
__status__ = 'Development'

from hpOneView.resources.resource import ResourceClient


class IdPoolsVsnRanges(object):
    URI = '/rest/id-pools/vsn/ranges'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def create(self, resource, timeout=-1):
        """
        Creates a vSN range.

        A range can be one of two types based upon the range category specified: Generated or Custom. The Generated
        range type automatically assigns start and end addresses to the range. The Custom range type requires a start
        address to be specified. The end address may also be specified but is optional.

        Args:
            resource (dict): Object to create
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.

        Returns:
            dict: Created id range
        """
        return self._client.create(resource, timeout=timeout)

    def get(self, id_or_uri):
        """
        Gets a vSN range.

        Using the allocator and collector associated with the range, IDs may be allocated from or collected back to the
        range.

        Args:
            id_or_uri: Could be either the vSN range id or uri

        Returns:
            dict: vSN range
        """
        return self._client.get(id_or_uri)

    def enable(self, information, id_or_uri=None, timeout=-1):
        """
        Enables or disables a vSN range.

        Args:
            information (dict): information to update.
            id_or_uri: id or uri of vSN range
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.

        Returns:
            dict: Updated resource

        """
        if id_or_uri:
            uri = self._client.build_uri(id_or_uri)

        return self._client.update(information, uri, timeout=timeout)

    def delete(self, resource, force=False, timeout=-1):
        """
        Deletes a vSN range.

        Args:
            resource (dict): object to delete
            force (bool):
                 If set to true the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.

        Returns:
            dict: Details of associated resource
        """
        return self._client.delete(resource, force=force, timeout=timeout)

    def get_allocated_fragments(self, resource, count=-1, start=0):
        """
        Gets all fragments that have been allocated in a vSN range.

        Args:
            resource: resource
            count: 
                 The number of resources to return. A count of -1 requests all the items. The actual number of items in
                 the response may differ from the requested count if the sum of start and count exceed the total number
                 of items, or if returning the requested number of items would take too long.
            start:
                The first item to return, using 0-based indexing. If not specified, the default is 0 - start with the
                first available item.

        Returns: the list of IDs

        """
        uri = resource[
            'uri'] + "/allocated-fragments?start={0}&count={1}".format(start, count)
        return self._client.get(uri)

    def allocate(self, information, id_or_uri=None, timeout=-1):
        """
        Allocates a set of IDs from a vSN range.

        The allocator returned contains the list of IDs successfully allocated.

        Args:
            information (dict):
                Information to update. Can result in system specified IDs or the system reserving user-specified IDs. 
            id_or_uri: id or uri of vSN range
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.

        Returns: (dict) allocator

        """
        if id_or_uri:
            uri = self._client.build_uri(id_or_uri) + "/allocator"

        return self._client.update(information, uri, timeout=timeout)

    def collect(self, information, id_or_uri=None, timeout=-1):
        """
        Collects a set of IDs back to a vSN range.

        The collector returned contains the list of IDs successfully collected.

        Args:
            information (dict):
                The list of IDs to be collected 
            id_or_uri: id or uri of vSN range
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.

        Returns:
            dict: collector containing list of collected IDs successfully collected. 

        """
        if id_or_uri:
            uri = self._client.build_uri(id_or_uri) + "/collector"

        return self._client.update(information, uri, timeout=timeout)

    def get_free_fragments(self, resource, count=-1, start=0):
        """
        Gets all the free fragments in a vSN range.

        Args:
            resource: resource
            count: 
                 The number of resources to return. A count of -1 requests all the items. The actual number of items in
                 the response may differ from the requested count if the sum of start and count exceed the total number
                 of items, or if returning the requested number of items would take too long.
            start:
                The first item to return, using 0-based indexing. If not specified, the default is 0 - start with the
                first available item.

        Returns: the list of IDs

        """
        uri = resource['uri'] + \
            "/free-fragments?start={0}&count={1}".format(start, count)
        return self._client.get(uri)
