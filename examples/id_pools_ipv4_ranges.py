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
    "name": "IPv4",
    "rangeCategory": "Custom",
    "startAddress": "10.10.2.2",
    "endAddress": "10.10.2.254",
    "subnetUri": "/rest/id-pools/ipv4/subnets/7e77926c-195c-4984-926d-c858fde63f9b"
}

print("\n Create an IPv4 Range for id pools")
ipv4_range = oneview_client.id_pools_ipv4_ranges.create(options)
pprint(ipv4_range)

print("\n Update the IPv4 Range")
ipv4_range['name'] = 'New Name'
ipv4_range = oneview_client.id_pools_ipv4_ranges.update(ipv4_range)
pprint(ipv4_range)

print("\n Get the IPv4 range by uri")
ipv4_range_byuri = oneview_client.id_pools_ipv4_ranges.get(ipv4_range['uri'])
pprint(ipv4_range_byuri)

print("\n Enable an IPv4 range")
ipv4_range = oneview_client.id_pools_ipv4_ranges.enable(
    {
        "type": "Range",
        "enabled": True
    },
    ipv4_range['uri'])
print(" IPv4 range enabled successfully.")

print("\n Get all allocated fragments in IPv4 range")
allocated_fragments = oneview_client.id_pools_ipv4_ranges.get_allocated_fragments(ipv4_range['uri'])
pprint(allocated_fragments)

print("\n Get all free fragments in IPv4 range")
allocated_fragments = oneview_client.id_pools_ipv4_ranges.get_free_fragments(ipv4_range['uri'])
pprint(allocated_fragments)

print("\n Disable an IPv4 range")
ipv4_range = oneview_client.id_pools_ipv4_ranges.enable({
    "type": "Range",
    "enabled": False
}, ipv4_range['uri'])
print(" IPv4 range disabled successfully.")

print("\n Delete the IPv4_range")
oneview_client.id_pools_ipv4_ranges.delete(ipv4_range)
print(" Successfully deleted IPv4 range")
