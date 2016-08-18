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

__title__ = 'server-profile-template'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP'
__license__ = 'MIT'
__status__ = 'Development'

from hpOneView.resources.resource import ResourceClient


class ServerProfileTemplate(object):
    URI = '/rest/server-profile-templates'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)
        self.__default_values = {
            'type': 'ServerProfileTemplateV1'
        }

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a list of server profile templates based on optional sorting and filtering, and constrained by start and
        count parameters.

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return.
                Providing a -1 for the count parameter will restrict the result set size to 64 server profile
                templates. The maximum number of profile templates is restricted to 256, i.e., if user requests more
                than 256, this will be internally limited to 256.
                The actual number of items in the response may differ from the
                requested count if the sum of start and count exceed the total number of items, or if returning the
                requested number of items would take too long.
            filter:
                A general filter/query string to narrow the list of items returned. The
                default is no filter - all resources are returned.
                Filters are supported for the name, description, affinity, macType, wwnType, serialNumberType, status,
                serverHardwareTypeUri, enclosureGroupUri, firmware.firmwareBaselineUri attributes.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time, with the oldest entry first.

        Returns:
            list: A list of server profile templates.

        """
        return self._client.get_all(start=start, count=count, filter=filter, sort=sort)

    def get(self, id_or_uri):
        """
        Gets a server profile template resource by ID or by uri.

        Args:
            id_or_uri: Could be either the server profile template resource id or uri.

        Returns:
            dict: The server profile template resource.
        """
        return self._client.get(id_or_uri=id_or_uri)

    def get_by(self, field, value):
        """
        Get all server profile templates that matches a specified filter.
        The search is case insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of server profile templates.
        """
        return self._client.get_by(field, value)

    def get_by_name(self, name):
        """
        Gets a server profile template by name.

        Args:
            name: Name of the server profile template.

        Returns:
            dict: The server profile template resource.
        """
        return self._client.get_by_name(name)

    def create(self, resource, timeout=-1):
        """
        Creates a server profile template.

        Args:
            resource (dict): Object to create.
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Created resource.

        """
        data = self.__default_values.copy()
        data.update(resource)
        return self._client.create(resource=data, timeout=timeout)

    def update(self, resource, id_or_uri):
        """
        Allows a server profile template object to have its configuration modified. These modifications can be as
        simple as a name or description change or much more complex changes around the networking configuration.
        It should be noted that selection of a virtual or physical MAC or Serial Number type is not mutable once a
        profile template has been created, and attempts to change those elements will not be applied to the target
        profile template. Connection requests can be one of the following types - port Auto, auto and explicit.
        An explicit request is where the request portId parameter includes the adapter, port and flexNic. An auto
        request  is where portId is set to "Auto" and a port auto request is where just the portId parameter includes
        just the adapter and port. The fields listed as required in the Request Body section need to be specified
        only when their associated parent is used.

        Args:
            id_or_uri: Could be either the template id or the template uri.
            resource (dict): Object to update.

        Returns:
            dict: The server profile template resource.
        """
        data = self.__default_values.copy()
        data.update(resource)
        return self._client.update(resource=data, uri=id_or_uri)

    def delete(self, resource, timeout=-1):
        """
        Deletes a server profile template object from the appliance based on its profile template UUID.

        Args:
            resource: Object to delete.
            timeout:
                Timeout in seconds. Wait task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.

        Returns:
            bool: Indicating if the resource was successfully deleted.
        """
        return self._client.delete(resource=resource, timeout=timeout)

    def get_new_profile(self, id_or_uri):
        """
        A profile object will be returned with the configuration based on this template. Specify the profile name and
        server hardware to assign. If template has any fibre channel connection which is specified as bootable but no
        boot target was defined, that connection will be instantiated as a non-bootable connection. So modify that
        connection to change it to bootable and to specify the boot target. This profile object can subsequently be
        used for the POST https://{appl}/rest/server-profiles/ API.

        Args:
            id_or_uri: Could be either the server profile template resource id or uri.

        Returns:
            dict: The server profile resource.
        """
        uri = self._client.build_uri(id_or_uri) + "/new-profile"
        return self._client.get(id_or_uri=uri)
