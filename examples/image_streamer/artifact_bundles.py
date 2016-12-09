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

import os
from pprint import pprint
from hpOneView.oneview_client import OneViewClient

EXAMPLE_CONFIG_FILE = os.path.join(os.path.dirname(__file__), '../config.json')

oneview_client = OneViewClient.from_json_file(EXAMPLE_CONFIG_FILE)

image_streamer_client = oneview_client.create_image_streamer_client()

artifact_bundles_information = {
    "name": "RHEL-7.2-artifact-bundle",
    "id": "3bc84107-66fb-4873-9c92-02e6c0f79582",
    "id_backup": "744587b5-d739-4575-9745-5bb9b3d19f71",
    "deployment_groups": "00c1344d-e4dd-43c3-a733-1664e159a36f"
}

artifact_bundles_to_be_created = {
    "name": "Artifact Bundles Test",
    "description": "Description of Artifact Bundles Test",
    "buildPlans":[
        {
        "resourceUri": "/rest/build-plans/bc2135ab-e8cf-4847-9bac-1c957073cfc2",
        "readOnly": "false"
        }
    ]
}


# Get all Artifacts Bundle
print("\nGet all Artifact Bundles")
artifact_bundles = image_streamer_client.artifact_bundles.get_all()
for artifacts_bundle in artifact_bundles:
    pprint(artifacts_bundle)


# Get the Artifacts Bundle by ID
print("\nGet the Artifact Bundles by ID")
artifacts_bundle = image_streamer_client.artifact_bundles.get(artifact_bundles_information['id'])
pprint(artifacts_bundle)


# Get the Artifacts Bundle by Name
print("\nGet the Artifact Bundles by Name")
artifacts_bundle = image_streamer_client.artifact_bundles.get_by_name(artifact_bundles_information['name'])
pprint(artifacts_bundle)


# Get all Backups for Artifact Bundles
print("\nGet all Backups for Artifact Bundles")
artifacts_bundle = image_streamer_client.artifact_bundles.get_backups()
pprint(artifacts_bundle)


# Get Backup for an Artifacts Bundle
print("\nGet Backups for an Artifacts Bundle")
artifacts_bundle = image_streamer_client.artifact_bundles.get_backups_by_id(artifact_bundles_information['id_backup'])
pprint(artifacts_bundle)

# Download archive for the Artifact Bundle
print("\nDownload archive for the Artifact Bundle")
artifacts_bundle = image_streamer_client.artifact_bundles.download_archive_artifact_bundle(artifact_bundles_information['id_backup'])
pprint(artifacts_bundle)

# Download the Artifact Bundle
print("\nDownload the Artifact Bundle")
artifacts_bundle = image_streamer_client.artifact_bundles.download_artifact_bundle("0ABDE00534F")
pprint(artifacts_bundle)

# Create a Backup for the Artifact Bundle
print("\nCreate Backup")
response = image_streamer_client.artifact_bundles.create_backup(artifact_bundles_information['deployment_groups'])
pprint(response)

# Create an Artifact Bundle
print("\nCreate")
response = image_streamer_client.artifact_bundles.create(artifact_bundles_to_be_created)
pprint(response)

# Delete an Artifact Bundle
print("\nDelete")
artifact_bundle = image_streamer_client.artifact_bundles.get_by_name(artifact_bundles_to_be_created['name'])
image_streamer_client.artifact_bundles.delete(artifact_bundle)
pprint("Done")

# Update an Artifact Bundle
print("\nUpdate")
artifact_bundle = image_streamer_client.artifact_bundles.get_by_name(artifact_bundles_to_be_created['name'])
response = image_streamer_client.artifact_bundles.update(artifact_bundle, 'Artifact Bundles Test Updated')
pprint(response)

# Extract an Artifact Bundle
print("\nExtract Backup")
response = image_streamer_client.artifact_bundles.extract_bundle(artifact_bundles_information['deployment_groups'])
pprint(response)

# Stop the creation of an Artifact Bundle
print("\nStop creation")
artifact_uri = "/rest/artifact-bundles/04939e89-bcb0-49fc-814f-1a6bc0a2f63c"
task_uri = "/rest/tasks/A15F9270-46FC-48DF-94A9-D11EDB52877E"
response = image_streamer_client.artifact_bundles.stop_artifact_creation(artifact_uri, task_uri)
pprint(response)

