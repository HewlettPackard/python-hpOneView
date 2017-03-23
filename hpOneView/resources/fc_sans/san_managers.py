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


class SanManagers(object):
    """
    SAN Managers API client.

    """
    URI = '/rest/fc-sans/device-managers'
    PROVIDER_URI = '/rest/fc-sans/providers'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)
        self._provider_client = ResourceClient(con, self.PROVIDER_URI)

    def get_all(self, start=0, count=-1, query='', sort=''):
        """
        Retrieves the list of registered SAN Managers.

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all items. The actual number of items in
                the response may differ from the requested count if the sum of start and count exceed the total number
                of items.
            query:
                A general query string to narrow the list of resources returned.
                The default is no query - all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.

        Returns:
            list: A list of SAN managers.

        """
        return self._client.get_all(start=start, count=count, query=query, sort=sort)

    def get(self, id_or_uri):
        """
        Retrieves a single registered SAN Manager by ID or URI.

        Args:
            id_or_uri: Can be either the SAN Manager resource ID or URI.

        Returns:
            dict: The SAN Manager resource.
        """
        return self._client.get(id_or_uri=id_or_uri)

    def update(self, resource, id_or_uri):
        """
        Updates a registered Device Manager.

        Args:
            resource (dict): Object to update.
            id_or_uri: Can be either the Device manager ID or URI.

        Returns:
            dict: The device manager resource.
        """
        return self._client.update(resource=resource, uri=id_or_uri)

    def add(self, resource, provider_uri_or_id, timeout=-1):
        """
        Adds a Device Manager under the specified provider.

        Args:
            resource (dict): Object to add.
            provider_uri_or_id: ID or URI of provider.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Added SAN Manager.
        """
        uri = self._provider_client.build_uri(provider_uri_or_id) + "/device-managers"
        return self._client.create(resource=resource, uri=uri, timeout=timeout)

    def get_provider_uri(self, provider_display_name):
        """
        Gets uri for a specific provider.

        Args:
            provider_display_name: Display name of the provider.

        Returns:
            uri
        """
        providers = self._provider_client.get_by('displayName', provider_display_name)
        return providers[0]['uri'] if providers else None

    def get_default_connection_info(self, provider_name):
        """
        Gets default connection info for a specific provider.

        Args:
            provider_name: Name of the provider.

        Returns:
            dict: Default connection information.
        """
        provider = self._provider_client.get_by_name(provider_name)
        if provider:
            return provider['defaultConnectionInfo']
        else:
            return {}

    def remove(self, resource, timeout=-1):
        """
        Removes a registered SAN Manager.

        Args:
            resource (dict): Object to delete.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates if the resource was successfully removed.
        """
        return self._client.delete(resource, timeout=timeout)

    def get_by_name(self, name):
        """
        Gets a SAN Manager by name.

        Args:
            name: Name of the SAN Manager

        Returns:
            dict: SAN Manager.
        """
        san_managers = self._client.get_all()
        result = [x for x in san_managers if x['name'] == name]
        return result[0] if result else None

    def get_by_provider_display_name(self, provider_display_name):
        """
        Gets a SAN Manager by provider display name.

        Args:
            provider_display_name: Name of the Provider Display Name

        Returns:
            dict: SAN Manager.
        """
        san_managers = self._client.get_all()
        result = [x for x in san_managers if x['providerDisplayName'] == provider_display_name]
        return result[0] if result else None
