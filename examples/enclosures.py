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
from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException
from config_loader import try_load_from_file

# This example is compatible only for C7000 enclosures

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

# The hostname, enclosure group URI, username, and password must be set on the configuration file
options = {
    "enclosureGroupUri": config['enclosure_group_uri'],
    "hostname": config['enclosure_hostname'],
    "username": config['enclosure_username'],
    "password": config['enclosure_password'],
    "licensingIntent": "OneView"
}

oneview_client = OneViewClient(config)

# Add an Enclosure
enclosure = oneview_client.enclosures.add(options)
enclosure_uri = enclosure['uri']
print("Added enclosure '{name}'.\n  URI = '{uri}'".format(**enclosure))

# Perform a patch operation, replacing the name of the enclosure
enclosure_name = enclosure['name'] + "-Updated"
print("Updating the enclosure to have a name of " + enclosure_name)
enclosure = oneview_client.enclosures.patch(enclosure_uri, 'replace', '/name', enclosure_name)
print("  Done.\n  URI = '{uri}', name = {name}".format(**enclosure))

# Find the recently added enclosure by name
print("Find an enclosure by name")
enclosure = oneview_client.enclosures.get_by('name', enclosure['name'])[0]
print("  URI = '{uri}'".format(**enclosure))

# Get by URI
print("Find an enclosure by URI")
enclosure = oneview_client.enclosures.get(enclosure_uri)
pprint(enclosure)

# Get all enclosures
print("Get all enclosures")
enclosures = oneview_client.enclosures.get_all()
for enc in enclosures:
    print('  {name}'.format(**enc))

# Update configuration
print("Reapplying the appliance's configuration on the enclosure")
try:
    oneview_client.enclosures.update_configuration(enclosure_uri)
    print("  Done.")
except HPOneViewException as e:
    print(e.msg)

print("Retrieve the environmental configuration data for the enclosure")
try:
    environmental_configuration = oneview_client.enclosures.get_environmental_configuration(enclosure_uri)
    print("  Enclosure calibratedMaxPower = {calibratedMaxPower}".format(**environmental_configuration))
except HPOneViewException as e:
    print(e.msg)

# Refresh the enclosure
print("Refreshing the enclosure")
try:
    refresh_state = {"refreshState": "RefreshPending"}
    enclosure = oneview_client.enclosures.refresh_state(enclosure_uri, refresh_state)
    print("  Done")
except HPOneViewException as e:
    print(e.msg)

# Get the enclosure script
print("Get the enclosure script")
try:
    script = oneview_client.enclosures.get_script(enclosure_uri)
    pprint(script)
except HPOneViewException as e:
    print(e.msg)

# Buid the SSO URL parameters
print("Build the SSO (Single Sign-On) URL parameters for the enclosure")
try:
    sso_url_parameters = oneview_client.enclosures.get_sso(enclosure_uri, 'Active')
    pprint(sso_url_parameters)
except HPOneViewException as e:
    print(e.msg)

# Get Statistics specifying parameters
print("Get the enclosure statistics")
try:
    enclosure_statistics = oneview_client.enclosures.get_utilization(enclosure_uri,
                                                                     fields='AveragePower',
                                                                     filter='startDate=2016-06-30T03:29:42.000Z',
                                                                     view='day')
    pprint(enclosure_statistics)
except HPOneViewException as e:
    print(e.msg)

# Remove the recently added enclosure
oneview_client.enclosures.remove(enclosure)
print("Enclosure removed successfully")
