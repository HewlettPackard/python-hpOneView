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

# Scope name to perform the patch operation
scope_name = ""

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
fcoe_networks = oneview_client.fcoe_networks

# Get all, with defaults
print("\nGet all fcoe-networks")
fcoe_nets = fcoe_networks.get_all()
pprint(fcoe_nets)

# Filter by name
print("\nGet all fcoe-networks filtering by name")
fcoe_nets_filtered = fcoe_networks.get_all(filter="\"'name'='OneViewSDK Test FCoE Network'\"")
pprint(fcoe_nets_filtered)

# Get all sorting by name descending
print("\nGet all fcoe-networks sorting by name")
fcoe_nets_sorted = fcoe_networks.get_all(sort='name:descending')
pprint(fcoe_nets_sorted)

# Get the first 10 records
print("\nGet the first ten fcoe-networks")
fcoe_nets_limited = fcoe_networks.get_all(0, 10)
pprint(fcoe_nets_limited)

# Get by name
fcoe_network = fcoe_networks.get_by_name(options['name'])
if fcoe_network:
    print("\nGot fcoe-network by name uri={}".format(fcoe_network.data['uri']))
else:
    # Create a FC Network
    fcoe_network = fcoe_networks.create(options)
    print("\nCreated fcoe-network '%s' successfully.\n  uri = '%s'" % (fcoe_network.data['name'], fcoe_network.data['uri']))

# Update autoLoginRedistribution from recently created network
resource = fcoe_network.data.copy()
resource['status'] = 'Warning'
resource['name'] = "{}-Renamed".format(options["name"])
fcoe_network.update(resource)
print("\nUpdated fcoe-network '%s' successfully.\n  uri = '%s'" % (fcoe_network.data['name'], fcoe_network.data['uri']))
print("  with attribute {'status': %s}" % fcoe_network.data['status'])

# Get by Uri
print("\nGet a fcoe-network by uri")
fcoe_nets_by_uri = fcoe_networks.get_by_uri(fcoe_network.data['uri'])
pprint(fcoe_nets_by_uri.data)

# Adds FCOE network to scope defined
if scope_name:
    print("\nGet scope then add the network to it")
    scope = oneview_client.scopes.get_by_name(scope_name)
    fcoe_with_scope = fcoe_network.patch('replace',
                                         '/scopeUris',
                                         [scope['uri']])
    pprint(fcoe_with_scope.data)

# Delete the created network
fcoe_network.delete()
print("\nSuccessfully deleted fcoe-network")
