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
"""
This example uses fc_networks to demonstrate how to use task_monitor to watch tasks
"""
import time
from hpOneView.oneview_client import OneViewClient
from hpOneView.resources.task_monitor import TaskMonitor
from config_loader import try_load_from_file

config = {
    "ip": "172.16.102.59",
    "credentials": {
        "authLoginDomain": "",
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

print("Connecting...")
oneview_client = OneViewClient(config)

options = {
    "name": "OneViewSDK Test FC Network",
    "connectionTemplateUri": None,
    "autoLoginRedistribution": True,
    "fabricType": "FabricAttach",
}

# TaskMonitor instance needs a connection
task_monitor = TaskMonitor(oneview_client.connection)

# Create a FC Network (non blocking)
print("Create fc-network with blocking=False")
task = oneview_client.fc_networks.create(options, blocking=False)
print("Waiting task completion...")
fc_network = task_monitor.wait_for_task(task, 20)
print("Task completed")
print("Created fc-network '%s' sucessfully.\n  uri = '%s'" % (fc_network['name'], fc_network['uri']))

# Update a FC Network (non blocking) - Using wait_for_task
fc_network['name'] = "OneViewSDK Test FC Network (renamed)"
print("Update fc-network with blocking=False")
task = oneview_client.fc_networks.update(fc_network, blocking=False)
print("Waiting task completion...")
fc_network = task_monitor.wait_for_task(task, 20)
print("Task completed")
print("Updated fc-network '%s' sucessfully.\n  uri = '%s'" % (fc_network['name'], fc_network['uri']))

# Update a FC Network (non blocking) - Using external wait loop
fc_network['name'] = "OneViewSDK Test FC Network (renamed again)"
task = oneview_client.fc_networks.update(fc_network, blocking=False)

# Check if task is still running, without timeout
print("Waiting task completion...")
while task_monitor.is_task_running(task):
    print("Waiting task completion...")
    time.sleep(1)
print("Task completed")

# Get associated resource
print("Getting associated resource...")
task, fc_network = task_monitor.get_associated_resource(task)
print("Task completed")
print("Updated fc-network '%s' sucessfully.\n  uri = '%s'" % (fc_network['name'], fc_network['uri']))

# Delete the created network
print("Deleting the fc-network")
task = oneview_client.fc_networks.delete(fc_network, blocking=False)
print("Waiting task completion...")
task = task_monitor.wait_for_task(task, 20)
print("Sucessfully deleted the fc-network")
