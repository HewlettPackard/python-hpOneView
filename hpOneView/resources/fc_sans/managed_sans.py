# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2019) Hewlett Packard Enterprise Development LP
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


from hpOneView.resources.resource import Resource, ensure_resource_client, unavailable_method


class ManagedSANs(Resource):
    """
    Managed SANs API client.

    """
    URI = '/rest/fc-sans/managed-sans'

    def __init__(self, connection, data=None):
        super(ManagedSANs, self).__init__(connection, data)

    def get_all(self, start=0, count=-1, query='', sort=''):
        """
        Retrieves the list of registered Managed SANs

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
            list: A list of Managed SANs
        """
        return self._helper.get_all(start=start, count=count, query=query, sort=sort)

    def get_by_name(self, name):
        """
        Gets a Managed SAN by name.

        Args:
            name: Name of the Managed SAN

        Returns:
            dict: Managed SAN.
        """
        managed_sans = self.get_all()
        result = [x for x in managed_sans if x['name'] == name]

        resource = result[0] if result else None
        if resource:
            resource = self.new(self._connection, resource)

        return resource

    def create(self):
        """Create method is not available"""
        unavailable_method()

    def delete(self):
        """Delete method is not available"""
        unavailable_method()

    @ensure_resource_client
    def get_endpoints(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a list of endpoints in a SAN.

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
            list: A list of endpoints.
        """
        uri = "{}/endpoints/".format(self.data["uri"])
        return self._helper.get_all(start, count, filter=filter, sort=sort, uri=uri)

    @ensure_resource_client
    def create_endpoints_csv_file(self, timeout=-1):
        """
        Creates an endpoints CSV file for a SAN.

        Args:
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        Returns:
            dict: Endpoint CSV File Response.
        """
        uri = "{}/endpoints/".format(self.data["uri"])
        return self._helper.do_post(uri, {}, timeout, None)

    @ensure_resource_client
    def create_issues_report(self, timeout=-1):
        """
        Creates an unexpected zoning report for a SAN.

        Args:
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        Returns:
            list: A list of FCIssueResponse dict.
        """
        uri = "{}/issues/".format(self.data["uri"])
        return self._helper.create_report(uri, timeout)

    def get_wwn(self, wwn):
        """
        Retrieves a list of associations between provided WWNs and the SANs (if any) on which they reside.

        Note:
            This method is available for API version 300 or later.

        Args:
            wwn (str): The WWN that may be associated with the SAN.

        Returns:
            list: Associations between provided WWNs and the SANs
        """
        uri = '/rest/fc-sans/managed-sans?locate=' + wwn
        return self._helper.do_get(uri)
