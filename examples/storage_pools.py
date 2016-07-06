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
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Find or add storage system
print("Find or add storage system")
s_systems = oneview_client.storage_systems.get_all()
if s_systems:
    s_system = s_systems[0]
    storage_system_added = False
    print("   Found storage system '{}' at uri: {}".format(
        s_system['name'], s_system['uri']))
else:
    options = {
        "ip_hostname": config['storage_system_hostname'],
        "username": config['storage_system_username'],
        "password": config['storage_system_password']
    }
    s_system = oneview_client.storage_systems.add(options)
    s_system['managedDomain'] = s_system['unmanagedDomains'][0]
    s_system = oneview_client.storage_systems.update(s_system)
    storage_system_added = True
    print("   Added storage system '{}' at uri: {}".format(
        s_system['name'], s_system['uri']))

# Find and add unmanaged storage pool for management
pool_name = ''
storage_pool_add = {}
print("Find and add unmanaged storage pool for management")
for pool in s_system['unmanagedPools']:
    if pool['domain'] == s_system['managedDomain']:
        pool_name = pool['name']
        break
if pool_name:
    print("   Found pool '{}'".format(pool_name))
    options = {
        "storageSystemUri": s_system['uri'],
        "poolName": pool_name
    }
    storage_pool_add = oneview_client.storage_pools.add(options)
    print("   Successfully added pool")
else:
    print("   No available unmanaged storage pools to add")

# Get all managed storage pools
print("Get all managed storage pools")
storage_pools_all = oneview_client.storage_pools.get_all()
for pool in storage_pools_all:
    print("   '{}' at uri: '{}'".format(pool['name'], pool['uri']))

# Get maximum of 5 storage pools sorted by freeCapacity in descending order.
print(
    "Get maximum of 5 storage pools  sorted by freeCapacity in descending order.")
storage_pools_filtered = oneview_client.storage_pools.get_all(
    0, 5, sort='freeCapacity:desc')
for pool in storage_pools_filtered:
    print("   '{}' at uri: '{}'".format(
        pool['name'], pool['uri']))

# Get storage pool by uri
storage_pool_by_uri = oneview_client.storage_pools.get(
    storage_pools_all[0]['uri'])
print("Got storage pool '{}' by   uri: '{}'".format(
    storage_pool_by_uri['name'], storage_pool_by_uri['uri']))
pprint(storage_pool_by_uri)

# Get storage pool by id
try:
    storage_pool_by_id = oneview_client.storage_pools.get(
        'CFA635CC-A9FB-4883-9B4B-BF65FA68FA57')
    print("Got storage pool '{}' by id 'CFA635CC-A9FB-4883-9B4B-BF65FA68FA57' at\n   uri: '{}'".format(
        storage_pool_by_id['name'], storage_pool_by_id['uri']))
    pprint(storage_pool_by_id)
except HPOneViewException as e:
    print(e.msg['message'])

# Remove storage pool
if storage_pool_add:
    print("Remove recently added storage pool")
    oneview_client.storage_pools.remove(storage_pool_add)
    print("   Done.")

# Remove storage system, if it was added
if storage_system_added:
    print("Remove recently added storage system")
    oneview_client.storage_systems.remove(s_system)
    print("   Done.")
