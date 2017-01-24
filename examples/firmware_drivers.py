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

from config_loader import try_load_from_file
from hpOneView.oneview_client import OneViewClient

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<oneview_administrator_name>",
        "password": "<oneview_administrator_password>",
    }
}

firmware_uri = "/rest/firmware-drivers/hp-firmware-hdd-a1b08f8a6b-HPGH-1_1_x86_64"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)

# Get by Uri
print("Get firmware baseline resource by URI.")
founded_firmware = oneview_client.firmware_drivers.get(firmware_uri)
firmware_name = founded_firmware['name']
print("Found a firmware by uri: '{0}'.".format(firmware_name))

# Find an firmware by name
print("\nGet firmware baseline resource by name.")
founded_firmware = oneview_client.firmware_drivers.get_by('name', firmware_name)[0]
print("Found a firmware by name: '{name}'.\n  uri = '{uri}'".format(**founded_firmware))

# Get all firmwares
print("\nGets the list of firmware baseline resources managed by the appliance.")
all_firmwares = oneview_client.firmware_drivers.get_all()
for firmware in all_firmwares:
    print('  {name}'.format(**firmware))

# Remove the firmware
print("\nDelete the firmware baseline resource")
oneview_client.firmware_drivers.delete(founded_firmware)
print("Firmware deleted successfully")
