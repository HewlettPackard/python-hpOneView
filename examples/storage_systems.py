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
from hpOneView.exceptions import HPOneViewException
from hpOneView.oneview_client import OneViewClient
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

options = {
    "hostname": config['storage_system_hostname'],
    "username": config['storage_system_username'],
    "password": config['storage_system_password'],
    "family": config['storage_system_family']
}

oneview_client = OneViewClient(config)

# Add and update storage system for management
try:
    storage_system = oneview_client.storage_systems.add(options)
    print("\nAdded storage system '%s'.\n   uri = '%s'" %
          (storage_system['name'], storage_system['uri']))
except HPOneViewException as e:
    storage_system = oneview_client.storage_systems.get_by_hostname(options['hostname'])
    if storage_system:
        print("\nStorage system '%s' was already added.\n   uri = '%s'" %
              (storage_system['name'], storage_system['uri']))
    else:
        print(e.msg)

# Adds managed domains and managed pools to StoreServ storage systems
# This is a one-time only action, after this you cannot change the managed values
if not storage_system['deviceSpecificAttributes']['managedDomain']:
    storage_system['deviceSpecificAttributes']['managedDomain'] = storage_system[
        'deviceSpecificAttributes']['discoveredDomains'][0]
    for pool in storage_system['deviceSpecificAttributes']['discoveredPools']:
        if pool['domain'] == storage_system['deviceSpecificAttributes']['managedDomain']:
            pool_to_manage = pool
            storage_system['deviceSpecificAttributes']['discoveredPools'].remove(pool)
            pprint(pool_to_manage)
            break
    storage_system['deviceSpecificAttributes']['managedPools'] = [pool_to_manage]
    oneview_client.storage_systems.update(storage_system)
    print("\nUpdated 'managedDomain' to '{}' so storage system can be managed".format(
          storage_system['deviceSpecificAttributes']['managedDomain']))
    print("\nManaged storage pool '{}' at uri: '{}'".format(storage_system['deviceSpecificAttributes'][
          'managedPools'][0]['name'], storage_system['deviceSpecificAttributes']['managedPools'][0]['uuid']))

# Get all managed storage systems
print("\nGet all managed storage systems")
storage_systems_all = oneview_client.storage_systems.get_all()
for ss in storage_systems_all:
    print("   '{}' at uri: '{}'".format(ss['name'], ss['uri']))

# Get maximum of 5 storage systems which belong to family of type 'StoreServ',
# sorted by freeCapacity in descending order.
print(
    "Get maximum of 5 storage systems which belong to family of type StoreServ, sorted by freeCapacity in "
    "descending order.")
filter = 'family=StoreServ'
storage_systems_filtered = oneview_client.storage_systems.get_all(
    0, 5, filter="\"'family'='StoreServ'\"", sort='freeCapacity:desc')
for ss in storage_systems_filtered:
    print("   '{}' at uri: '{}'".format(ss['name'], ss['uri']))
if not storage_systems_filtered:
    print("   No storage systems matching parameters")

# Get the list of supported host types
print("\nGet supported host types")
support_host_types = oneview_client.storage_systems.get_host_types()
pprint(support_host_types)

# Get a list of storage pools
print("\nGet a list of storage pools managed by storage system")
storage_pools = oneview_client.storage_systems.get_storage_pools(
    storage_system['uri'])
pprint(storage_pools)

# Get a specified storage system by id
try:
    storage_system_by_id = oneview_client.storage_systems.get('TXQ1010307')
    print("\nGot storage system by id 'TXQ1010307' at uri '{}'".format(
        storage_system_by_id['uri']))
except HPOneViewException as e:
    print(e.msg)

print("\nGet all reachable storage ports which are managed by the storage system")
reachable_ports = oneview_client.storage_systems.get_reachable_ports(storage_system['uri'])
pprint(reachable_ports)

print("\nGet templates related to a storage system")
templates = oneview_client.storage_systems.get_templates(storage_system['uri'])
pprint(templates)

# Remove storage system
print("\nRemove storage system")
oneview_client.storage_systems.remove(storage_system)
print("   Done.")
