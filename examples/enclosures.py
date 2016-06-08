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
        "authLoginDomain": "",
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Get all, with default values
print("Get all enclosures")
enclosures = oneview_client.enclosures.get_all()
pprint(enclosures)

# Find an enclosure by name
print("Get enclosure by name")
enclosures = oneview_client.enclosures.get_by('name', 'OneViewSDK-Test-Enclosure')
if len(enclosures) > 0:
    enclosure = enclosures[0]
    print("Found enclosure by name: '%s'.\n  uri = '%s'" % (enclosure['name'], enclosure['uri']))
else:
    print("Enclosure not found.")

# Get Statistics with defaults
ENCLOSURE_ID = "09SGH102X6J1"

print("Get enclosure statistics")
try:
    enclosure_statistics = oneview_client.enclosures.get_utilization(ENCLOSURE_ID)
    pprint(enclosure_statistics)
except HPOneViewException as e:
    print(e.msg['message'])

# Get Statistics specifying parameters
print("Get enclosure statistics")
try:
    enclosure_statistics = oneview_client.enclosures.get_utilization(ENCLOSURE_ID,
                                                                     fields='AveragePower',
                                                                     filter='startDate=2016-05-30T03:29:42.000Z',
                                                                     view='day')
    pprint(enclosure_statistics)
except HPOneViewException as e:
    print(e.msg['message'])
