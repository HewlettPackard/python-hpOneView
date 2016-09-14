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

options = {
    "name": "OneView Test Volume Template",
    "provisioning":
        {
            "capacity": "235834383322",
            "provisionType": "Thin",
            "storagePoolUri": ""
        },
        "type": "StorageVolumeTemplateV3"
}

oneview_client = OneViewClient(config)

# Find or add storage pool to use in template
print("Find or add storage pool to use in template")
storage_pools = oneview_client.storage_pools.get_all()
storage_pool_added = False
storage_system_added = False
if storage_pools:
    storage_pool = storage_pools[0]
    print("   Found storage pool '{name}' at uri: '{uri}".format(**storage_pool))
else:
    # Find or add storage system
    storage_pool_added = True
    print("   Find or add storage system")
    s_systems = oneview_client.storage_systems.get_all()
    if s_systems:
        s_system = s_systems[0]
        storage_system_added = False
        print("      Found storage system '{name}' at uri: {uri}".format(**s_system))
    else:
        options_storage = {
            "ip_hostname": config['storage_system_hostname'],
            "username": config['storage_system_username'],
            "password": config['storage_system_password']
        }
        s_system = oneview_client.storage_systems.add(options_storage)
        s_system['managedDomain'] = s_system['unmanagedDomains'][0]
        s_system = oneview_client.storage_systems.update(s_system)
        storage_system_added = True
        print("      Added storage system '{name}' at uri: {uri}".format(**s_system))

    # Find and add unmanaged storage pool for management
    pool_name = ''
    storage_pool = {}
    print("   Find and add unmanaged storage pool for management")
    for pool in s_system['unmanagedPools']:
        if pool['domain'] == s_system['managedDomain']:
            pool_name = pool['name']
            break
    if pool_name:
        print("      Found pool '{}'".format(pool_name))
        options_pool = {
            "storageSystemUri": s_system['uri'],
            "poolName": pool_name
        }
        storage_pool = oneview_client.storage_pools.add(options_pool)
        print("      Successfully added pool")
    else:
        print("      No available unmanaged storage pools to add")

# Create storage volume template
print("Create storage volume template")
options['provisioning']['storagePoolUri'] = storage_pool['uri']
volume_template = oneview_client.storage_volume_templates.create(options)
pprint(volume_template)

# Update storage volume template
print("Update '{name}' at uri: {uri}".format(**volume_template))
volume_template['description'] = "updated description"
volume_template = oneview_client.storage_volume_templates.update(volume_template)
print("   Updated with 'description': '{description}'".format(**volume_template))

# Get all storage volume templates
print("Get all storage volume templates")
volume_templates = oneview_client.storage_volume_templates.get_all()
for template in volume_templates:
    print("   '{name}' at uri: {uri}".format(**template))

# Get storage volume template by id
try:
    template_id = "71e74304-0697-4fd7-997b-2385fe98b5b4"
    print("Get storage volume template by id: '{}'".format(template_id))
    volume_template_byid = oneview_client.storage_volume_templates.get(template_id)
    print("   Found '{name}' at uri: {uri}".format(**volume_template_byid))
except HPOneViewException as e:
    print(e.msg)

# Get storage volume template by uri
print("Get storage volume template by uri: '{uri}'".format(**volume_template))
volume_template_byid = oneview_client.storage_volume_templates.get(template_id)
print("   Found '{name}' at uri: {uri}".format(**volume_template_byid))

# Get storage volume template by name
print("Get storage volume template by 'name': '{name}'".format(**volume_template))
volume_template_byname = oneview_client.storage_volume_templates.get_by('name', volume_template['name'])[0]
print("   Found '{name}' at uri: {uri}".format(**volume_template_byname))

# Remove storage volume template
print("Delete storage volume template")
oneview_client.storage_volume_templates.delete(volume_template)
print("   Done.")

# Remove storage pool
if storage_pool_added:
    print("Remove recently added storage pool")
    oneview_client.storage_pools.remove(storage_pool)
    print("   Done.")

# Remove storage system, if it was added
if storage_system_added:
    print("Remove recently added storage system")
    oneview_client.storage_systems.remove(s_system)
    print("   Done.")
