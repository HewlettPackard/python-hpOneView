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

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

options = {
    "destination": "1.1.1.1",
    "communityString": "testOne",
    "port": 162
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Add appliance device SNMP v1 Trap Destination
snmp_v1_trap = oneview_client.appliance_device_snmp_v1_trap_destinations.create(options)
snmp_v1_trap_uri = snmp_v1_trap['uri']
print("\n## Create appliance SNMP v1 trap destination successfully!")
pprint(snmp_v1_trap)

# Add appliance device SNMP v1 Trap Destination with ID
trap_id = 9
snmp_v1_trap = oneview_client.appliance_device_snmp_v1_trap_destinations.create(options, trap_id)
print("\n## Create appliance SNMP v1 trap destination successfully!")
pprint(snmp_v1_trap)

# Lists the appliance device SNMP v1 Trap Destination
snmp_v1_trap = oneview_client.appliance_device_snmp_v1_trap_destinations.get_all()
print("\n## Got appliance SNMP v1 trap destination successfully!")
pprint(snmp_v1_trap)

# Lists the appliance device SNMP v1 Trap Destination by destination (unique)
snmp_v1_trap = oneview_client.appliance_device_snmp_v1_trap_destinations.get_by('destination', '1.1.1.1')
print("\n## Got appliance SNMP v1 trap by destination successfully!")
pprint(snmp_v1_trap)

# Get by URI
print("Find an SNMP v1 trap destination by URI")
snmp_v1_trap = oneview_client.appliance_device_snmp_v1_trap_destinations.get(snmp_v1_trap_uri)
pprint(snmp_v1_trap)

# Change appliance device SNMP v1 Trap Destination - Only Community String and Port can be changed
snmp_v1_trap['communityString'] = 'testTwo'
snmp_v1_trap = oneview_client.appliance_device_snmp_v1_trap_destinations.update(snmp_v1_trap)
print("\n## Update appliance SNMP v1 trap destination successfully!")
pprint(snmp_v1_trap)

# Delete Created Entry
del_result = oneview_client.appliance_device_snmp_v1_trap_destinations.delete(snmp_v1_trap)
print("\n## Delete appliance SNMP v1 trap destination successfully!")
pprint(del_result)
