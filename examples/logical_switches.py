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

# This resource is only available on C7000 enclosures

config = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# A Logical Switch Group, the Switches IP address/host name, and credentials must be set to run this example
logical_switch_group_uri = '/rest/logical-switch-groups/af370d9a-f2f4-4beb-a1f1-670930d6741d'
management_host_1 = '172.18.16.1'
management_host_2 = '172.18.16.2'
ssh_username = ''
ssh_password = ''

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
        "logicalSwitchGroupUri": logical_switch_group_uri,
        "switchCredentialConfiguration": [
            {
                "snmpV1Configuration": {
                    "communityString": "public"
                },
                "logicalSwitchManagementHost": management_host_1,
                "snmpVersion": "SNMPv1",
                "snmpPort": 161
            }, {
                "snmpV1Configuration": {
                    "communityString": "public"
                },
                "logicalSwitchManagementHost": management_host_2,
                "snmpVersion": "SNMPv1",
                "snmpPort": 161
            }
        ]
    },
    "logicalSwitchCredentials": [switch_connection_properties, switch_connection_properties]
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Create a Logical Switch
logical_switch = oneview_client.logical_switches.create(options)
print("Created Logical Switch '{name}' successfully.\n  uri = '{uri}'".format(**logical_switch))

# Find the recently created Logical Switch by name
logical_switch = oneview_client.logical_switches.get_by('name', 'Test Logical Switch')[0]
print("Found Logical Switch by name: '{name}'.\n  uri = '{uri}'".format(**logical_switch))
pprint(logical_switch)

# Update the name of the Logical Switch
options_update = {
    "logicalSwitch": {
        "name": "Renamed Logical Switch",
        "uri": logical_switch['uri'],
        "switchCredentialConfiguration": logical_switch['switchCredentialConfiguration'],
        "logicalSwitchGroupUri": logical_switch_group_uri,
        "consistencyStatus": "CONSISTENT"
    },
    "logicalSwitchCredentials": [switch_connection_properties, switch_connection_properties]
}
logical_switch = oneview_client.logical_switches.update(options_update)
print("Updated Logical Switch successfully.\n  uri = '{uri}'".format(**logical_switch))
print("  with attribute name = {name}".format(**logical_switch))

# Get all, with defaults
print("Get all Logical Switches")
logical_switches = oneview_client.logical_switches.get_all()
for logical_switch in logical_switches:
    print('  Name: {name}').format(**logical_switch)

# Get by URI
print("Get a Logical Switch by URI")
logical_switch = oneview_client.logical_switches.get(logical_switch['uri'])
pprint(logical_switch)

# Reclaim the top-of-rack switches in the logical switch
print("Reclaim the top-of-rack switches in the logical switch")
logical_switch = oneview_client.logical_switches.refresh(logical_switch['uri'])
print("  Done.")

# Delete the Logical Switch
oneview_client.logical_switches.delete(logical_switch)
print("Logical switch deleted successfully.")
