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
from hpOneView.exceptions import HPOneViewException
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

power_device_information = {
    "name": "MyPdd",
    "ratedCapacity": 40
}

power_device_information_ipdu = {
    "hostname": "172.18.8.12",
    "username": "",
    "password": ""
}

# Add a Power Device
power_device_added = oneview_client.power_devices.add(power_device_information)
print('Added Power Device {name} successfully'.format(**power_device_added))

# Add and Discover an iPDU
ipdu = oneview_client.power_devices.add_ipdu(power_device_information_ipdu)
print('Added iPDU {name} successfully'.format(**ipdu))

# Retrieve Power Device by URI
power_device = oneview_client.power_devices.get(power_device_added['uri'])
print('Get power device by URI, retrieved {name} successfully'.format(**power_device))

# Update the Power Device
power_device['name'] = "New Power Device Name"
power_device = oneview_client.power_devices.update(power_device)
print('Power device {name} updated successfully'.format(**power_device))

# Update the Power Device State
power_device = oneview_client.power_devices.get_by('deviceType', 'HPIpduOutlet')
power_device_state = oneview_client.power_devices.update_power_state(power_device[0]['uri'], {"powerState": "Off"})
print('Power device state updated successfully:')
pprint(power_device_state)

# Get the Power Device state
power_device_state = oneview_client.power_devices.get_power_state(power_device[0]['uri'])
print('Getting the new power device state:')
pprint(power_device_state)

# Update the Device Refresh State
power_device_refresh = oneview_client.power_devices.update_refresh_state(power_device[0]['uri'],
                                                                         {"refreshState": "RefreshPending"})
print('Power device state refreshed successfully:')
pprint(power_device_refresh)

# Update the Power Device UID State
power_device_state = oneview_client.power_devices.update_uid_state(power_device[0]['uri'], {"uidState": "On"})
print('Power device UID state updated successfully')

# Get the Power Device UID State
power_device_uid_state = oneview_client.power_devices.get_uid_state(power_device[0]['uri'])
print('Getting the new power device UID state: ' + power_device_uid_state)

# Get power device utilization with defaults
print("Get power device utilization")
try:
    power_devices_utilization = oneview_client.power_devices.get_utilization(power_device[0]['uri'])
    pprint(power_devices_utilization)
except HPOneViewException as e:
    print(e.msg['message'])

# Get power device utilization specifying parameters
print("Get power device statistics with parameters")
try:
    power_devices_utilization = oneview_client.power_devices.get_utilization(
        power_device[0]['uri'],
        fields='AveragePower',
        filter='startDate=2016-05-30T11:20:44.541Z,endDate=2016-05-30T19:20:44.541Z',
        view='hour')
    pprint(power_devices_utilization)
except HPOneViewException as e:
    print(e.msg['message'])

# Remove added power devices
oneview_client.power_devices.remove(ipdu)
oneview_client.power_devices.remove_synchronous(power_device_added)
print("Successfully removed power devices")
