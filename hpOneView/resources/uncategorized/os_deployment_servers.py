# -*- coding: utf-8 -*-
###
# (C) Copyright (2017) Hewlett Packard Enterprise Development LP
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

from hpOneView.resources.resource import ResourceClient, extract_id_from_uri


class OsDeploymentServers(object):
    URI = '/rest/deployment-servers'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', fields='', query='', sort='', view=''):
        """
        Gets a list of Deployment Servers based on optional sorting and filtering, and constrained by start and count
        parameters.

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
            fields:
                Specifies which fields should be returned in the result set.
            query:
                 A general query string to narrow the list of resources returned. The default
                 is no query - all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.
            view:
                Return a specific subset of the attributes of the resource or collection, by
                specifying the name of a predefined view. The default view is expand - show all
                attributes of the resource and all elements of collections of resources.

        Returns:
             list: Os Deployment Servers
        """
        return self._client.get_all(start, count, filter=filter, sort=sort, query=query, fields=fields, view=view)

    def get(self, id_or_uri):
        """
        Get the details of the particular OS Deployment Server based on its URI or ID.

        Args:
            id_or_uri:
                Can be either the Os Deployment Server ID or the URI

        Returns:
            dict: Os Deployment Server
        """
        return self._client.get(id_or_uri)

    def get_by(self, field, value):
        """
        Gets all Os Deployment Servers that match the filter.
        The search is case-insensitive.

        Args:
            field: field name to filter
            value: value to filter

        Returns:
            list: Os Deployment Servers
        """
        return self._client.get_by(field, value)

    def get_by_name(self, name):
        """
        Gets the Os Deployment Server by name.

        Args:
            name: Name of the Os Deployment Server

        Returns:
            dict: Os Deployment Server
        """
        os_deployment_server = self.get_by('name', name) or [None]
        return os_deployment_server[0]

    def add(self, resource, timeout=-1):
        """
        Adds a Deployment Server using the information provided in the request body. Note: The type of the Deployment
        Server is always assigned as "Image streamer".

        Args:
            resource (dict):
                Deployment Manager resource.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: The added resource.
        """
        return self._client.create(resource, timeout=timeout)

    def update(self, resource, force=False, timeout=-1):
        """
        Updates the Deployment Server resource. The properties that are omitted (not included as part
        of the request body) are ignored.

        Args:
            resource (dict): Object to update.
            force:
                If set to true, the operation completes despite any problems with network connectivity or errors on
                the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.

        Returns:
            Updated resource.
        """
        return self._client.update(resource, timeout=timeout, force=force)

    def delete(self, resource, force=False, timeout=-1):
        """
        Deletes a Deployment Server object based on its UUID or URI.

        Args:
            resource (dict):
                Object to delete.
            force:
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates if the volume was successfully deleted.
        """

        return self._client.delete(resource, force=force, timeout=timeout)

    def get_networks(self):
        """
        Gets a list of all the One View networks.

        Returns:
             list: Networks
        """
        uri = self.URI + '/network'
        return self._client.get(uri)

    def get_appliances(self, start=0, count=-1, filter='', fields='', query='', sort='', view=''):
        """
        Gets a list of all the Image Streamer resources based on optional sorting and filtering, and constrained
        by start and count parameters.

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
            fields:
                Specifies which fields should be returned in the result set.
            query:
                 A general query string to narrow the list of resources returned. The default
                 is no query - all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.
            view:
                Return a specific subset of the attributes of the resource or collection, by
                specifying the name of a predefined view. The default view is expand - show all
                attributes of the resource and all elements of collections of resources.

        Returns:
             list: Image Streamer resources associated with the Deployment Servers.
        """
        uri = self.URI + '/image-streamer-appliances'
        return self._client.get_all(start, count, filter=filter, sort=sort, query=query, fields=fields, view=view,
                                    uri=uri)

    def get_appliance(self, id_or_uri, fields=''):
        """
        Gets the particular Image Streamer resource based on its ID or URI.

        Args:
            id_or_uri:
                Can be either the Os Deployment Server ID or the URI
            fields:
                Specifies which fields should be returned in the result.

        Returns:
             dict: Image Streamer resource.
        """
        uri = self.URI + '/image-streamer-appliances/' + extract_id_from_uri(id_or_uri)
        if fields:
            uri += '?fields=' + fields

        return self._client.get(uri)

    def get_appliance_by_name(self, appliance_name):
        """
        Gets the particular Image Streamer resource based on its name.

        Args:
            appliance_name:
                The Image Streamer resource name.

        Returns:
             dict: Image Streamer resource.
        """
        appliances = self.get_appliances()

        if appliances:
            for appliance in appliances:
                if appliance['name'] == appliance_name:
                    return appliance
        return None
