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
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

networks = "/rest/fcoe-networks/7f0f74a0-4957-47ac-81c1-f573aa6d83de"
scope_uris = "/rest/scopes/63d1ca81-95b3-41f1-a1ee-f9e1bc2d635f"

# Request body for create operation
# Supported from API version >= 500
options = {
    "rootTemplateUri": "/rest/storage-volume-templates/5dbaf127-053b-4988-82fe-a80800eef1f3",
    "properties": {
        "name": {
            "title": "Volume name",
            "description": "A volume name between 1 and 100 characters",
            "meta": {"locked": "false"},
            "type": "string",
            "required": "true",
            "maxLength": 100,
            "minLength": 1},

        "size": {
            "meta": {
                "locked": "false",
                "semanticType": "capacity"
            },
            "type": "integer",
            "title": "Capacity",
            "default": 1073741824,
            "maximum": 17592186044416,
            "minimum": 268435456,
            "required": "true",
            "description": "The capacity of the volume in bytes"
        },
        "description": {
            "meta": {
                "locked": "false"
            },
            "type": "string",
            "title": "Description",
            "default": "",
            "maxLength": 2000,
            "minLength": 0,
            "description": "A description for the volume"
        },
        "isShareable": {
            "meta": {
                "locked": "false"
            },
            "type": "boolean",
            "title": "Is Shareable",
            "default": "false",
            "description": "The shareability of the volume"
        },
        "storagePool": {
            "meta": {
                "locked": "false",
                "createOnly": "true",
                "semanticType": "device-storage-pool"
            },
            "type": "string",
            "title": "Storage Pool",
            "format": "x-uri-reference",
            "required": "true",
            "description": "A common provisioning group URI reference",
            "default": "/rest/storage-pools/0DB2A6C7-04D3-4830-9229-A80800EEF1F1"
        },
        "snapshotPool": {
            "meta": {
                "locked": "true",
                "semanticType": "device-snapshot-storage-pool"
            },
            "type": "string",
            "title": "Snapshot Pool",
            "format": "x-uri-reference",
            "default": "/rest/storage-pools/0DB2A6C7-04D3-4830-9229-A80800EEF1F1",
            "description": "A URI reference to the common provisioning group used to create snapshots"
        },
        "provisioningType": {
            "enum": [
                "Thin",
                "Full",
                "Thin Deduplication"
            ],
            "meta": {
                "locked": "true",
                "createOnly": "true"
            },
            "type": "string",
            "title": "Provisioning Type",
            "default": "Thin",
            "description": "The provisioning type for the volume"
        }
    },
    "name": "test_02",
    "description": "desc"
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
volume_template = oneview_client.storage_volume_templates.create(options)
pprint(volume_template)

template_id = volume_template["uri"].split('/')[-1]

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
    print("Get storage volume template by id: '{}'".format(template_id))
    volume_template_byid = oneview_client.storage_volume_templates.get(template_id)
    print("   Found '{name}' at uri: {uri}".format(**volume_template_byid))
except HPOneViewException as e:
    print(e.msg)

# Get storage volume template by uri
print("Get storage volume template by uri: '{uri}'".format(**volume_template))
volume_template_by_uri = oneview_client.storage_volume_templates.get(volume_template['uri'])
print("   Found '{name}' at uri: {uri}".format(**volume_template_by_uri))

# Get storage volume template by name
print("Get storage volume template by 'name': '{name}'".format(**volume_template))
volume_template_byname = oneview_client.storage_volume_templates.get_by('name', volume_template['name'])[0]
print("   Found '{name}' at uri: {uri}".format(**volume_template_byname))

# Gets the storage templates that are connected on the specified networks
# scoper_uris and private_allowed_only parameters supported only with API version >= 600
print("Get torage templates that are connected on the specified networks")
storage_templates = oneview_client.storage_volume_templates.get_reachable_volume_templates(
    networks=networks, scope_uris=scope_uris, private_allowed_only=False)
print(storage_templates)

# Retrieves all storage systems that is applicable to the storage volume template.
print("Get storage systems that is applicable to the storage volume template")
storage_systems = oneview_client.storage_volume_templates.get_compatible_systems(
    id_or_uri=template_id)
print(storage_systems)

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
