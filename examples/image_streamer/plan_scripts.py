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

plan_script_information = {
    "description": "Description of this plan script",
    "name": "Demo Plan Script",
    "hpProvided": False,
    "planType": "deploy",
    "content": 'echo "test script"'
}

# Create a Plan Script
print("Create a Plan Script")
plan_script = image_streamer_client.plan_scripts.create(plan_script_information)
pprint(plan_script)
print("***** done *****\n")

# Update the Plan Script
print("Update the Plan Script")
plan_script["description"] = "New description"
plan_script["content"] = 'echo "Commands"\necho "Command 2"'
plan_script = image_streamer_client.plan_scripts.update(plan_script)
pprint(plan_script)
print("***** done *****\n")

# Get the Plan Script by URI
print("Get the Plan Script by URI")
plan_script = image_streamer_client.plan_scripts.get(plan_script['uri'])
pprint(plan_script)
print("***** done *****\n")

# Retrieve the modified contents of the Plan Script
print("Retrieves the modified contents of the Plan Script")
differences = image_streamer_client.plan_scripts.retrieve_differences(plan_script['uri'], "Script content")
pprint(differences)
print("***** done *****\n")

# Get all Plan Scripts
print("Get all Plan Scripts")
plan_scripts = image_streamer_client.plan_scripts.get_all()
for plan_script_item in plan_scripts:
    print(plan_script_item['name'])
print("***** done *****\n")

# Get used by and read only 
print("Gets builds plans which uses a particular read only plan script")
build_plans = image_streamer_client.plan_scripts.get_usedby_and_readonly("cbfd487e-3d92-4eb4-b877-f9ea7c16a271")
for build_plan_item in build_plans:
    print(build_plan_item["name"])
print("**********done***********\n")

# Delete the Plan Script
print("Delete the Plan Script")
image_streamer_client.plan_scripts.delete(plan_script)
print("Plan Script deleted successfully")
