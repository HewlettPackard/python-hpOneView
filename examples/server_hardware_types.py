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
    "ip": "",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Get the first 10 records, sorting by name descending
print(
    "Get the first 10 server hardware types, sorting by name descending, filtering by name")
server_hardware_types = oneview_client.server_hardware_types.get_all(
    0, 10, sort='name:descending')
pprint(server_hardware_types, depth=3)

# Get all, with defaults
print("Get all server hardware types")
server_hardware_types = oneview_client.server_hardware_types.get_all()
pprint(server_hardware_types, depth=3)

# Get by uri
try:
    print("Get a Server Hardware Type by uri")
    server_hardware_type_byuri = oneview_client.server_hardware_types.get(
        '/rest/server-hardware-types/9410638A-2691-4F40-9098-6585F252C31F')
    pprint(server_hardware_type_byuri, depth=2)
except HPOneViewException as e:
    print(e.msg)

# Get by Id and update
try:
    print("Get a Server Hardware Type by id")
    server_hardware_type_byid = oneview_client.server_hardware_types.get(
        'B2576419-D2BC-4289-8C35-5BDF1EDD719C')
    pprint(server_hardware_type_byid, depth=2)
    update = {
        'description': "Updated Description"
    }
    server_hardware_type_updated = oneview_client.server_hardware_types.update(
        update, server_hardware_type_byid['uri'])
    print("Server Hardware type '{}' updated: \n 'description': '{}'".format(
        server_hardware_type_updated['name'], server_hardware_type_updated['description']))
except HPOneViewException as e:
    print(e.msg)

# Get by ID and delete server hardware type
try:
    print("Get a Server Hardware Type by id")
    server_hardware_type_delete = oneview_client.server_hardware_types.get(
        '2C0DF6DF-5E20-4B50-AECE-3E63E106E224')
    oneview_client.server_hardware_types.delete(server_hardware_type_delete)
    print("successfully deleted Server Hardware Type")
except HPOneViewException as e:
    print(e.msg)
