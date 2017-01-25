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
from config_loader import try_load_from_file

config = {
    "ip": "",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

options = {
    "name": "OneViewSDK Test Network Set"
}

options_ethernet1 = {
    "name": "OneViewSDK Test Ethernet Network1",
    "vlanId": 200,
    "ethernetNetworkType": "Tagged",
    "purpose": "General",
    "smartLink": False,
    "privateNetwork": False,
    "connectionTemplateUri": None,
}

options_ethernet2 = {
    "name": "OneViewSDK Test Ethernet Network2",
    "vlanId": 201,
    "ethernetNetworkType": "Tagged",
    "purpose": "General",
    "smartLink": False,
    "privateNetwork": False,
    "connectionTemplateUri": None,
}
# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Create two Ethernet networks
ethernet_network1 = oneview_client.ethernet_networks.create(options_ethernet1)
ethernet_network2 = oneview_client.ethernet_networks.create(options_ethernet2)
print("Created ethernet-networks successfully.\n  uri = '%s' and \n\t'%s'" %
      (ethernet_network1['uri'], ethernet_network2['uri']))

# create Network set containing Ethernet networks
options['networkUris'] = [
    ethernet_network1['uri'],
    ethernet_network2['uri']
]
network_set = oneview_client.network_sets.create(options)
print('Created network-set {} successfully'.format(network_set['name']))

# Find recently created network set by name
network_set = oneview_client.network_sets.get_by(
    'name', 'OneViewSDK Test Network Set')[0]
print("Found network set by name: '%s'.\n  uri = '%s'" %
      (network_set['name'], network_set['uri']))

# Get network set without Ethernet networks
try:
    print("Get network-set without Ethernet:")
    net_set_without_ethernet = oneview_client.network_sets.get_without_ethernet(network_set['uri'])
    pprint(net_set_without_ethernet)
except HPOneViewException as e:
    print(e.msg)

# Update name of recently created network set
network_set['name'] = 'OneViewSDK Test Network Set Re-named'
network_set = oneview_client.network_sets.update(network_set)
print("Updated network set '%s' successfully.\n  uri = '%s'" %
      (network_set['name'], network_set['uri']))
print("  with attribute {'name': %s}" %
      network_set['name'])

# Get all network sets
print("Get all network sets")
net_sets = oneview_client.network_sets.get_all()
pprint(net_sets)

# Get all network sets without Ethernet
print("Get all network sets without Ethernet")
net_sets_without_ethernet = oneview_client.network_sets.get_all_without_ethernet()
pprint(net_sets_without_ethernet)

# Delete network set
oneview_client.network_sets.delete(network_set)
print("Successfully deleted network set")

# Delete Ethernet networks
oneview_client.ethernet_networks.delete(ethernet_network1)
oneview_client.ethernet_networks.delete(ethernet_network2)
print("Successfully deleted Ethernet networks")
