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

__title__ = 'resource'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2016) Hewlett Packard Enterprise ' \
                ' Development LP'
__license__ = 'MIT'
__status__ = 'Development'

import logging
from urllib.parse import quote
from hpOneView.common import get_members
from hpOneView.resources.task_monitor import TaskMonitor
from hpOneView.exceptions import HPOneViewUnknownType

RESOURCE_CLIENT_RESOURCE_WAS_NOT_PROVIDED = 'Resource was not provided'
RESOURCE_CLIENT_INVALID_FIELD = 'Invalid field was provided'
RESOURCE_CLIENT_INVALID_ID = 'Invalid id was provided'
RESOURCE_CLIENT_UNKNOWN_OBJECT_TYPE = 'Unknown object type'
UNRECOGNIZED_URI = 'Unrecognized URI for this resource'

logger = logging.getLogger(__name__)


class ResourceClient(object):
    """
    This class implements common functions for HpOneView API rest
    """

    def __init__(self, con, uri):
        self._connection = con
        self._uri = uri
        self._task_monitor = TaskMonitor(con)

    def get_members(self, uri):
        # TODO: common is deprecated, refactor get_members implementation
        return get_members(self._connection.get(uri))

    def get_all(self, start=0, count=-1, filter='', query='', sort='', view='', fields=''):
        """
        the use of optional parameters are described here:
        http://h17007.www1.hpe.com/docs/enterprise/servers/oneview2.0/cic-api/en/api-docs/current/index.html

        Known issues:
            - Pass "'" inside a parameter is not supported by One View API

        Returns: a dictionary with requested data

        """
        if filter:
            filter = "&filter=" + quote(filter)

        if query:
            query = "&query=" + quote(query)

        if sort:
            sort = "&sort=" + quote(sort)

        if view:
            view = "&view=" + quote(view)

        if fields:
            fields = "&fields=" + quote(fields)

        uri = "{0}?start={1}&count={2}{3}{4}{5}{6}{7}".format(self._uri, start, count, filter, query, sort, view,
                                                              fields)

        logger.debug('Getting all resources : with uri : %s' % uri)

        result = self.get_members(uri)

        logger.debug("Getting all resources : count : %i" % len(result))

        return result

    def delete(self, resource, force=False, blocking=True, verbose=False, timeout=60):

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
            uri = self._uri + "/" + resource

        if force:
            uri += '?force=True'

        logger.debug("Delete resource (uri = %s, resource = %s)" % (self._uri, str(resource)))

        task, body = self._connection.delete(uri)
        if blocking:
            task = self._task_monitor.wait_for_task(task, timeout=timeout)

        return task

    def get_schema(self):
        logger.debug('Get schema (uri = %s, resource = %s)' % (self._uri, self._uri))
        return self._connection.get(self._uri + '/schema')

    def get(self, id_or_uri):
        """
        Args:
            id_or_uri: Could be either the resource id or the resource uri
        Returns:
             The requested resource
        """
        if not id_or_uri:
            logger.exception(RESOURCE_CLIENT_INVALID_ID)
            raise ValueError(RESOURCE_CLIENT_INVALID_ID)

        if "/" in id_or_uri:
            return self.get_by_uri(id_or_uri)

        logger.debug('Get resource (uri = %s, ID = %s)' % (self._uri, str(id_or_uri)))

        return self._connection.get(self._uri + '/' + id_or_uri)

    def update(self, resource, uri=None, blocking=True):
        if not resource:
            logger.exception(RESOURCE_CLIENT_RESOURCE_WAS_NOT_PROVIDED)
            raise ValueError(RESOURCE_CLIENT_RESOURCE_WAS_NOT_PROVIDED)

        logger.debug('Update async (uri = %s, resource = %s)' % (self._uri, str(resource)))

        if not uri:
            uri = resource['uri']

        task, body = self._connection.put(uri, resource)

        if not task:
            return body

        if blocking:
            return self._task_monitor.wait_for_task(task, 60)

        return task

    def create(self, resource, blocking=True):
        if not resource:
            logger.exception(RESOURCE_CLIENT_RESOURCE_WAS_NOT_PROVIDED)
            raise ValueError(RESOURCE_CLIENT_RESOURCE_WAS_NOT_PROVIDED)

        logger.debug('Create (uri = %s, resource = %s)' % (self._uri, str(resource)))

        task, entity = self._connection.post(self._uri, resource)
        if blocking:
            return self._task_monitor.wait_for_task(task, 60)
        return task

    def get_by(self, field, value):
        """
        This function uses get_all passing a filter
        The search is case insensitive
        Args:
            field: field name to filter
            value: value to filter

        Returns: dict

        """
        if not field:
            logger.exception(RESOURCE_CLIENT_INVALID_FIELD)
            raise ValueError(RESOURCE_CLIENT_INVALID_FIELD)

        logger.debug('Get by (uri = %s, field = %s, value = %s)' % (self._uri, field, str(value)))

        filter = "\"'{0}'='{1}'\"".format(field, value)
        return self.get_all(filter=filter)

    def get_by_uri(self, uri):
        if self._uri in uri:
            logger.debug('Get resource by uri : uri : %s' % uri)
            return self._connection.get(uri)
        else:
            logger.exception('Get by uri : unrecognized uri: (%s)' % uri)
            raise HPOneViewUnknownType(UNRECOGNIZED_URI)

    def get_utilization(self, id, fields=None, filter=None, refresh=False, view=None):
        """
        Retrieves historical utilization data for the specified resource, metrics, and time span.

        Args:
            id: resource identification
            fields:
                Name of the supported metric(s) to be retrieved in the format METRIC[,METRIC]...
                If unspecified, all metrics supported are returned.

            filter:
                Filters should be in the format FILTER_NAME=VALUE[,FILTER_NAME=VALUE]...
                E.g.: 'startDate=2016-05-30T11:20:44.541Z,endDate=2016-05-30T19:20:44.541Z'

                startDate
                    Start date of requested starting time range in ISO 8601 format. If omitted, the startDate is
                    determined by the endDate minus 24 hours.
                endDate
                    End date of requested starting time range in ISO 8601 format. When omitted the endDate includes
                    the latest data sample available.

                If an excessive number of samples would otherwise be returned, the results will be segmented. The
                caller is responsible for comparing the returned sliceStartTime with the requested startTime in the
                response. If the sliceStartTime is greater than the oldestSampleTime and the requested start time,
                the caller is responsible for repeating the request with endTime set to sliceStartTime to obtain the
                next segment. This process is repeated until the full data set is retrieved.

                If the resource has no data, the UtilizationData is still returned, but will contain no samples and
                sliceStartTime/sliceEndTime will be equal. oldestSampleTime/newestSampleTime will still be set
                appropriately (null if no data is available). If the filter just does not happen to overlap the data
                that a resource does have, then the metric history service will return null sample values for any
                missing samples.

            refresh:
                Specifies that if necessary an additional request will be queued to obtain the most recent
                utilization data from the iLO. The response will not include any refreshed data. To track the
                availability of the newly collected data, monitor the TaskResource identified by the refreshTaskUri
                property in the response. If null, no refresh was queued.

            view:
                Specifies the resolution interval length of the samples to be retrieved. This is reflected in the
                resolution in the returned response. Utilization data is automatically purged to stay within storage
                space constraints. Supported views are listed below.

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

        Returns: dict

        """

        if not id:
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

        uri = "{0}/{1}/utilization{2}".format(self._uri, id, query)

        return self._connection.get(uri)

    def __make_query_filter(self, filter):
        filters = filter.split(",")
        formated_filter = "&filter=".join(quote(f) for f in filters)
        return "&filter=" + formated_filter
