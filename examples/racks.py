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

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# NOTE: To run this sample you must define the name of an already managed enclosure
enclosure_name = "Encl1"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Retrieve enclosure using enclosure_name
enclosure = oneview_client.enclosures.get_by('name', enclosure_name)[0]

# Add empty rack with default values
print("\nAdd an empty rack with default values")
empty_rack_options = {
    "name": "OneViewSDK Test Empty Rack"
}
rack_empty = oneview_client.racks.add(empty_rack_options)
pprint(rack_empty)

# Add a rack
print("\nAdd rack with custom size and a single mounted enclosure at slot 20")
rack_options = {
    "uuid": "4b4b87e2-eea8-4c90-8eca-b72eaaeecggf",
    "name": "OneViewSDK Test Rack",
    "depth": 1500,
    "height": 2500,
    "width": 1200,
    "rackMounts": [{
        "mountUri": enclosure['uri'],
        "topUSlot": 20,
        "uHeight": 10
    }]
}
rack_custom = oneview_client.racks.add(rack_options)
pprint(rack_custom)

# Get device topology
print("\nGet device topology for '{name}'".format(**rack_custom))
topology = oneview_client.racks.get_device_topology(rack_custom['uri'])
pprint(topology)

# Get all racks
print("\nGet all racks")
racks_all = oneview_client.racks.get_all()
for rack in racks_all:
    print("   '{name}' at uri: {uri}".format(**rack))

# Get five racks, sorting by name ascending
print("\nGet five racks, sorted by name ascending")
count = 5
sort = 'name:asc'
racks_sorted = oneview_client.racks.get_all(count=count, sort=sort)
for rack in racks_sorted:
    print("   '{name}' at uri: {uri}".format(**rack))

# Get rack by UUID
print("\nGet rack by 'uuid': '{uuid}'".format(**rack_custom))
rack_byUuid = oneview_client.racks.get_by('uuid', rack_custom['uuid'])
print("   Found '{name}' at uri: {uri}".format(**rack))

# Update the name of a rack
print("\nUpdate the name of '{name}' at uri: '{uri}'".format(**rack_custom))
rack_custom['name'] = rack_custom['name'] + "-updated"
rack_custom = oneview_client.racks.update(rack_custom)
print("   Updated rack to have name: '{name}'".format(**rack_custom))

# Remove created racks
print("\nRemove created racks by resource")
oneview_client.racks.remove(rack_custom)
oneview_client.racks.remove(rack_empty)
print("   Done.")
