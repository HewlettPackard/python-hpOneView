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

import logging

from config_loader import try_load_from_file
from hpOneView.oneview_client import OneViewClient

"""
hpOneView do not add any handlers other than NullHandler.
The configuration of handlers is the prerogative of the developer who uses hpOneView library.
This example uses a StreamHandler to send the logging output to streams sys.stdout and sys.stderr.
"""

logger = logging.getLogger('hpOneView')

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(name)-12s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


config = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

options = {
    "name": "OneViewSDK Test FC Network",
    "connectionTemplateUri": None,
    "autoLoginRedistribution": True,
    "fabricType": "FabricAttach",
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Create a FC Network
fc_network = oneview_client.fc_networks.create(options)

# Find recently created network by name
fc_network = oneview_client.fc_networks.get_by('name', 'OneViewSDK Test FC Network')[0]

# Update autoLoginRedistribution from recently created network
fc_network['autoLoginRedistribution'] = False
fc_network = oneview_client.fc_networks.update(fc_network)

# Get all, with defaults
fc_nets = oneview_client.fc_networks.get_all()
# Filter by name
fc_nets_filtered = oneview_client.fc_networks.get_all(filter="\"'name'='OneViewSDK Test FC Network'\"")

# Get all sorting by name descending
fc_nets_sorted = oneview_client.fc_networks.get_all(sort='name:descending')

# Get the first 10 records
fc_nets_limited = oneview_client.fc_networks.get_all(0, 10)

# Get the created network by uri
oneview_client.fc_networks.get(fc_network['uri'])

# Delete the created network
oneview_client.fc_networks.delete(fc_network)

# Get by Id. This Id doesn't exist
oneview_client.fc_networks.get('3518be0e-17c1-4189-8f81-66t3444f6155')
