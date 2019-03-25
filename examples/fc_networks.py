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
from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException
from config_loader import try_load_from_file

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    },
    "api_version": 800
}

options = {
    "name": "OneViewSDK Test FC Network",
    "connectionTemplateUri": None,
    "autoLoginRedistribution": True,
    "fabricType": "FabricAttach",
    "linkStabilityTime": 30,
}

# Scope name to perform the patch operation
scope_name = "test_scope"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)
fc_networks = oneview_client.fc_networks

# Get all, with defaults
print("\nGet all fc-networks")
fc_nets = fc_networks.get_all()
pprint(fc_nets)

# Get the first 10 records
print("\nGet the first ten fc-networks")
fc_nets_limited = fc_networks.get_all(0, 10)
pprint(fc_nets_limited)

# Filter by name
print("\nGet all fc-networks filtering by name")
fc_nets_filtered = fc_networks.get_all(filter="\"'name'='Updated FC'\"")
pprint(fc_nets_filtered)

# Get all sorting by name descending
print("\nGet all fc-networks sorting by name")
fc_nets_sorted = fc_networks.get_all(sort='name:descending')
pprint(fc_nets_sorted)

# Find recently created network by name
print("\nGet FC Network by name")
fc_network = fc_networks.get_by_name(options['name'])

if fc_network:
    print("\nFound fc-network by name: '%s'.\n  uri = '%s'" % (fc_network.data['name'], fc_network.data['uri']))
else:
    # Create a FcNetWork with the options provided
    fc_network = fc_networks.create(data=options)
    print("\nCreated a fc-network with name: '%s'.\n  uri = '%s'" % (fc_network.data['name'], fc_network.data['uri']))

# Get by uri
print("\nGet a fc-network by uri")
fc_nets_by_uri = fc_networks.get_by_uri(fc_network.data['uri'])
pprint(fc_nets_by_uri.data)

# Update autoLoginRedistribution from recently created network
data_to_update = {'autoLoginRedistribution': False,
                  'name': 'Updated FC'}
fc_network.update(data=data_to_update)
print("\nUpdated fc-network '%s' successfully.\n  uri = '%s'" % (fc_network.data['name'], fc_network.data['uri']))
print("  with attribute {'autoLoginRedistribution': %s}" % fc_network.data['autoLoginRedistribution'])

# Adds fcnetwork to scope defined
print("\nGet scope then add the network to it")
scope = oneview_client.scopes.get_by_name(scope_name)
print(scope['uri'])
if scope:
    try:
        fc_with_scope = fc_network.patch('replace',
                                         '/scopeUris',
                                         [scope['uri']])
        pprint(fc_with_scope)
    except HPOneViewException, e:
        print(e)

# Delete the created network
fc_network.delete()
print("\nSuccessfully deleted fc-network")
