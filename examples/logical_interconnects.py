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
from pprint import pprint

from hpOneView.oneview_client import OneViewClient
from examples.config_loader import try_load_from_file

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# To run this example, a logical interconnect name is required
logical_interconnect_name = "SYN03_LE-SYN03_LIG"

# To install the firmware driver, a firmware driver name is required
firmware_driver_name = "HPE Synergy Custom SPP 2018110 2019 02 15, 2019.02.15.00"

# An Enclosure name must be set to create/delete an interconnect at a given location
enclosure_name = "SYN03_Frame1"

# Define the scope name to add the logical interconnect to it
scope_name = "test"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
logical_interconnects = oneview_client.logical_interconnects

# Get all logical interconnects
print("\nGet all logical interconnects")
all_logical_interconnects = logical_interconnects.get_all()
for logical_interconnect in all_logical_interconnects:
    print('  Name: {name}').format(**logical_interconnect)

# Get installed firmware
print("\nGet the installed firmware for a logical interconnect that matches the specified name.")
firmwares = oneview_client.firmware_drivers.get_by('name', firmware_driver_name)
firmware = firmwares[0] if firmwares else None

print("\nGet the enclosure that matches the specified name.")
enclosures = oneview_client.enclosures.get_by_name(enclosure_name)
enclosure = enclosures.data if enclosures else None

# Get a logical interconnect by name
logical_interconnect = logical_interconnects.get_by_name(logical_interconnect_name)
print("\nFound logical interconnect by name {name}.\n URI: {uri}").format(**logical_interconnect.data)
print(logical_interconnect.data)

# Install the firmware to a logical interconnect
if firmware:
    print("\nInstall the firmware to a logical interconnect that matches the specified ID.")
    firmware_to_install = dict(
        command="Update",
        sppUri=firmware['uri']
    )
    installed_firmware = logical_interconnect.install_firmware(firmware_to_install)
    pprint(installed_firmware)

# Get scope to be added
print("\nGet the scope that matches the specified name.")
scope = oneview_client.scopes.get_by_name(scope_name)

# Performs a patch operation
# This operation is not supported in API version 200 and 600.
if scope and oneview_client.api_version not in [200, 600]:
    print("\nPatches the logical interconnect adding one scope to it")
    logical_interconnect.patch('replace',
                               '/scopeUris',
                               [scope['uri']])
    pprint(logical_interconnect.data)

print("\nGet the Ethernet interconnect settings for the logical interconnect")
ethernet_settings = logical_interconnect.get_ethernet_settings()
pprint(ethernet_settings)

# Update the Ethernet interconnect settings for the logical interconnect
ethernet_settings = logical_interconnect.data['ethernetSettings'].copy()
ethernet_settings['macRefreshInterval'] = 10
logical_interconnect_updated = logical_interconnect.update_ethernet_settings(ethernet_settings)
print("\nUpdated the ethernet settings")
print("  with attribute 'macRefreshInterval' = {macRefreshInterval}".format(**logical_interconnect_updated['ethernetSettings']))

# Update the internal networks on the logical interconnect
ethernet_network_options = {
    "name": "OneViewSDK Test Ethernet Network on Logical Interconnect",
    "vlanId": 200,
    "ethernetNetworkType": "Tagged",
    "purpose": "General",
    "smartLink": False,
    "privateNetwork": False,
    "connectionTemplateUri": None,
}
ethernet_network = oneview_client.ethernet_networks.get_by_name(ethernet_network_options['name'])
if not ethernet_network:
    ethernet_network = oneview_client.ethernet_networks.create(ethernet_network_options)

logical_interconnect_updated = logical_interconnect.update_internal_networks([ethernet_network.data['uri']])
print("\nUpdated internal networks on the logical interconnect")
print("  with attribute 'internalNetworkUris' = {internalNetworkUris}".format(**logical_interconnect_updated))

# Get the internal VLAN IDs
print("\nGet the internal VLAN IDs for the provisioned networks on the logical interconnect")
internal_vlans = logical_interconnect.get_internal_vlans()
pprint(internal_vlans)

# Update the interconnect settings
# End-point supported only in api-versions 500 and below.
if oneview_client.api_version <= 500:
    print("\nUpdates the interconnect settings on the logical interconnect")
    interconnect_settings = {
        'ethernetSettings': logical_interconnect.data['ethernetSettings'].copy(),
        'fcoeSettings': {}
    }
    interconnect_settings['ethernetSettings']['macRefreshInterval'] = 7
    logical_interconnect_updated = logical_interconnect.update_settings(interconnect_settings)
    print("Updated interconnect settings on the logical interconnect")
    print("  with attribute 'macRefreshInterval' = {macRefreshInterval}".format(**logical_interconnect_updated['ethernetSettings']))
    pprint(logical_interconnect_updated)

# Get the SNMP configuration for the logical interconnect
print("\nGet the SNMP configuration for the logical interconnect")
snmp_configuration = logical_interconnect.get_snmp_configuration()
pprint(snmp_configuration)

# Update the SNMP configuration for the logical interconnect
print("\nUpdate the SNMP configuration for the logical interconnect")
snmp_configuration['enabled'] = True
logical_interconnect_updated = logical_interconnect.update_snmp_configuration(snmp_configuration)
interconnect_snmp = logical_interconnect_updated['snmpConfiguration']
print("  Updated SNMP configuration at uri: {uri}\n  with 'enabled': '{enabled}'".format(**interconnect_snmp))

# Get a collection of ports from the member interconnects which are eligible for assignment to an analyzer port
print("\nGet a collection of ports from the member interconnects which are eligible for assignment to "
      "an analyzer port on the logical interconnect")
unassigned_ports = logical_interconnect.get_unassigned_ports()
pprint(unassigned_ports)

# Get a collection of uplink ports from the member interconnects which are eligible for assignment to an analyzer port
print("\nGet a collection of uplink ports from the member interconnects which are eligible for assignment to "
      "an analyzer port on the logical interconnect")
unassigned_uplink_ports = logical_interconnect.get_unassigned_uplink_ports()
pprint(unassigned_uplink_ports)

# Get the port monitor configuration of a logical interconnect
print("\nGet the port monitor configuration of a logical interconnect")
monitor_configuration = logical_interconnect.get_port_monitor()
pprint(monitor_configuration)

# Update port monitor configuration of a logical interconnect
print("\nUpdate the port monitor configuration of a logical interconnect")
monitor_configuration['enablePortMonitor'] = True
logical_interconnect_updated = logical_interconnect.update_port_monitor(monitor_configuration)
print("  Updated port monitor at uri: {uri}\n  with 'enablePortMonitor': '{enablePortMonitor}'".format(
      **logical_interconnect_updated['portMonitor']))

# Update the configuration on the logical interconnect
print("\nUpdate the configuration on the logical interconnect")
logical_interconnect_updated = logical_interconnect.update_configuration()
print("  Done.")

# Return the logical interconnect to a consistent state
print("\nReturn the logical interconnect to a consistent state")
logical_interconnect_updated = logical_interconnect.update_compliance()
print("  Done. The current consistency state is {consistencyStatus}.".format(**logical_interconnect_updated))

# Generate the forwarding information base dump file for the logical interconnect
print("\nGenerate the forwarding information base dump file for the logical interconnect")
fwd_info_datainfo = logical_interconnect.create_forwarding_information_base()
pprint(fwd_info_datainfo)

# Get the forwarding information base data for the logical interconnect
print("\nGet the forwarding information base data for the logical interconnect")
fwd_information = logical_interconnect.get_forwarding_information_base()
pprint(fwd_information)

# Get the QoS aggregated configuration for the logical interconnect.
print("\nGets the QoS aggregated configuration for the logical interconnect.")
qos = logical_interconnect.get_qos_aggregated_configuration()
pprint(qos)

# Update the QOS aggregated configuration
print("\nUpdate QoS aggregated settings on the logical interconnect")
qos['activeQosConfig']['configType'] = 'Passthrough'
li = logical_interconnect.update_qos_aggregated_configuration(qos)
pprint(li['qosConfiguration'])

# Get the telemetry configuration of the logical interconnect
print("\nGet the telemetry configuration of the logical interconnect")
telemetry_configuration = logical_interconnect.get_telemetry_configuration()
pprint(telemetry_configuration)

# Update telemetry configuration
print("\nUpdate the telemetry configuration")
telemetry_config = {
    "sampleCount": 12,
    "enableTelemetry": True,
    "sampleInterval": 300
}
logical_interconnect_updated = logical_interconnect.update_telemetry_configurations(configuration=telemetry_config)
pprint(logical_interconnect_updated)

# Create an interconnect at a specified location
if enclosure['uri']:
    print("\nCreate an interconnect at the specified location")
    bay = 1
    location = {
        "locationEntries": [
            {"type": "Enclosure", "value": enclosure['uri']},
            {"type": "Bay", "value": bay}
        ]
    }
    interconnect = logical_interconnects.create_interconnect(location)
    pprint(interconnect)

    logical_interconnects.delete_interconnect(enclosure['uri'], bay)
    print("\nThe interconnect was successfully deleted.")
