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


class StorageVolumeTemplates(object):
    """
    Storage Volume Templates API client.

    """
    URI = '/rest/storage-volume-templates'

    DEFAULT_VALUES = {
        '200': {"type": "StorageVolumeTemplateV3"},
        '300': {"type": "StorageVolumeTemplateV3"}
    }

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a list of storage volume templates.

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
            list: A list of storage volume templates.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def create(self, resource, timeout=-1):
        """
        Creates a new storage volume template.

        Args:
            resource (dict):
                Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Created storage volume template.
        """
        custom_headers = {'Accept-Language': 'en_US'}
        return self._client.create(resource, timeout=timeout, custom_headers=custom_headers,
                                   default_values=self.DEFAULT_VALUES)

    def get(self, id_or_uri):
        """
        Gets the specified storage volume template resource by ID or by URI.

        Args:
            id_or_uri: Can be either the storage volume template ID or the storage volume template URI.

        Returns:
            dict: The storage volume template
        """
        return self._client.get(id_or_uri)

    def get_connectable_volume_templates(self, start=0, count=-1, filter='', query='', sort=''):
        """
        Gets the storage volume templates that are available on the specified networks based on the storage system
        port's expected network connectivity. If there are no storage volume templates that meet the specified
        connectivity criteria, an empty collection will be returned.

        Returns:
            list: Storage volume templates.
        """
        uri = self.URI + "/connectable-volume-templates"

        get_uri = self._client.build_query_uri(start=start, count=count, filter=filter,
                                               query=query, sort=sort, uri=uri)
        return self._client.get(get_uri)

    def get_reachable_volume_templates(self, start=0, count=-1, filter='', query='', sort='',
                                       networks=None, scope_uris='', private_allowed_only=False):
        """
        Gets the storage templates that are connected on the specified networks based on the storage system
        port's expected network connectivity.

        Returns:
            list: Storage volume templates.
        """
        uri = self.URI + "/reachable-volume-templates"

        uri += "?networks={}&privateAllowedOnly={}".format(networks, private_allowed_only)

        get_uri = self._client.build_query_uri(start=start, count=count, filter=filter,
                                               query=query, sort=sort, uri=uri, scope_uris=scope_uris)
        return self._client.get(get_uri)

    def get_compatible_systems(self, id_or_uri):
        """
        Retrieves a collection of all storage systems that is applicable to this storage volume template.

        Args:
            id_or_uri:
                Can be either the power device id or the uri

        Returns:
            list: Storage systems.
        """
        uri = self._client.build_uri(id_or_uri) + "/compatible-systems"
        return self._client.get(uri)

    def delete(self, resource, force=False, timeout=-1):
        """
        Deletes the specified storage volume template.

        Args:
            resource (dict):
                Object to remove.
            force (bool):
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
        Returns:
            bool: Indicates if the resource was successfully deleted.
        """
        custom_headers = {'Accept-Language': 'en_US', 'If-Match': '*'}
        return self._client.delete(resource, force=force, timeout=timeout, custom_headers=custom_headers)

    def update(self, resource, timeout=-1):
        """
        Updates a storage volume template.

        Args:
            resource (dict):
                Object to update.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated storage volume system
        """
        custom_headers = {'Accept-Language': 'en_US'}
        return self._client.update(resource, timeout=timeout, custom_headers=custom_headers,
                                   default_values=self.DEFAULT_VALUES)

    def get_by(self, field, value):
        """
        Gets all storage volume templates that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of storage volume templates that match the filter.
        """
        return self._client.get_by(field, value)
