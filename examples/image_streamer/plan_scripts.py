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
from hpOneView.image_streamer_client import ImageStreamerClient

EXAMPLE_CONFIG_FILE = os.path.join(os.path.dirname(__file__), '../config_image_streamer.json')

image_streamer_client = ImageStreamerClient.from_json_file(EXAMPLE_CONFIG_FILE)

plan_script_information = {
    "type": "PlanScript",
    "description": "Description of this plan script",
    "name": "ESXiPlanScriptqq",
    "hpProvided": False,
    "planType": "deploy",
    "content": "f"
}

# Create a Plan Script
print("Create a Plan Script")
plan_script = image_streamer_client.plan_scripts.create(plan_script_information)
pprint(plan_script)

# Update the Plan Script
print("Update the Plan Script")
plan_script_information["description"] = "Nes description"
plan_script = image_streamer_client.plan_scripts.update(plan_script_information)
pprint(plan_script)

# Get the Plan Script by URI
print("Get the Plan Script by URI")
plan_script = image_streamer_client.plan_scripts.get(plan_script['uri'])
pprint(plan_script)

# Get all Plan Scripts
print("Get all Plan Scripts")
plan_scripts = image_streamer_client.plan_scripts.get_all()
pprint(plan_scripts)

# Delete the Plan Script
print("Delete the Plan Script")
plan_scripts = image_streamer_client.plan_scripts.delete(plan_script)
pprint(plan_script)
