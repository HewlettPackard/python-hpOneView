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

# To run this example fill the ip and the credentials bellow or use a configuration file
config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>",
    },
    "api_version": 800
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)
uplink_sets = oneview_client.uplink_sets


# To run this example you can define an logical interconnect uri (logicalInterconnectUri), ethernet network uri
# and ethernet name or the example will attempt to retrieve those automatically from the appliance.
logical_interconnect_uri = None
ethernet_network_uri = None
ethernet_network_name = None

# Attempting to get first LI and Ethernet uri and use them for this example
if logical_interconnect_uri is None:
    logical_interconnect_uri = oneview_client.logical_interconnects.get_all()[0]['uri']
if ethernet_network_uri is None:
    enet = oneview_client.ethernet_networks.get_all()
    ethernet_network_uri = enet[0]['uri']

    # Ethernet name to test add/remove of network uris
    if not ethernet_network_name:
        ethernet_network_name = enet[1]['name']

options = {
    "name": "Uplink Set Demo",
    "status": "OK",
    "logicalInterconnectUri": logical_interconnect_uri,
    "networkUris": [
        ethernet_network_uri
    ],
    "fcNetworkUris": [],
    "fcoeNetworkUris": [],
    "portConfigInfos": [],
    "connectionMode": "Auto",
    "networkType": "Ethernet",
    "manualLoginRedistributionState": "NotSupported",
}

# Get a paginated list of uplink set resources sorting by name ascending and filtering by status
print("\nGet a list of uplink sets")
all_uplink_sets = uplink_sets.get_all(0, 15, sort='name:ascending')
for uplink_set in all_uplink_sets:
    print('  %s' % uplink_set['name'])

if all_uplink_sets:
    # Get an uplink set resource by uri
    print("\nGet an uplink set by uri")
    uplink_uri = all_uplink_sets[0]['uri']
    uplink_set = uplink_sets.get_by_uri(uplink_uri)
    pprint(uplink_set.data)

# Get an uplink set resource by name
print("\nGet uplink set by name")
uplink_set = uplink_sets.get_by_name(options["name"])
if uplink_set:
    print("Found uplink set at uri '{uri}'\n  by name = '{name}'".format(**uplink_set.data))
else:
    # Create an uplink set
    print("\nCreate an uplink set")
    uplink_set = uplink_sets.create(options)
    print("Created uplink set '{name}' successfully.\n  uri = '{uri}'".format(**uplink_set.data))

# Update an uplink set
print("\nUpdate an uplink set")
uplink_set.data['name'] = 'Renamed Uplink Set Demo'
uplink_set.update(uplink_set.data)
print("Updated uplink set name to '{name}' successfully.\n  uri = '{uri}'".format(**uplink_set.data))

# Add an ethernet network to the uplink set
# To run this example you must define an ethernet network uri or ID below
if ethernet_network_name:
    print("\nAdd an ethernet network to the uplink set")
    uplink_added_ethernet = uplink_set.add_ethernet_networks(ethernet_network_name)
    print("The uplink set with name = '{name}' have now the networkUris:\n {networkUris}".format(**uplink_added_ethernet))

# Remove an ethernet network from the uplink set
# To run this example you must define an ethernet network uri or ID below
if ethernet_network_name:
    print("\nRemove an ethernet network of the uplink set")
    uplink_removed_ethernet = uplink_set.remove_ethernet_networks(ethernet_network_name)
    print("The uplink set with name = '{name}' have now the networkUris:\n {networkUris}".format(**uplink_removed_ethernet))

# Get the associated ethernet networks of an uplink set
print("\nGet the associated ethernet networks of the uplink set")
networks = uplink_set.get_ethernet_networks()
pprint(networks)

# Delete the recently created uplink set
print("\nDelete the uplink set")
uplink_set.delete()
print("Successfully deleted the uplink set")
