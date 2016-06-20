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
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

data = {
    "name": "Enclosure Group 1",
    "stackingMode": "Enclosure",
    "interconnectBayMappings":
        [
            {
                "interconnectBay": 1,
            },
            {
                "interconnectBay": 2,
            },
            {
                "interconnectBay": 3,
            },
            {
                "interconnectBay": 4,
            },
            {
                "interconnectBay": 5,
            },
            {
                "interconnectBay": 6,
            },
            {
                "interconnectBay": 7,
            },
            {
                "interconnectBay": 8,
            }
        ]
}

# Create a Enclosure Group
print("Create a Enclosure Group")
created_eg = oneview_client.enclosure_groups.create(data)
pprint(created_eg)

# Get the first 10 records, sorting by name descending
print("Get the ten first Enclosure Groups, sorting by name descending")
egs = oneview_client.enclosure_groups.get_all(0, 10,
                                              sort='name:descending')
pprint(egs)

# Get Enclosure Group by property
result = oneview_client.enclosure_groups.get_by('name', 'Enclosure Group 1')
if len(result) > 0:
    eg = result[0]
    print("Found Enclosure Group by name: '%s'.\n  uri = '%s'" % (eg['name'], eg['uri']))
else:
    print("No Enclosure Group found.")

# Get all, with default
print("Get all Enclosure Groups")
egs = oneview_client.enclosure_groups.get_all()
pprint(egs)

# Get by Id
try:
    print("Get a Enclosure Group by id")
    eg_byid = oneview_client.enclosure_groups.get('54184fae-42d5-4248-a732-cfe5115f7857')
    pprint(eg_byid)
except HPOneViewException as e:
    print(e.msg['message'])

# Get by uri
try:
    print("Get a Enclosure Group by uri")
    eg_byuri = oneview_client.enclosure_groups.get(egs[0]["uri"])
    pprint(eg_byuri)
except HPOneViewException as e:
    print(e.msg['message'])

# Gets the configuration script of a Enclosure Group
try:
    print("Gets the configuration script of a Enclosure Group")
    script = oneview_client.enclosure_groups.get_script(egs[0]["uri"])
    print(script)
except HPOneViewException as e:
    print(e.msg['message'])

# Delete a Enclosure Group
print("Delete the created Enclosure Group")
oneview_client.enclosure_groups.delete(created_eg)
print("Sucessfully deleted Enclosure Group")
