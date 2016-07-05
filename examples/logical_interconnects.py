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
from pprint import pprint

from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException
from config_loader import try_load_from_file

config = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}


# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Get all logical interconnects
print("Get all logical interconnects")
logical_interconnects = oneview_client.logical_interconnects.get_all()
for logical_interconnect in logical_interconnects:
    print('  Name: {}').format(logical_interconnect['name'])

logical_interconnect = logical_interconnects[0]

# Get a logical interconnect by name
logical_interconnect = oneview_client.logical_interconnects.get_by_name(logical_interconnect['name'])
print("Found logical interconnect by name {}.\n URI: {}").format(logical_interconnect['name'],
                                                                 logical_interconnect['uri'])

# Get by URI
try:
    print("Get a logical interconnect by URI")
    logical_interconnect_by_uri = oneview_client.logical_interconnects.get(logical_interconnect['uri'])
    pprint(logical_interconnect_by_uri)
except HPOneViewException as e:
    print(e.msg['message'])

# Update the Ethernet interconnect settings for the logical interconnect
ethernet_settings = logical_interconnect['ethernetSettings'].copy()
ethernet_settings['macRefreshInterval'] = 10
logical_interconnect = oneview_client.logical_interconnects.update_ethernet_settings(logical_interconnect['uri'],
                                                                                     ethernet_settings,
                                                                                     force=True)
current_mac_refresh_interval = str(logical_interconnect['ethernetSettings']['macRefreshInterval'])
print("Updated the ethernet settings")
print("  with attribute 'macRefreshInterval' = {}").format(current_mac_refresh_interval)

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
print("Updated internal networks on the logical interconnect")
print("  with attribute 'internalNetworkUris' = {}").format(logical_interconnect['internalNetworkUris'])

# Get the internal VLAN IDs
print("Get the internal VLAN IDs for the provisioned networks on the logical interconnect")
internal_vlans = oneview_client.logical_interconnects.get_internal_vlans(logical_interconnect['uri'])
pprint(internal_vlans)

# Update the interconnect settings
interconnect_settings = {
    'ethernetSettings': logical_interconnect['ethernetSettings'].copy(),
    'fcoeSettings': {}
}
interconnect_settings['ethernetSettings']['macRefreshInterval'] = 7

logical_interconnect = oneview_client.logical_interconnects.update_settings(logical_interconnect['uri'],
                                                                            interconnect_settings)
current_mac_refresh_interval = str(logical_interconnect['ethernetSettings']['macRefreshInterval'])

print("Updated interconnect settings on the logical interconnect")
print("  with attribute 'macRefreshInterval' = {}").format(current_mac_refresh_interval)
pprint(logical_interconnect)

# Get a collection of uplink ports from the member interconnects which are eligible for assignment to an analyzer port
print("Get a collection of uplink ports from the member interconnects which are eligible for assignment to "
      "an analyzer port on the logical interconnect")
unassigned_uplink_ports = oneview_client.logical_interconnects.get_unassigned_uplink_ports(logical_interconnect['uri'])
pprint(unassigned_uplink_ports)

# Get the telemetry configuration of the logical interconnect
print("Get the telemetry configuration of the logical interconnect")
telemetry_configuration_uri = logical_interconnect['telemetryConfiguration']['uri']
telemetry_configuration = oneview_client.logical_interconnects.get_telemetry_configuration(telemetry_configuration_uri)
pprint(telemetry_configuration)

# Update the configuration on the logical interconnect
print("Update the configuration on the logical interconnect")
logical_interconnect = oneview_client.logical_interconnects.update_configuration(logical_interconnect['uri'])
print("  Done.")

# Return the logical interconnect to a consistent state
print("Return the logical interconnect to a consistent state")
logical_interconnect = oneview_client.logical_interconnects.update_compliance(logical_interconnect['uri'])
print("  Done. The current consistency state is {}.").format(logical_interconnect['consistencyStatus'])
