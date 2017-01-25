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

PROVIDER_NAME = 'Brocade Network Advisor'

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<oneview_administrator_name>",
        "password": "<oneview_administrator_password>",
    }
}

# # To run this sample you must define the following resources for a Brocade Network Advisor
manager_host = None
manager_port = None
manager_username = None
manager_password = None

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Print default connection info for Brocade Network Advisor
print("Get {} default connection info".format(PROVIDER_NAME))
default_info = oneview_client.san_managers.get_default_connection_info(PROVIDER_NAME)
for property in default_info:
    print("   '{name}' - '{value}'".format(**property))

# Add a Brocade Network Advisor
provider_uri = oneview_client.san_managers.get_provider_uri(PROVIDER_NAME)
options = {
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
san_manager_brocade = oneview_client.san_managers.add(options, provider_uri)
pprint(san_manager_brocade)

# Refresh device manager
print("Refresh SAN manager")
info = {
    'refreshState': "RefreshPending"
}
san_manager_brocade = oneview_client.san_managers.update(resource=info, id_or_uri=san_manager_brocade['uri'])
print("   'refreshState' successfully updated to '{refreshState}'".format(**san_manager_brocade))

# Get SAN manager by uri
print("Get SAN manager by uri")
san_manager_byuri = oneview_client.san_managers.get(san_manager_brocade['uri'])
print("   Found '{name}' at uri: {uri}".format(**san_manager_byuri))

# Get all SAN managers
print("Get all SAN managers")
san_managers = oneview_client.san_managers.get_all()
for manager in san_managers:
    print("   '{name}' at uri: {uri}".format(**manager))

# Filter by name
print("Get a SAN Manager by name")
san_managers_by_name = oneview_client.san_managers.get_by_name(manager_host)
pprint(san_managers_by_name)

# Delete the SAN Manager previously created
oneview_client.san_managers.remove(san_manager_brocade)
print("The SAN Manager was deleted successfully.")
