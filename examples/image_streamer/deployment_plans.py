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

import os
from pprint import pprint
from hpOneView.oneview_client import OneViewClient

EXAMPLE_CONFIG_FILE = os.path.join(os.path.dirname(__file__), '../config.json')

oneview_client = OneViewClient.from_json_file(EXAMPLE_CONFIG_FILE)

image_streamer_client = oneview_client.create_image_streamer_client()

# To run this example set a valid Build Plan URI
deployment_plan_information = {
    "name": "Demo Deployment Plan",
    "description": "",
    "hpProvided": "false",
    "oeBuildPlanURI": "/rest/build-plans/1beb9333-66a8-48d5-82b6-1bda1a81582a",
}

if oneview_client.api_version >= 500:
    deployment_plan_information["type"] = "OEDeploymentPlanV5"

# Create a Deployment Plan
print("Create a Deployment Plan")
deployment_plan_created = image_streamer_client.deployment_plans.create(deployment_plan_information)
pprint(deployment_plan_created)

# Update the Deployment Plan
print("\nUpdate the Deployment Plan")
deployment_plan_created["name"] = "Demo Deployment Plan - Renamed"
deployment_plan_updated = image_streamer_client.deployment_plans.update(deployment_plan_created)
pprint(deployment_plan_updated)

# Get the Deployment Plan by URI
print("\nGet the Deployment Plan by URI")
deployment_plan_by_uri = image_streamer_client.deployment_plans.get(deployment_plan_created['uri'])
pprint(deployment_plan_by_uri)

# Get the Deployment Plan by name
print("\nGet the Deployment Plan by name")
deployment_plan_by_name = image_streamer_client.deployment_plans.get_by('name', deployment_plan_updated['name'])
pprint(deployment_plan_by_name)

# Get all Deployment Plans
print("\nGet all Deployment Plans")
deployment_plans = image_streamer_client.deployment_plans.get_all()
for deployment_plan in deployment_plans:
    print(deployment_plan['name'])

if oneview_client.api_version >= 600:
    # Get the list of ServerProfile and ServerProfileTemplate URI that are using OEDP {id}
    print("\nGet the list of ServerProfile and ServerProfileTemplate URI that are using OEDP {id}")
    deployment_osdp = image_streamer_client.deployment_plans.get_osdp(deployment_plan_created['id'])
    pprint(deployment_osdp)

if oneview_client.api_version >= 500:
    # Get the list of ServerProfile and ServerProfileTemplate URI that are using OEDP {id}
    print("\nGet the list of ServerProfile and ServerProfileTemplate URI that are using OEDP {id}")
    deployment_osdp = image_streamer_client.deployment_plans.get_osdp(deployment_plan_created['id'])
    pprint(deployment_osdp)

# Delete the Deployment Plan
print("\nDelete the Deployment Plan")
image_streamer_client.deployment_plans.delete(deployment_plan_by_uri)
print("Deployment Plan deleted successfully")
