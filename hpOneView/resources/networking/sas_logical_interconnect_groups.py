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

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()


from hpOneView.resources.resource import Resource


class SasLogicalInterconnectGroups(Resource):
    """
    SAS Logical Interconnect Groups API client.

    Note:
        This resource is only available on HPE Synergy.

    """
    URI = '/rest/sas-logical-interconnect-groups'

    DEFAULT_VALUES = {
        '300': {'type': 'sas-logical-interconnect-group'},
        '500': {'type': 'sas-logical-interconnect-group'},
        '600': {'type': 'sas-logical-interconnect-groupV2'},
        '800': {'type': 'sas-logical-interconnect-groupV2'},
    }

    def __init__(self, connection, data=None):
        super(SasLogicalInterconnectGroups, self).__init__(connection, data)

    def get_all(self, start=0, count=-1, filter='', sort='', scope_uris='', query=''):
        """
        Gets a paginated collection of SAS logical interconnect groups. The collection is based
        on optional sorting and filtering and is constrained by start and count parameters.

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
            scope_uris:
                An expression to restrict the resources returned according to the scopes to
                which they are assigned.
            query (str):
                 A general query string to narrow the list of resources returned.
                 The default is no query - all resources are returned.

        Returns:
            list: A list of SAS logical interconnect groups.
        """
        return self._helper.get_all(start, count, filter=filter, sort=sort,
                                    scope_uris=scope_uris, query=query)
