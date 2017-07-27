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
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Find or add storage system
print("Find or add storage system")
s_systems = oneview_client.storage_systems.get_all()
storage_system_added = True
if s_systems:
    s_system = s_systems[0]
    if s_system['deviceSpecificAttributes']['managedPools']:
        storage_system_added = False
        print("   Found storage system '{}' at uri: {}".format(
            s_system['name'], s_system['uri']))
    elif s_system['hostname'] == config['storage_system_hostname']:
        oneview_client.storage_systems.remove(s_system, force=True)
        print("   Removing Storage System since it has no storage pools managed")


if storage_system_added:
    options = {
        "hostname": config['storage_system_hostname'],
        "username": config['storage_system_username'],
        "password": config['storage_system_password'],
        "family": config['storage_system_family']
    }
    s_system = oneview_client.storage_systems.add(options)
    print("   Added storage system '{}' at uri: {}".format(
        s_system['name'], s_system['uri']))
    s_system['deviceSpecificAttributes']['managedDomain'] = s_system[
        'deviceSpecificAttributes']['discoveredDomains'][0]
    print("   Discovering Storage Pools...")
    s_system['deviceSpecificAttributes']['managedPools'] = []
    for pool in s_system['deviceSpecificAttributes']['discoveredPools']:
        if pool['domain'] == s_system['deviceSpecificAttributes']['managedDomain']:
            s_system['deviceSpecificAttributes']['managedPools'].append(pool)
            s_system['deviceSpecificAttributes']['discoveredPools'].remove(pool)
            print("        Discovered '{}' storage pool").format(pool['name'])
    s_system = oneview_client.storage_systems.update(s_system)
    print("   Added the discovered pools for management")
    storage_system_added = True
    print


# Get all managed storage pools
print("\nGet all storage pools")
storage_pools_all = oneview_client.storage_pools.get_all()
for pool in storage_pools_all:
    print("   '{}' state is {}".format(pool['name'], pool['state']))

# Get all managed storage pools
print("\nGet all managed storage pools")
storage_pools_all = oneview_client.storage_pools.get_all(filter='isManaged=True')
for pool in storage_pools_all:
    print("   '{}' state is {}".format(pool['name'], pool['state']))

# Remove first storage pool
if storage_pools_all:
    remove_pool = storage_pools_all[0]
    print("\nRemove '{}' storage pool from management").format(remove_pool['name'])
    remove_pool['isManaged'] = False
    oneview_client.storage_pools.update(remove_pool)
    print("   Done.")

# Get all managed storage pools
print("\nGet all unmanaged storage pools")
storage_pools_all = oneview_client.storage_pools.get_all(filter='isManaged=False')
for pool in storage_pools_all:
    print("   '{}' state is {}".format(pool['name'], pool['state']))
