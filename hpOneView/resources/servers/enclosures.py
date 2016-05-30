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

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()

__title__ = 'enclosures'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2016) Hewlett Packard Enterprise ' \
                ' Development LP'
__license__ = 'MIT'
__status__ = 'Development'

from hpOneView.resources.resource import ResourceClient
from urllib.parse import quote


class Enclosures(object):
    URI = '/rest/enclosures'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_utilization(self, id, fields=None, filter=None, refresh=False, view=None):
        """
        Retrieves historical utilization data for the specified enclosure, metrics, and time span.

        Args:
            id:
            fields:
                 Name of the metric(s) to be retrieved in the format METRIC[,METRIC]... Enclosures support the following
                  utilization metrics:

                AmbientTemperature
                    Inlet air temperature in degrees Celsius during this sample interval.
                AveragePower
                    Average power consumption in Watts during this sample interval.
                PeakPower
                    Peak power consumption in Watts during this sample interval.
                PowerCap
                    Dynamic power cap setting on the server hardware in Watts during this sample interval.
                DeratedCapacity
                    Enclosure dynamic power cap derated capacity setting in Watts during this sample interval.
                RatedCapacity
                    Enclosure dynamic power cap rated capacity setting in Watts during this sample interval.

                If unspecified, all metrics supported are returned.
            filter:
                 Provides an expression of the requested time range of data. One condition (startDate/endDate) is
                  specified per filter specification as described below. The condition must be specified via the
                  equals (=) operator.

                startDate
                    Start date of requested starting time range in ISO 8601 format (2016-05-31T07:20:00.000Z). If omitted,
                     the startDate is determined by the endDate minus 24 hours.
                endDate
                    End date of requested starting time range in ISO 8601 format. When omitted the endDate includes the
                    latest data sample available.

                If an excessive number of samples would otherwise be returned, the results will be segmented. The caller
                is responsible for comparing the returned sliceStartTime with the requested startTime in the response.
                If the sliceStartTime is greater than the oldestSampleTime and the requested start time, the caller is
                responsible for repeating the request with endTime set to sliceStartTime to obtain the next segment.
                This process is repeated until the full data set is retrieved.

                If the resource has no data, the UtilizationData is still returned, but will contain no samples and
                sliceStartTime/sliceEndTime will be equal. oldestSampleTime/newestSampleTime will still be set
                appropriately (null if no data is available). If the filter just does not happen to overlap the data
                that a resource does have, then the metric history service will return null sample values for any
                missing samples.

            refresh:
                 Specifies that if necessary an additional request will be queued to obtain the most recent utilization
                  data from the enclosure. The response will not include any refreshed data. To track the availability
                  of the newly collected data, monitor the TaskResource identified by the refreshTaskUri property in
                  the response. If null, no refresh was queued.
            view:
                 Specifies the resolution interval length of the samples to be retrieved. This is reflected in the
                 resolution in the returned response. Utilization data is automatically purged to stay within storage
                 space constraints. Supported views are listed below.

                native (DEFAULT)
                    Resolution of the samples returned will be one sample for each 5-minute time period. This is the
                    default view and matches the resolution of the data returned by the enclosure. Samples at this
                     resolution are retained up to one year.
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

        query = ''

        if filter:
            query += "&filter=" + quote(filter)

        if fields:
            query += "&fields=" + quote(fields)

        if refresh:
            query += "&refresh=true"

        if view:
            query += "&view=" + quote(view)

        if query:
            query = "?" + query[1:]

        uri = "{0}/{1}/utilization{2}".format(self.URI, id, query)

        return self._client.get(uri)
