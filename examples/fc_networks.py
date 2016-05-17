# -*- coding: utf-8 -*-

from pprint import pprint
from hpOneView.oneview_client import OneViewClient

config = {
    "ip": "172.16.102.59",
    "credentials": {
        "authLoginDomain": "",
        "userName": "administrator",
        "password": ""
    }
}

options = {
    "name": "OneViewSDK Test FC Network",
    "connectionTemplateUri": None,
    "autoLoginRedistribution": True,
    "fabricType": "FabricAttach",
}
oneview_client = OneViewClient(config)

# Create a FC Network
fc_network = oneview_client.fc_networks.create(options)
print("Created fc-network '%s' sucessfully.\n  uri = '%s'" % (fc_network['name'], fc_network['uri']))

# Find recently created network by name
fc_network = oneview_client.fc_networks.get_by('name', 'OneViewSDK Test FC Network')[0]
print("Found fc-network by name: '%s'.\n  uri = '%s'" % (fc_network['name'], fc_network['uri']))

# Update autoLoginRedistribution from recently created network
fc_network['autoLoginRedistribution'] = False
fc_network = oneview_client.fc_networks.update(fc_network)
print("Updated fc-network '%s' sucessfully.\n  uri = '%s'" % (fc_network['name'], fc_network['uri']))
print("  with attribute {'autoLoginRedistribution': %s}" % fc_network['autoLoginRedistribution'])

# Get all, with defaults
print("Get all fc-networks")
fc_nets = oneview_client.fc_networks.get_all()
pprint(fc_nets)

# Filter by name
print("Get all fc-networks filtering by name")
fc_nets_filtered = oneview_client.fc_networks.get_all(filter="\"'name'='OneViewSDK Test FC Network'\"")
pprint(fc_nets_filtered)

# Get all sorting by name descending
print("Get all fc-networks sorting by name")
fc_nets_sorted = oneview_client.fc_networks.get_all(sort='name:descending')
pprint(fc_nets_sorted)

# Get the first 10 records
print("Get the first ten fc-networks")
fc_nets_limited = oneview_client.fc_networks.get_all(0, 10)
pprint(fc_nets_limited)

# Get by Id
print("Get a fc-network by id")
fc_nets_byid = oneview_client.fc_networks.get('3518be0e-17c1-4189-8f81-83f3724f6155')
pprint(fc_nets_byid)

# Delete the created network
oneview_client.fc_networks.delete(fc_network)
print("Sucessfully deleted fc-network")
