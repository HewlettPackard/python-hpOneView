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

from config_loader import try_load_from_file
from hpOneView.exceptions import HPOneViewException
from hpOneView.oneview_client import OneViewClient

config = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

options = {
    "type": "logical-switch-group",
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

# Get switch type to use in creation of logical switch group
print("Get switch type to use in creation of logical switch group")
switch_type = oneview_client.switch_types.get_all()[0]
print("   Found switch type at uri: '{}'".format(switch_type['uri']))

# Create a logical switch group
print("Create a logical switch group")
options['switchMapTemplate']['switchMapEntryTemplates'][0]['permittedSwitchTypeUri'] = switch_type['uri']
created_lsg = oneview_client.logical_switch_groups.create(options)
print("   Created logical switch group '{name}' at uri: '{uri}'".format(**created_lsg))

# Get all, with defaults
print("Get all Logical Switch Groups")
lsgs = oneview_client.logical_switch_groups.get_all()
for lsg in lsgs:
    print("   '{name}' at uri: '{uri}'".format(**lsg))

# Get the first 10 records, sorting by name descending, filtering by name
print(
    "Get the first Logical Switch Groups, sorting by name descending, filtering by name")
lsgs = oneview_client.logical_switch_groups.get_all(
    0, 10, sort='name:descending', filter="\"'name'='OneView Test Logical Switch Group'\"")
for lsg in lsgs:
    print("   '{name}' at uri: '{uri}'".format(**lsg))

# Get Logical Switch by property
lsg_getby = oneview_client.logical_switch_groups.get_by('name', 'OneView Test Logical Switch Group')[0]
print(
    "Found logical switch group by name: '{name}' at uri = '{uri}'".format(**lsg_getby))

# Update a logical switch group
print("Update the name of a logical switch group")
lsg_to_update = created_lsg.copy()
lsg_to_update["name"] = "Renamed Logical Switch Group"
updated_lsg = oneview_client.logical_switch_groups.update(lsg_to_update)
print("   Successfully updated logical switch group with name '{name}'".format(**updated_lsg))

# Update a logical switch group by adding another switch with a relative value of 2
print(
    "Update a logical switch group by adding another switch with a relative value of 2")
lsg_to_update = updated_lsg.copy()
switch_options = {
    "logicalLocation": {
        "locationEntries": [{
            "relativeValue": 2,
            "type": "StackingMemberId",
        }]
    },
    "permittedSwitchTypeUri": switch_type['uri']
}
lsg_to_update['switchMapTemplate']['switchMapEntryTemplates'].append(switch_options)
updated_lsg = oneview_client.logical_switch_groups.update(lsg_to_update)
pprint(updated_lsg)

# Get by Id
try:
    lsg_id = "a98b4190-de9a-4b24-9579-f290d02de54e"
    print("Get a Logical Switch Group by id '{}'".format(lsg_id))
    lsg_byid = oneview_client.logical_switch_groups.get(lsg_id)
    print("   Found logical switch group '{name}' by id at uri '{uri}'".format(**lsg_byid))
except HPOneViewException as e:
    print(e.msg['message'])

# Get by uri
try:
    print("Get a Logical Switch Group by uri")
    lsg_byuri = oneview_client.logical_switch_groups.get(created_lsg["uri"])
    print("   Found logical switch group '{name}' by uri '{uri}'".format(**lsg_byuri))
except HPOneViewException as e:
    print(e.msg['message'])

# Delete a logical switch group
print("Delete the created logical switch group")
oneview_client.logical_switch_groups.delete(updated_lsg)
print("   Successfully deleted logical switch group")
