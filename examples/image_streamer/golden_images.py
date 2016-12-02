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

# You must set a valid osVolumeURI and buildPlanUri
golden_image_information = {
    "type": "GoldenImage",
    "name": "Demo Golden Image Creation",
    "description": "Test",
    "imageCapture": "true",
    "osVolumeURI": "/rest/os-volumes/57f2d803-9c11-4f9a-bc02-71804a0fcc3e",
    "buildPlanUri": "/rest/build-plans/b199aada-ed44-4785-8ced-cd979386d4db"
}

golden_image_upload = {
    "name": "Demo Golden Image",
    "description": "Test",
}

local_image_file_name = 'c:/Util/Licenses.zip'

# Create a Golden Image
print("Create a Golden Image")
golden_image_created = image_streamer_client.golden_images.create(golden_image_information)
pprint(golden_image_created)
print("***** done *****\n")

# Upload a Golden Image
print("Upload a Golden Image")
image_streamer_client.golden_images.upload(local_image_file_name, golden_image_upload)
print("***** done *****\n")

# Get the Golden Image by URI
print("Get the Golden Image by URI")
golden_image = image_streamer_client.golden_images.get_by('name', golden_image_upload['name'])[0]
pprint(golden_image)
print("***** done *****\n")

# Update the Golden Image
print("Update the Golden Image")
golden_image["description"] = "New description"
golden_image = image_streamer_client.golden_images.update(golden_image)
pprint(golden_image)
print("***** done *****\n")

# Get the Golden Image by URI
print("Get the Golden Image by URI")
golden_image = image_streamer_client.golden_images.get(golden_image['uri'])
pprint(golden_image)
print("***** done *****\n")

# Download the Golden Image
print("Get the Golden Image")
golden_image_file = image_streamer_client.golden_images.download(golden_image['uri'])
print("***** golden_image_file downloaded *****\n")

# Retrieve archived logs of the Golden Image
print("Retrieve archived logs of the Golden Image")
archieve = image_streamer_client.golden_images.get_archive(golden_image_created['uri'])
pprint(archieve)
print("***** done *****\n")

# Get all Golden Images
print("Get all Golden Images")
golden_images = image_streamer_client.golden_images.get_all()
for golden_image_item in golden_images:
    print(golden_image_item['name'])
print("***** done *****\n")

# Delete the Golden Image
print("Delete the Golden Images")
image_streamer_client.golden_images.delete(golden_image)
image_streamer_client.golden_images.delete(golden_image_created)
print("Golden Images deleted successfully")
