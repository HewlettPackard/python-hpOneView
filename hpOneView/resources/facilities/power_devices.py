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


class PowerDevices(object):
    """
    Power Devices API client.

    """
    URI = '/rest/power-devices'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', query='', sort=''):
        """
        Gets a set of power delivery device resources according to the specified parameters. Filters can be used to get
        a specific set of power delivery devices. With no filters specified, the API returns a potentially paginated
        list of all the power delivery device resources subject to start/count/sort parameters.

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
            query:
                 A general query string to narrow the list of resources returned. The default
                 is no query - all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.

        Returns:
             list of power devices
        """
        return self._client.get_all(start, count, filter=filter, sort=sort, query=query)

    def get(self, id_or_uri):
        """
        Gets a single power delivery device resource based upon its uri or id.

        Args:
            id_or_uri:
                Can be either the power device id or the uri

        Returns:
            dict: The power device
        """
        return self._client.get(id_or_uri)

    def add(self, information, timeout=-1):
        """
        Adds a power delivery device resource based upon the attributes specified. Use this method to create a
        representation of power delivery devices that provide power to other resources but cannot otherwise be
        discovered by the management appliance.

        Args:
            information:
                power device information
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: added power device.
        """
        return self._client.create(information, timeout=timeout)

    def remove(self, resource, force=False, timeout=-1):
        """
        Deletes the set of power-devices according to the specified parameters. A filter is required to identify the
        set of resources to be deleted.

        Args:
            resource: dict object to remove
            force:
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
             bool: operation success
        """
        return self._client.delete(resource, force=force, timeout=timeout)

    def add_ipdu(self, information, timeout=-1):
        """
        Add an HP iPDU and bring all components under management by discovery of its management module. Bring the
        management module under exclusive management by the appliance, configure any management or data collection
        settings, and create a private set of administrative credentials to enable ongoing communication and management
        of the iPDU. Use "force" to claim the device, even if claimed by another management appliance

        Args:
            resource: power device information
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: added power device.
        """
        uri = self.URI + "/discover"
        return self._client.create(information, uri=uri, timeout=timeout)

    def update(self, resource, timeout=-1):
        """
        Updates the resource for the specified {id}. The properties that are omitted (not included as part of the the
        request body) are reset to their respective default values. The id and uuid properties are required and cannot
        be changed.

        Args:
            resource (dict): Object to update
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated power device
        """
        return self._client.update(resource, timeout=timeout)

    def get_power_state(self, id_or_uri):
        """
        Gets the power state (on, off or unknown) of the specified power delivery device that supports power control.
        The device must be an HP Intelligent Outlet.

        Args:
            id_or_uri:
                Can be either the power device id or the uri

        Returns:
            str: The power state
        """
        uri = self._client.build_uri(id_or_uri) + "/powerState"
        return self._client.get(uri)

    def update_power_state(self, id_or_uri, power_state):
        """
        Sets the power state of the specified power delivery device. The device must be an HP Intelligent Outlet.

        Args:
            id_or_uri:
                Can be either the power device id or the uri
            power_state:
                {"powerState":"On|Off"}

        Returns:
            str: The power state
        """
        uri = self._client.build_uri(id_or_uri) + "/powerState"
        return self._client.update(power_state, uri)

    def update_refresh_state(self, id_or_uri, refresh_state_data):
        """
        Refreshes a given intelligent power delivery device.

        Args:
            id_or_uri:
                Can be either the power device id or the uri
            refresh_state_data:
                Power device refresh request

        Returns:
            str: The power state
        """
        uri = self._client.build_uri(id_or_uri) + "/refreshState"
        return self._client.update(refresh_state_data, uri=uri)

    def remove_synchronous(self, resource, force=False, timeout=-1):
        """
        Deletes the resource specified by {id} synchronously.

        Args:
            resource: dict object to remove
            force:
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: operation success
        """
        uri = self._client.build_uri(resource['uri']) + "/synchronous"
        remove_resource = {'uri': uri}
        return self._client.delete(remove_resource, force=force, timeout=timeout)

    def get_uid_state(self, id_or_uri):
        """
        Retrieves the unit identification (UID) state (on, off, unknown) of the specified power outlet or extension bar
        resource. The device must be an HP iPDU component with a locator light (HP Intelligent Load Segment,
        HP AC Module, HP Intelligent Outlet Bar, or HP Intelligent Outlet).

        Args:
            id_or_uri:
                Can be either the power device id or the uri

        Returns:
            str: unit identification (UID) state
        """
        uri = self._client.build_uri(id_or_uri) + "/uidState"
        return self._client.get(uri)

    def update_uid_state(self, id_or_uri, refresh_state_data):
        """
        Sets the unit identification (UID) light state of the specified power delivery device. The device must be an
        HP iPDU component with a locator light (HP Intelligent Load Segment, HP AC Module, HP Intelligent Outlet Bar,
        or HP Intelligent Outlet)

        Args:
            id_or_uri:
                Can be either the power device id or the uri
            refresh_state_data:
                Power device refresh request

        Returns:
            str: The UID state
        """
        uri = self._client.build_uri(id_or_uri) + "/uidState"
        return self._client.update(refresh_state_data, uri)

    def get_utilization(self, id_or_uri, fields=None, filter=None, refresh=False, view=None):
        """
        Retrieves historical utilization data for the specified metrics and time span. The device must be a component
        of an HPE iPDU.

        Args:
            id_or_uri:
                The power device id or the resource uri
            fields:
                Name of the metric(s) to be retrieved in the format METRIC[,METRIC]...If unspecified, all metrics
                supported are returned. Power delivery devices support the following utilization metrics:

                    * AveragePower
                        Average power consumption in Watts during this sample interval.
                    * PeakPower
                        Peak power consumption in Watts during this sample interval.

            filter (list or str):
                Filters should be in the format: FILTER_NAME=VALUE[,FILTER_NAME=VALUE]...

                For Example: 'startDate=2016-05-30T11:20:44.541Z,endDate=2016-05-30T19:20:44.541Z'

                startDate:
                    Start date of requested starting time range in ISO 8601 format. If omitted, the startDate is
                    determined by the endDate minus 24 hours.
                endDate:
                    End date of requested starting time range in ISO 8601 format. When omitted the endDate includes the
                    latest data sample available.

                If an excessive number of samples would otherwise be returned, the results will be segmented. The caller
                is responsible for comparing the returned sliceStartTime with the requested startTime in the response.
                If the sliceStartTime is greater than the oldestSampleTime and the requested start time, the caller is
                responsible for repeating the request with endTime set to sliceStartTime to obtain the next segment.
                This process is repeated until the full data set is retrieved.

                If the resource has no data, the UtilizationData is still returned, but will contain no samples and
                sliceStartTime/sliceEndTime will be equal. oldestSampleTime/newestSampleTime will still be set
                appropriately (null if no data is available). If the filter does not happen to overlap the data
                that a resource does have, then the metric history service will return null sample values for any
                missing samples.

            refresh:
                Specifies that if necessary, an additional request will be queued to obtain the most recent utilization
                data from the enclosure. The response will not include any refreshed data. To track the availability
                of the newly collected data, monitor the TaskResource identified by the refreshTaskUri property in
                the response. If null, no refresh was queued.
            view:
                Specifies the resolution interval length of the samples to be retrieved. This is reflected in the
                resolution in the returned response. Utilization data is automatically purged to stay within storage
                space constraints. Supported views are listed below:

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

        Returns:
            dict: Utilization data
        """

        return self._client.get_utilization(id_or_uri, fields, filter, refresh, view)

    def get_by(self, field, value):
        """
        Gets all power devices that match the filter
        The search is case-insensitive

        Args:
            field: field name to filter
            value: value to filter

        Returns:
            dict: power devices
        """
        return self._client.get_by(field, value)
