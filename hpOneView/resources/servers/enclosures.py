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

from hpOneView.resources.resource import (Resource, ResourcePatchMixin,
                                          ResourceZeroBodyMixin, ResourceUtilizationMixin,
                                          ensure_resource_client)


class Enclosures(ResourcePatchMixin, ResourceZeroBodyMixin, ResourceUtilizationMixin, Resource):
    """
    Enclosures API client.

    """
    URI = '/rest/enclosures'

    def __init__(self, connection, data=None):
        super(Enclosures, self).__init__(connection, data)

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
        result = self._helper.get_all(start=start,
                                      count=count,
                                      filter=filter,
                                      sort=sort,
                                      scope_uris=scope_uris)

        return result

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
        return self.update_with_zero_body(uri=uri, timeout=timeout)

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

        return new_resource

    @ensure_resource_client
    def get_environmental_configuration(self):
        """
        Gets the settings that describe the environmental configuration (supported feature set, calibrated minimum &
        maximum power, location & dimensions, ...) of the enclosure resource.

        Returns:
            Settings that describe the environmental configuration.
        """
        uri = '{}/environmentalConfiguration'.format(self.data['uri'])
        return self._helper.do_get(uri)

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
        return self._helper.do_put(uri, configuration, timeout, None)

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
        return self._helper.do_put(uri, configuration, timeout, None)

    @ensure_resource_client
    def get_script(self):
        """
        Gets the script of the enclosure.

        Returns:
            Enclosure script.
        """
        uri = "{}/script".format(self.data['uri'])
        return self._helper.do_get(uri)

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
        return self._helper.do_get(uri)

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

        return self._helper.do_post(uri, csr_data, -1, headers)

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

        return self._helper.do_get(uri)

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
        return self._helper.do_put(uri, certificate_data, -1, headers)
