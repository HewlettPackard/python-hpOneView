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
from config_loader import try_load_from_file

# This resource is only available on C7000 enclosures

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# A Logical Switch Group, the Switches IP address/host name, and credentials must be set to run this example
logical_switch_group_name = '<lsg_name>'
switch_ip_1 = '<switch_ip_or_hostname>'
switch_ip_2 = '<switch_ip_or_hostname>'
ssh_username = '<user_name_for_switches>'
ssh_password = '<password_for_switches>'

# To run the scope patch operations in this example, a scope name is required.
scope_name = "<scope_name>"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Check for existance of Logical Switch Group specified, otherwise stops execution
logical_switch_group = oneview_client.logical_switch_groups.get_by('name', logical_switch_group_name)[0]
if logical_switch_group:
    print('Found logical switch group "%s" with uri: %s' % (logical_switch_group['name'], logical_switch_group['uri']))
else:
    raise Exception('Logical switch group "%s" was not found on the appliance.' % logical_switch_group_name)

switch_connection_properties = {
    "connectionProperties": [{
        "propertyName": "SshBasicAuthCredentialUser",
        "value": ssh_username,
        "valueFormat": "Unknown",
        "valueType": "String"
    }, {
        "propertyName": "SshBasicAuthCredentialPassword",
        "value": ssh_password,
        "valueFormat": "SecuritySensitive",
        "valueType": "String"
    }]
}

options = {
    "logicalSwitch": {
        "name": "Test Logical Switch",
        "logicalSwitchGroupUri": logical_switch_group['uri'],
        "switchCredentialConfiguration": [
            {
                "snmpV1Configuration": {
                    "communityString": "public"
                },
                "logicalSwitchManagementHost": switch_ip_1,
                "snmpVersion": "SNMPv1",
                "snmpPort": 161
            }, {
                "snmpV1Configuration": {
                    "communityString": "public"
                },
                "logicalSwitchManagementHost": switch_ip_2,
                "snmpVersion": "SNMPv1",
                "snmpPort": 161
            }
        ]
    },
    "logicalSwitchCredentials": [switch_connection_properties, switch_connection_properties]
}

# Create a Logical Switch
logical_switch = oneview_client.logical_switches.create(options)
print("\nCreated Logical Switch '{name}' successfully.\n  uri = '{uri}'".format(**logical_switch))

# Find the recently created Logical Switch by name
logical_switch = oneview_client.logical_switches.get_by('name', 'Test Logical Switch')[0]
print("\nFound Logical Switch by name: '{name}'.\n  uri = '{uri}'".format(**logical_switch))

# Update the name of the Logical Switch
options_update = {
    "logicalSwitch": {
        "name": "Renamed Logical Switch",
        "uri": logical_switch['uri'],
        "switchCredentialConfiguration": logical_switch['switchCredentialConfiguration'],
        "logicalSwitchGroupUri": logical_switch_group['uri'],
        "consistencyStatus": "CONSISTENT"
    },
    "logicalSwitchCredentials": [switch_connection_properties, switch_connection_properties]
}
logical_switch = oneview_client.logical_switches.update(options_update)
print("\nUpdated Logical Switch successfully.\n  uri = '{uri}'".format(**logical_switch))
print("  with attribute name = {name}".format(**logical_switch))

# Get scope to be added
print("\nGet the scope named '%s'." % scope_name)
scope = oneview_client.scopes.get_by_name(scope_name)

# Performs a patch operation on the Logical Switch
if scope:
    print("\nPatches the logical switch assigning the '%s' scope to it." % scope_name)
    logical_switch = oneview_client.logical_switches.patch(logical_switch['uri'],
                                                           'replace',
                                                           '/scopeUris',
                                                           [scope['uri']])
    pprint(logical_switch)

# Get all, with defaults
print("\nGet all Logical Switches")
logical_switches = oneview_client.logical_switches.get_all()
for logical_switch in logical_switches:
    print('  Name: %s' % logical_switch['name'])

# Get by URI
print("\nGet a Logical Switch by URI")
logical_switch = oneview_client.logical_switches.get(logical_switch['uri'])
pprint(logical_switch)

# Reclaim the top-of-rack switches in the logical switch
print("\nReclaim the top-of-rack switches in the logical switch")
logical_switch = oneview_client.logical_switches.refresh(logical_switch['uri'])
print("  Done.")

# Delete the Logical Switch
oneview_client.logical_switches.delete(logical_switch)
print("\nLogical switch deleted successfully.")
