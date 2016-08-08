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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

__title__ = 'server-profile-template'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP'
__license__ = 'MIT'
__status__ = 'Development'

from hpOneView.resources.resource import ResourceClient


class SanManagers(object):
    URI = '/rest/fc-sans/device-managers'
    PROVIDER_URI = '/rest/fc-sans/providers'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)
        self._provider_client = ResourceClient(con, self.PROVIDER_URI)

    def get_all(self, start=0, count=-1, query='', sort=''):
        """
        Retrieves the list of registered SAN Managers

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all the items. The actual number of items in
                the response may differ from the requested count if the sum of start and count exceed the total number
                of items, or if returning the requested number of items would take too long
            query:
                A general query string to narrow the list of resources returned.
                The default is no query - all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time, with the oldest entry first.

        Returns:
            list: A list of SAN managers

        """
        return self._client.get_all(start=start, count=count, query=query, sort=sort)

    def get(self, id_or_uri):
        """
        Retrieves a single registered SAN Manager by id or uri

        Args:
            id_or_uri: Could be either the SAN Manager resource id or uri.

        Returns:
            dict: The SAN Manager resource.
        """
        return self._client.get(id_or_uri=id_or_uri)

    def update(self, resource, id_or_uri):
        """
        Updates a registered Device Manager

        Args:
            id_or_uri: Could be either the Device manager id or uri.
            resource (dict): Object to update.

        Returns:
            dict: The device manager resource.
        """
        return self._client.update(resource=resource, uri=id_or_uri)

    def add(self, resource, provider_uri_or_id, timeout=-1):
        """
        Adds a Device Manager under the specified provider

        Args:
            resource: dict object to add
            provider_uri_or_id: id or uri of provider
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Added SAN Manager
        """
        uri = self._provider_client.build_uri(provider_uri_or_id) + "/device-managers"
        return self._client.create(resource=resource, uri=uri, timeout=timeout)

    def get_provider_uri(self, provider_name):
        """
        Gets uri for a specific provider

        Args:
            name: Name of the provider

        Returns:
            uri
        """
        return self._provider_client.get_by_name(provider_name)['uri']

    def get_default_connection_info(self, provider_name):
        """
        Gets default connection info for a specific provider

        Args:
            name: Name of the provider

        Returns:
            dict: default connection information
        """
        provider = self._provider_client.get_by_name(provider_name)
        if provider:
            return provider['defaultConnectionInfo']
        else:
            return {}
