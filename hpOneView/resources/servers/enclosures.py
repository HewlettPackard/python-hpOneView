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

from hpOneView.resources.task_monitor import TaskMonitor
from hpOneView.resources.resource import Resource, ResourceHelper, ensure_resource_client


class Enclosures(Resource):
    """
    Enclosures API client.

    """
    URI = '/rest/enclosures'

    def __init__(self, connection, data=None):
        task_monitor = TaskMonitor(connection)
        helper = ResourceHelper(self.URI, connection, task_monitor)
        super(Enclosures, self).__init__(connection, task_monitor, helper, data)

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
        return self.create(data=information, timeout=timeout)

    def remove(self, force=False):
        """
        Remove enclosure
        """
        self.delete(force=force)

    def patch(self, operation, path, value, custom_headers=None, timeout=-1):
        """Uses the PATCH to update a resource.

        Only one operation can be performed in each PATCH call.

        Args
            operation: Patch operation
            path: Path
            value: Value
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
            custom_headers: Allows to add custom http headers.

        Returns:
            Updated resource.
        """
        uri = self.data['uri']
        return  self._resource_helper.patch(uri, operation, path, value, custom_headers, timeout)

    def update_configuration(self, timeout=-1):
        """
        Reapplies the appliance's configuration on the enclosure. This includes running the same configure steps
        that were performed as part of the enclosure add.

        Args:
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            Enclosure
        """
        uri = "{}/configuration".format(self.data['uri'])
        return self._resource_helper.update_with_zero_body(uri=uri, timeout=timeout)

    def get_by_hostname(self, hostname):
        """Get enclosure by it's hostname"""
        def filter_by_hostname(hostname, enclosure):
            is_primary_ip = ('activeOaPreferredIP' in enclosure and enclosure['activeOaPreferredIP'] == hostname)
            is_standby_ip = ('standbyOaPreferredIP' in enclosure and enclosure['standbyOaPreferredIP'] == hostname)
            return is_primary_ip or is_standby_ip

        enclosures = self.get_all()
        result = [x for x in enclosures if filter_by_hostname(hostname, x)]

        if result:
            new_resource = self.new(self._connection, result[0])
        else:
            new_resource = None

        return  new_resource

    @ensure_resource_client
    def get_environmental_configuration(self):
        """
        Gets the settings that describe the environmental configuration (supported feature set, calibrated minimum &
        maximum power, location & dimensions, ...) of the enclosure resource.

        Returns:
            Settings that describe the environmental configuration.
        """
        uri = '{}/environmentalConfiguration'.format(self.data['uri'])
        return self._resource_helper.do_get(uri)

    @ensure_resource_client
    def update_environmental_configuration(self, configuration, timeout=-1):
        """
        Sets the calibrated max power of an unmanaged or unsupported enclosure.

        Args:
            configuration: Configuration
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            Settings that describe the environmental configuration.
        """
        uri = '{}/environmentalConfiguration'.format(self.data['uri'])
        return self._resource_helper.do_put(uri, configuration, timeout, None)

    @ensure_resource_client
    def refresh_state(self, configuration, timeout=-1):
        """
        Refreshes the enclosure along with all of its components, including interconnects and servers. Any new
        hardware is added and any hardware that is no longer present within the enclosure is removed. The
        configuration dict must have the "refreshState" field set to "Refreshing" and optionally
        provide information to re-claim the enclosure (for example: IP address, user name, password, etc.).

        Args:
            configuration: Configuration
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            Enclosure
        """
        uri = "{}/refreshState".format(self.data['uri'])
        return self._resource_helper.do_put(uri, configuration, timeout, None)

    @ensure_resource_client
    def get_script(self):
        """
        Gets the script of the enclosure.

        Returns:
            Enclosure script.
        """
        uri = "{}/script".format(self.data['uri'])
        return self._resource_helper.do_get(uri)

    @ensure_resource_client
    def get_sso(self, role):
        """
        Builds the SSO (Single Sign-On) URL parameters for the specified enclosure. This allows the user to
        log in to the enclosure without providing credentials. This API is currently only supported by C7000 enclosures.

        Args:
            role: Role

        Returns:
            SSO (Single Sign-On) URL parameters.
        """
        uri = "{}/sso?role={}".format(self.data['uri'], role)
        return self._resource_helper.do_get(uri)

    @ensure_resource_client
    def get_utilization(self, fields=None, filter=None, refresh=False, view=None):
        """Retrieves historical utilization data for the specified resource, metrics, and time span.

        Args:
            fields: Name of the supported metric(s) to be retrieved in the format METRIC[,METRIC]...
                If unspecified, all metrics supported are returned.

            filter (list or str): Filters should be in the format FILTER_NAME=VALUE[,FILTER_NAME=VALUE]...
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

            refresh: Specifies that if necessary, an additional request will be queued to obtain the most recent
                utilization data from the iLO. The response will not include any refreshed data. To track the
                availability of the newly collected data, monitor the TaskResource identified by the refreshTaskUri
                property in the response. If null, no refresh was queued.

            view: Specifies the resolution interval length of the samples to be retrieved. This is reflected in the
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
        uri = self.data['uri']
        return self._resource_helper.get_utilization(uri, fields=None, filter=None, refresh=False, view=None)

    @ensure_resource_client
    def generate_csr(self, csr_data, bay_number=None):
        """
        Creates a Certificate Signing Request (CSR) for an enclosure.

        Args:
            csr_data: Dictionary with csr details.
            bay_number: OA from which the CSR should be generated.

        Returns:
            Enclosure.
        """
        uri = "{}/https/certificaterequest".format(self.data['uri'])

        if bay_number:
            uri += "?bayNumber=%d" % (bay_number)

        headers = {'Content-Type': 'application/json'}

        return self._resource_helper.do_post(uri, csr_data, -1, headers)

    @ensure_resource_client
    def get_csr(self, bay_number=None):
        """
        Get an enclosure's Certificate Signing Request (CSR) that was generated by previous POST to the same URI.

        Args:
            bay_number: OA to retrieve the previously generated CSR.

        Returns:
            dict
        """
        uri = "{}/https/certificaterequest".format(self.data['uri'])

        if bay_number:
            uri += "?bayNumber=%d" % (bay_number)

        return self._resource_helper.do_get(uri)

    @ensure_resource_client
    def import_certificate(self, certificate_data, bay_number=None):
        """
        Imports a signed server certificate into the enclosure.

        Args:
            certificate_data: Dictionary with Signed certificate and type.
            bay_number: OA to which the signed certificate will be imported.

        Returns:
            Enclosure.
        """
        uri = "{}/https/certificaterequest".format(self.data['uri'])

        if bay_number:
            uri += "?bayNumber=%d" % (bay_number)

        headers = {'Content-Type': 'application/json'}
        return self._resource_helper.do_put(uri, certificate_data, -1, headers)
