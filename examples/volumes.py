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

# To run this example you must have created a volume on OneView and defined here its id
volume_id = ''

options = {
    "name": "Test Snapshot",
    "description": "Description for the snapshot",
    "snapshotType": "PhysicalCopy"
}

oneview_client = OneViewClient(config)

# Create a snapshot
print("\nCreate a snapshot")
volume = oneview_client.volumes.create_snapshot(volume_id, options)
print("Created a snapshot for the volume '{deviceVolumeName}'".format(**volume))

# Get recently created snapshot resource by name
print("\nGet snapshot by name")
created_snapshot = oneview_client.volumes.get_snapshot_by(volume_id, 'name', 'Test Snapshot')[0]
print("Found snapshot at uri '{uri}'\n  by name = '{name}'".format(**created_snapshot))

snapshot_uri = created_snapshot['uri']

# Get recently created snapshot resource by uri
print("\nGet a snapshot")
try:
    snapshot = oneview_client.volumes.get_snapshot(snapshot_uri, volume_id)
    pprint(snapshot)
except HPOneViewException as e:
    print(e.msg['message'])

# Get a paginated list of snapshot resources sorting by name ascending
print("\nGet a list of snapshots")
all_snapshots = oneview_client.volumes.get_snapshots(volume_id, 0, 10, sort='name:ascending')
for snapshot in all_snapshots:
    print('  %s' % snapshot['name'])

# Delete the recently created snapshot resource
print("\nDelete the recently created snapshot")
returned = oneview_client.volumes.delete_snapshot(created_snapshot)
print("Snapshot deleted successfully")
