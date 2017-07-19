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


from hpOneView.resources.resource import ResourceClient, extract_id_from_uri


class Alerts(object):
    URI = '/rest/alerts'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get(self, id_or_uri):
        """
        Retrieve an alert by its URI or ID.

        Args:
            id_or_uri: alert ID or URI.

        Returns:
            dict: The alert.

        """

        alert = self._client.get(id_or_uri)
        return alert

    def get_all(self, start=0, count=-1, filter='', query='', sort='', view=''):
        """
        Gets all the alerts based upon filters provided.

        Args:
            start:
                 The first item to return, using 0-based indexing. If not specified, the default is 0 - start with the
                 first available item.
            count:
                The number of resources to return. A count of -1 requests all items. The actual number of items in
                the response may differ from the requested count if the sum of start and count exceed the total number
                of items.
            filter (list or str):
                 A general filter/query string to narrow the list of items returned. The default is no filter; all
                 resources are returned.
            query:
                 A general query string to narrow the list of resources returned. The default is no query (all
                 resources are returned).
            sort:
                The sort order of the returned data set. By default, the sort order is based on create time, with the
                oldest entry first.
            view:
                 Returns a specific subset of the attributes of the resource or collection, by specifying the name of a
                 predefined view. The default view is expand (show all attributes of the resource and all elements of
                 collections of resources).

        Returns:
            list: A list of alerts.
        """
        return self._client.get_all(start=start, count=count, filter=filter, query=query, sort=sort, view=view)

    def get_by(self, field, value):
        """
        Gets all alerts that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: List of alerts.

        """
        return self._client.get_by(field, value)

    def delete(self, resource):
        """
        Deletes an alert.

        Args:
            resource: dict object to delete

        Returns:
            bool: Indicates if the resource was successfully deleted.

        """
        return self._client.delete(resource)

    def delete_all(self, filter, timeout=-1):
        """
        Deletes all Alert objects from the appliance that match the provided filter.

        Args:
            filter (list or str):
                 A general filter string to narrow the list of items to delete. The default is no filter; all
                 resources are deleted.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates whether the alerts were successfully deleted.
        """
        return self._client.delete_all(filter=filter, timeout=timeout)

    def update(self, resource, id_or_uri=None, timeout=-1):
        """
        Updates the specified alert resource.

        Args:
            resource (dict): Object to update.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated alert.
        """
        uri = resource.pop('uri', None)
        if not uri:
            if not id_or_uri:
                raise ValueError("URI was not provided")
            uri = self._client.build_uri(id_or_uri)
        return self._client.update(resource=resource, uri=uri, timeout=timeout)

    def delete_alert_change_log(self, id_or_uri):
        """
        Deletes alert change log by alert ID or URI.

        Args:
            id_or_uri: alert ID or URI.
        """
        uri = self.URI + "/AlertChangeLog/" + extract_id_from_uri(id_or_uri)
        resource = {
            "uri": uri
        }
        self._client.delete(resource)
