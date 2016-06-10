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
from hpOneView.exceptions import HPOneViewException
from hpOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file

config = {
    "ip": "",
    "credentials": {
        "authLoginDomain": "",
        "userName": "administrator",
        "password": ""
    }
}

options = {
    "name": "OneViewSDK Test Ethernet Network",
    "vlanId": 200,
    "ethernetNetworkType": "Tagged",
    "purpose": "General",
    "smartLink": False,
    "privateNetwork": False,
    "connectionTemplateUri": None,
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Create an ethernet Network
ethernet_network = oneview_client.ethernet_networks.create(options)
print("Created ethernet-network '%s' sucessfully.\n  uri = '%s'" %
      (ethernet_network['name'], ethernet_network['uri']))

# Find recently created network by name
ethernet_network = oneview_client.ethernet_networks.get_by(
    'name', 'OneViewSDK Test Ethernet Network')[0]
print("Found ethernet-network by name: '%s'.\n  uri = '%s'" %
      (ethernet_network['name'], ethernet_network['uri']))

# Update purpose recently created network
ethernet_network['purpose'] = 'Management'
ethernet_network = oneview_client.ethernet_networks.update(ethernet_network)
print("Updated ethernet-network '%s' sucessfully.\n  uri = '%s'" %
      (ethernet_network['name'], ethernet_network['uri']))
print("  with attribute {'purpose': %s}" % ethernet_network['purpose'])

# Get all, with defaults
print("Get all ethernet-networks")
ethernet_nets = oneview_client.ethernet_networks.get_all()
pprint(ethernet_nets)

# Filter by name
print("Get all ethernet-networks filtering by name")
ethernet_nets_filtered = oneview_client.ethernet_networks.get_all(
    filter="\"'name'='OneViewSDK Test Ethernet Network'\"")
pprint(ethernet_nets_filtered)

# Get all sorting by name descending
print("Get all ethernet-networks sorting by name")
ethernet_nets_sorted = oneview_client.ethernet_networks.get_all(
    sort='name:descending')
pprint(ethernet_nets_sorted)

# Get the first 10 records
print("Get the first ten ethernet-networks")
ethernet_nets_limited = oneview_client.ethernet_networks.get_all(0, 10)
pprint(ethernet_nets_limited)

# Get by Id
try:
    print("Get an ethernet-network by id")
    ethernet_nets_byid = oneview_client.ethernet_networks.get(
        '42c25912-7350-411b-8b9c-daeef96fa775')
    pprint(ethernet_nets_byid)
except HPOneViewException as e:
    print(e.msg['message'])

# Get by Uri
print("Get an ethernet-network by uri")
ethernet_nets_by_uri = oneview_client.ethernet_networks.get(
    ethernet_network['uri'])
pprint(ethernet_nets_by_uri)

# Get URIs of associated profiles
print("Get associated profiles uri(s)")
associated_profiles = oneview_client.ethernet_networks.get_associated_profiles(
    'b17671cb-e106-4ccb-bb66-5f1d6f034ece')
pprint(associated_profiles)

# Get URIs of uplink port group
print("Get uplink port group uri(s)")
uplink_group = oneview_client.ethernet_networks.get_associated_uplink_groups(
    'b17671cb-e106-4ccb-bb66-5f1d6f034ece')
pprint(uplink_group)

# Delete the created network
oneview_client.ethernet_networks.delete(ethernet_network)
print("Sucessfully deleted ethernet-network")
