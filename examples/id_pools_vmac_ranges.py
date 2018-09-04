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

options = {
    "type": "Range",
    "startAddress": "E2:13:C6:F0:00:00",
    "endAddress": "E2:13:C6:FF:FF:FF",
    "rangeCategory": "Custom"
}

options_additional = {
    "type": "Range",
    "name": None,
    "prefix": None,
    "enabled": True,
    "rangeCategory": "Generated",
    "startAddress": "E2:13:C6:F0:00:00",
    "endAddress": "E2:13:C6:FF:FF:FF",
    "totalCount": 1048575,
    "freeIdCount": 1048575,
    "allocatedIdCount": 0,
    "allocatorUri":
        "/rest/id-pools/vmac/ranges/5613a502-9253-45c6-aa78-a83635241cf8/allocator",
    "collectorUri":
        "/rest/id-pools/vmac/ranges/5613a502-9253-45c6-aa78-a83635241cf8/collector",
    "reservedIdCount": 0,
    "freeFragmentUri":
        "/rest/id-pools/vmac/ranges/5613a502-9253-45c6-aa78-a83635241cf8/free-fragments?start=0&count=-1",
    "allocatedFragmentUri":
        "/rest/id-pools/vmac/ranges/5613a502-9253-45c6-aa78-a83635241cf8/allocated-fragments?start=0&count=-1",
    "uri":
        "/rest/id-pools/vmac/ranges/5613a502-9253-45c6-aa78-a83635241cf8",
    "category": "id-range-VMAC",
    "eTag": None,
    "created": "2013-03-20 01:29:10.570",
    "modified": "2013-03-20 01:29:10.570"

}

# Create vmac Range for id pools
vmac_range = oneview_client.id_pools_vmac_ranges.create(options)
pprint(vmac_range.data)

# Get vmac range by uri
vmac_range_byuri = oneview_client.id_pools_vmac_ranges.get_by_uri(vmac_range.data['uri'])
print("Got vmac range from '{}' to '{}' by uri:\n   '{}'".format(vmac_range_byuri.data[
      'startAddress'], vmac_range_byuri.data['endAddress'], vmac_range_byuri.data['uri']))

# Enable a vMAC range
information = {
    "type": "Range",
    "enabled": True
}
vmac_range = vmac_range.enable(information)
print("Successfully enabled vmac range at\n   'uri': {}\n   with 'enabled': {}".format(
    vmac_range.data['uri'], vmac_range.data['enabled']))

# Allocate a set of IDs from vmac range
information = {
    "count": 10
}
successfully_allocated_ids = vmac_range.allocate(information)
print("Successfully allocated IDs:")
pprint(successfully_allocated_ids)

# Get all allocated fragments in vmac range
print("Get all allocated fragments in vmac range")
allocated_fragments = vmac_range.get_allocated_fragments()
pprint(allocated_fragments)

# Get all free fragments in vmac range
print("Get all free fragments in vmac range")
allocated_fragments = vmac_range.get_free_fragments()
pprint(allocated_fragments)

# Collect a set of IDs back to vmac range
try:
    information = {
        "idList": successfully_allocated_ids['idList']
    }
    successfully_collected_ids = vmac_range.collect(information)
except HPOneViewException as e:
    print(e.msg)

# Disable a vmac range
information = {
    "type": "Range",
    "enabled": False
}
vmac_range = vmac_range.enable(information)
print("Successfully disabled vmac range at\n   'uri': {}\n   with 'enabled': {}".format(vmac_range.data['uri'], vmac_range.data['enabled']))

# Delete vmac_range
vmac_range.delete()
print("Successfully deleted vmac range")

# Create vmac Range for id pools with more options specified
print("Create vMAC range with more options specified for id pools")
vmac_range = oneview_client.id_pools_vmac_ranges.create(options_additional)
pprint(vmac_range.data)

# Delete vmac_range
vmac_range.delete()
print("Successfully deleted newly created vMAC range")
