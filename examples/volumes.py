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

from config_loader import try_load_from_file
from hpOneView.exceptions import HPOneViewException
from hpOneView.oneview_client import OneViewClient

config = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

# To run this example, you may set a WWN to add a volume using the WWN of the volume (optional)
unmanaged_volume_wwn = ''

oneview_client = OneViewClient(config)

# Defines the storage system and the storage pool which are provided to create the volumes
storage_system = oneview_client.storage_systems.get_all()[0]
storage_pools = oneview_client.storage_pools.get_all()
storage_pool_available = False
for sp in storage_pools:
    if sp['storageSystemUri'] == storage_system['uri']:
        storage_pool_available = True
        storage_pool = sp
if not storage_pool_available:
    raise ValueError("ERROR: No storage pools found attached to the storage system")

# Create a volume with a Storage Pool
print("\nCreate a volume with a specified Storage Pool")

options_with_storage_pool = {
    "name": 'ONEVIEW_SDK_TEST_VOLUME_TYPE_1',
    "description": 'Test volume with common creation: Storage Pool',
    "provisioningParameters": {
        "provisionType": 'Full',
        "shareable": True,
        "requestedCapacity": 1024 * 1024 * 1024,  # 1GB
        "storagePoolUri": storage_pool['uri']
    }
}
volume_with_storage_pool = oneview_client.volumes.create(options_with_storage_pool)
pprint(volume_with_storage_pool)

# Create a volume with a Storage System, a Storage Pool, and a Snapshot Pool
print("\nCreate a volume with a specified Snapshot Pool")

options_with_snapshot_pool = {
    "name": 'ONEVIEW_SDK_TEST_VOLUME_TYPE_3',
    "description": 'Test volume with common creation: Storage System + Storage Pool + Snapshot Pool',
    "provisioningParameters": {
        "provisionType": 'Full',
        "shareable": True,
        "requestedCapacity": 1024 * 1024 * 1024,  # 1GB
        "storagePoolUri": storage_pool['uri']
    },
    "storageSystemUri": storage_system['uri'],
    "snapshotPoolUri": storage_pool['uri']
}
volume_with_snapshot_pool = oneview_client.volumes.create(options_with_snapshot_pool)
pprint(volume_with_snapshot_pool)

# Add a volume for management by the appliance using the WWN of the volume
if unmanaged_volume_wwn:
    print("\nAdd a volume for management by the appliance using the WWN of the volume")

    options_with_wwn = {
        "type": "AddStorageVolumeV2",
        "name": 'ONEVIEW_SDK_TEST_VOLUME_TYPE_4',
        "description": 'Test volume added for management: Storage System + Storage Pool + WWN',
        "storageSystemUri": storage_system['uri'],
        "wwn": unmanaged_volume_wwn,
        "provisioningParameters": {
            "shareable": False
        }
    }
    volume_added_with_wwn = oneview_client.volumes.create(options_with_wwn)
    pprint(volume_added_with_wwn)

# Get all managed volumes
print("\nGet a list of all managed volumes")
volumes = oneview_client.volumes.get_all()
for volume in volumes:
    print('  Name: {name}').format(**volume)

# Find a volume by name
volume = oneview_client.volumes.get_by('name', volume_with_storage_pool['name'])[0]
print("\nFound a volume by name: '{name}'.\n  uri = '{uri}'".format(**volume))

# Update the name of the volume recently found to 'ONEVIEW_SDK_TEST_VOLUME_TYPE_1_RENAMED'
volume['name'] = 'ONEVIEW_SDK_TEST_VOLUME_TYPE_1_RENAMED'
volume = oneview_client.volumes.update(volume)
print("\nVolume updated successfully.\n  uri = '{uri}'\n  with attribute 'name' = {name}".format(**volume))

# Find a volume by URI
volume_uri = volume_with_storage_pool['uri']
volume = oneview_client.volumes.get(volume_uri)
print("\nFind a volume by URI")
pprint(volume)

# Create a snapshot
print("\nCreate a snapshot")

snapshot_options = {
    "name": "Test Snapshot",
    "description": "Description for the snapshot",
    "snapshotType": "PhysicalCopy"
}
volume_with_snapshot_pool = oneview_client.volumes.create_snapshot(volume_with_snapshot_pool['uri'], snapshot_options)
print("Created a snapshot for the volume '{name}'".format(**volume_with_snapshot_pool))

# Get recently created snapshot resource by name
print("\nGet a snapshot by name")
created_snapshot = oneview_client.volumes.get_snapshot_by(volume_with_snapshot_pool['uri'], 'name', 'Test Snapshot')[0]
print("Found snapshot at uri '{uri}'\n  by name = '{name}'".format(**created_snapshot))

snapshot_uri = created_snapshot['uri']

# Get recently created snapshot resource by uri
print("\nGet a snapshot")
try:
    snapshot = oneview_client.volumes.get_snapshot(snapshot_uri, volume_uri)
    pprint(snapshot)
except HPOneViewException as e:
    print(e.msg['message'])

# Get a paginated list of snapshot resources sorting by name ascending
print("\nGet a list of the first 10 snapshots")
snapshots = oneview_client.volumes.get_snapshots(volume_with_snapshot_pool['uri'], 0, 10, sort='name:ascending')
for snapshot in snapshots:
    print('  {name}'.format(**snapshot))

# Delete the recently created snapshot resource
print("\nDelete the recently created snapshot")
returned = oneview_client.volumes.delete_snapshot(created_snapshot)
print("Snapshot deleted successfully")

# Get the list of all extra managed storage volume paths from the appliance
extra_volumes = oneview_client.volumes.get_extra_managed_storage_volume_paths()
print("\nGet the list of all extra managed storage volume paths from the appliance")
pprint(extra_volumes)

# Remove extra presentations from the specified volume on the storage system
print("\nRemove extra presentations from the specified volume on the storage system")
oneview_client.volumes.repair(volume['uri'])
print("  Done.")

# Get all the attachable volumes which are managed by the appliance
print("\nGet all the attachable volumes which are managed by the appliance")
attachable_volumes = oneview_client.volumes.get_attachable_volumes()
pprint(attachable_volumes)

print("\nDelete the recently created volumes")
if oneview_client.volumes.delete(volume_with_storage_pool):
    print("The volume, that was previously created with a Storage Pool, was deleted from OneView and storage system")
if oneview_client.volumes.delete(volume_with_snapshot_pool):
    print("The volume, that was previously created with a Snapshot Pool, was deleted from OneView and storage system")
if unmanaged_volume_wwn and oneview_client.volumes.delete(volume_added_with_wwn, export_only=True):
    print("The volume, that was previously added using the WWN of the volume, was deleted from OneView")
