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

storage_pool_name = 'FST_CPG1'

# Get the storage pool by name to use in options
storage_pool = oneview_client.storage_pools.get_by('name', storage_pool_name)[0]

# Gets the first Root Storage Volume Template available to use in options
root_template = oneview_client.storage_volume_templates.get_all(filter="\"isRoot='True'\"")[0]

options = {
    "name": "vt1",
    "description": "",
    "rootTemplateUri": root_template['uri'],
    "properties": {
        "name": {
            "meta": {
                "locked": False
            },
            "type": "string",
            "title": "Volume name",
            "required": True,
            "maxLength": 100,
            "minLength": 1,
            "description": "A volume name between 1 and 100 characters"
        },
        "size": {
            "meta": {
                "locked": False,
                "semanticType": "capacity"
            },
            "type": "integer",
            "title": "Capacity",
            "default": 1073741824,
            "maximum": 17592186044416,
            "minimum": 268435456,
            "required": True,
            "description": "The capacity of the volume in bytes"
        },
        "description": {
            "meta": {
                "locked": False
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
                "locked": False
            },
            "type": "boolean",
            "title": "Is Shareable",
            "default": False,
            "description": "The shareability of the volume"
        },
        "storagePool": {
            "meta": {
                "locked": False,
                "createOnly": True,
                "semanticType": "device-storage-pool"
            },
            "type": "string",
            "title": "Storage Pool",
            "format": "x-uri-reference",
            "required": True,
            "description": "A common provisioning group URI reference",
            "default": storage_pool['uri']
        },
        "snapshotPool": {
            "meta": {
                "locked": True,
                "semanticType": "device-snapshot-storage-pool"
            },
            "type": "string",
            "title": "Snapshot Pool",
            "format": "x-uri-reference",
            "default": storage_pool['uri'],
            "description": "A URI reference to the common provisioning group used to create snapshots"
        },
        "provisioningType": {
            "enum": [
                "Thin",
                "Full",
                "Thin Deduplication"
            ],
            "meta": {
                "locked": True,
                "createOnly": True
            },
            "type": "string",
            "title": "Provisioning Type",
            "default": "Thin",
            "description": "The provisioning type for the volume"
        }
    }
}

oneview_client = OneViewClient(config)

# Create storage volume template
print("\nCreate storage volume template")
volume_template = oneview_client.storage_volume_templates.create(options)
pprint(volume_template)

# Update storage volume template
print("\nUpdate '{name}' at uri: {uri}".format(**volume_template))
volume_template['description'] = "updated description"
volume_template = oneview_client.storage_volume_templates.update(volume_template)
print("   Updated with 'description': '{description}'".format(**volume_template))

# Get all storage volume templates
print("\nGet all storage volume templates")
volume_templates = oneview_client.storage_volume_templates.get_all()
for template in volume_templates:
    print("   '{name}' at uri: {uri}".format(**template))

# Get storage volume template by id
try:
    template_id = volume_templates[0]['uri'].split('/')[-1]
    print("\nGet storage volume template by id: '{}'".format(template_id))
    volume_template_byid = oneview_client.storage_volume_templates.get(template_id)
    print("   Found '{name}' at uri: {uri}".format(**volume_template_byid))
except HPOneViewException as e:
    print(e.msg)

# Get storage volume template by uri
print("\nGet storage volume template by uri: '{uri}'".format(**volume_template))
volume_template_by_uri = oneview_client.storage_volume_templates.get(volume_template['uri'])
print("   Found '{name}' at uri: {uri}".format(**volume_template_by_uri))

# Get storage volume template by name
print("\nGet storage volume template by 'name': '{name}'".format(**volume_template))
volume_template_byname = oneview_client.storage_volume_templates.get_by('name', volume_template['name'])[0]
print("   Found '{name}' at uri: {uri}".format(**volume_template_byname))

# Get reachable volume templates
print("\nGet reachable volume templates")
cvt = oneview_client.storage_volume_templates.get_reachable_volume_templates()
print("Retrieved the following reachable volume templates:")
for template in cvt['members']:
    print("   '{name}' at uri: {uri}".format(**template))

# Get compatible systems to this storage volume templates
print("\nGet list of compatible systems to this storage volume templates")
cs = oneview_client.storage_volume_templates.get_compatible_systems(volume_templates[0]['uri'])
print("Retrieved the following list of compatible systems:")
for storage_system in cs['members']:
    print("   '{name}' at uri: {uri}".format(**storage_system))

# Remove storage volume template
print("\nDelete storage volume template")
oneview_client.storage_volume_templates.delete(volume_template)
print("   Done.")
