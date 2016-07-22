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

# To run this example fill the ip and the credentials bellow or use a configuration file
config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<oneview_administrator_name>",
        "password": "<oneview_administrator_password>",
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

options = {
    "name": "Test Snapshot",
    "description": "Description for the snapshot",
    "snapshotType": "PhysicalCopy"
}

oneview_client = OneViewClient(config)

# Get a paginated list of uplink set resources sorting by name ascending and filtering by status
print("\nGet a list of uplink sets")
uplink_sets = oneview_client.uplink_sets.get_all(0, 15, sort='name:ascending', filter="\"'status'='OK'\"")
for uplink_set in uplink_sets:
    print('  %s' % uplink_set['name'])

uplink_set_name = uplink_sets[0]['name']

# Get an uplink set resource by name
print("\nGet uplink set by name")
uplink_set = oneview_client.uplink_sets.get_by('name', uplink_set_name)[0]
print("Found uplink set at uri '{uri}'\n  by name = '{name}'".format(**uplink_set))

uplink_set_uri = uplink_sets[0]['uri']

# Get an uplink set resource by uri
print("\nGet an uplink set by uri")
try:
    uplink_set = oneview_client.uplink_sets.get(uplink_set_uri)
    pprint(uplink_set)
except HPOneViewException as e:
    print(e.msg)
