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
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

options = {
    "name": "OneViewSDK Test FC Network",
    "connectionTemplateUri": None,
    "autoLoginRedistribution": True,
    "fabricType": "FabricAttach",
    "linkStabilityTime": 30,
}

# FC Network ID to perform a get by ID
fc_network_id = ""

# Scope name to perform the patch operation
scope_name = ""

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Create a FC Network
fc_network = oneview_client.fc_networks.create(options)
print("\nCreated fc-network '%s' successfully.\n  uri = '%s'" % (fc_network['name'], fc_network['uri']))

# Find recently created network by name
fc_network = oneview_client.fc_networks.get_by('name', 'OneViewSDK Test FC Network')[0]
print("\nFound fc-network by name: '%s'.\n  uri = '%s'" % (fc_network['name'], fc_network['uri']))

# Update autoLoginRedistribution from recently created network
fc_network['autoLoginRedistribution'] = False
fc_network = oneview_client.fc_networks.update(fc_network)
print("\nUpdated fc-network '%s' successfully.\n  uri = '%s'" % (fc_network['name'], fc_network['uri']))
print("  with attribute {'autoLoginRedistribution': %s}" % fc_network['autoLoginRedistribution'])

# Get all, with defaults
print("\nGet all fc-networks")
fc_nets = oneview_client.fc_networks.get_all()
pprint(fc_nets)

# Filter by name
print("\nGet all fc-networks filtering by name")
fc_nets_filtered = oneview_client.fc_networks.get_all(filter="\"'name'='OneViewSDK Test FC Network'\"")
pprint(fc_nets_filtered)

# Get all sorting by name descending
print("\nGet all fc-networks sorting by name")
fc_nets_sorted = oneview_client.fc_networks.get_all(sort='name:descending')
pprint(fc_nets_sorted)

# Get the first 10 records
print("\nGet the first ten fc-networks")
fc_nets_limited = oneview_client.fc_networks.get_all(0, 10)
pprint(fc_nets_limited)

# Get by Id
if fc_network_id:
    try:
        print("\nGet a fc-network by id")
        fc_nets_byid = oneview_client.fc_networks.get(fc_network_id)
        pprint(fc_nets_byid)
    except HPOneViewException as e:
        print(e.msg)

# Get by Uri
print("\nGet a fc-network by uri")
fc_nets_by_uri = oneview_client.fc_networks.get(fc_network['uri'])
pprint(fc_nets_by_uri)

# Adds ethernet to scope defined
if scope_name:
    print("\nGet scope then add the network to it")
    scope = oneview_client.scopes.get_by_name(scope_name)
    fc_with_scope = oneview_client.fc_networks.patch(fc_network['uri'],
                                                     'replace',
                                                     '/scopeUris',
                                                     [scope['uri']])
    pprint(fc_with_scope)

# Delete the created network
oneview_client.fc_networks.delete(fc_network)
print("\nSuccessfully deleted fc-network")
