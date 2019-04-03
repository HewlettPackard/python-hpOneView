# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2019 Hewlett Packard Enterprise Development LP
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


from hpOneView.resources.resource import (Resource, ResourceUtilizationMixin,
                                          ResourcePatchMixin, ensure_resource_client)


class ServerHardware(ResourcePatchMixin, ResourceUtilizationMixin, Resource):
    """
    The server hardware resource is a representation of a physical server.
    The server hardware resource provides methods for server management tasks such
    as applying a profile, importing a server and managing an iLO.

    """
    URI = '/rest/server-hardware'

    def __init__(self, connection, data=None):
        super(ServerHardware, self).__init__(connection, data)

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
        return self.create(information, timeout=timeout)

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
        uri = "{}/discovery".format(self.URI)
        return self.create(information, uri=uri, timeout=timeout)

    def remove(self, force=False, timeout=-1):
        """
        Removes the rackserver with the specified URI.
        Note: This operation is only supported on appliances that support rack-mounted servers.

        Args:
            force (bool):
                If set to true, the operation completes despite any problems with
                network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates whether the resource was successfully removed.
        """
        return self.delete(force=force, timeout=timeout)

    @ensure_resource_client
    def get_bios(self):
        """
        Gets the list of BIOS/UEFI values currently set on the physical server.

        Returns:
            dict: Dictionary of BIOS/UEFI values.
        """
        uri = "{}/bios".format(self.data["uri"])
        return self._helper.do_get(uri)

    @ensure_resource_client
    def get_environmental_configuration(self):
        """
        Gets the settings that describe the environmental configuration (supported feature set, calibrated minimum and
        maximum power, location and dimensions, etc.) of the server hardware resource.

        Returns:
            dict: Environmental configuration settings.
        """
        uri = "{}/environmentalConfiguration".format(self.data["uri"])
        return self._helper.do_get(uri)

    @ensure_resource_client
    def update_environmental_configuration(self, configuration, timeout=-1):
        """
        Sets the calibrated max power of an unmanaged or unsupported server hardware resource.

        Args:
            configuration (dict): Environmental configuration.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Environmental configuration settings.
        """
        uri = "{}/environmentalConfiguration".format(self.data["uri"])
        return self._helper.update(configuration, uri, timeout=timeout)

    @ensure_resource_client
    def get_ilo_sso_url(self, ip=None):
        """
        Retrieves the URL to launch a Single Sign-On (SSO) session for the iLO web interface. If the server hardware is
        unsupported, the resulting URL will not use SSO and the iLO web interface will prompt for credentials.
        This is not supported on G7/iLO3 or earlier servers.

        Args:
            ip: IP address or host name of the server's iLO management processor

        Returns:
            URL
        """
        uri = "{}/iloSsoUrl".format(self.data["uri"])

        if ip:
            uri = "{}?ip={}".format(uri, ip)

        return self._helper.do_get(uri)

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
        return self._helper.get_all(start, count, filter, query, sort, '', '', uri)

    @ensure_resource_client
    def get_firmware(self):
        """
        Get the firmware inventory of a server.

        Note:
            This method is available for API version 300 or later.

        Returns:
            dict: Server Hardware firmware.
        """
        uri = "{}/firmware".format(self.data["uri"])
        return self._helper.do_get(uri)

    @ensure_resource_client
    def get_java_remote_console_url(self, ip=None):
        """
        Generates a Single Sign-On (SSO) session for the iLO Java Applet console and returns the URL to launch it.
        If the server hardware is unmanaged or unsupported, the resulting URL will not use SSO and the iLO Java Applet
        will prompt for credentials. This is not supported on G7/iLO3 or earlier servers.

        Args:
            ip: IP address or host name of the server's iLO management processor

        Returns:
            URL
        """
        uri = "{}/javaRemoteConsoleUrl".format(self.data["uri"])

        if ip:
            uri = "{}?ip={}".format(uri, ip)

        return self._helper.do_get(uri)

    @ensure_resource_client
    def update_mp_firware_version(self, timeout=-1):
        """
        Updates the iLO firmware on a physical server to a minimum ILO firmware version required by OneView to
        manage the server.

        Args:
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
        Returns:
            Resource
        """
        uri = "{}/mpFirmwareVersion".format(self.data["uri"])
        return self._helper.do_put(uri, None, timeout, None)

    @ensure_resource_client
    def update_power_state(self, configuration, timeout=-1):
        """
        Refreshes the server hardware to fix configuration issues.

        Args:
            configuration (dict): Power state configuration.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            Resource
        """
        uri = "{}/powerState".format(self.data["uri"])
        return self._helper.update(configuration, uri, timeout=timeout)

    @ensure_resource_client
    def refresh_state(self, configuration, timeout=-1):
        """
        Refreshes the server hardware to fix configuration issues.

        Args:
            configuration: Refresh state configuration.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            Resource
        """
        uri = "{}/refreshState".format(self.data["uri"])
        return self._helper.update(configuration, uri=uri, timeout=timeout)

    @ensure_resource_client
    def get_remote_console_url(self, ip=None):
        """
        Generates a Single Sign-On (SSO) session for the iLO Integrated Remote Console Application (IRC) and returns the
        URL to launch it. If the server hardware is unmanaged or unsupported, the resulting URL will not use SSO and the
        IRC application will prompt for credentials. Use of this URL requires a previous installation of the iLO IRC and
        is supported only on Windows clients.

        Args:
            ip: IP address or host name of the server's iLO management processor

        Returns:
            URL
        """
        uri = "{}/remoteConsoleUrl".format(self.data["uri"])

        if ip:
            uri = "{}?ip={}".format(uri, ip)

        return self._helper.do_get(uri)

    @ensure_resource_client
    def get_physical_server_hardware(self):
        """
        Information describing an 'SDX' partition including a list of physical server blades represented by a server
        hardware. Used with SDX enclosures only.

        Returns:
            Resource
        """
        uri = "{}/physicalServerHardware".format(self.data["uri"])
        return self._helper.do_get(uri)
