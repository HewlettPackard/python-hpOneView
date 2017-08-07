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

# To run all parts of this example, a server profile uri, volume uri, volume attachment id and
# path id must be defined.
serverProfileUri = None
storageVolumeUri = None
attachment_id = None
path_id = None

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Get all volume attachments
print("\nGet all volume attachments")
volume_attachments = oneview_client.storage_volume_attachments.get_all()
for attachment in volume_attachments:
    print('\n#### Storage Volume Attachment info:')
    pprint(attachment)

# Get all storage volume attachments filtering by storage volume URI
try:
    print("\nGet all storage volume attachments filtering by storage volume URI")
    filter = "storageVolumeUri='{}'".format(storageVolumeUri)
    volume_attachments_filtered = oneview_client.storage_volume_attachments.get_all(filter=filter)
    for attachment in volume_attachments_filtered:
        print('\n#### Storage Volume Attachment info:')
        pprint(attachment)
except HPOneViewException as e:
    print(e.msg)

# Get the list of extra unmanaged storage volumes
print("\nGet the list of extra unmanaged storage volumes")
unmanaged_storage_volumes = oneview_client.storage_volume_attachments.get_extra_unmanaged_storage_volumes()
pprint(unmanaged_storage_volumes)

# Removes extra presentations from a specified server profile.
try:
    info = {
        "type": "ExtraUnmanagedStorageVolumes",
        "resourceUri": serverProfileUri
    }
    print("\nRemoves extra presentations from a specified server profile at uri: '{}".format(serverProfileUri))
    oneview_client.storage_volume_attachments.remove_extra_presentations(info)
    print("   Done.")
except HPOneViewException as e:
    print(e.msg)

# Get storage volume attachment by id
try:
    print("\nGet storage volume attachment by id: '{}'".format(attachment_id))
    volume_attachment_byid = oneview_client.storage_volume_attachments.get(attachment_id)
    print('\n#### Storage Volume Attachment info:')
    pprint(attachment)
except HPOneViewException as e:
    print(e.msg)

if volume_attachments:
    # Get storage volume attachment by uri
    print("\nGet storage volume attachment by uri: '{uri}'".format(**volume_attachments[0]))
    volume_attachment_byid = oneview_client.storage_volume_attachments.get(volume_attachments[0]['uri'])
    print('\n#### Storage Volume Attachment info:')
    pprint(attachment)

    if oneview_client.api_version < 500:
        # Get all volume attachment paths
        print("\nGet all volume attachment paths for volume attachment at uri: {uri}".format(**volume_attachment_byid))
        paths = oneview_client.storage_volume_attachments.get_paths(volume_attachment_byid['uri'])
        for path in paths:
            print("   Found path at uri: {uri}".format(**path))

        if paths:
            # Get specific volume attachment path by uri
            print("\nGet specific volume attachment path by uri")
            path_byuri = oneview_client.storage_volume_attachments.get_paths(
                volume_attachment_byid['uri'], paths[0]['uri'])
            pprint(path_byuri)

# Get volume attachment path by id
if path_id and oneview_client.api_version < 500:
    try:
        print("\nGet volume attachment path by id: '{}'\n  at attachment with id: '{}'".format(path_id, attachment_id))
        path_byid = oneview_client.storage_volume_attachments.get_paths(attachment_id, path_id)
        pprint(path_byid)
    except HPOneViewException as e:
        print(e.msg)
