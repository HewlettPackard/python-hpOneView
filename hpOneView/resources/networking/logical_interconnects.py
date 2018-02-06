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


class LogicalInterconnects(object):
    """
    Logical Interconnects API client.

    """
    URI = '/rest/logical-interconnects'
    FIRMWARE_PATH = "/firmware"
    SNMP_CONFIGURATION_PATH = "/snmp-configuration"
    PORT_MONITOR_PATH = "/port-monitor"
    LOCATIONS_PATH = "/locations/interconnects"
    FORWARDING_INFORMATION_PATH = "/forwarding-information-base"
    QOS_AGGREGATED_CONFIGURATION = "/qos-aggregated-configuration"
    locations_uri = "{uri}{locations}".format(uri=URI, locations=LOCATIONS_PATH)

    SETTINGS_DEFAULT_VALUES = {
        '200': {"type": "InterconnectSettingsV3"},
        '300': {"type": "InterconnectSettingsV201"},
        '500': {"type": "InterconnectSettingsV201"},
        '600': {"type": "InterconnectSettingsV201"}
    }

    SETTINGS_ETHERNET_DEFAULT_VALUES = {
        '200': {"type": "EthernetInterconnectSettingsV3"},
        '300': {"type": "EthernetInterconnectSettingsV201"},
        '500': {"type": "EthernetInterconnectSettingsV201"},
        '600': {"type": "EthernetInterconnectSettingsV4"}
    }

    SETTINGS_TELEMETRY_CONFIG_DEFAULT_VALUES = {
        '200': {"type": "telemetry-configuration"},
        '300': {"type": "telemetry-configuration"},
        '500': {"type": "telemetry-configuration"},
        '600': {"type": "telemetry-configuration"}
    }

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a list of logical interconnects based on optional sorting and filtering and is constrained by start
        and count parameters.

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
            list: A list of logical interconnects.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def get(self, id_or_uri):
        """
        Gets a logical interconnect by ID or by URI.

        Args:
            id_or_uri: Can be either the logical interconnect id or the logical interconnect uri.

        Returns:
            dict: The logical interconnect.
        """
        return self._client.get(id_or_uri)

    def get_by_name(self, name):
        """
        Gets a logical interconnect by name.

        Args:
            name: Name of the logical interconnect.

        Returns:
            dict: Logical Interconnect.
        """
        logical_interconnects = self._client.get_all()
        result = [x for x in logical_interconnects if x['name'] == name]
        return result[0] if result else None

    def update_compliance(self, id_or_uri, timeout=-1):
        """
        Returns logical interconnects to a consistent state. The current logical interconnect state is
        compared to the associated logical interconnect group.

        Any differences identified are corrected, bringing the logical interconnect back to a consistent
        state. Changes are asynchronously applied to all managed interconnects. Note that if the changes detected
        involve differences in the interconnect map between the logical interconnect group and the logical interconnect,
        the process of bringing the logical interconnect back to a consistent state might involve automatically removing
        existing interconnects from management and/or adding new interconnects for management.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Logical Interconnect.
        """
        uri = self._client.build_uri(id_or_uri) + "/compliance"
        return self._client.update_with_zero_body(uri, timeout=timeout)

    def update_ethernet_settings(self, id_or_uri, configuration, force=False, timeout=-1):
        """
        Updates the Ethernet interconnect settings for the logical interconnect.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            configuration:  Ethernet interconnect settings.
            force: If set to true, the operation completes despite any problems with network connectivity or errors
                on the resource itself. The default is false.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Logical Interconnect.
        """
        uri = self._client.build_uri(id_or_uri) + "/ethernetSettings"
        return self._client.update(configuration, uri=uri, force=force, timeout=timeout)

    def update_internal_networks(self, id_or_uri, network_uri_list, force=False, timeout=-1):
        """
        Updates internal networks on the logical interconnect.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            network_uri_list: List of Ethernet network uris.
            force: If set to true, the operation completes despite any problems with network connectivity or errors
                on the resource itself. The default is false.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Logical Interconnect.
        """
        uri = self._client.build_uri(id_or_uri) + "/internalNetworks"
        return self._client.update(network_uri_list, uri=uri, force=force, timeout=timeout)

    def get_internal_vlans(self, id_or_uri):
        """
        Gets the internal VLAN IDs for the provisioned networks on a logical interconnect.

        Args:
            id_or_uri: Can be either the logical interconnect group id or the logical interconnect group uri

        Returns:
            dict: Collection of URIs

        """
        uri = self._client.build_uri(id_or_uri) + "/internalVlans"
        return self._client.get_collection(uri)

    def update_settings(self, id_or_uri, settings, force=False, timeout=-1):
        """
        Updates interconnect settings on the logical interconnect. Changes to interconnect settings are asynchronously
        applied to all managed interconnects.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            settings: Interconnect settings
            force: If set to true, the operation completes despite any problems with network connectivity or errors
                on the resource itself. The default is false.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Logical Interconnect
        """
        data = settings.copy()

        if 'ethernetSettings' in data:
            data['ethernetSettings'] = self._client.merge_default_values(data['ethernetSettings'],
                                                                         self.SETTINGS_ETHERNET_DEFAULT_VALUES)

        uri = self._client.build_uri(id_or_uri) + "/settings"
        return self._client.update(data, uri=uri, force=force, timeout=timeout,
                                   default_values=self.SETTINGS_DEFAULT_VALUES)

    def update_configuration(self, id_or_uri, timeout=-1):
        """
        Asynchronously applies or re-applies the logical interconnect configuration to all managed interconnects.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Logical Interconnect.
        """
        uri = self._client.build_uri(id_or_uri) + "/configuration"
        return self._client.update_with_zero_body(uri=uri, timeout=timeout)

    def get_snmp_configuration(self, id_or_uri):
        """
        Gets the SNMP configuration for a logical interconnect.

        Args:
            id_or_uri: Can be either the logical interconnect group id or the logical interconnect group uri.

        Returns:
            dict: SNMP configuration.
        """
        uri = self._client.build_uri(id_or_uri) + self.SNMP_CONFIGURATION_PATH
        return self._client.get(uri)

    def update_snmp_configuration(self, id_or_uri, configuration, timeout=-1):
        """
        Updates the SNMP configuration of a logical interconnect. Changes to the SNMP configuration are asynchronously
        applied to all managed interconnects.

        Args:
            id_or_uri: Can be either the logical interconnect id or the logical interconnect uri.
            configuration: snmp configuration.

        Returns:
            dict: The Logical Interconnect.
        """
        data = configuration.copy()
        if 'type' not in data:
            data['type'] = 'snmp-configuration'

        uri = self._client.build_uri(id_or_uri) + self.SNMP_CONFIGURATION_PATH
        return self._client.update(data, uri=uri, timeout=timeout)

    def get_unassigned_uplink_ports(self, id_or_uri):
        """
        Gets a collection of uplink ports from the member interconnects which are eligible for assignment to an
        analyzer port. To be eligible, a port must be a valid uplink, must not be a member of an existing uplink set,
        and must not currently be used for stacking.

        Args:
            id_or_uri: Can be either the logical interconnect group id or the logical interconnect group uri.

        Returns:
            dict: Collection of uplink ports.
        """
        uri = self._client.build_uri(id_or_uri) + "/unassignedUplinkPortsForPortMonitor"
        return self._client.get_collection(uri)

    def get_port_monitor(self, id_or_uri):
        """
        Gets the port monitor configuration of a logical interconnect.

        Args:
            id_or_uri: Can be either the logical interconnect id or the logical interconnect uri.
        Returns:
            dict: The Logical Interconnect.
        """
        uri = self._client.build_uri(id_or_uri) + self.PORT_MONITOR_PATH
        return self._client.get(uri)

    def update_port_monitor(self, id_or_uri, resource, timeout=-1):
        """
        Updates the port monitor configuration of a logical interconnect.

        Args:
            id_or_uri: Can be either the logical interconnect id or the logical interconnect uri.
            resource: Port monitor configuration.

        Returns:
            dict: Port monitor configuration.
        """
        data = resource.copy()
        if 'type' not in data:
            data['type'] = 'port-monitor'

        uri = self._client.build_uri(id_or_uri) + self.PORT_MONITOR_PATH
        return self._client.update(data, uri=uri, timeout=timeout)

    def get_telemetry_configuration(self, telemetry_configuration_uri):
        """
        Gets the telemetry configuration of a logical interconnect.

        Args:
            telemetry_configuration_uri: Telemetry Configuration URI.

        Returns:
            dict: Telemetry configuration.

        """
        return self._client.get(telemetry_configuration_uri)

    def create_interconnect(self, location_entries, timeout=-1):
        """
        Creates an interconnect at the given location.

        Warning:
            It does not create the LOGICAL INTERCONNECT itself.
            It will fail if no interconnect is already present on the specified position.

        Args:
            location_entries (dict): Dictionary with location entries.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Created interconnect.
        """
        return self._client.create(location_entries, uri=self.locations_uri, timeout=timeout)

    def delete_interconnect(self, enclosure_uri, bay, timeout=-1):
        """
        Deletes an interconnect from a location.

        Warning:
            This won't delete the LOGICAL INTERCONNECT itself and might cause inconsistency between the enclosure
            and Logical Interconnect Group.

        Args:
            enclosure_uri: URI of the Enclosure
            bay: Bay
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicating if the interconnect was successfully deleted.
        """
        uri = "{path}?location=Enclosure:{enclosure_uri},Bay:{bay}".format(path=self.LOCATIONS_PATH,
                                                                           enclosure_uri=enclosure_uri,
                                                                           bay=bay)
        return self._client.delete(uri, timeout=timeout)

    def get_firmware(self, id_or_uri):
        """
        Gets the installed firmware for a logical interconnect.

        Args:
            id_or_uri: Can be either the logical interconnect id or the logical interconnect uri.

        Returns:
            dict: LIFirmware.
        """
        firmware_uri = self._client.build_subresource_uri(id_or_uri, subresource_path=self.FIRMWARE_PATH)
        return self._client.get(firmware_uri)

    def install_firmware(self, firmware_information, id_or_uri):
        """
        Installs firmware to a logical interconnect. The three operations that are supported for the firmware
        update are Stage (uploads firmware to the interconnect), Activate (installs firmware on the interconnect),
        and Update (which does a Stage and Activate in a sequential manner).

        Args:
            firmware_information: Options to install firmware to a logical interconnect.
            id_or_uri: Can be either the logical interconnect id or the logical interconnect uri.

        Returns:
            dict
        """
        firmware_uri = self._client.build_subresource_uri(id_or_uri, subresource_path=self.FIRMWARE_PATH)
        return self._client.update(firmware_information, firmware_uri)

    def get_forwarding_information_base(self, id_or_uri, filter=''):
        """
        Gets the forwarding information base data for a logical interconnect. A maximum of 100 entries is returned.
        Optional filtering criteria might be specified.

        Args:
            id_or_uri:
                Can be either the logical interconnect id or the logical interconnect uri.
            filter (list or str):
                Filtering criteria may be specified using supported attributes: interconnectUri, macAddress,
                internalVlan, externalVlan, and supported relation = (Equals). macAddress is 12 hexadecimal digits with
                a colon between each pair of digits (upper case or lower case).
                The default is no filter; all resources are returned.

        Returns:
            list: A set of interconnect MAC address entries.
        """
        uri = self._client.build_uri(id_or_uri) + self.FORWARDING_INFORMATION_PATH
        return self._client.get_collection(uri, filter=filter)

    def create_forwarding_information_base(self, id_or_uri, timeout=-1):
        """
        Generates the forwarding information base dump file for a logical interconnect.

        Args:
            id_or_uri:
                Can be either the logical interconnect id or the logical interconnect uri.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        Returns: Interconnect Forwarding Information Base DataInfo.
        """
        uri = self._client.build_uri(id_or_uri) + self.FORWARDING_INFORMATION_PATH
        return self._client.create_with_zero_body(uri=uri, timeout=timeout)

    def get_qos_aggregated_configuration(self, id_or_uri):
        """
        Gets the QoS aggregated configuration for the logical interconnect.

        Args:
            id_or_uri:
                Can be either the logical interconnect id or the logical interconnect uri.

        Returns:
            dict: QoS Configuration.
        """
        uri = self._client.build_uri(id_or_uri) + self.QOS_AGGREGATED_CONFIGURATION
        return self._client.get(uri)

    def update_qos_aggregated_configuration(self, id_or_uri, qos_configuration, timeout=-1):
        """
        Updates the QoS aggregated configuration for the logical interconnect.

        Args:
            id_or_uri:
                Can be either the logical interconnect id or the logical interconnect uri.
            qos_configuration:
                QOS configuration.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        Returns:
            dict: Logical Interconnect.
        """
        uri = self._client.build_uri(id_or_uri) + self.QOS_AGGREGATED_CONFIGURATION
        return self._client.update(qos_configuration, uri=uri, timeout=timeout)

    def update_telemetry_configurations(self, tc_id_or_uri, configuration, id_or_uri=None, timeout=-1):
        """
        Updates the telemetry configuration of a logical interconnect. Changes to the telemetry configuration are
        asynchronously applied to all managed interconnects.

        Args:
            tc_id_or_uri:
                Can be either the telemetry configuration id or uri.
            configuration:
                The telemetry configuration for the logical interconnect.
            id_or_uri:
                Can be either the logical interconnect id or uri.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        Returns:
            dict: The Logical Interconnect.
        """
        uri = self._client.build_subresource_uri(id_or_uri, tc_id_or_uri, 'telemetry-configurations')
        return self._client.update(configuration, uri=uri, timeout=timeout,
                                   default_values=self.SETTINGS_TELEMETRY_CONFIG_DEFAULT_VALUES)

    def get_ethernet_settings(self, id_or_uri):
        """
        Gets the Ethernet interconnect settings for the Logical Interconnect.

        Args:
            id_or_uri:
                Can be either the logical interconnect id or uri.

        Returns:
            dict: Ethernet Interconnect Settings
        """
        uri = self._client.build_uri(id_or_uri) + '/ethernetSettings'
        return self._client.get(uri)

    def patch(self, id_or_uri, operation, path, value, timeout=-1):
        """
        Uses the PATCH to update a resource for a given logical interconnect.

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
        return self._client.patch(id_or_uri, operation, path, value, timeout=timeout)
