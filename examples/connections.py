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
from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException
from config_loader import try_load_from_file

config = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Get all connections
print("Get all connections")
cons = oneview_client.connections.get_all()
pprint(cons)

# Get all connections with interconnectUri filter
try:
    print("Get connections based on interconnect uri")
    filter = "interconnectUri='/rest/interconnects/794079a2-7eb4-4992-8027-e9743a40f5b0'"
    cons_interconnectUri = oneview_client.connections.get_all(filter=filter)
    pprint(cons_interconnectUri)
except HPOneViewException as e:
    print(e.msg)

# Get first 10 connections, sorted by name
print("Get first 10 connections, sorting by name")
cons_sorted = oneview_client.connections.get_all(0, 10, sort='name:descending')
pprint(cons_sorted)

# Find connection by name
try:
    print("Get connection by name")
    con_byName = oneview_client.connections.get_by(
        'name', "name981375475-1465399560370")
    pprint(con_byName)
except HPOneViewException as e:
    print(e.msg)


# Get by Uri
try:
    print("Get connection by uri")
    con_byUri = oneview_client.connections.get(
        '/rest/connections/58ffb307-3087-4c9d-8574-44e8a79e0d6e')
    pprint(con_byUri)
except HPOneViewException as e:
    print(e.msg)
