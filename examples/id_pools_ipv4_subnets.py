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
    "type": "Subnet",
    "name": "IPv4Subnet",
    "networkId": '10.10.1.0',
    "subnetmask": "255.255.255.0",
    "gateway": "10.10.1.1",
    "domain": "example.com",
    "dnsServers": ["10.10.10.215"]
}

print('\n Create IPv4 subnet for id pools')
ipv4_subnet = oneview_client.id_pools_ipv4_subnets.create(data=options)
pprint(ipv4_subnet.data)

print('\n Update IPv4 subnet for id pools')
ipv4_subnet.data['name'] = 'Changed Name'
ipv4_subnet = ipv4_subnet.update(data=ipv4_subnet.data)
pprint(ipv4_subnet.data)

print('\n Get all IPv4 subnet')
all_subnets = ipv4_subnet.get_all()
pprint(all_subnets)

print('\n Get IPv4 subnet by uri')
ipv4_subnet_byuri = oneview_client.id_pools_ipv4_subnets.get_by_uri(ipv4_subnet.data['uri'])
pprint(ipv4_subnet_byuri.data)

print('\n Delete IPv4 subnet')
ipv4_subnet.delete()
print(" Successfully deleted IPv4 subnet")
