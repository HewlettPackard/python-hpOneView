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
import time

from config_loader import try_load_from_file
from hpOneView.exceptions import HPOneViewException
from hpOneView.oneview_client import OneViewClient

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

# To run this example, you may set a name to add the volume to management in HPE OneView (optional)
storage_pool_name = 'CPG-SSD'

# To run this example, you may set a name to add the volume to management in HPE OneView (optional)
unmanaged_volume_name = ''

oneview_client = OneViewClient(config)

print("\nGet the storage system and the storage pool to create the volumes")
storage_system = oneview_client.storage_systems.get_by_hostname(config['storage_system_hostname'])
print("    Got storage system '{name}' with hostname '{hostname}' in {uri}".format(**storage_system))
storage_pools = oneview_client.storage_pools.get_all()
storage_pool_available = False
for sp in storage_pools:
    if sp['storageSystemUri'] == storage_system['uri']:
        if (storage_pool_name and sp['name'] == storage_pool_name) or (not storage_pool_name):
            storage_pool_available = True
            storage_pool = sp
            print("    Got storage pool '{name}' from storage system '{storageSystemUri}'".format(**storage_pool))
if not storage_pool_available:
    raise ValueError("ERROR: No storage pools found attached to the storage system")

print("    Get template to be used in the new volume")
volume_template = oneview_client.storage_volume_templates.get_by('storagePoolUri', storage_pool['uri'])[0]

# Create a volume with a Storage Pool
print("\nCreate a volume with a specified Storage Pool")

options_with_storage_pool = {
    "properties": {
        "name": 'ONEVIEW_SDK_TEST_VOLUME_STORE_SERV',
        "description": 'Test volume with common creation: Storage Pool',
        "storagePool": storage_pool['uri'],
        "size": 1024 * 1024 * 1024,  # 1GB
        "provisioningType": 'Thin',
        "isShareable": True,
        "snapshotPool": storage_pool['uri']
    },
    "templateUri": volume_template['uri'],
    "isPermanent": True
}
volume = oneview_client.volumes.create(options_with_storage_pool)
pprint(volume)

managed_volume = None
if unmanaged_volume_name:
    print("\nAdd a volume for management to the appliance using the name of the volume")

    unmanaged_add_options = {
        "deviceVolumeName": unmanaged_volume_name,
        "description": 'Unmanaged test volume added for management: Storage System + Storage Pool + Name',
        "storageSystemUri": storage_system['uri'],
        "isShareable": True
    }
    managed_volume = oneview_client.volumes.add_from_existing(unmanaged_add_options)
    pprint(managed_volume)

# Get all managed volumes
print("\nGet a list of all managed volumes")
volumes = oneview_client.volumes.get_all()
for found_volume in volumes:
    print('  Name: {name}').format(**found_volume)

# Create a snapshot
print("\nCreate a snapshot")

snapshot_options = {
    "name": "Test Snapshot",
    "description": "Description for the snapshot",
}
volume = oneview_client.volumes.create_snapshot(volume['uri'], snapshot_options)
print("Created a snapshot for the volume '{name}'".format(**volume))

# Get recently created snapshot resource by name
print("\nGet a snapshot by name")
created_snapshot = oneview_client.volumes.get_snapshot_by(volume['uri'], 'name', 'Test Snapshot')[0]
print("Found snapshot at uri '{uri}'\n  by name = '{name}'".format(**created_snapshot))

snapshot_uri = created_snapshot['uri']

# Get recently created snapshot resource by uri
print("\nGet a snapshot")
try:
    snapshot = oneview_client.volumes.get_snapshot(snapshot_uri, volume['uri'])
    pprint(snapshot)
except HPOneViewException as e:
    print(e.msg)

print("\nCreate a new volume from the snapshot")
from_snapshot_options = {
    "properties": {
        "name": 'TEST_VOLUME_FROM_SNAPSHOT',
        "description": 'Create volume from snapshot and template {name}'.format(**volume_template),
        "provisioningType": 'Thin',
        "isShareable": True,
        "size": 1024 * 1024 * 1024,  # 1GB
        "storagePool": storage_pool['uri']
    },
    "templateUri": volume_template['uri'],
    "snapshotUri": snapshot_uri,
    "isPermanent": True
}

try:
    volume_from_snapshot = oneview_client.volumes.create_from_snapshot(from_snapshot_options)
    print("Created volume '{name}': {description}. URI: {uri}".format(**volume_from_snapshot))
except HPOneViewException as e:
    print(e.msg)

# Get all the attachable volumes which are managed by the appliance
print("\nGet all the attachable volumes which are managed by the appliance")
attachable_volumes = oneview_client.volumes.get_attachable_volumes()
pprint(attachable_volumes)

print("\nDelete the recently created volumes")
if oneview_client.volumes.delete(volume):
    print("The volume that was previously created with a Storage Pool was deleted from OneView and storage system")

if oneview_client.volumes.delete(volume_from_snapshot):
    print("The volume that was previously created with from Snaphsot was deleted from OneView and storage system")

if managed_volume and oneview_client.volumes.delete(managed_volume, supress_device_updates=True):
    print("The unamanged volume that was previously added using the name was deleted from OneView only")
