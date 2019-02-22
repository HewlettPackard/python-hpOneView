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

# Set api_version to 600, default is 300 and this API has been introduced since API 600.
config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    },
    "api_version": 600
}

options = {
    "type": "Users",
    "userName": "user1",
    "securityLevel": "Authentication and privacy",
    "authenticationProtocol": "SHA512",
    "authenticationPassphrase": "authPass",
    "privacyProtocol": "AES-256",
    "privacyPassphrase": "1234567812345678"
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Add appliance device SNMP v3 users
snmp_v3_user = oneview_client.appliance_device_snmp_v3_users.create(options)
snmp_v3_user_uri = snmp_v3_user['uri']
print("\n## Create appliance SNMP v3 user successfully!")
pprint(snmp_v3_user)

# Lists the appliance SNMPv3 users
snmp_v3_users_list = oneview_client.appliance_device_snmp_v3_users.get_all()
print("\n## Got appliance SNMP v3 users successfully!")
pprint(snmp_v3_users_list)

# Get first element of the List
snmp_v3_users = snmp_v3_users_list.pop()

# Get by URI
print("Find an SNMP v3 user by URI")
snmp_v3_user = oneview_client.appliance_device_snmp_v3_users.get(snmp_v3_user_uri)
pprint(snmp_v3_user)

# Change appliance device SNMP v3 users
snmp_v3_user['authenticationPassphrase'] = "newAuthPass"
snmp_v3_user['privacyPassphrase'] = "8765432187654321"
snmp_v3_user = oneview_client.appliance_device_snmp_v3_users.update(snmp_v3_user)
print("\n## Update appliance SNMP v3 user successfully!")
pprint(snmp_v3_user)

# Delete Created Entry
del_result = oneview_client.appliance_device_snmp_v3_users.delete(snmp_v3_user)
print("\n## Delete appliance SNMP v3 user successfully!")
pprint(del_result)
