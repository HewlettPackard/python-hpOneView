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

build_plan_information = {
    "name": "Demo Build Plan",
    "oeBuildPlanType": "deploy"
}

# Create a Build Plan
print("Create an OS Build Plan")
build_plan_created = image_streamer_client.build_plans.create(build_plan_information)
pprint(build_plan_created)

# Update the Build Plan
print("\nUpdate the OS Build Plan")
build_plan_created["name"] = "Demo Build Plan - Renamed"
build_plan_updated = image_streamer_client.build_plans.update(build_plan_created)
pprint(build_plan_updated)

# Get the Build Plan by URI
print("\nGet the OS Build Plan by URI")
build_plan_by_uri = image_streamer_client.build_plans.get(build_plan_updated['uri'])
pprint(build_plan_by_uri)

# Get all Build Plans
print("\nGet all OS Build Plans")
build_plans = image_streamer_client.build_plans.get_all()
for build_plan in build_plans:
    print(build_plan['name'])

# Delete the Build Plan
print("\nDelete the OS Build Plan")
image_streamer_client.build_plans.delete(build_plan_by_uri)
print("OS Build Plan deleted successfully")
