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

# This resource is only available on C7000 enclosures

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# provide info about your switch here
switch_id = "7a2704e2-564d-4163-8745-2a0b807a5e03"
switch_uri = "/rest/switches/" + switch_id

port_name = "1.1"
port_id = "{switch_id}:{port_name}".format(**locals())

# To run the scope patch operations in this example, a scope name is required.
scope_name = "scope1"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

print("\nGet a switch statistics:\n")
try:
    switch_statistics = oneview_client.switches.get_statistics(switch_uri)
    pprint(switch_statistics)
except HPOneViewException as e:
    print(e.msg)

print("\nGet a switch statistics with portName\n")
try:
    switch_statistics = oneview_client.switches.get_statistics(switch_uri, "1.2")
    pprint(switch_statistics)
except HPOneViewException as e:
    print(e.msg)

print("\nGet all switches in domain\n")
switches_all = oneview_client.switches.get_all()
pprint(switches_all)

try:
    print("\nGet switch by id\n")
    switch_by_id = oneview_client.switches.get(switch_id)
    pprint(switch_by_id)
except HPOneViewException as e:
    print(e.msg)

try:
    print("\nGet switch by uri\n")
    switch_by_uri = oneview_client.switches.get(switch_uri)
    pprint(switch_by_uri)
except HPOneViewException as e:
    print(e.msg)

try:
    print("\nGet environmental configuration of switch by id\n")
    switch_by_id = oneview_client.switches.get_environmental_configuration(switch_id)
    pprint(switch_by_id)
except HPOneViewException as e:
    print(e.msg)

try:
    print("\nGet environmental configuration of switch by uri\n")
    switch_env_conf = oneview_client.switches.get_environmental_configuration(switch_uri)
    pprint(switch_env_conf)
except HPOneViewException as e:
    print(e.msg)

try:
    print("\nGet switch by rack name\n")
    switch_by_rack_name = oneview_client.switches.get_by("rackName", "Test Name")
    pprint(switch_by_rack_name)
except HPOneViewException as e:
    print(e.msg)

# Get scope to be added
print("\nTrying to retrieve scope named '%s'." % scope_name)
scope = oneview_client.scopes.get_by_name(scope_name)

# Performs a patch operation on the Logical Switch
if scope and oneview_client.api_version == 500:
    print("\nPatches the switch assigning the '%s' scope to it." % scope_name)
    switch_by_uri = oneview_client.switches.patch(switch_by_uri['uri'],
                                                  'replace',
                                                  '/scopeUris',
                                                  [scope['uri']])
    pprint(switch_by_uri)

if oneview_client.api_version >= 300:
    try:
        print("\nUpdate the switch ports\n")

        ports_to_update = [{
            "enabled": True,
            "portId": port_id,
            "portName": port_name
        }]

        ports = oneview_client.switches.update_ports(id_or_uri=switch_id, ports=ports_to_update)
        print("  Done.")
    except HPOneViewException as e:
        print(e.msg)

# Delete the migrated switch
print("\nDelete a switch:\n")
try:
    oneview_client.switches.delete(switch_by_id)
    print("Successfully deleted the switch")
except HPOneViewException as e:
    print(e.msg)
