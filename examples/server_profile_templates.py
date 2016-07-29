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

server_profile_name = "ProfileTemplate101"
server_hardware_type_uri = "/rest/server-hardware-types/94B55683-173F-4B36-8FA6-EC250BA2328B"
enclosure_group_uri = "/rest/enclosure-groups/ad5e9e88-b858-4935-ba58-017d60a17c89"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Create a server profile template
print("Create a basic connection-less server profile template ")
basic_template_options = dict(
    name=server_profile_name,
    serverHardwareTypeUri=server_hardware_type_uri,
    enclosureGroupUri=enclosure_group_uri
)
basic_template = oneview_client.server_profile_templates.create(basic_template_options)
pprint(basic_template)

# Update bootMode from recently created template
print("\nUpdate bootMode from recently created template")
template_to_update = basic_template.copy()
template_to_update["bootMode"] = dict(manageMode=True, mode="BIOS")
updated = oneview_client.server_profile_templates.update(
    resource=template_to_update,
    id_or_uri=template_to_update["uri"]
)
pprint(updated)

# Get all
print("\nGet list of all server profile templates")
all_templates = oneview_client.server_profile_templates.get_all()
for template in all_templates:
    print('  %s' % template['name'])

# Get by property
print("\nGet a list of server profile templates that matches the specified macType")
template_mac_type = all_templates[1]["macType"]
templates = oneview_client.server_profile_templates.get_by('macType', template_mac_type)
for template in templates:
    print('  %s' % template['name'])

# Get by name
print("\nGet a server profile templates by name")
template = oneview_client.server_profile_templates.get_by_name(server_profile_name)
pprint(template)

# Get by uri
print("\nGet a server profile template by uri")
template_uri = all_templates[0]["uri"]
template = oneview_client.server_profile_templates.get(template_uri)
pprint(template)

# Get new profile
print("\nGet new profile")
profile = oneview_client.server_profile_templates.get_new_profile(template_uri)
pprint(profile)

# Delete the created template
print("\nDelete the created template")
oneview_client.server_profile_templates.delete(basic_template)
print("The template was successfully deleted.")
