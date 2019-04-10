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

from config_loader import try_load_from_file
from hpOneView.oneview_client import OneViewClient

# This resource is only available on C7000 enclosures

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# To run the scope patch operations in this example, a scope name is required.
scope_name = "test"

options = {
    "name": "OneView Test Logical Switch Group",
    "switchMapTemplate": {
        "switchMapEntryTemplates": [{
            "logicalLocation": {
                "locationEntries": [{
                    "relativeValue": 1,
                    "type": "StackingMemberId"
                }]
            },
            "permittedSwitchTypeUri": ""
        }]
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
logical_switch_groups = oneview_client.logical_switch_groups
switch_types = oneview_client.switch_types

# Get all, with defaults
print("\nGet all Logical Switch Groups")
lsgs = logical_switch_groups.get_all()
for lsg in lsgs:
    print("   '{name}' at uri: '{uri}'".format(**lsg))

# Get the first 10 records, sorting by name descending, filtering by name
print("\nGet the first Logical Switch Groups, sorting by name descending, filtering by name")
lsgs = logical_switch_groups.get_all(
    0, 10, sort='name:descending', filter="\"'name'='OneView Test Logical Switch Group'\"")
for lsg in lsgs:
    print("   '{name}' at uri: '{uri}'".format(**lsg))

# Get Logical Switch by property
lsg_getby = logical_switch_groups.get_by('name', 'OneView Test Logical Switch Group')
if lsg_getby:
    print("\nFound logical switch group by name: '{name}' at uri = '{uri}'".format(**lsg_getby[0]))

    print("\nGet a Logical Switch Group by uri")
    lsg_byuri = logical_switch_groups.get_by_uri(lsg_getby[0]["uri"])
    print("   Found logical switch group '{name}' by uri '{uri}'".format(**lsg_byuri.data))

# Get switch type to use in creation of logical switch group
print("\nGet switch type to use in creation of logical switch group")
switch_type = switch_types.get_by_name("Arista 7060X")
print("   Found switch type at uri: '{}'".format(switch_type.data['uri']))

lsg = logical_switch_groups.get_by_name(options["name"])
if not lsg:
    # Create a logical switch group
    print("\nCreate a logical switch group")
    options['switchMapTemplate']['switchMapEntryTemplates'][0]['permittedSwitchTypeUri'] = switch_type.data['uri']
    lsg = oneview_client.logical_switch_groups.create(options)
    print("   Created logical switch group '{name}' at uri: '{uri}'".format(**lsg.data))

# Update a logical switch group
print("\nUpdate the name of a logical switch group")
lsg_to_update = lsg.data.copy()
lsg_to_update["name"] = "Renamed Logical Switch Group"
lsg.update(lsg_to_update)
print("   Successfully updated logical switch group with name '{name}'".format(**lsg.data))

# Update a logical switch group by adding another switch with a relative value of 2
print("\nUpdate a logical switch group by adding another switch with a relative value of 2")
lsg_to_update = lsg.data.copy()
switch_options = {
    "logicalLocation": {
        "locationEntries": [{
            "relativeValue": 2,
            "type": "StackingMemberId",
        }]
    },
    "permittedSwitchTypeUri": switch_type.data['uri']
}
lsg_to_update['switchMapTemplate']['switchMapEntryTemplates'].append(switch_options)
lsg.update(lsg_to_update)
pprint(lsg.data)

# Get scope to be added
print("\nGet the scope named '%s'." % scope_name)
scope = oneview_client.scopes.get_by_name(scope_name)

# Performs a patch operation on the Logical Switch Group
if scope and oneview_client.api_version <= 500:
    print("\nPatches the logical switch group assigning the '%s' scope to it." % scope_name)
    lsg.patch('replace',
              '/scopeUris',
              [scope['uri']])
    pprint(lsg.data)

# Delete a logical switch group
print("\nDelete the created logical switch group")
lsg.delete()
print("   Successfully deleted logical switch group")
