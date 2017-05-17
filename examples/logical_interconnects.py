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
from pprint import pprint

from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException
from examples.config_loader import try_load_from_file

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# To run this example, a logical interconnect name is required
logical_interconnect_name = ""

# To install the firmware driver, a firmware driver name is required
firmware_driver_name = ""

# An Enclosure name must be set to create/delete an interconnect at a given location
enclosure_name = ""

# Define the scope name to add the logical interconnect to it
scope_name = ""

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Get by name
print("\nGet a logical interconnect by name")
logical_interconnect = oneview_client.logical_interconnects.get_by_name(logical_interconnect_name)
pprint(logical_interconnect)

# Get installed firmware
print("\nGet the installed firmware for a logical interconnect that matches the specified name.")
firmwares = oneview_client.firmware_drivers.get_by('name', firmware_driver_name)
firmware = None
if firmwares:
    firmware = firmwares[0]

# Get scope to be added
print("\nGet the scope that matches the specified name.")
scope = oneview_client.scopes.get_by_name(scope_name)

print("\nGet the enclosure that matches the specified name.")
enclosures = oneview_client.enclosures.get_by('name', enclosure_name)
enclosure = None
if enclosures:
    enclosure = enclosures[0]

# Install the firmware to a logical interconnect
if firmware:
    print("\nInstall the firmware to a logical interconnect that matches the specified ID.")
    firmware_to_install = dict(
        command="Update",
        sppUri=firmware['uri']
    )
    installed_firmware = oneview_client.logical_interconnects.install_firmware(firmware_to_install,
                                                                               logical_interconnect['uri'])
    pprint(installed_firmware)

# Performs a patch operation
if scope:
    print("\nPatches the logical interconnect adding one scope to it")
    updated_logical_interconnect = oneview_client.logical_interconnects.patch(logical_interconnect['uri'],
                                                                              'replace',
                                                                              '/scopeUris',
                                                                              [scope['uri']])
    pprint(updated_logical_interconnect)

# Get all logical interconnects
print("\nGet all logical interconnects")
logical_interconnects = oneview_client.logical_interconnects.get_all()
for logical_interconnect in logical_interconnects:
    print('  Name: {name}').format(**logical_interconnect)

logical_interconnect = logical_interconnects[0]

# Get a logical interconnect by name
logical_interconnect = oneview_client.logical_interconnects.get_by_name(logical_interconnect['name'])
print("\nFound logical interconnect by name {name}.\n URI: {uri}").format(**logical_interconnect)

print("\nGet the Ethernet interconnect settings for the logical interconnect")
ethernet_settings = oneview_client.logical_interconnects.get_ethernet_settings(logical_interconnect['uri'])
pprint(ethernet_settings)

# Update the Ethernet interconnect settings for the logical interconnect
ethernet_settings = logical_interconnect['ethernetSettings'].copy()
ethernet_settings['macRefreshInterval'] = 10
logical_interconnect = oneview_client.logical_interconnects.update_ethernet_settings(logical_interconnect['uri'],
                                                                                     ethernet_settings,
                                                                                     force=True)
print("\nUpdated the ethernet settings")
print("  with attribute 'macRefreshInterval' = {macRefreshInterval}".format(**logical_interconnect['ethernetSettings']))

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
ethernet_networks = oneview_client.ethernet_networks.get_by('name', ethernet_network_options['name'])
if len(ethernet_networks) > 0:
    ethernet_network = ethernet_networks[0]
else:
    ethernet_network = oneview_client.ethernet_networks.create(ethernet_network_options)

logical_interconnect = oneview_client.logical_interconnects.update_internal_networks(logical_interconnect['uri'],
                                                                                     [ethernet_network['uri']])
print("\nUpdated internal networks on the logical interconnect")
print("  with attribute 'internalNetworkUris' = {internalNetworkUris}".format(**logical_interconnect))

# Get the internal VLAN IDs
print("\nGet the internal VLAN IDs for the provisioned networks on the logical interconnect")
internal_vlans = oneview_client.logical_interconnects.get_internal_vlans(logical_interconnect['uri'])
pprint(internal_vlans)

# Update the interconnect settings
print("\nUpdates the interconnect settings on the logical interconnect")
interconnect_settings = {
    'ethernetSettings': logical_interconnect['ethernetSettings'].copy(),
    'fcoeSettings': {}
}
interconnect_settings['ethernetSettings']['macRefreshInterval'] = 7
logical_interconnect = oneview_client.logical_interconnects.update_settings(logical_interconnect['uri'],
                                                                            interconnect_settings)
print("Updated interconnect settings on the logical interconnect")
print("  with attribute 'macRefreshInterval' = {macRefreshInterval}".format(**logical_interconnect['ethernetSettings']))
pprint(logical_interconnect)

# Get the SNMP configuration for the logical interconnect
print("\nGet the SNMP configuration for the logical interconnect")
snmp_configuration = oneview_client.logical_interconnects.get_snmp_configuration(logical_interconnect['uri'])
pprint(snmp_configuration)

# Update the SNMP configuration for the logical interconnect
try:
    print("\nUpdate the SNMP configuration for the logical interconnect")
    snmp_configuration['enabled'] = True
    logical_interconnect = oneview_client.logical_interconnects.update_snmp_configuration(logical_interconnect['uri'],
                                                                                          snmp_configuration)
    interconnect_snmp = logical_interconnect['snmpConfiguration']
    print("  Updated SNMP configuration at uri: {uri}\n  with 'enabled': '{enabled}'".format(**interconnect_snmp))
except HPOneViewException as e:
    print(e.msg)

# Get a collection of uplink ports from the member interconnects which are eligible for assignment to an analyzer port
print("\nGet a collection of uplink ports from the member interconnects which are eligible for assignment to "
      "an analyzer port on the logical interconnect")
unassigned_uplink_ports = oneview_client.logical_interconnects.get_unassigned_uplink_ports(logical_interconnect['uri'])
pprint(unassigned_uplink_ports)

# Get the port monitor configuration of a logical interconnect
print("\nGet the port monitor configuration of a logical interconnect")
monitor_configuration = oneview_client.logical_interconnects.get_port_monitor(logical_interconnect['uri'])
pprint(monitor_configuration)

# Update port monitor configuration of a logical interconnect
try:
    print("\nUpdate the port monitor configuration of a logical interconnect")
    monitor_configuration['enablePortMonitor'] = True
    logical_interconnect = oneview_client.logical_interconnects.update_port_monitor(
        logical_interconnect['uri'], monitor_configuration)
    print("  Updated port monitor at uri: {uri}\n  with 'enablePortMonitor': '{enablePortMonitor}'".format(
        **logical_interconnect['portMonitor']))
except HPOneViewException as e:
    print(e.msg)

# Get the telemetry configuration of the logical interconnect
print("\nGet the telemetry configuration of the logical interconnect")
telemetry_configuration_uri = logical_interconnect['telemetryConfiguration']['uri']
telemetry_configuration = oneview_client.logical_interconnects.get_telemetry_configuration(telemetry_configuration_uri)
pprint(telemetry_configuration)

print("\nUpdate the telemetry configuration")
telemetry_config = {
    "sampleCount": 12,
    "enableTelemetry": True,
    "sampleInterval": 300
}
logical_interconnect_updated = oneview_client.logical_interconnects.update_telemetry_configurations(
    configuration=telemetry_config, tc_id_or_uri=telemetry_configuration_uri)
pprint(logical_interconnect_updated)

# Update the configuration on the logical interconnect
print("\nUpdate the configuration on the logical interconnect")
logical_interconnect = oneview_client.logical_interconnects.update_configuration(logical_interconnect['uri'])
print("  Done.")

# Return the logical interconnect to a consistent state
print("\nReturn the logical interconnect to a consistent state")
logical_interconnect = oneview_client.logical_interconnects.update_compliance(logical_interconnect['uri'])
print("  Done. The current consistency state is {consistencyStatus}.".format(**logical_interconnect))

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
    interconnect = oneview_client.logical_interconnects.create_interconnect(location)
    pprint(interconnect)

    oneview_client.logical_interconnects.delete_interconnect(enclosure['uri'], bay)
    print("\nThe interconnect was successfully deleted.")

# Generate the forwarding information base dump file for the logical interconnect
print("\nGenerate the forwarding information base dump file for the logical interconnect")
fwd_info_datainfo = oneview_client.logical_interconnects.create_forwarding_information_base(logical_interconnect['uri'])
pprint(fwd_info_datainfo)

# Get the forwarding information base data for the logical interconnect
print("\nGet the forwarding information base data for the logical interconnect")
fwd_information = oneview_client.logical_interconnects.get_forwarding_information_base(logical_interconnect['uri'])
pprint(fwd_information)

# Get the QoS aggregated configuration for the logical interconnect.
print("\nGets the QoS aggregated configuration for the logical interconnect.")
qos = oneview_client.logical_interconnects.get_qos_aggregated_configuration(logical_interconnect['uri'])
pprint(qos)

# Update the QOS aggregated configuration
try:
    print("\nUpdate QoS aggregated settings on the logical interconnect")
    qos['activeQosConfig']['configType'] = 'Passthrough'
    li = oneview_client.logical_interconnects.update_qos_aggregated_configuration(logical_interconnect['uri'], qos)
    pprint(li['qosConfiguration'])
except HPOneViewException as e:
    print(e.msg)
