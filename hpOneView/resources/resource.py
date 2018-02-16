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
from future.utils import lmap

standard_library.install_aliases()

import logging
import os

from urllib.parse import quote
from hpOneView.resources.task_monitor import TaskMonitor
from hpOneView.exceptions import HPOneViewUnknownType, HPOneViewException
from hpOneView.exceptions import HPOneViewValueError

RESOURCE_CLIENT_RESOURCE_WAS_NOT_PROVIDED = 'Resource was not provided'
RESOURCE_CLIENT_INVALID_FIELD = 'Invalid field was provided'
RESOURCE_CLIENT_INVALID_ID = 'Invalid id was provided'
RESOURCE_CLIENT_UNKNOWN_OBJECT_TYPE = 'Unknown object type'
UNRECOGNIZED_URI = 'Unrecognized URI for this resource'
RESOURCE_CLIENT_TASK_EXPECTED = "Failed: Expected a TaskResponse."
RESOURCE_ID_OR_URI_REQUIRED = 'It is required to inform the Resource ID or URI.'


logger = logging.getLogger(__name__)


def merge_resources(resource1, resource2):
    """
    Updates a copy of resource1 with resource2 values and returns the merged dictionary.

    Args:
        resource1: original resource
        resource2: resource to update resource1

    Returns:
        dict: merged resource
    """
    merged = resource1.copy()
    merged.update(resource2)
    return merged


def merge_default_values(resource_list, default_values):
    """
    Generate a new list where each item of original resource_list will be merged with the default_values.

    Args:
        resource_list: list with items to be merged
        default_values: properties to be merged with each item list. If the item already contains some property
            the original value will be maintained.

    Returns:
        list: list containing each item merged with default_values
    """

    def merge_item(resource):
        return merge_resources(default_values, resource)

    return lmap(merge_item, resource_list)


class ResourceClient(object):
    """
    This class implements common functions for HpOneView API rest
    """

    def __init__(self, con, uri):
        self._connection = con
        self._uri = uri
        self._task_monitor = TaskMonitor(con)

    def build_query_uri(self, start=0, count=-1, filter='', query='', sort='', view='', fields='', uri=None, scope_uris=''):
        """
        Builds the URI given the parameters.

        More than one request can be send to get the items, regardless the query parameter 'count', because the actual
        number of items in the response might differ from the requested count. Some types of resource have a limited
        number of items returned on each call. For those resources, additional calls are made to the API to retrieve
        any other items matching the given filter. The actual number of items can also differ from the requested call
        if the requested number of items would take too long.

        The use of optional parameters for OneView 2.0 is described at:
        http://h17007.www1.hpe.com/docs/enterprise/servers/oneview2.0/cic-api/en/api-docs/current/index.html

        Note:
            Single quote - "'" - inside a query parameter is not supported by OneView API.

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all items (default).
            filter (list or str):
                A general filter/query string to narrow the list of items returned. The default is no
                filter; all resources are returned.
            query:
                A single query parameter can do what would take multiple parameters or multiple GET requests using
                filter. Use query for more complex queries. NOTE: This parameter is experimental for OneView 2.0.
            sort:
                The sort order of the returned data set. By default, the sort order is based on create time with the
                oldest entry first.
            view:
                Returns a specific subset of the attributes of the resource or collection by specifying the name of a
                predefined view. The default view is expand (show all attributes of the resource and all elements of
                the collections or resources).
            fields:
                Name of the fields.
            uri:
                A specific URI (optional)
            scope_uris:
                An expression to restrict the resources returned according to the scopes to
                which they are assigned.

        Returns:
            uri: The complete uri
        """

        if filter:
            filter = self.__make_query_filter(filter)

        if query:
            query = "&query=" + quote(query)

        if sort:
            sort = "&sort=" + quote(sort)

        if view:
            view = "&view=" + quote(view)

        if fields:
            fields = "&fields=" + quote(fields)

        if scope_uris:
            scope_uris = "&scopeUris=" + quote(scope_uris)

        path = uri if uri else self._uri
        self.__validate_resource_uri(path)

        symbol = '?' if '?' not in path else '&'

        uri = "{0}{1}start={2}&count={3}{4}{5}{6}{7}{8}{9}".format(path, symbol, start, count, filter, query, sort,
                                                                   view, fields, scope_uris)

        return uri

    def get_all(self, start=0, count=-1, filter='', query='', sort='', view='', fields='', uri=None, scope_uris=''):
        """
        Gets all items according with the given arguments.

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all items (default).
            filter (list or str):
                A general filter/query string to narrow the list of items returned. The default is no
                filter; all resources are returned.
            query:
                A single query parameter can do what would take multiple parameters or multiple GET requests using
                filter. Use query for more complex queries. NOTE: This parameter is experimental for OneView 2.0.
            sort:
                The sort order of the returned data set. By default, the sort order is based on create time with the
                oldest entry first.
            view:
                Returns a specific subset of the attributes of the resource or collection by specifying the name of a
                predefined view. The default view is expand (show all attributes of the resource and all elements of
                the collections or resources).
            fields:
                Name of the fields.
            uri:
                A specific URI (optional)
            scope_uris:
                An expression to restrict the resources returned according to the scopes to
                which they are assigned.

        Returns:
            list: A list of items matching the specified filter.
        """

        uri = self.build_query_uri(start=start, count=count, filter=filter,
                                   query=query, sort=sort, view=view, fields=fields, uri=uri, scope_uris=scope_uris)

        logger.debug('Getting all resources with uri: {0}'.format(uri))

        result = self.__do_requests_to_getall(uri, count)

        return result

    def delete_all(self, filter, force=False, timeout=-1):
        """
        Deletes all resources from the appliance that match the provided filter.

        Args:
            filter:
                A general filter/query string to narrow the list of items deleted.
            force:
                If set to true, the operation completes despite any problems with network connectivity or errors
                on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates if the resources were successfully deleted.
        """
        uri = "{}?filter={}&force={}".format(self._uri, quote(filter), force)
        logger.debug("Delete all resources (uri = %s)" % uri)

        task, body = self._connection.delete(uri)

        if not task:
            # 204 NO CONTENT
            # Successful return from a synchronous delete operation.
            return True

        return self._task_monitor.wait_for_task(task, timeout=timeout)

    def delete(self, resource, force=False, timeout=-1, custom_headers=None):

        if not resource:
            logger.exception(RESOURCE_CLIENT_RESOURCE_WAS_NOT_PROVIDED)
            raise ValueError(RESOURCE_CLIENT_RESOURCE_WAS_NOT_PROVIDED)

        if isinstance(resource, dict):
            if 'uri' in resource and resource['uri']:
                uri = resource['uri']
            else:
                logger.exception(RESOURCE_CLIENT_UNKNOWN_OBJECT_TYPE)
                raise HPOneViewUnknownType(RESOURCE_CLIENT_UNKNOWN_OBJECT_TYPE)
        else:
            uri = self.build_uri(resource)

        if force:
            uri += '?force=True'

        logger.debug("Delete resource (uri = %s, resource = %s)" %
                     (self._uri, str(resource)))

        task, body = self._connection.delete(uri, custom_headers=custom_headers)

        if not task:
            # 204 NO CONTENT
            # Successful return from a synchronous delete operation.
            return True

        task = self._task_monitor.wait_for_task(task, timeout=timeout)

        return task

    def get_schema(self):
        logger.debug('Get schema (uri = %s, resource = %s)' %
                     (self._uri, self._uri))
        return self._connection.get(self._uri + '/schema')

    def get(self, id_or_uri):
        """
        Args:
            id_or_uri: Can be either the resource ID or the resource URI.

        Returns:
             The requested resource.
        """
        uri = self.build_uri(id_or_uri)
        logger.debug('Get resource (uri = %s, ID = %s)' %
                     (uri, str(id_or_uri)))
        return self._connection.get(uri)

    def get_collection(self, id_or_uri, filter=''):
        """
        Retrieves a collection of resources.

        Use this function when the 'start' and 'count' parameters are not allowed in the GET call.
        Otherwise, use get_all instead.

        Optional filtering criteria may be specified.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            filter (list or str): General filter/query string.

        Returns:
             Collection of the requested resource.
        """
        if filter:
            filter = self.__make_query_filter(filter)
            filter = "?" + filter[1:]

        uri = "{uri}{filter}".format(uri=self.build_uri(id_or_uri), filter=filter)
        logger.debug('Get resource collection (uri = %s)' % uri)
        response = self._connection.get(uri)
        return self.__get_members(response)

    def update_with_zero_body(self, uri, timeout=-1, custom_headers=None):
        """
        Makes a PUT request to update a resource when no request body is required.

        Args:
            uri:
                Can be either the resource ID or the resource URI.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
            custom_headers:
                Allows set specific HTTP headers.

        Returns:
            Updated resource.
        """
        logger.debug('Update with zero length body (uri = %s)' % uri)

        return self.__do_put(uri, None, timeout, custom_headers)

    def update(self, resource, uri=None, force=False, timeout=-1, custom_headers=None, default_values={}):
        """
        Makes a PUT request to update a resource when a request body is required.

        Args:
            resource:
                OneView resource dictionary.
            uri:
                Can be either the resource ID or the resource URI.
            force:
                If set to true, the operation completes despite any problems with network connectivity or errors
                on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
            custom_headers:
                Allows set specific HTTP headers.
            default_values:
                Dictionary with default values grouped by OneView API version. This dictionary will be be merged with
                the resource dictionary only if the dictionary does not contain the keys.
                This argument is optional and the default value is an empty dictionary.
                Ex.:
                    default_values = {
                        '200': {"type": "logical-switch-group"},
                        '300': {"type": "logical-switch-groupV300"}
                    }

        Returns:
            Updated resource.
        """
        if not resource:
            logger.exception(RESOURCE_CLIENT_RESOURCE_WAS_NOT_PROVIDED)
            raise ValueError(RESOURCE_CLIENT_RESOURCE_WAS_NOT_PROVIDED)

        logger.debug('Update async (uri = %s, resource = %s)' %
                     (self._uri, str(resource)))

        if not uri:
            uri = resource['uri']

        if force:
            uri += '?force=True'

        resource = self.merge_default_values(resource, default_values)

        return self.__do_put(uri, resource, timeout, custom_headers)

    def create_with_zero_body(self, uri=None, timeout=-1, custom_headers=None):
        """
        Makes a POST request to create a resource when no request body is required.

        Args:
            uri:
                Can be either the resource ID or the resource URI.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
            custom_headers:
                Allows set specific HTTP headers.

        Returns:
            Created resource.
        """
        if not uri:
            uri = self._uri

        logger.debug('Create with zero body (uri = %s)' % uri)

        return self.__do_post(uri, {}, timeout, custom_headers)

    def create(self, resource, uri=None, timeout=-1, custom_headers=None, default_values={}):
        """
        Makes a POST request to create a resource when a request body is required.

        Args:
            resource:
                OneView resource dictionary.
            uri:
                Can be either the resource ID or the resource URI.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
            custom_headers:
                Allows set specific HTTP headers.
            default_values:
                Dictionary with default values grouped by OneView API version. This dictionary will be be merged with
                the resource dictionary only if the dictionary does not contain the keys.
                This argument is optional and the default value is an empty dictionary.
                Ex.:
                    default_values = {
                        '200': {"type": "logical-switch-group"},
                        '300': {"type": "logical-switch-groupV300"}
                    }

        Returns:
            Created resource.
        """
        if not resource:
            logger.exception(RESOURCE_CLIENT_RESOURCE_WAS_NOT_PROVIDED)
            raise ValueError(RESOURCE_CLIENT_RESOURCE_WAS_NOT_PROVIDED)

        if not uri:
            uri = self._uri

        logger.debug('Create (uri = %s, resource = %s)' %
                     (uri, str(resource)))

        resource = self.merge_default_values(resource, default_values)

        return self.__do_post(uri, resource, timeout, custom_headers)

    def upload(self, file_path, uri=None, timeout=-1):
        """
        Makes a multipart request.

        Args:
            file_path:
                File to upload.
            uri:
                A specific URI (optional).
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Response body.
        """
        if not uri:
            uri = self._uri

        upload_file_name = os.path.basename(file_path)
        task, entity = self._connection.post_multipart_with_response_handling(uri, file_path, upload_file_name)

        if not task:
            return entity

        return self._task_monitor.wait_for_task(task, timeout)

    def patch(self, id_or_uri, operation, path, value, timeout=-1, custom_headers=None):
        """
        Uses the PATCH to update a resource.

        Only one operation can be performed in each PATCH call.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            operation: Patch operation
            path: Path
            value: Value
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            Updated resource.
        """
        patch_request_body = [{'op': operation, 'path': path, 'value': value}]

        return self.patch_request(id_or_uri=id_or_uri,
                                  body=patch_request_body,
                                  timeout=timeout,
                                  custom_headers=custom_headers)

    def patch_request(self, id_or_uri, body, timeout=-1, custom_headers=None):
        """
        Uses the PATCH to update a resource.

        Only one operation can be performed in each PATCH call.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            body: Patch request body
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            Updated resource.
        """
        uri = self.build_uri(id_or_uri)

        logger.debug('Patch resource (uri = %s, data = %s)' % (uri, body))

        custom_headers_copy = custom_headers.copy() if custom_headers else {}
        if self._connection._apiVersion >= 300 and 'Content-Type' not in custom_headers_copy:
            custom_headers_copy['Content-Type'] = 'application/json-patch+json'

        task, entity = self._connection.patch(uri, body, custom_headers=custom_headers_copy)

        if not task:
            return entity

        return self._task_monitor.wait_for_task(task, timeout)

    def get_by(self, field, value, uri=None):
        """
        This function uses get_all passing a filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.
            uri: Resource uri.

        Returns:
            dict
        """
        if not field:
            logger.exception(RESOURCE_CLIENT_INVALID_FIELD)
            raise ValueError(RESOURCE_CLIENT_INVALID_FIELD)

        if not uri:
            uri = self._uri
        self.__validate_resource_uri(uri)

        logger.debug('Get by (uri = %s, field = %s, value = %s)' %
                     (uri, field, str(value)))

        filter = "\"{0}='{1}'\"".format(field, value)
        results = self.get_all(filter=filter, uri=uri)

        # Workaround when the OneView filter does not work, it will filter again
        if "." not in field:
            # This filter only work for the first level
            results = [item for item in results if str(item.get(field, '')).lower() == value.lower()]

        return results

    def get_by_name(self, name):
        """
        Retrieve a resource by its name.

        Args:
            name: Resource name.

        Returns:
            dict
        """
        result = self.get_by('name', name)
        if not result:
            return None
        else:
            return result[0]

    def get_utilization(self, id_or_uri, fields=None, filter=None, refresh=False, view=None):
        """
        Retrieves historical utilization data for the specified resource, metrics, and time span.

        Args:
            id_or_uri:
                Resource identification
            fields:
                Name of the supported metric(s) to be retrieved in the format METRIC[,METRIC]...
                If unspecified, all metrics supported are returned.

            filter (list or str):
                Filters should be in the format FILTER_NAME=VALUE[,FILTER_NAME=VALUE]...
                E.g.: 'startDate=2016-05-30T11:20:44.541Z,endDate=2016-05-30T19:20:44.541Z'

                startDate
                    Start date of requested starting time range in ISO 8601 format. If omitted, the startDate is
                    determined by the endDate minus 24 hours.
                endDate
                    End date of requested starting time range in ISO 8601 format. When omitted, the endDate includes
                    the latest data sample available.

                If an excessive number of samples would otherwise be returned, the results will be segmented. The
                caller is responsible for comparing the returned sliceStartTime with the requested startTime in the
                response. If the sliceStartTime is greater than the oldestSampleTime and the requested start time,
                the caller is responsible for repeating the request with endTime set to sliceStartTime to obtain the
                next segment. This process is repeated until the full data set is retrieved.

                If the resource has no data, the UtilizationData is still returned but will contain no samples and
                sliceStartTime/sliceEndTime will be equal. oldestSampleTime/newestSampleTime will still be set
                appropriately (null if no data is available). If the filter does not happen to overlap the data
                that a resource has, then the metric history service will return null sample values for any
                missing samples.

            refresh:
                Specifies that if necessary, an additional request will be queued to obtain the most recent
                utilization data from the iLO. The response will not include any refreshed data. To track the
                availability of the newly collected data, monitor the TaskResource identified by the refreshTaskUri
                property in the response. If null, no refresh was queued.

            view:
                Specifies the resolution interval length of the samples to be retrieved. This is reflected in the
                resolution in the returned response. Utilization data is automatically purged to stay within storage
                space constraints. Supported views are listed below:

                native
                    Resolution of the samples returned will be one sample for each 5-minute time period. This is the
                    default view and matches the resolution of the data returned by the iLO. Samples at this resolution
                    are retained up to one year.
                hour
                    Resolution of the samples returned will be one sample for each 60-minute time period. Samples are
                    calculated by averaging the available 5-minute data samples that occurred within the hour, except
                    for PeakPower which is calculated by reporting the peak observed 5-minute sample value data during
                    the hour. Samples at this resolution are retained up to three years.
                day
                    Resolution of the samples returned will be one sample for each 24-hour time period. One day is a
                    24-hour period that starts at midnight GMT regardless of the time zone in which the appliance or
                    client is located. Samples are calculated by averaging the available 5-minute data samples that
                    occurred during the day, except for PeakPower which is calculated by reporting the peak observed
                    5-minute sample value data during the day. Samples at this resolution are retained up to three
                    years.

        Returns:
            dict
        """

        if not id_or_uri:
            raise ValueError(RESOURCE_CLIENT_INVALID_ID)

        query = ''

        if filter:
            query += self.__make_query_filter(filter)

        if fields:
            query += "&fields=" + quote(fields)

        if refresh:
            query += "&refresh=true"

        if view:
            query += "&view=" + quote(view)

        if query:
            query = "?" + query[1:]

        uri = "{0}/utilization{1}".format(self.build_uri(id_or_uri), query)

        return self._connection.get(uri)

    def create_report(self, uri, timeout=-1):
        """
        Creates a report and returns the output.

        Args:
            uri: URI
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            list:
        """
        logger.debug('Creating Report (uri = %s)'.format(uri))
        task, _ = self._connection.post(uri, {})

        if not task:
            raise HPOneViewException(RESOURCE_CLIENT_TASK_EXPECTED)

        task = self._task_monitor.get_completed_task(task, timeout)

        return task['taskOutput']

    def build_uri(self, id_or_uri):
        if not id_or_uri:
            logger.exception(RESOURCE_CLIENT_INVALID_ID)
            raise ValueError(RESOURCE_CLIENT_INVALID_ID)

        if "/" in id_or_uri:
            self.__validate_resource_uri(id_or_uri)
            return id_or_uri
        else:
            return self._uri + "/" + id_or_uri

    def build_subresource_uri(self, resource_id_or_uri=None, subresource_id_or_uri=None, subresource_path=''):
        if subresource_id_or_uri and "/" in subresource_id_or_uri:
            return subresource_id_or_uri
        else:
            if not resource_id_or_uri:
                raise HPOneViewValueError(RESOURCE_ID_OR_URI_REQUIRED)

            resource_uri = self.build_uri(resource_id_or_uri)

            uri = "{}/{}/{}".format(resource_uri, subresource_path, str(subresource_id_or_uri or ''))
            uri = uri.replace("//", "/")

            if uri.endswith("/"):
                uri = uri[:-1]

            return uri

    def download(self, uri, file_path):
        """
        Downloads the contents of the requested URI to a stream.

        Args:
            uri: URI
            file_path: File path destination

        Returns:
            bool: Indicates if the file was successfully downloaded.
        """
        with open(file_path, 'wb') as file:
            return self._connection.download_to_stream(file, uri)

    def __validate_resource_uri(self, path):
        if self._uri not in path:
            logger.exception('Get by uri : unrecognized uri: (%s)' % path)
            raise HPOneViewUnknownType(UNRECOGNIZED_URI)

    def __make_query_filter(self, filters):
        if isinstance(filters, list):
            formated_filter = "&filter=".join(quote(f) for f in filters)
        else:
            formated_filter = quote(filters)

        return "&filter=" + formated_filter

    def __get_members(self, mlist):
        if mlist and 'members' in mlist and mlist['members']:
            return mlist['members']
        else:
            return []

    def __do_post(self, uri, resource, timeout, custom_headers):
        task, entity = self._connection.post(uri, resource, custom_headers=custom_headers)

        if not task:
            return entity

        return self._task_monitor.wait_for_task(task, timeout)

    def __do_put(self, uri, resource, timeout, custom_headers):
        task, body = self._connection.put(uri, resource, custom_headers=custom_headers)

        if not task:
            return body

        return self._task_monitor.wait_for_task(task, timeout)

    def __do_requests_to_getall(self, uri, requested_count):
        items = []

        while uri:
            logger.debug('Making HTTP request to get all resources. Uri: {0}'.format(uri))
            response = self._connection.get(uri)
            members = self.__get_members(response)
            items += members

            logger.debug("Response getAll: nextPageUri = {0}, members list length: {1}".format(uri, str(len(members))))
            uri = self.__get_next_page(response, items, requested_count)

        logger.debug('Total # of members found = {0}'.format(str(len(items))))
        return items

    def __get_next_page(self, response, items, requested_count):
        next_page_is_empty = response.get('nextPageUri') is None
        has_different_next_page = not response.get('uri') == response.get('nextPageUri')
        has_next_page = not next_page_is_empty and has_different_next_page

        if len(items) >= requested_count and requested_count != -1:
            return None

        return response.get('nextPageUri') if has_next_page else None

    def merge_default_values(self, resource, default_values):
        if not default_values:
            return resource

        merged_resource = None

        if not isinstance(resource, list):
            api_version = str(self._connection._apiVersion)
            data = default_values.get(api_version, {}).copy()
            merged_resource = merge_resources(data, resource)

        return merged_resource or resource


def transform_list_to_dict(list):
    """
        Transforms a list into a dictionary, putting values as keys
    Args:
        id:
    Returns:
        dict: dictionary built
    """

    ret = {}

    for value in list:
        if isinstance(value, dict):
            ret.update(value)
        else:
            ret[str(value)] = True

    return ret


def extract_id_from_uri(id_or_uri):
    """
    Extract ID from the end of the URI

    Args:
        id_or_uri: ID or URI of the OneView resources.

    Returns:
        str: The string founded after the last "/"
    """
    if '/' in id_or_uri:
        return id_or_uri[id_or_uri.rindex('/') + 1:]
    else:
        return id_or_uri
