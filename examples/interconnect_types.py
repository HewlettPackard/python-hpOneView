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
from hpOneView.exceptions import HPOneViewException
from config_loader import try_load_from_file

config = {
    "ip": "",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Get all supported interconnect types
print("Get all supported interconnect types")
interconnect_types = oneview_client.interconnect_types.get_all()
pprint(interconnect_types, depth=2)

# Get all sorting by name descending
print("Get all interconnect-types sorting by name")
interconnect_types_sorted = oneview_client.interconnect_types.get_all(
    sort='name:descending')
pprint(interconnect_types_sorted, depth=2)

# Get by Id
try:
    print("Get an interconnect_type by id")
    interconnect_types_byid = oneview_client.interconnect_types.get(
        'e28949fa-8681-433d-9808-a9146feb8048')
    pprint(interconnect_types_byid, depth=1)
except HPOneViewException as e:
    print(e.msg)

# Get by name
try:
    print("Get an interconnect_type by name")
    interconnect_type_byname = oneview_client.interconnect_types.get_by(
        'name', 'HP VC Flex-10 Enet Module')[0]
    pprint(interconnect_type_byname, depth=1)
except HPOneViewException as e:
    print(e.msg)
