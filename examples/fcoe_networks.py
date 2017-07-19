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
from hpOneView.exceptions import HPOneViewException
from hpOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

options = {
    "name": "OneViewSDK Test FCoE Network",
    "vlanId": "201",
    "connectionTemplateUri": None,
}

# FCoE Network ID to perform a get by ID
fcoe_network_id = ""

# Scope name to perform the patch operation
scope_name = ""

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Create a FC Network
fcoe_network = oneview_client.fcoe_networks.create(options)
print("\nCreated fcoe-network '%s' successfully.\n  uri = '%s'" % (fcoe_network['name'], fcoe_network['uri']))

# Find recently created network by name
fcoe_network = oneview_client.fcoe_networks.get_by('name', 'OneViewSDK Test FCoE Network')[0]
print("\nFound fcoe-network by name: '%s'.\n  uri = '%s'" % (fcoe_network['name'], fcoe_network['uri']))

# Update autoLoginRedistribution from recently created network
fcoe_network['status'] = 'Warning'
fcoe_network = oneview_client.fcoe_networks.update(fcoe_network)
print("\nUpdated fcoe-network '%s' successfully.\n  uri = '%s'" % (fcoe_network['name'], fcoe_network['uri']))
print("  with attribute {'status': %s}" % fcoe_network['status'])

# Get all, with defaults
print("\nGet all fcoe-networks")
fcoe_nets = oneview_client.fcoe_networks.get_all()
pprint(fcoe_nets)

# Filter by name
print("\nGet all fcoe-networks filtering by name")
fcoe_nets_filtered = oneview_client.fcoe_networks.get_all(filter="\"'name'='OneViewSDK Test FCoE Network'\"")
pprint(fcoe_nets_filtered)

# Get all sorting by name descending
print("\nGet all fcoe-networks sorting by name")
fcoe_nets_sorted = oneview_client.fcoe_networks.get_all(sort='name:descending')
pprint(fcoe_nets_sorted)

# Get the first 10 records
print("\nGet the first ten fcoe-networks")
fcoe_nets_limited = oneview_client.fcoe_networks.get_all(0, 10)
pprint(fcoe_nets_limited)

# Get by ID
if fcoe_network_id:
    try:
        print("\nGet a fcoe-network by id")
        fcoe_nets_byid = oneview_client.fcoe_networks.get(fcoe_network_id)
        pprint(fcoe_nets_byid)
    except HPOneViewException as e:
        print(e.msg)

# Get by Uri
print("\nGet a fcoe-network by uri")
fcoe_nets_by_uri = oneview_client.fcoe_networks.get(fcoe_network['uri'])
pprint(fcoe_nets_by_uri)

# Adds ethernet to scope defined
if scope_name:
    print("\nGet scope then add the network to it")
    scope = oneview_client.scopes.get_by_name(scope_name)
    fcoe_with_scope = oneview_client.fcoe_networks.patch(fcoe_network['uri'],
                                                         'replace',
                                                         '/scopeUris',
                                                         [scope['uri']])
    pprint(fcoe_with_scope)

# Delete the created network
oneview_client.fcoe_networks.delete(fcoe_network)
print("\nSuccessfully deleted fcoe-network")
