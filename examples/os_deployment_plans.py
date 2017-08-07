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

from config_loader import try_load_from_file
from hpOneView.oneview_client import OneViewClient

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<user>",
        "password": "<password>"
    }
}

# To run this example you must define an OS Deployment Plan ID
os_deployment_plan_id = "81decf85-0dff-4a5e-8a95-52994eeb6493"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

print("\nGet OS Deployment Plans by Filter:")
os_deployment_plans = oneview_client.os_deployment_plans.get_by('deploymentType', 'I3S')
pprint(os_deployment_plans)

print("\nGet the OS Deployment Plan by Name:")
os_deployment_plans = oneview_client.os_deployment_plans.get_by_name('Deployment Plan')
pprint(os_deployment_plans)

print("\nGet all OS Deployment Plans:")
os_deployment_plans_all = oneview_client.os_deployment_plans.get_all()
pprint(os_deployment_plans_all)

print("\nGet an OS Deployment Plan by ID:")
os_deployment_plan = oneview_client.os_deployment_plans.get(os_deployment_plan_id)
pprint(os_deployment_plan)
