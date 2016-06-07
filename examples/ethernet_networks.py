# -*- coding: utf-8 -*-

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

# Delete the created network
oneview_client.ethernet_networks.delete(ethernet_network)
print("Sucessfully deleted ethernet-network")
