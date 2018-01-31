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


class ServerHardware(object):
    """
    The server hardware resource is a representation of a physical server.
    The server hardware resource provides methods for server management tasks such
    as applying a profile, importing a server and managing an iLO.

    """
    URI = '/rest/server-hardware'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_utilization(self, id_or_uri, fields=None, filter=None, refresh=False, view=None):
        """
        Retrieves historical utilization data for the specified resource, metrics, and time span.

        Args:
            id_or_uri: Resource identification or URI.
            fields:
                Name of the metrics to be retrieved in the format METRIC[,METRIC]...

                If unspecified, all metrics supported are returned.

                Server hardware supports the following utilization metrics:

                    AmbientTemperature
                        Inlet air temperature in degrees Celsius during this sample interval.
                    AveragePower
                        Average power consumption in Watts during this sample interval.
                    PeakPower
                        Peak power consumption in Watts during this sample interval.
                    PowerCap
                        Dynamic power cap setting on the server hardware in Watts during this sample interval.
                    CpuUtilization
                        CPU utilization of all CPUs in percent during this sample interval.
                    CpuAverageFreq
                        Average CPU frequency in Mhz during this sample interval.

            filter (list or str):
                Provides an expression of the requested time range of data. One condition (startDate/endDate) is
                specified per filter specification as described below. The condition must be specified via the
                equals (=) operator.

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

                If the resource has no data, the UtilizationData is still returned, but will contain no samples and
                sliceStartTime/sliceEndTime will be equal. oldestSampleTime/newestSampleTime will still be set
                appropriately (null if no data is available). If the filter just does not happen to overlap the data
                that a resource does have, then the metric history service will return null sample values for any
                missing samples.

            refresh:
                Specifies that, if necessary, an additional request will be queued to obtain the most recent
                utilization data from the iLO. The response will not include any refreshed data. To track the
                availability of the newly collected data, monitor the TaskResource identified by the refreshTaskUri
                property in the response. If null, no refresh was queued.

            view:
                Specifies the resolution interval length of the samples to be retrieved. This is reflected in the
                resolution in the returned response. Utilization data is automatically purged to stay within storage
                space constraints. See the following supported views.

                native
                    Resolution of the samples returned will be one sample for each 5-minute time period. This is the
                    default view and matches the resolution of the data returned by the iLO. Samples at this resolution
                    are retained up to one year.
                hour
                    Resolution of the samples returned will be one sample for each 60-minute time period. Samples are
                    calculated by averaging the available 5-minute data samples that occurred within the hour, except
                    for PeakPower, which is calculated by reporting the peak observed 5-minute sample value data during
                    the hour. Samples at this resolution are retained up to three years.
                day
                    Resolution of the samples returned will be one sample for each 24-hour time period. One day is a
                    24-hour period that starts at midnight GMT, regardless of the time zone in which the appliance or
                    client is located. Samples are calculated by averaging the available 5-minute data samples that
                    occurred during the day, except for PeakPower, which is calculated by reporting the peak observed
                    5-minute sample value data during the day. Samples at this resolution are retained up to three
                    years.

        Returns:
            dict
        """

        return self._client.get_utilization(id_or_uri, fields=fields, filter=filter, refresh=refresh, view=view)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a list of server hardware resources. Returns a list of resources based on optional sorting and filtering,
        and constrained by start and count parameters.

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
            list: A list of server hardware resources.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def add(self, information, timeout=-1):
        """
        Adds a rack-mount server for management by the appliance. This API initiates the asynchronous addition of
        supported server models.

        Note: Servers in an enclosure are added by adding the enclosure resource. This is
        only supported on appliances that support rack-mounted servers.

        Args:
            information (dict): Object to create
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Created rack-mount server.
        """
        return self._client.create(information, timeout=timeout)

    def add_multiple_servers(self, information, timeout=-1):
        """
        Adds multiple rack-mount servers for management by the appliance. This API initiates the asynchronous addition of
        supported server models.

        Note: Servers in an enclosure are added by adding the enclosure resource. This is
        only supported on appliances that support rack-mounted servers.

        This is only supported for api version 600

        Args:
            information (dict): Objects to create
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Created rack-mount servers.
        """
        uri = self._client.build_uri(self.URI) + "/discovery"
        return self._client.create(information, uri=uri, timeout=timeout)

    def get(self, id_or_uri):
        """
        Gets a server hardware resource by ID or by URI.

        Args:
            id_or_uri: Can be either the server hardware resource ID or URI.

        Returns:
            dict: The server hardware resource
        """
        return self._client.get(id_or_uri)

    def get_by(self, field, value):
        """
        Gets all server hardware that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            dict
        """
        return self._client.get_by(field, value)

    def remove(self, resource, force=False, timeout=-1):
        """
        Removes the rackserver with the specified URI.
        Note: This operation is only supported on appliances that support rack-mounted servers.

        Args:
            resource (dict):
                Object to delete.
            force (bool):
                If set to true, the operation completes despite any problems with
                network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates whether the resource was successfully removed.
        """
        return self._client.delete(resource, force=force, timeout=timeout)

    def get_bios(self, id_or_uri):
        """
        Gets the list of BIOS/UEFI values currently set on the physical server.

        Args:
            id_or_uri: Can be either the server hardware resource ID or URI.

        Returns:
            dict: Dictionary of BIOS/UEFI values.
        """
        uri = self._client.build_uri(id_or_uri) + "/bios"
        return self._client.get(uri)

    def get_environmental_configuration(self, id_or_uri):
        """
        Gets the settings that describe the environmental configuration (supported feature set, calibrated minimum and
        maximum power, location and dimensions, etc.) of the server hardware resource.

        Args:
            id_or_uri: Can be either the server hardware resource ID or URI.

        Returns:
            dict: Environmental configuration settings.
        """
        uri = self._client.build_uri(id_or_uri) + "/environmentalConfiguration"
        return self._client.get(uri)

    def update_environmental_configuration(self, configuration, id_or_uri, timeout=-1):
        """
        Sets the calibrated max power of an unmanaged or unsupported server hardware resource.

        Args:
            id_or_uri: Can be either the server hardware resource ID or URI.
            configuration (dict): Environmental configuration.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Environmental configuration settings.
        """
        uri = self._client.build_uri(id_or_uri) + "/environmentalConfiguration"
        return self._client.update(configuration, uri, timeout=timeout)

    def get_ilo_sso_url(self, id_or_uri):
        """
        Retrieves the URL to launch a Single Sign-On (SSO) session for the iLO web interface. If the server hardware is
        unsupported, the resulting URL will not use SSO and the iLO web interface will prompt for credentials.
        This is not supported on G7/iLO3 or earlier servers.

        Args:
            id_or_uri: Can be either the server hardware resource ID or URI.

        Returns:
            URL
        """
        uri = self._client.build_uri(id_or_uri) + "/iloSsoUrl"
        return self._client.get(uri)

    def get_all_firmwares(self, filter='', start=0, count=-1, query='', sort=''):
        """
        Gets a list of firmware inventory across all servers. To filter the returned data, specify a filter
        expression to select a particular server model, component name, and/or component firmware version.

        Note:
            This method is available for API version 300 or later.

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
                A general query string to narrow the list of resources returned. The default is no query; all resources
                are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.

        Returns:
            list: List of firmware inventory.
        """
        uri = self.URI + "/*/firmware"
        return self._client.get_all(start, count, filter, query, sort, '', '', uri)

    def get_firmware(self, id_or_uri):
        """
        Get the firmware inventory of a server.

        Note:
            This method is available for API version 300 or later.

        Args:
            id_or_uri: Can be either the server hardware resource ID or URI.

        Returns:
            dict: Server Hardware firmware.
        """
        uri = self._client.build_uri(id_or_uri) + "/firmware"
        return self._client.get(uri)

    def patch(self, id_or_uri, operation, path, value, timeout=-1):
        """
        Performs a specific patch operation for the given server. If the server supports the particular operation,
        the operation is performed and a response is returned to the caller with the results.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            operation: Patch operation
            path: Path
            value: Value
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated resource.
        """
        return self._client.patch(id_or_uri, operation, path, value, timeout=timeout)

    def get_java_remote_console_url(self, id_or_uri):
        """
        Generates a Single Sign-On (SSO) session for the iLO Java Applet console and returns the URL to launch it.
        If the server hardware is unmanaged or unsupported, the resulting URL will not use SSO and the iLO Java Applet
        will prompt for credentials. This is not supported on G7/iLO3 or earlier servers.

        Args:
            id_or_uri: Can be either the server hardware resource ID or URI.

        Returns:
            URL
        """
        uri = self._client.build_uri(id_or_uri) + "/javaRemoteConsoleUrl"
        return self._client.get(uri)

    def update_mp_firware_version(self, id_or_uri, timeout=-1):
        """
        Updates the iLO firmware on a physical server to a minimum ILO firmware version required by OneView to
        manage the server.

        Args:
            id_or_uri:
                Can be either the server hardware resource ID or URI.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
        Returns:
            Resource
        """
        uri = self._client.build_uri(id_or_uri) + "/mpFirmwareVersion"
        return self._client.update_with_zero_body(uri, timeout)

    def update_power_state(self, configuration, id_or_uri, timeout=-1):
        """
        Refreshes the server hardware to fix configuration issues.

        Args:
            id_or_uri: Can be either the server hardware resource ID or URI.
            configuration (dict): Power state configuration.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            Resource
        """
        uri = self._client.build_uri(id_or_uri) + "/powerState"
        return self._client.update(configuration, uri, timeout=timeout)

    def refresh_state(self, configuration, id_or_uri, timeout=-1):
        """
        Refreshes the server hardware to fix configuration issues.

        Args:
            id_or_uri: Can be either the server hardware resource ID or URI.
            configuration: Refresh state configuration.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            Resource
        """
        uri = self._client.build_uri(id_or_uri) + "/refreshState"
        return self._client.update(configuration, uri=uri, timeout=timeout)

    def get_remote_console_url(self, id_or_uri):
        """
        Generates a Single Sign-On (SSO) session for the iLO Integrated Remote Console Application (IRC) and returns the
        URL to launch it. If the server hardware is unmanaged or unsupported, the resulting URL will not use SSO and the
        IRC application will prompt for credentials. Use of this URL requires a previous installation of the iLO IRC and
        is supported only on Windows clients.

        Args:
            id_or_uri: Can be either the server hardware resource ID or URI.

        Returns:
            URL
        """
        uri = self._client.build_uri(id_or_uri) + "/remoteConsoleUrl"
        return self._client.get(uri)

    def get_physical_server_hardware(self, id_or_uri):
        """
        Information describing an 'SDX' partition including a list of physical server blades represented by a server
        hardware. Used with SDX enclosures only.

        Args:
            id_or_uri: Can be either the server hardware resource ID or URI.

        Returns:
            Resource
        """
        uri = self._client.build_uri(id_or_uri) + "/physicalServerHardware"
        return self._client.get(uri)
