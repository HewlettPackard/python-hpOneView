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
from hpOneView.exceptions import HPOneViewException

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# NOTE: This example requires a SPP and a hotfix inside the appliance.

options = {
    "customBaselineName": "FirmwareDriver1_Example"
}

firmware_name = "HPE Synergy Frame Link Module"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)

# Get a firmware by name
print("\nGet firmware by name.")
firmware = oneview_client.firmware_drivers.get_by('name', firmware_name)[0]
firmware_uri = firmware['uri']
print("Found a firmware by name: '{name}'.\n  uri = '{uri}'".format(**firmware))

# Get by Uri
print("\nGet firmware resource by URI.")
firmware = oneview_client.firmware_drivers.get(firmware_uri)
print("Found a firmware by uri: '{0}'.".format(firmware_name))

# Get all firmwares
print("\nGet list of firmwares managed by the appliance.")
all_firmwares = oneview_client.firmware_drivers.get_all()
for firmware in all_firmwares:
    print('  {name}'.format(**firmware))

# Getting a SPP and a hotfix from within the Appliance to use in the custom SPP creation.
try:
    hotfix = oneview_client.firmware_drivers.get_by('bundleType', "Hotfix")[0]
    options['hotfixUris'] = [hotfix['uri']]
    print("\nHotfix named %s found within appliance. Saving for custom SPP." % hotfix['name'])
except IndexError:
    raise HPOneViewException('No available hotfixes found within appliance. Stopping run.')

try:
    spp = oneview_client.firmware_drivers.get_by('bundleType', "SPP")[0]
    options['baselineUri'] = spp['uri']
    print("\nSPP named %s found within appliance. Saving for custom SPP." % spp['name'])
except IndexError:
    raise HPOneViewException('No available SPPs found within appliance. Stopping run.')

# Create the custom SPP
print("\nCreate the custom SPP '%s'" % options['customBaselineName'])
firmware = oneview_client.firmware_drivers.create(options)
print("  Custom SPP '%s' created successfully" % options['customBaselineName'])

# Remove the firmware
print("\nDelete the custom SPP '%s'" % options['customBaselineName'])
oneview_client.firmware_drivers.delete(firmware)
print("  Custom SPP '%s' deleted successfully" % options['customBaselineName'])
