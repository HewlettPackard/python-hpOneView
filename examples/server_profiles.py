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

from config_loader import try_load_from_file
from hpOneView.exceptions import HPOneViewException
from hpOneView.oneview_client import OneViewClient

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<oneview_administrator_name>",
        "password": "<oneview_administrator_password>",
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# To run this sample you must define a server hardware type uri and an enclosure group uri
enclosure_group_uri = None
server_hardware_type_uri = None

# To run the example 'get a specific storage system' you must define a storage system ID
storage_system_id = None

# To run the example 'get port model associated with a server hardware' you must define a server hardware uri
server_hardware_uri = None

try:
    # Create a server profile template to associate with the server profile
    basic_server_template = oneview_client.server_profile_templates.create(dict(
        name="ProfileTemplate101",
        serverHardwareTypeUri=server_hardware_type_uri,
        enclosureGroupUri=enclosure_group_uri
    ))
    server_template_uri = basic_server_template['uri']

    # Create a server profile
    print("\nCreate a basic connection-less assigned server profile")
    basic_profile_options = dict(
        name="Profile101",
        serverProfileTemplateUri=server_template_uri,
        serverHardwareTypeUri=server_hardware_type_uri,
        enclosureGroupUri=enclosure_group_uri
    )
    basic_profile = oneview_client.server_profiles.create(basic_profile_options)
    profile_uri = basic_profile["uri"]
    pprint(basic_profile)
except HPOneViewException as e:
    print(e.msg)

# Update bootMode from recently created profile
print("\nUpdate bootMode from recently created profile")
profile_to_update = basic_profile.copy()
profile_to_update["bootMode"] = dict(manageMode=True, mode="BIOS")
profile_updated = oneview_client.server_profiles.update(resource=profile_to_update, id_or_uri=profile_to_update["uri"])
pprint(profile_updated)

# Patch
print("\nUpdate the profile configuration from server profile template")
profile_updated = oneview_client.server_profiles.patch(id_or_uri=profile_uri, operation="replace",
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
profile = oneview_client.server_profiles.get_by_name("Profile101")
pprint(profile)

# Get by uri
print("\nGet a server profile by uri")
profile = oneview_client.server_profiles.get(profile_uri)
pprint(profile)

if oneview_client.api_version <= 500:
    # Retrieve ServerProfile schema
    # This method available only for API version <= 500
    print("\nRetrieve the generated ServerProfile schema")
    schema = oneview_client.server_profiles.get_schema()
    pprint(schema)

try:
    # Server profile compliance preview
    print("\nGets the preview of manual and automatic updates required to make the server profile consistent "
          "with its template.")
    schema = oneview_client.server_profiles.get_compliance_preview(profile_uri)
    pprint(schema)
except HPOneViewException as e:
    print(e.msg)

# Get profile ports
print("\nRetrieve the port model associated with a server hardware type and enclosure group")
profile_ports = oneview_client.server_profiles.get_profile_ports(enclosureGroupUri=enclosure_group_uri,
                                                                 serverHardwareTypeUri=server_hardware_type_uri)
pprint(profile_ports)

try:
    # Get profile ports
    if server_hardware_uri:
        print("\nRetrieve the port model associated with a server hardware")
        profile_ports = oneview_client.server_profiles.get_profile_ports(serverHardwareUri=server_hardware_uri)
        pprint(profile_ports)
except HPOneViewException as e:
    print(e.msg)

try:
    # Retrieve the error or status messages associated with the specified profile
    print("\nList profile status messages associated with a profile")
    messages = oneview_client.server_profiles.get_messages(profile_uri)
    pprint(messages)
except HPOneViewException as e:
    print(e.msg)

try:
    # Transform an server profile
    print("\nTransform an existing profile by supplying a new server hardware type and/or enclosure group.")
    server_transformed = oneview_client.server_profiles.get_transformation(
        basic_profile['uri'], enclosureGroupUri=enclosure_group_uri, serverHardwareTypeUri=server_hardware_type_uri)

    print("Transformation complete. Updating server profile with the new configuration.")
    profile_updated = oneview_client.server_profiles.update(server_transformed, server_transformed["uri"])
    pprint(profile_updated)
except HPOneViewException as e:
    print(e.msg)

try:
    # Get the list of networks and network sets that are available to a server profile along with their respective ports
    print("\nList all Ethernet networks associated with a server hardware type and enclosure group")
    available_networks = oneview_client.server_profiles.get_available_networks(
        enclosureGroupUri=enclosure_group_uri, serverHardwareTypeUri=server_hardware_type_uri, view='Ethernet')
    pprint(available_networks)
except HPOneViewException as e:
    print(e.msg)

try:
    # Get the all Ethernet networks associated with a server hardware type, enclosure group and scopeuris
    if oneview_client.api_version >= 600:
        enclosure_group_uri = "/rest/enclosure-groups/8cf8fd62-ad9f-4946-abf7-6dac9cb59253"
        server_hardware_type_uri = "/rest/server-hardware-types/B342B5D4-387D-4DEB-ADBB-9D7256DF2A47"
        available_networks = oneview_client.server_profiles.get_available_networks(enclosureGroupUri=enclosure_group_uri,
                                                                                   serverHardwareTypeUri=server_hardware_type_uri, view='Ethernet',
                                                                                   scope_uris="\"'/rest/scopes/3bb0c754-fd38-45af-be8a-4d4419de06e9'\"")
        if len(available_networks) > 0:
            pprint(available_networks)
        else:
            print("No Server Profiles Group found.")
except HPOneViewException as e:
    print(e.msg)

try:
    # Get the list of available servers
    print("\nList all available servers associated with a server hardware type and enclosure group")
    available_servers = oneview_client.server_profiles.get_available_servers(
        enclosureGroupUri=enclosure_group_uri, serverHardwareTypeUri=server_hardware_type_uri)
    pprint(available_servers)
except HPOneViewException as e:
    print(e.msg)

try:
    # List available storage systems
    print("\nList available storage systems associated with the given enclosure group URI and server hardware type URI")
    available_storage_systems = oneview_client.server_profiles.get_available_storage_systems(
        count=25, start=0, enclosureGroupUri=enclosure_group_uri, serverHardwareTypeUri=server_hardware_type_uri)
    pprint(available_storage_systems)
except HPOneViewException as e:
    print(e.msg)

try:
    # Get a specific storage system
    if storage_system_id:
        print("\nRetrieve a specific storage system associated with the given enclosure group URI, a server hardware"
              " type URI and a storage system ID")
        available_storage_system = oneview_client.server_profiles.get_available_storage_system(
            storageSystemId=storage_system_id, enclosureGroupUri=enclosure_group_uri,
            serverHardwareTypeUri=server_hardware_type_uri)
        pprint(available_storage_system)
except HPOneViewException as e:
    print(e.msg)

try:
    # List available targets
    print("\nList all available servers and bays for a given enclosure group.")
    available_targets = oneview_client.server_profiles.get_available_targets(enclosureGroupUri=enclosure_group_uri)
    pprint(available_targets)
except HPOneViewException as e:
    print(e.msg)


# Generate a new Server Profile Template based on an existing Server Profile
new_spt = oneview_client.server_profiles.get_new_profile_template(basic_profile['uri'])
print('\nNew SPT generated:')
pprint(new_spt)

new_spt['name'] = 'spt_generated_from_sp'

new_spt = oneview_client.server_profile_templates.create(new_spt)
print('\nNew SPT created successfully.')

oneview_client.server_profile_templates.delete(new_spt)
print('\nDropped recently created SPT.')


# Delete the created server profile
print("\nDelete the created server profile")
oneview_client.server_profiles.delete(basic_profile)
print("The server profile was successfully deleted.")

# Delete the created server profile template
oneview_client.server_profile_templates.delete(basic_server_template)

# Delete all server profile (filtering)
print("\nRemove all profiles that match the name 'Profile fake'")
# Create a new profile to delete
oneview_client.server_profiles.create(dict(
    name="Profile fake",
    serverHardwareTypeUri=server_hardware_type_uri,
    enclosureGroupUri=enclosure_group_uri
))
oneview_client.server_profiles.delete_all(filter="name='Profile fake'")
print("The server profiles were successfully deleted.")
