# -*- coding: utf-8 -*-
###
# (C) Copyright (2018) Hewlett Packard Enterprise Development LP
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

# Set api_version to 600, default is 300 and this API is introduced since API 600.
config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    },
    "api_version": 600
}

options = {
    "type": "Destination",
    "destinationAddress": "1.1.1.1",
    "userId": "a8cda396-584b-4b68-98a2-4ff9f4d3c01a",
    "port": 162
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Lists the appliance device read community
snmp_v3_trap_list = oneview_client.appliance_device_snmp_v3_trap_destinations.get_all()
print("\n## Got appliance SNMP v3 trap destination successfully!")
pprint(snmp_v3_trap_list)

# Get first element of the List
snmp_v3_trap = snmp_v3_trap_list.pop()

# Add appliance device SNMP v3 Trap Destination
snmp_v3_trap = oneview_client.appliance_device_snmp_v3_trap_destinations.create(options)
print("\n## Crate appliance SNMP v3 trap destination successfully!")
pprint(snmp_v3_trap)

# Change appliance device SNMP v3 Trap Destination - Only Community String and Port can be changed
snmp_v3_trap['destinationAddress'] = "1.1.9.9"
snmp_v3_trap = oneview_client.appliance_device_snmp_v3_trap_destinations.update(snmp_v3_trap)
print("\n## Update appliance SNMP v3 trap destination successfully!")
pprint(snmp_v3_trap)

# Delete Created Entry
del_result = oneview_client.appliance_device_snmp_v1_trap_destinations.delete(snmp_v3_trap)
print("\n## Delete appliance SNMP v3 trap destination successfully!")
pprint(del_result)
