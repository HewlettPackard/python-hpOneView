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
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

options = {
    "name": "OneViewSDK Test FCoE Network",
    "vlanId": "201",
    "connectionTemplateUri": None,
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Create a FC Network
fcoe_network = oneview_client.fcoe_networks.create(options)
print("Created fcoe-network '%s' successfully.\n  uri = '%s'" % (fcoe_network['name'], fcoe_network['uri']))

# Find recently created network by name
fcoe_network = oneview_client.fcoe_networks.get_by('name', 'OneViewSDK Test FCoE Network')[0]
print("Found fcoe-network by name: '%s'.\n  uri = '%s'" % (fcoe_network['name'], fcoe_network['uri']))

# Update autoLoginRedistribution from recently created network
fcoe_network['status'] = 'Warning'
fcoe_network = oneview_client.fcoe_networks.update(fcoe_network)
print("Updated fcoe-network '%s' successfully.\n  uri = '%s'" % (fcoe_network['name'], fcoe_network['uri']))
print("  with attribute {'status': %s}" % fcoe_network['status'])

# Get all, with defaults
print("Get all fcoe-networks")
fcoe_nets = oneview_client.fcoe_networks.get_all()
pprint(fcoe_nets)

# Filter by name
print("Get all fcoe-networks filtering by name")
fcoe_nets_filtered = oneview_client.fcoe_networks.get_all(filter="\"'name'='OneViewSDK Test FCoE Network'\"")
pprint(fcoe_nets_filtered)

# Get all sorting by name descending
print("Get all fcoe-networks sorting by name")
fcoe_nets_sorted = oneview_client.fcoe_networks.get_all(sort='name:descending')
pprint(fcoe_nets_sorted)

# Get the first 10 records
print("Get the first ten fcoe-networks")
fcoe_nets_limited = oneview_client.fcoe_networks.get_all(0, 10)
pprint(fcoe_nets_limited)

# Get by Id
try:
    print("Get a fcoe-network by id")
    fcoe_nets_byid = oneview_client.fcoe_networks.get('452cf2a8-e5a0-4b9c-9961-0dc6deb80d01')
    pprint(fcoe_nets_byid)
except HPOneViewException as e:
    print(e.msg['message'])

# Get by Uri
print("Get a fcoe-network by uri")
fcoe_nets_by_uri = oneview_client.fcoe_networks.get(fcoe_network['uri'])
pprint(fcoe_nets_by_uri)

# Delete the created network
oneview_client.fcoe_networks.delete(fcoe_network)
print("Successfully deleted fcoe-network")
