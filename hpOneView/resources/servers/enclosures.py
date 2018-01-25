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


class Enclosures(object):
    """
    Enclosures API client.

    """
    URI = '/rest/enclosures'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort='', scope_uris=''):
        """
        Gets a paginated collection of Enclosures. The collection is based on optional sorting and filtering, and
        constrained by start and count parameters.

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
            list: A list of Enclosures.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort, scope_uris=scope_uris)

    def get_by(self, field, value):
        """
        Gets all Enclosures that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of Enclosures.
        """
        return self._client.get_by(field, value)

    def add(self, information, timeout=-1):
        """
        C7000:
            Takes information about an enclosure (for example: IP address, username, password) and uses
            it to claim/configure the enclosure and add its components to the appliance.

        Synergy:
            Adds a remote enclosure and all the enclosures linked to that enclosure by their frame link
            modules. The remote enclosures' frame link modules must not be claimed by another appliance.
            The IP used must be the frame link module's Link Local IPv6 address.

        Args:
            information: Enclosure information to add.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Enclosure.

        """
        return self._client.create(information, timeout=timeout)

    def get(self, id_or_uri):
        """
        Returns the enclosure with the specified ID, if it exists.

        Args:
            id_or_uri: ID or URI of the Enclosure.

        Returns:
            dict: Enclosure.
        """
        return self._client.get(id_or_uri)

    def patch(self, id_or_uri, operation, path, value, timeout=-1):
        """
        Uses the PATCH to update a resource for a given enclosure.

        Only one operation can be performed in each PATCH call.

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
        headers = {'If-Match': '*'}
        return self._client.patch(id_or_uri, operation, path, value, timeout=timeout, custom_headers=headers)

    def remove(self, resource, force=False, timeout=-1):
        """
        Removes and unconfigures the specified enclosure from the appliance. All components of the enclosure (for
        example: blades and interconnects) are unconfigured/removed as part of this process.

        If the force option is set to "true", then any errors encountered as part of unconfiguring the enclosure or its
        components are ignored and the enclosure is removed regardless of any errors that occur.

        Args:
            resource: Dict object to delete;
            force:
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates if the resource was successfully removed.
        """
        return self._client.delete(resource, force=force, timeout=timeout)

    def update_configuration(self, id_or_uri, timeout=-1):
        """
        Reapplies the appliance's configuration on the enclosure. This includes running the same configure steps
        that were performed as part of the enclosure add.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            Enclosure
        """
        uri = self._client.build_uri(id_or_uri) + "/configuration"
        return self._client.update_with_zero_body(uri, timeout=timeout)

    def get_environmental_configuration(self, id_or_uri):
        """
        Gets the settings that describe the environmental configuration (supported feature set, calibrated minimum &
        maximum power, location & dimensions, ...) of the enclosure resource.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.

        Returns:
            Settings that describe the environmental configuration.
        """
        uri = self._client.build_uri(id_or_uri) + '/environmentalConfiguration'
        return self._client.get(uri)

    def update_environmental_configuration(self, id_or_uri, configuration, timeout=-1):
        """
        Sets the calibrated max power of an unmanaged or unsupported enclosure.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            configuration: Configuration
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            Settings that describe the environmental configuration.
        """
        uri = self._client.build_uri(id_or_uri) + '/environmentalConfiguration'
        return self._client.update(configuration, uri=uri, timeout=timeout)

    def refresh_state(self, id_or_uri, configuration, timeout=-1):
        """
        Refreshes the enclosure along with all of its components, including interconnects and servers. Any new
        hardware is added and any hardware that is no longer present within the enclosure is removed. The
        configuration dict must have the "refreshState" field set to "Refreshing" and optionally
        provide information to re-claim the enclosure (for example: IP address, user name, password, etc.).

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            configuration: Configuration
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            Enclosure
        """
        uri = self._client.build_uri(id_or_uri) + "/refreshState"
        return self._client.update(configuration, uri=uri, timeout=timeout)

    def get_script(self, id_or_uri):
        """
        Gets the script of the enclosure.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.

        Returns:
            Enclosure script.
        """
        uri = self._client.build_uri(id_or_uri) + "/script"
        return self._client.get(uri)

    def get_sso(self, id_or_uri, role):
        """
        Builds the SSO (Single Sign-On) URL parameters for the specified enclosure. This allows the user to
        log in to the enclosure without providing credentials. This API is currently only supported by C7000 enclosures.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            role: Role

        Returns:
            SSO (Single Sign-On) URL parameters.
        """
        uri = self._client.build_uri(id_or_uri) + "/sso?role=%s" % role
        return self._client.get(uri)

    def get_utilization(self, id_or_uri, fields=None, filter=None, refresh=False, view=None):
        """
        Retrieves historical utilization data for the specified enclosure, metrics, and time span.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            fields: Name of the metrics to be retrieved in the format METRIC[,METRIC]...

                If unspecified, all metrics supported are returned.

                Enclosures support the following utilization metrics:
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

            filter (list or str):
                Provides an expression of the requested time range of data. One condition (startDate/endDate) is
                specified per filter specification as described below. The condition must be specified via the
                equals (=) operator.

                startDate
                    Start date of requested starting time range in ISO 8601 format (2016-05-31T07:20:00.000Z).
                    If omitted, the startDate is determined by the endDate minus 24 hours.
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

    def generate_csr(self, csr_data, id_or_uri, bay_number=None):
        """
        Creates a Certificate Signing Request (CSR) for an enclosure.

        Args:
            csr_data: Dictionary with csr details.
            id_or_uri: Can be either the resource ID or the resource URI.
            bay_number: OA from which the CSR should be generated.

        Returns:
            Enclosure.
        """

        uri = self._client.build_uri(id_or_uri) + "/https/certificaterequest"

        if bay_number:
            uri += "?bayNumber=%d" % (bay_number)

        headers = {'Content-Type': 'application/json'}
        return self._client.create(csr_data, uri=uri, custom_headers=headers)

    def get_csr(self, id_or_uri, bay_number=None):
        """
        Get an enclosure's Certificate Signing Request (CSR) that was generated by previous POST to the same URI.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            bay_number: OA to retrieve the previously generated CSR.

        Returns:
            dict
        """

        uri = self._client.build_uri(id_or_uri) + "/https/certificaterequest"

        if bay_number:
            uri += "?bayNumber=%d" % (bay_number)

        return self._client.get(uri)

    def import_certificate(self, certificate_data, id_or_uri, bay_number=None):
        """
        Imports a signed server certificate into the enclosure.

        Args:
            certificate_data: Dictionary with Signed certificate and type.
            id_or_uri: Can be either the resource ID or the resource URI.
            bay_number: OA to which the signed certificate will be imported.

        Returns:
            Enclosure.
        """

        uri = self._client.build_uri(id_or_uri) + "/https/certificaterequest"

        if bay_number:
            uri += "?bayNumber=%d" % (bay_number)

        headers = {'Content-Type': 'application/json'}
        return self._client.update(certificate_data, uri=uri, custom_headers=headers)
