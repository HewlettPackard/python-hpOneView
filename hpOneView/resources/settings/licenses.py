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


class Licenses(object):
    """
    Licenses. Gets a list of all license resources that are known by the appliance.

    """
    URI = '/rest/licenses'

    DEFAULT_VALUES = {
        '200': {'type': 'LicenseList'},
        '300': {"type": "LicenseList"},
        '500': {"type": "LicenseListV500"},
        '600': {"type": "LicenseListV500"}
    }


    def __init__(self, con):
        self._client = ResourceClient(con, self.URI)

    def create(self, resource, timeout=-1):
        """
        Add a license to the appliance.

        Args:
            resource (dict): Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Created resource.

        """
        return self._client.create(resource, timeout=timeout, default_values=self.DEFAULT_VALUES)


    def get_licenses(self):
        """
        Returns the range of possible API versions supported by the appliance.
        The response contains the current version and the minimum version.
        The current version is the recommended version to specify in the REST header.
        The other versions are supported for backward compatibility, but might not support the most current features.

        Returns:
            dict: The minimum and maximum supported API versions.
        """
        licenses = self._client.get(self.URI)
        return licenses


    def get_license_id(self, id_or_uri):
        """
        Gets the Fibre Channel network with the specified ID.

        Args:
            id_or_uri: ID or URI of Fibre Channel network.

        Returns:
            dict: The Fibre Channel network.
        """
        return self._client.get(id_or_uri)

    def delete(self, id_or_uri):
        """
        Deletes a Fibre Channel network.
        Any deployed connections that are using the network are placed in the 'Failed' state.

        Args:
            resource: dict object to delete
            force:
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates if the resource was successfully deleted.

        """
        return self._client.delete(id_or_uri)
 
