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


from hpOneView.resources.resource import ResourceClient


class SasInterconnects(object):
    """
    SAS Interconnects API client.

    Note:
        This resource is only available on HPE Synergy.

    """
    URI = '/rest/sas-interconnects'

    def __init__(self, con):
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, fields='', filter='', query='', sort='', view=''):
        """
        Get list of SAS interconnects each with port details.

        Args:
            start:
                 The first item to return, using 0-based indexing. If not specified, the default is 0 - start with the
                 first available item.
            count:
                The number of resources to return. A count of -1 requests all items. The actual number of items in
                the response may differ from the requested count if the sum of start and count exceeds the total number
                of items.
            fields:
                 Specifies which fields should be returned in the result set.
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
            list: A list of SAS interconnects.
        """
        return self._client.get_all(start=start, count=count, filter=filter, query=query, sort=sort, view=view,
                                    fields=fields)

    def get(self, id_or_uri):
        """
        Gets the SAS Interconnect with the specified ID or URI.

        Args:
            id_or_uri:
                Can be either the SAS interconnect id or the SAS interconnect uri

        Returns:
            dict: SAS Interconnect.
        """
        return self._client.get(id_or_uri)

    def get_by(self, field, value):
        """
        Gets all SAS Interconnects that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of SAS Interconnects.
        """
        return self._client.get_by(field, value)

    def patch(self, id_or_uri, operation, path, value, timeout=-1):
        """
        Update powerState, uidState, softResetState or hardResetState using PATCH operation

        Args:
            id_or_uri:
                Can be either the SAS interconnect id or the SAS interconnect uri
            operation:
                The type of operation: "replace" is the only value allowed for this resource.
            path:
                The JSON path the operation is to use. The exact meaning depends on the type of operation.
            value:
                The value to replace.

        Returns:
            dict: SAS Interconnect
        """
        return self._client.patch(id_or_uri=id_or_uri, operation=operation, path=path, value=value, timeout=timeout)

    def refresh_state(self, id_or_uri, configuration):
        """
        Refresh a SAS Interconnect.

        Args:
            id_or_uri:
                Can be either the SAS interconnect id or the SAS interconnect uri
            configuration: Configuration

        Returns:
            dict: SAS Interconnect
        """
        uri = self._client.build_uri(id_or_uri) + "/refreshState"
        return self._client.update(uri=uri, resource=configuration)
