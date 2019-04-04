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
    },
    "api_version": 800
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
profile_templates = oneview_client.server_profile_templates

# Dependency resources
hardware_types = oneview_client.server_hardware_types
enclosure_groups = oneview_client.enclosure_groups

# These variables must be defined according with your environment
server_profile_name = "ProfileTemplate101"
hardware_type_name = "SY 480 Gen9 1"
enclosure_group_name = "SYN03_EC"
hardware_type_for_transformation = "SY 480 Gen9 2"
enclosure_group_for_transformation = "SYN03_EC"

hardware_type = hardware_types.get_by_name(hardware_type_name)
enclosure_group = enclosure_groups.get_by_name(enclosure_group_name)

# Get all
print("\nGet list of all server profile templates")
all_templates = profile_templates.get_all()
for template in all_templates:
    print('  %s' % template['name'])

# Get Server Profile Template by scope_uris
if oneview_client.api_version >= 600:
    server_profile_templates_by_scope_uris = profile_templates.get_all(
        scope_uris="\"'/rest/scopes/3bb0c754-fd38-45af-be8a-4d4419de06e9'\"")
    if len(server_profile_templates_by_scope_uris) > 0:
        print("Found %d Server profile Templates" % (len(server_profile_templates_by_scope_uris)))
        i = 0
        while i < len(server_profile_templates_by_scope_uris):
            print("Found Server Profile Template by scope_uris: '%s'.\n  uri = '%s'" % (server_profile_templates_by_scope_uris[i]['name'],
                                                                                        server_profile_templates_by_scope_uris[i]['uri']))
            i += 1
        pprint(server_profile_templates_by_scope_uris)
    else:
        print("No Server Profile Template found.")

# Get by property
print("\nGet a list of server profile templates that matches the specified macType")
template_mac_type = all_templates[1]["macType"]
templates = profile_templates.get_by('macType', template_mac_type)
for template in templates:
    print('  %s' % template['name'])

# Get available networks
print("\nGet available networks")
available_networks = profile_templates.get_available_networks(enclosureGroupUri=enclosure_group.data["uri"],
                                                              serverHardwareTypeUri=hardware_type.data["uri"])
print(available_networks)

# Get by name
print("\nGet a server profile templates by name")
template = oneview_client.server_profile_templates.get_by_name(server_profile_name)
if template:
    pprint(template.data)
else:
    # Create a server profile template
    print("Create a basic connection-less server profile template ")
    basic_template_options = dict(
        name=server_profile_name,
        serverHardwareTypeUri=hardware_type.data["uri"],
        enclosureGroupUri=enclosure_group.data["uri"]
    )
    template = profile_templates.create(basic_template_options)
    pprint(template.data)

# Update bootMode from recently created template
print("\nUpdate bootMode from recently created template")
template_to_update = template.data.copy()
template_to_update["bootMode"] = dict(manageMode=True, mode="BIOS")
template.update(template_to_update)
pprint(template.data)

# Get new profile
print("\nGet new profile")
profile = template.get_new_profile()
pprint(profile)

if oneview_client.api_version >= 300:
    # Get server profile template transformation
    print("\nGet a server profile template transformation")
    hardware = hardware_types.get_by_name(hardware_type_for_transformation)
    enclosure_group = enclosure_groups.get_by_name(enclosure_group_for_transformation)

    transformation = template.get_transformation(hardware.data["uri"],
                                                 enclosure_group.data["uri"])
    pprint(transformation)

# Delete the created template
print("\nDelete the created template")
template.delete()
print("The template was successfully deleted.")
