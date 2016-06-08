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
    "ip": "172.16.102.59",
    "credentials": {
        "authLoginDomain": "",
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Get all, with defaults
print("Get all Logical Interconnect Groups")
ligs = oneview_client.logical_interconnect_groups.get_all()
pprint(ligs)

# Get the first 10 records, sorting by name descending, filtering by name
print("Get the first Logical Interconnect Groups, sorting by name descending, filtering by name")
ligs = oneview_client.logical_interconnect_groups.get_all(
    0, 10, sort='name:descending', filter="\"'name'='Test Logical Interconnect Group'\"")
pprint(ligs)

# Get by Id
try:
    print("Get a Logical Interconnect Group by id")
    lig_byid = oneview_client.logical_interconnect_groups.get('f0a0a113-ec97-41b4-83ce-d7c92b900e7c')
    pprint(lig_byid)
except HPOneViewException as e:
    print(e.msg['message'])

# Get by uri
print("Get a Logical Interconnect Group by uri")
lig_byuri = oneview_client.logical_interconnect_groups.get(
    '/rest/logical-interconnect-groups/f0a0a113-ec97-41b4-83ce-d7c92b900e7c')
pprint(lig_byuri)

# Get default settings
print("Get the default interconnect settings for a logical interconnect group")
lig_default_settings = oneview_client.logical_interconnect_groups.get_default_settings()
pprint(lig_default_settings)
