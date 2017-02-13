# -*- coding: utf-8 -*-
###
# (C) Copyright (2017) Hewlett Packard Enterprise Development LP
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

from examples.config_loader import try_load_from_file
from hpOneView.oneview_client import OneViewClient

config = {
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# To run this example you must set valid URI of the network resource and of the image streamer appliance
management_network_uri = ""
appliance_uri = ""

print("Add an Os Deployment Server:")
resource = {
    "description": "OS Deployment Server",
    "name": "I3s-Deployment Server",
    "mgmtNetworkUri": management_network_uri,
    "applianceUri": appliance_uri,
}
os_deployment_server_added = oneview_client.os_deployment_servers.add(resource)
pprint(os_deployment_server_added)

print("Get all Os Deployment Servers:")
os_deployment_servers_all = oneview_client.os_deployment_servers.get_all(start=0, count=-1, filter='state=Connected')
pprint(os_deployment_servers_all)

os_deployment_server_uri = os_deployment_server_added['uri']

print("Get an Os Deployment Server by URI:")
os_deployment_server = oneview_client.os_deployment_servers.get(os_deployment_server_uri)
pprint(os_deployment_server)

print("Get Os Deployment Servers by Filter:")
os_deployment_servers = oneview_client.os_deployment_servers.get_by('state', 'Connected')
pprint(os_deployment_servers)

print("Get the Os Deployment Server by Name:")
os_deployment_servers = oneview_client.os_deployment_servers.get_by_name("OS Deployment Server")
pprint(os_deployment_servers)

print("Get all Deployment Servers Networks:")
networks = oneview_client.os_deployment_servers.get_networks()
pprint(networks)

print("List all the Image Streamer resources associated with deployment-server:")
appliances = oneview_client.os_deployment_servers.get_appliances()
pprint(appliances)

print("List the particular Image Streamer resource with an given URI:")
appliance = oneview_client.os_deployment_servers.get_appliance(appliances[0]['uri'], 'name')
pprint(appliance)

print("Update the Deployment Server description:")
os_deployment_server_added['description'] = "Description Updated"
os_deployment_server_updated = oneview_client.os_deployment_servers.update(os_deployment_server_added)
pprint(os_deployment_server_updated)

print("Delete the added Deployment Server:")
oneview_client.os_deployment_servers.delete(os_deployment_server_updated)
print("Done")
