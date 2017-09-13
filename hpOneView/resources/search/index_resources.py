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

from hpOneView.resources.resource import ResourceClient
from urllib.parse import quote


class IndexResources(object):
    """
    Index Resources API client.

    """

    URI = '/rest/index/resources'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, category='', count=-1, fields='', filter='', padding=0, query='', reference_uri='',
                sort='', start=0, user_query='', view=''):
        """
        Gets a list of index resources based on optional sorting and filtering and is constrained by start
        and count parameters.

        Args:
            category (str or list):
                 Category of resources. Multiple Category parameters are applied with OR condition.
            count (int):
                The number of resources to return. A count of -1 requests all items.
                The actual number of items in the response might differ from the requested
                count if the sum of start and count exceeds the total number of items.
            fields (str):
                Specifies which fields should be returned in the result set.
            filter (list or str):
                A general filter/query string to narrow the list of items returned. The
                default is no filter; all resources are returned.
            padding (int):
                Number of resources to be returned before the reference URI resource.
            query (str):
                 A general query string to narrow the list of resources returned.
                 The default is no query - all resources are returned.
            reference_uri (str):
                Load one page of resources, pagination is applied with reference to referenceUri provided.
            sort (str):
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.
            start (int):
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            user_query (str):
                Free text Query string to search the resources. This will match the string in any field that is indexed.
            view (str):
                Return a specific subset of the attributes of the resource or collection, by specifying the name of a predefined view.

        Returns:
            list: A list of index resources.
        """
        uri = self.URI + '?'

        uri += self.__list_or_str_to_query(category, 'category')
        uri += self.__list_or_str_to_query(count, 'count')
        uri += self.__list_or_str_to_query(fields, 'fields')
        uri += self.__list_or_str_to_query(filter, 'filter')
        uri += self.__list_or_str_to_query(padding, 'padding')
        uri += self.__list_or_str_to_query(query, 'query')
        uri += self.__list_or_str_to_query(reference_uri, 'referenceUri')
        uri += self.__list_or_str_to_query(sort, 'sort')
        uri += self.__list_or_str_to_query(start, 'start')
        uri += self.__list_or_str_to_query(user_query, 'userQuery')
        uri += self.__list_or_str_to_query(view, 'view')

        uri = uri.replace('?&', '?')

        response = self._client.get(uri)

        if response and 'members' in response and response['members']:
            return response['members']
        else:
            return []

    def get(self, uri):
        """
        Gets an index resource by URI.

        Args:
            uri: The resource URI.

        Returns:
            dict: The index resource.
        """
        uri = self.URI + uri
        return self._client.get(uri)

    def get_aggregated(self, attribute, category, child_limit=6, filter='', query='', user_query=''):
        """
        Gets a list of index resources based on optional sorting and filtering and is constrained by start
        and count parameters.

        Args:
            attribute (list or str):
                Attribute to pass in as query filter.
            category (str):
                Category of resources. Multiple Category parameters are applied with an OR condition.
            child_limit (int):
                Number of resources to be retrieved. Default=6.
            filter (list or str):
                A general filter/query string to narrow the list of items returned. The
                default is no filter; all resources are returned.
            query (str):
                A general query string to narrow the list of resources returned.
                The default is no query - all resources are returned.
            user_query (str):
                Free text Query string to search the resources.
                This will match the string in any field that is indexed.

        Returns:
            list: An aggregated list of index resources.
        """
        uri = self.URI + '/aggregated?'

        # Add attribute to query
        uri += self.__list_or_str_to_query(attribute, 'attribute')
        uri += self.__list_or_str_to_query(category, 'category')
        uri += self.__list_or_str_to_query(child_limit, 'childLimit')
        uri += self.__list_or_str_to_query(filter, 'filter')
        uri += self.__list_or_str_to_query(query, 'query')
        uri += self.__list_or_str_to_query(user_query, 'userQuery')

        uri = uri.replace('?&', '?')

        return self._client.get(uri)

    def __list_or_str_to_query(self, list_or_str, field_name):
        formated_query = ''
        if list_or_str:
            if isinstance(list_or_str, list):
                for f in list_or_str:
                    formated_query = formated_query + "&{0}=".format(field_name) + ''.join(quote(str(f)))
            else:
                formated_query = "&{0}=".format(field_name) + str(list_or_str)
        return formated_query
