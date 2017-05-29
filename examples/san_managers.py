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
from hpOneView.oneview_client import OneViewClient

# This example has options pre-defined for 'Brocade Network Advisor' and 'Cisco' type SAN Managers
PROVIDER_NAME = 'Cisco'

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<oneview_administrator_name>",
        "password": "<oneview_administrator_password>",
    }
}

# # To run this sample you must define the following resources for a Brocade Network Advisor
manager_host = '172.18.20.1'
manager_port = 161
manager_username = 'dcs-SHA'
manager_password = 'dcsdcsdcs'  # 'hpinvent!'

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Print default connection info for Brocade Network Advisor
print("\nGet {} default connection info:".format(PROVIDER_NAME))
default_info = oneview_client.san_managers.get_default_connection_info(PROVIDER_NAME)
for property in default_info:
    print("   '{name}' - '{value}'".format(**property))
# Add a Brocade Network Advisor
provider_uri = oneview_client.san_managers.get_provider_uri(PROVIDER_NAME)

options_for_brocade = {
    'providerDisplayName': PROVIDER_NAME,
    'connectionInfo': [
        {
            'name': 'Host',
            'value': manager_host
        },
        {
            'name': 'Port',
            'value': manager_port
        },
        {
            'name': 'Username',
            'value': manager_username
        },
        {
            'name': 'Password',
            'value': manager_password
        },
        {
            'name': 'UseSsl',
            'value': True
        }
    ]
}

options_for_cisco = {
    'providerDisplayName': PROVIDER_NAME,
    'connectionInfo': [
        {
            'name': 'Host',
            'displayName': 'Host',
            'required': True,
            'value': manager_host,
            'valueFormat': 'IPAddressOrHostname',
            'valueType': 'String'
        },
        {
            'name': 'SnmpPort',
            'displayName': 'SnmpPort',
            'required': True,
            'value': manager_port,
            'valueFormat': 'None',
            'valueType': 'Integer'
        },
        {
            'name': 'SnmpUserName',
            'displayName': 'SnmpUserName',
            'required': True,
            'value': manager_username,
            'valueFormat': 'None',
            'valueType': 'String'
        },
        {
            'name': 'SnmpAuthLevel',
            'displayName': 'SnmpAuthLevel',
            'required': True,
            'value': 'authnopriv',
            'valueFormat': 'None',
            'valueType': 'String'
        },
        {
            'name': 'SnmpAuthProtocol',
            'displayName': 'SnmpAuthProtocol',
            'required': False,
            'value': 'sha',
            'valueFormat': 'None',
            'valueType': 'String'
        },
        {
            'name': 'SnmpAuthString',
            'displayName': 'SnmpAuthString',
            'required': False,
            'value': manager_password,
            'valueFormat': 'SecuritySensitive',
            'valueType': 'String'
        },
        {
            'name': 'SnmpPrivProtocol',
            'displayName': 'SnmpPrivProtocol',
            'required': False,
            'value': '',
            'valueFormat': 'None',
            'valueType': 'String'
        },
        {
            'name': 'SnmpPrivString',
            'displayName': 'SnmpPrivString',
            'required': False,
            'value': '',
            'valueFormat': 'SecuritySensitive',
            'valueType': 'String'
        }
    ]
}

if PROVIDER_NAME == 'Brocade Network Advisor':
    san_manager = oneview_client.san_managers.add(options_for_brocade, provider_uri)
elif PROVIDER_NAME == 'Cisco':
    san_manager = oneview_client.san_managers.add(options_for_cisco, provider_uri)
else:
    provider_error_msg = 'Options for the "%s" provider not pre-added to this example file. Validate '
    provider_error_msg < 'and or create options for that provider and remove this exception.' % PROVIDER_NAME
    raise Exception(provider_error_msg)

pprint(san_manager)

print("\nRefresh SAN manager")
info = {
    'refreshState': "RefreshPending"
}
san_manager = oneview_client.san_managers.update(resource=info, id_or_uri=san_manager['uri'])
print("   'refreshState' successfully updated to '{refreshState}'".format(**san_manager))

print("\nGet SAN manager by uri")
san_manager_byuri = oneview_client.san_managers.get(san_manager['uri'])
print("   Found '{name}' at uri: {uri}".format(**san_manager_byuri))

print("\nGet all SAN managers")
san_managers = oneview_client.san_managers.get_all()
for manager in san_managers:
    print("   '{name}' at uri: {uri}".format(**manager))

print("\nGet a SAN Manager by name")
san_managers_by_name = oneview_client.san_managers.get_by_name(manager_host)
pprint(san_managers_by_name)

print("\nDelete the SAN Manager previously created...")
oneview_client.san_managers.remove(san_manager)
print("The SAN Manager was deleted successfully.")
