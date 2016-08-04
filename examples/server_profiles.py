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
from hpOneView.oneview_client import OneViewClient

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<oneview_administrator_name>",
        "password": "<oneview_administrator_password>",
    }
}

# To run this sample you must define a server hardware type uri, an eclosure group uri and a server profile id with
# an associated server profile template
server_hardware_type_uri = None
enclosure_group_uri = None
server_profile_id = None

server_profile_name = "Profile101"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Create a server profile
print("\nCreate a basic connection-less assigned server profile")
basic_profile_options = dict(
    name=server_profile_name,
    serverHardwareTypeUri=server_hardware_type_uri,
    enclosureGroupUri=enclosure_group_uri
)
basic_profile = oneview_client.server_profiles.create(basic_profile_options)
pprint(basic_profile)

# Update bootMode from recently created profile
print("\nUpdate bootMode from recently created profile")
profile_to_update = basic_profile.copy()
profile_to_update["bootMode"] = dict(manageMode=True, mode="BIOS")
profile_updated = oneview_client.server_profiles.update(resource=profile_to_update, id_or_uri=profile_to_update["uri"])
pprint(profile_updated)

# Patch
print("\nUpdate the profile configuration from server profile template")
profile_updated = oneview_client.server_profiles.patch(id_or_uri=server_profile_id, operation="replace",
                                                       path="/templateCompliance", value="Compliant")
pprint(profile_updated)

# Get all
print("\nGet list of all server profiles")
all_profiles = oneview_client.server_profiles.get_all()
for profile in all_profiles:
    print('  %s' % profile['name'])

# Get by property
print("\nGet a list of server profiles that matches the specified macType")
profile_mac_type = all_profiles[1]["macType"]
profiles = oneview_client.server_profiles.get_by('macType', profile_mac_type)
for profile in profiles:
    print('  %s' % profile['name'])

# Get by name
print("\nGet a server profile by name")
profile = oneview_client.server_profiles.get_by_name(server_profile_name)
pprint(profile)

# Get by uri
print("\nGet a server profile by uri")
profile_uri = all_profiles[0]["uri"]
profile = oneview_client.server_profiles.get(profile_uri)
pprint(profile)

# Retrieve ServerProfile schema
print("\nRetrieve the generated ServerProfile schema")
schema = oneview_client.server_profiles.get_schema()
pprint(schema)

# Server profile compliance preview
print("\nGets the preview of manual and automatic updates required to make the server profile consistent "
      "with its template.")
schema = oneview_client.server_profiles.get_compliance_preview(server_profile_id)
pprint(schema)

# Get profile ports
print("\nRetrieve the port model associated with a server hardware type and enclosure group")
profile_ports = oneview_client.server_profiles.get_profile_ports(enclosureGroupUri=enclosure_group_uri,
                                                                 serverHardwareTypeUri=server_hardware_type_uri)
pprint(profile_ports)

# Get profile ports
# To run this example you must define a server hardware uri
server_hardware_uri = None
if server_hardware_uri:
    print("\nRetrieve the port model associated with a server hardware")
    profile_ports = oneview_client.server_profiles.get_profile_ports(serverHardwareUri=server_hardware_uri)
    pprint(profile_ports)

# Delete the created server profile
print("\nDelete the created server profile")
oneview_client.server_profiles.delete(basic_profile)
print("The server profile was successfully deleted.")
