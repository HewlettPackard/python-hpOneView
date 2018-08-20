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

pool_type_vsn = 'vsn'
pool_type_vwwn = 'vwwn'
pool_type_vmac = 'vmac'
pool_type_ipv4 = 'ipv4'

print("\n Gets the Pool: " + pool_type_vsn)
id_pool_1 = oneview_client.id_pools.get_by_name(pool_type_vsn)
pprint(id_pool_1.data)

print("\n Gets the Pool: " + pool_type_vwwn)
id_pool_2 = oneview_client.id_pools.get_by_name(pool_type_vwwn)
pprint(id_pool_2.data)

print("\n Gets the Pool: " + pool_type_vmac)
id_pool_3 = oneview_client.id_pools.get_by_name(pool_type_vmac)
pprint(id_pool_3.data)

print("\n Gets the Pool: " + pool_type_ipv4)
id_pool_4 = oneview_client.id_pools.get_by_name(pool_type_ipv4)
pprint(id_pool_4.data)

print("\n Enable the Id Pool")
id_pool_1.enable({"type": "Pool", "enabled": True})
print(" Id Pool enabled")

print("\n Generates a random range")
rnd_range = id_pool_1.generate()
pprint(rnd_range)

print("\n Allocates a set of IDs from a pool")
allocated_ids = id_pool_1.allocate({"count": 10})
pprint(allocated_ids)

print("\n Checks the range availability in the Id pool")
range_availability = id_pool_1.get_check_range_availability(['VCGYOAF00P', 'VCGYOAF002'])
pprint(range_availability)

print("\n Validates a set of user specified IDs to reserve in the pool")
validated = id_pool_1.validate({'idList': ['VCGYOAA023', 'VCGYOAA024']})
pprint(validated)

print("\n Validates an Id Pool")
get_validate = id_pool_1.validate_id_pool(['172.18.9.11'])
pprint(get_validate)

print("\n Collect a set of IDs back to Id Pool")
try:
    collected_ids = id_pool_1.collect({"idList": allocated_ids['idList']})
    pprint(collected_ids)
except HPOneViewException as e:
    print(e.msg)
