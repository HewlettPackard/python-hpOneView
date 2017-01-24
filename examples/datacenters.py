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
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

datacenter_information = {
    "name": "MyDatacenter",
    "width": 5000, "depth": 5000
}

# Add a Data Center
datacenter_added = oneview_client.datacenters.add(datacenter_information)
print('Added Data Center {name} successfully\n'.format(**datacenter_added))

# Retrieve Data Center by URI
datacenter = oneview_client.datacenters.get(datacenter_added['uri'])
print('Get Data Center by URI: retrieved {name} successfully\n'.format(**datacenter))

# Update the Data Center
datacenter['name'] = "New Data Center Name"
datacenter = oneview_client.datacenters.update(datacenter)
print('Data Center {name} updated successfully\n'.format(**datacenter))

# Get the Data Center by name
datacenter_list = oneview_client.datacenters.get_by('name', "New Data Center Name")
print('Get Data Center device by name: {name}\n'.format(**datacenter))

# Get the Data Center visual content
print("Getting the Data Center visual content...")
datacenter_visual_content = oneview_client.datacenters.get_visual_content(datacenter['uri'])
pprint(datacenter_visual_content)

# Remove added Data Center
oneview_client.datacenters.remove(datacenter)
print("\nSuccessfully removed the data center")

# Add a data center again and call Remove All
datacenter_added = oneview_client.datacenters.add(datacenter_information)
oneview_client.datacenters.remove_all(filter="name matches '%'")
print("\nSuccessfully removed all data centers")
