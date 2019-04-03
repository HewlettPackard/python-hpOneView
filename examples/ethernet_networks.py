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

from config_loader import try_load_from_file
from hpOneView.oneview_client import OneViewClient

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    },
    "api_version": 800
}

options = {
    "name": "OneViewSDK Test Ethernet Network",
    "vlanId": 200,
    "ethernetNetworkType": "Tagged",
    "purpose": "General",
    "smartLink": False,
    "privateNetwork": False,
    "connectionTemplateUri": None
}

options_bulk = {
    "vlanIdRange": "1-5,7",
    "purpose": "General",
    "namePrefix": "TestNetwork",
    "smartLink": False,
    "privateNetwork": False,
    "bandwidth": {
        "maximumBandwidth": 10000,
        "typicalBandwidth": 2000
    }
}

# Scope name to perform the patch operation
scope_name = ""
ethernet_name = "OneViewSDK Test Ethernet Network"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)
ethernet_networks = oneview_client.ethernet_networks

# Get all, with defaults
print("\nGet all ethernet-networks")
ethernet_nets = ethernet_networks.get_all()
for net in ethernet_nets:
    print("   '{name}' at uri: '{uri}'".format(**net))

# Get by Uri
print("\nGet an ethernet-network by uri")
ethernet_network_uri = ethernet_nets[0]['uri']
ethernet_nets_by_uri = ethernet_networks.get_by_uri(ethernet_network_uri)
pprint(ethernet_nets_by_uri.data)

# Filter by name
print("\nGet all ethernet-networks filtering by name")
ethernet_nets_filtered = ethernet_networks.get_all(
    filter="\"'name'='OneViewSDK Test Ethernet Network'\"")
for net in ethernet_nets_filtered:
    print("   '{name}' at uri: '{uri}'".format(**net))

# Get all sorting by name descending
print("\nGet all ethernet-networks sorting by name")
ethernet_nets_sorted = ethernet_networks.get_all(sort='name:descending')
for net in ethernet_nets_sorted:
    print("   '{name}' at uri: '{uri}'".format(**net))

# Get the first 10 records
print("\nGet the first ten ethernet-networks")
ethernet_nets_limited = ethernet_networks.get_all(0, 10)
for net in ethernet_nets_limited:
    print("   '{name}' at uri: '{uri}'".format(**net))

# Find network by name
print("\nFind network by name")
ethernet_network = oneview_client.ethernet_networks.get_by_name(ethernet_name)
if ethernet_network:
    print("Found ethernet-network by name: '{name}'.\n   uri = '{uri}'" .format(**ethernet_network.data))
else:
    # Create an ethernet Network
    print("\nCreate an ethernet network")
    ethernet_network = oneview_client.ethernet_networks.create(options)
    print("Created ethernet-network '{name}' successfully.\n   uri = '{uri}'" .format(**ethernet_network.data))

# Create bulk ethernet networks
print("\nCreate bulk ethernet networks")
ethernet_nets_bulk = ethernet_networks.create_bulk(options_bulk)
pprint(ethernet_nets_bulk)

# Update purpose recently created network
print("\nUpdate the purpose attribute from the recently created network")
ethernet_data = ethernet_network.data
ethernet_data['purpose'] = 'Management'
ethernet_network = ethernet_network.update(ethernet_data)
print("Updated ethernet-network '{name}' successfully.\n   uri = '{uri}'\n   with attribute ['purpose': {purpose}]"
      .format(**ethernet_network.data))

# Get URIs of associated profiles
print("\nGet associated profiles uri(s)")
associated_profiles = ethernet_network.get_associated_profiles()
pprint(associated_profiles)

# Get URIs of uplink port group
print("\nGet uplink port group uri(s)")
uplink_group_uris = ethernet_network.get_associated_uplink_groups()
pprint(uplink_group_uris)

# Get the associated uplink set resources
print("\nGet associated uplink sets")
uplink_sets = oneview_client.uplink_sets
for uri in uplink_group_uris:
    uplink = uplink_sets.get_by_uri(uri)
    pprint(uplink.data)

# Adds ethernet to scope defined
if scope_name:
    print("\nGet scope then add the network to it")
    scope = oneview_client.scopes.get_by_name(scope_name)
    ethernet_with_scope = ethernet_network.patch('replace',
                                                 '/scopeUris',
                                                 [scope['uri']])
    pprint(ethernet_with_scope)

# Delete bulk ethernet networks
print("\nDelete bulk ethernet networks")
for net in ethernet_nets_bulk:
    ethernet_networks.get_by_uri(net['uri']).delete()
print("   Done.")

# Delete the created network
print("\nDelete the ethernet network")
ethernet_network.delete()
print("Successfully deleted ethernet-network")
