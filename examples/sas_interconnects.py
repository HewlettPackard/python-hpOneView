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

# WARNING: This example works only with the API version 3 or higher

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

# Get all, with defaults
print("Get all sas-interconnects")
all_sas_interconnects = oneview_client.sas_interconnects.get_all()
pprint(all_sas_interconnects)

# Get the first 10 records
print("\nGet the first ten sas-interconnects")
sas_interconnects_limited = oneview_client.sas_interconnects.get_all(0, 10)
pprint(sas_interconnects_limited)

if all_sas_interconnects:
    interconnect_uri = all_sas_interconnects[0]['uri']

    # Get by Id
    try:
        print("\nGet a sas-interconnects by id")
        interconnect_id = interconnect_uri.rsplit('/')[-1]
        sas_interconnect_by_id = oneview_client.sas_interconnects.get(id_or_uri=interconnect_id)
        pprint(sas_interconnect_by_id)
    except HPOneViewException as e:
        print(e.msg)

    # Get by Uri
    print("\nGet a sas-interconnect by uri")
    sas_interconnect_by_uri = oneview_client.sas_interconnects.get(id_or_uri=interconnect_uri)
    pprint(sas_interconnect_by_uri)
