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
import re
from hpOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file

# This resource is only available on HPE Synergy

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

# Get all interconnect link topologies
print("Get all interconnect link topologies")
interconnect_link_topologies = oneview_client.interconnect_link_topologies.get_all()
pprint(interconnect_link_topologies)

# Get all sorting by name descending
print("Get all interconnect link topologies sorting by name")
interconnect_link_topologies_sorted = oneview_client.interconnect_link_topologies.get_all(sort='name:descending')
pprint(interconnect_link_topologies_sorted)

# Get by uri
if interconnect_link_topologies:
    print("Get an interconnect link topology by uri")
    ilt_uri = interconnect_link_topologies[0]['uri']
    ilt_byuri = oneview_client.interconnect_link_topologies.get(ilt_uri)
    print("   Found '{name}' at uri: {uri}".format(**ilt_byuri))

# Get by Id
if interconnect_link_topologies:
    print("Get an interconnect link topology by id")
    ilt_id = re.sub("/rest/interconnect-link-topologies/", '', interconnect_link_topologies[0]['uri'])
    ilt_byid = oneview_client.interconnect_link_topologies.get(ilt_id)
    print("   Found '{name}' at uri: {uri}".format(**ilt_byid))

# Get by name
if interconnect_link_topologies:
    print("Get an interconnect link topology by name")
    ilt_byname = oneview_client.interconnect_link_topologies.get_by(
        'name', interconnect_link_topologies[0]['name'])[0]
    print("   Found '{name}' at uri: {uri}".format(**ilt_byname))
