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
from hpOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file

config = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)


# Set the URI of existent resources to be added/removed to/from the scope
resource_uri_1 = "/rest/ethernet-networks/50e703bf-5103-459d-857c-7c49adcd37ca"
resource_uri_2 = "/rest/ethernet-networks/fa22aaaa-d348-41ad-85e7-1ca09c58891d"
resource_uri_3 = "/rest/fc-networks/56e05cd3-148a-4fc3-84f6-12ac58ae230f"

# Create a scope
print("Create the scope")
options = {
    "name": "SampleScope",
    "description": "Sample Scope description"
}
scope = oneview_client.scopes.create(options)
pprint(scope)

# Update the name of the scope
print("Update the scope")
scope['name'] = "SampleScopeRenamed"
scope = oneview_client.scopes.update(scope)
pprint(scope)

# Find the recently created scope by name
scope_by_name = oneview_client.scopes.get_by_name('SampleScopeRenamed')
print("Found scope by name: '{name}'.\n  uri = '{uri}'".format(**scope_by_name))

# Find the recently created scope by URI
scope_by_uri = oneview_client.scopes.get(scope['uri'])
print("Found scope by URI: '{uri}'.\n  name = '{name}'".format(**scope_by_uri))

# Get all scopes
print("Get all Scopes")
scopes = oneview_client.scopes.get_all()
pprint(scopes)

# Update the scope resource assignments
print("Update the scope resource assignments, adding two resources")
options = {
    "addedResourceUris": [resource_uri_1, resource_uri_2]
}
oneview_client.scopes.update_resource_assignments(scope['uri'], options)
print("  Done.")

print("Update the scope resource assignments, adding one resource and removing another previously added")
options = {
    "removedResourceUris": [resource_uri_1],
    "addedResourceUris": [resource_uri_3]
}
oneview_client.scopes.update_resource_assignments(scope['uri'], options)
print("  Done.")

# Delete the scope
oneview_client.scopes.delete(scope)
print("Scope deleted successfully.")
