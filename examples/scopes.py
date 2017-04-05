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
        "userName": "<user>",
        "password": "<password>"
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

default_options = {
    "ethernetNetworkType": "Tagged",
    "purpose": "General",
    "smartLink": False,
    "privateNetwork": False,
    "connectionTemplateUri": None,
}

# Set the URI of existent resources to be added/removed to/from the scope
resource_uri_1 = oneview_client.ethernet_networks.get_by('name', 'Scope OneView SDK Ethernet 1')[0]['uri']
resource_uri_2 = oneview_client.ethernet_networks.get_by('name', 'Scope OneView SDK Ethernet 2')[0]['uri']
resource_uri_3 = oneview_client.ethernet_networks.get_by('name', 'Scope OneView SDK Ethernet 3')[0]['uri']

# Create a scope
print("\n## Create the scope")
options = {
    "name": "SampleScope",
    "description": "Sample Scope description"
}
scope = oneview_client.scopes.create(options)
pprint(scope)

# Update the name of the scope
print("\n## Update the scope")
scope['name'] = "SampleScopeRenamed"
scope = oneview_client.scopes.update(scope)
pprint(scope)

# Find the recently created scope by name
scope_by_name = oneview_client.scopes.get_by_name('SampleScopeRenamed')
print("\n## Found scope by name: '{name}'.\n  uri = '{uri}'".format(**scope_by_name))

# Find the recently created scope by URI
scope_by_uri = oneview_client.scopes.get(scope['uri'])
print("\n## Found scope by URI: '{uri}'.\n  name = '{name}'".format(**scope_by_uri))

# Get all scopes
print("\n## Get all Scopes")
scopes = oneview_client.scopes.get_all()
pprint(scopes)

# Update the scope resource assignments (Available only in API300)
try:
    print("\n## Update the scope resource assignments, adding two resources")
    options = {
        "addedResourceUris": [resource_uri_1, resource_uri_2]
    }
    oneview_client.scopes.update_resource_assignments(scope['uri'], options)
    print("  Done.")

    print("\n## Update the scope resource assignments, adding one resource and removing another previously added")
    options = {
        "removedResourceUris": [resource_uri_1],
        "addedResourceUris": [resource_uri_3]
    }
    oneview_client.scopes.update_resource_assignments(scope['uri'], options)
    print("  Done.")
except HPOneViewException as e:
    print(e.msg)

# Patch the scope assigning and unassigning two ethernet resources (Available only in API500)
try:
    print("\n## Patch the scope adding two resource uris")
    resource_list = [resource_uri_1, resource_uri_2]
    edited_scope = oneview_client.scopes.patch(scope['uri'], 'replace', '/addedResourceUris', resource_list)
    pprint(edited_scope)

    print("\n## Patch the scope removing the two previously added resource uris")
    edited_scope = oneview_client.scopes.patch(scope['uri'], 'replace', '/removedResourceUris', resource_list)
    pprint(edited_scope)
except HPOneViewException as e:
    print(e.msg)

# Delete the scope
oneview_client.scopes.delete(scope)
print("\n## Scope deleted successfully.")
