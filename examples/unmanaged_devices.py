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

from config_loader import try_load_from_file
from hpOneView.oneview_client import OneViewClient

config = {
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

unmanaged_device_information = {
    "name": "MyUnmanagedDevice",
    "model": "Procurve 4200VL",
    "deviceType": "Server"
}

# Add an Unmanaged Device
unmanaged_device_added = oneview_client.unmanaged_devices.add(unmanaged_device_information)
print('Added Unmanaged Device "{name}" successfully\n'.format(**unmanaged_device_added))

# Retrieve Unmanaged Device by URI
unmanaged_device = oneview_client.unmanaged_devices.get(unmanaged_device_added['uri'])
print('Get unmanaged device by URI, retrieved "{name}" successfully\n'.format(**unmanaged_device))

# Update the Unmanaged Device
unmanaged_device['name'] = "New Unmanaged Device Name"
unmanaged_device = oneview_client.unmanaged_devices.update(unmanaged_device)
print('Unmanaged Device "{name}" updated successfully\n'.format(**unmanaged_device))

# Get all Unmanaged Devices
print("Get all Unmanaged Devices:")
unmanaged_devices_all = oneview_client.unmanaged_devices.get_all()
for unm_dev in unmanaged_devices_all:
    print(" - " + unm_dev['name'])

# Get unmanaged device environmental configuration
env_config = oneview_client.unmanaged_devices.get_environmental_configuration(unmanaged_device_added['uri'])
print('Get Environmental Configuration result:')
pprint(env_config)

# Remove added unmanaged device
oneview_client.unmanaged_devices.remove(unmanaged_device_added)
print("Successfully removed the unmanaged device")

# Add another unmanaged device and remove all
unmanaged_device_added = oneview_client.unmanaged_devices.add(unmanaged_device_information)
oneview_client.unmanaged_devices.remove_all("name matches '%'")
print("Successfully removed all the unmanaged device")
