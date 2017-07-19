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


class ConnectionTemplates(object):
    """
    Connection Templates API client.

    """
    URI = '/rest/connection-templates'

    DEFAULT_VALUES = {
        '200': {"type": "connection-template"},
        '300': {"type": "connection-template"},
        '500': {"type": "connection-template"}
    }

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a paginated collection of all connection templates based on the specified
        parameters. Filters can be used in the URL to control the number of connection
        templates that are returned.

        With no filters specified, the API returns all connection templates.

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
            list: A list of connection templates.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def get(self, id_or_uri):
        """
        Gets the connection template with the specified ID or URI.

        Args:
            id_or_uri: ID or URI of connection template.

        Returns:
            dict: the connection template
        """
        return self._client.get(id_or_uri)

    def get_by(self, field, value):
        """
        Gets all connection templates that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of connection templates.
        """
        return self._client.get_by(field, value)

    def get_default(self):
        """
        Gets the default network connection template. This is the default connection template used
        for construction of networks. Its value is copied when a new connection template is made.

        Returns:
            dict:
        """
        uri = self.URI + "/defaultConnectionTemplate"
        return self._client.get(uri)

    def update(self, resource, timeout=-1):
        """
        Updates connection template.

        Args:
            resource (dict): Object to update.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        Returns:
            dict: Updated resource.
        """
        return self._client.update(resource, timeout=timeout, default_values=self.DEFAULT_VALUES)
