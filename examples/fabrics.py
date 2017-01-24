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
from hpOneView.exceptions import HPOneViewException
from hpOneView.oneview_client import OneViewClient

config = {
    "ip": "",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# To run this example you must to defined here a fabric id
fabric_id = 'a7896ce7-c11d-4658-829d-142bc66a85e4'

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Get all fabrics
print("Get all fabrics")
fabrics = oneview_client.fabrics.get_all()
pprint(fabrics)

# Get all sorting by name descending
print("\nGet all fabrics sorting by name")
fabrics_sorted = oneview_client.fabrics.get_all(sort='name:descending')
pprint(fabrics_sorted)

# Get by Id
try:
    print("\nGet a fabric by id")
    fabrics_byid = oneview_client.fabrics.get(fabric_id)
    pprint(fabrics_byid)
except HPOneViewException as e:
    print(e.msg)

# Get by name
print("\nGet a fabrics by name")
fabric_byname = oneview_client.fabrics.get_by('name', 'DefaultFabric')[0]
pprint(fabric_byname)

# These methods are available for API version 300 or later
if oneview_client.api_version >= 300:
    # Get reserved vlan ID range for the fabric.
    print("\nGet reserved vlan ID range for the fabric")
    vlan_pool = oneview_client.fabrics.get_reserved_vlan_range(fabric_id)
    pprint(vlan_pool)

    # Update the reserved vlan ID range for the fabric
    vlan_pool_data = {
        "start": 100,
        "length": 100
    }
    print("\nUpdate the reserved vlan ID range for the fabric.")
    fabric_byname = oneview_client.fabrics.update_reserved_vlan_range(fabric_id, vlan_pool_data)
    pprint(fabric_byname)
