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


class SasLogicalInterconnects(object):
    """
    SAS Logical Interconnects API client.

    """
    URI = '/rest/sas-logical-interconnects'

    def __init__(self, con):
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, fields='', filter='', query='', sort='', view=''):
        """
        Gets a list of SAS Logical Interconnects based on optional sorting and filtering and constrained by start and
        count parameters.

        Args:
            start:
                 The first item to return, using 0-based indexing. If not specified, the default is 0 - start with the
                 first available item.
            count:
                The number of resources to return. A count of -1 requests all items. The actual number of items in
                the response may differ from the requested count if the sum of start and count exceeds the total number
                of items.
            fields:
                 Specifies which fields should be returned in the result set.
            filter (list or str):
                 A general filter/query string to narrow the list of items returned. The default is no filter; all
                 resources are returned.
            query:
                 A general query string to narrow the list of resources returned. The default is no query (all
                 resources are returned).
            sort:
                The sort order of the returned data set. By default, the sort order is based on create time, with the
                oldest entry first.
            view:
                 Returns a specific subset of the attributes of the resource or collection, by specifying the name of a
                 predefined view. The default view is expand (show all attributes of the resource and all elements of
                 collections of resources).

        Returns:
            list: A list of SAS logical interconnects.
        """
        return self._client.get_all(start=start, count=count, filter=filter, query=query, sort=sort, view=view,
                                    fields=fields)

    def get(self, id_or_uri):
        """
        Gets the SAS Logical Interconnect with the specified ID or URI.

        Args:
            id_or_uri:
                Can be either the SAS Logical Interconnect ID or URI.

        Returns:
            dict: SAS Logical Interconnect.
        """
        return self._client.get(id_or_uri)

    def get_by(self, field, value):
        """
        Gets all SAS Logical Interconnects that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of SAS Logical Interconnects.
        """
        return self._client.get_by(field, value)

    def update_firmware(self, firmware_information, id_or_uri):
        """
        Installs firmware to the member interconnects of a SAS Logical Interconnect.

        Args:
            firmware_information: Options to install firmware to a SAS Logical Interconnect.
            id_or_uri: Can be either the SAS Logical Interconnect ID or URI.

        Returns:
            dict: SAS Logical Interconnect Firmware.
        """
        firmware_uri = self._client.build_uri(id_or_uri) + "/firmware"
        return self._client.update(firmware_information, firmware_uri)

    def get_firmware(self, id_or_uri):
        """
        Gets baseline firmware information for a SAS Logical Interconnect.

        Args:
            id_or_uri: Can be either the SAS Logical Interconnect ID or URI.

        Returns:
            dict: SAS Logical Interconnect Firmware.
        """
        firmware_uri = self._client.build_uri(id_or_uri) + "/firmware"
        return self._client.get(firmware_uri)

    def update_compliance_all(self, information, timeout=-1):
        """
        Returns SAS Logical Interconnects to a consistent state. The current SAS Logical Interconnect state is
        compared to the associated SAS Logical Interconnect group.

        Args:
            information: Can be either the resource ID or URI.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: SAS Logical Interconnect.
        """

        uri = self.URI + "/compliance"
        return self._client.update(information, uri, timeout=timeout)

    def update_compliance(self, id_or_uri, timeout=-1):
        """
        Returns a SAS Logical Interconnect to a consistent state. The current SAS Logical Interconnect state is
        compared to the associated SAS Logical Interconnect group.

        Args:
            id_or_uri: Can be either the resource ID or URI.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: SAS Logical Interconnect.
        """
        uri = self._client.build_uri(id_or_uri) + "/compliance"
        return self._client.update_with_zero_body(uri, timeout=timeout)

    def replace_drive_enclosure(self, information, id_or_uri):
        """
        When a drive enclosure has been physically replaced, initiate the replacement operation that enables the
        new drive enclosure to take over as a replacement for the prior drive enclosure. The request requires
        specification of both the serial numbers of the original drive enclosure and its replacement to be provided.

        Args:
            information: Options to replace the drive enclosure.
            id_or_uri: Can be either the SAS Logical Interconnect ID or URI.

        Returns:
            dict: SAS Logical Interconnect.
        """

        uri = self._client.build_uri(id_or_uri) + "/replaceDriveEnclosure"
        return self._client.create(information, uri)

    def update_configuration(self, id_or_uri):
        """
        Asynchronously applies or re-applies the SAS Logical Interconnect configuration to all managed interconnects
        of a SAS Logical Interconnect.

        Args:
            id_or_uri: Can be either the SAS Logical Interconnect ID or URI.

        Returns:
            dict: SAS Logical Interconnect.
        """
        uri = self._client.build_uri(id_or_uri) + "/configuration"
        return self._client.update_with_zero_body(uri)
