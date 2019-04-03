# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2019) Hewlett Packard Enterprise Development LP
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
from config_loader import try_load_from_file

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)
oneview_client = OneViewClient(config)
server_hardware_types = oneview_client.server_hardware_types

# Get the first 10 records, sorting by name descending
print("\nGet the first 10 server hardware types, sorting by name descending, filtering by name")
server_hardware_types_all = server_hardware_types.get_all(0, 10, sort='name:descending')
pprint(server_hardware_types_all, depth=2)

# Get all, with defaults
print("\nGet all server hardware types")
server_hardware_types_all = server_hardware_types.get_all()
pprint(server_hardware_types_all, depth=3)

# Get by uri
print("\nGet a Server Hardware Type by uri")
server_hardware_type_by_uri = server_hardware_types.get_by_uri(server_hardware_types_all[0]["uri"])
pprint(server_hardware_type_by_uri.data, depth=2)

# Get by name and update
print("\nGet a Server Hardware Type by name")
server_hardware_type = server_hardware_types.get_by_name("SY 480 Gen9 1")
pprint(server_hardware_type.data, depth=2)
update = {
    'description': "Updated Description"
}
server_hardware_type.update(update)
print("\nServer Hardware type '{}' updated: \n 'description': '{}'".format(
    server_hardware_type.data['name'],
    server_hardware_type.data['description']))
