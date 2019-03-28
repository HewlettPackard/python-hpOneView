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

# This resource is only available on HPE Synergy

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
sas_interconnect_types = oneview_client.sas_interconnect_types

# Get all
print("\nGet all SAS Interconnect Types")
sas_interconnect_types_all = sas_interconnect_types.get_all()
pprint(sas_interconnect_types_all)

if sas_interconnect_types_all:
    # Get by URI
    print("\nGet a SAS Interconnect Type by URI")
    uri = sas_interconnect_types_all[0]['uri']
    sas_interconnect_type_by_uri = sas_interconnect_types.get_by_uri(uri)
    pprint(sas_interconnect_type_by_uri.data)

    # Get by name
    print("\nGet a SAS Interconnect Type by name")
    name = sas_interconnect_types_all[0]['name']
    sas_interconnect_type_by_name = sas_interconnect_types.get_by_name(name)
    pprint(sas_interconnect_type_by_name.data)
