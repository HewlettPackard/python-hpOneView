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

from pprint import pprint
from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException
from config_loader import try_load_from_file

config = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

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
print("Added enclosure '%s'.\n  uri = '%s'" % (enclosure['name'], enclosure['uri']))

# Update the enclosure name
enclosure_name = enclosure['name'] + "-Updated"
print("Updates the enclosure to have a name of '%s'" % enclosure_name)
enclosure = oneview_client.enclosures.patch(enclosure['uri'], 'replace', '/name', enclosure_name)
print("  Completed.\n  uri = '%s', name = %s" % (enclosure['uri'], enclosure['name']))

# Find the recently added enclosure by name
enclosure = oneview_client.enclosures.get_by('name', enclosure['name'])[0]
print("Found an enclosure by name: '%s'.\n  uri = '%s'" % (enclosure['name'], enclosure['uri']))

# Get by Uri
enclosure = oneview_client.enclosures.get(enclosure['uri'])
print("Found an enclosure by uri: '%s'." % enclosure['name'])

# Get all enclosures
print("Get all enclosures")
enclosures = oneview_client.enclosures.get_all()
for enc in enclosures:
    print('  %s' % enc['name'])

print("Reapply the appliance's configuration on the enclosure")
try:
    oneview_client.enclosures.update_configuration(enclosure['uri'])
    print("  Done.")
except HPOneViewException as e:
    print(e.msg['message'])

print("Retrieve environmental configuration data for the enclosure")
try:
    environmental_configuration = oneview_client.enclosures.get_environmental_configuration(enclosure['uri'])
    print("  Enclosure calibratedMaxPower = %s" % environmental_configuration['calibratedMaxPower'])
except HPOneViewException as e:
    print("  %s" % e.msg['message'])

print("Set the calibrated max power of the enclosure")
try:
    config = {"calibratedMaxPower": 2500}
    environmental_configuration = oneview_client.enclosures.update_environmental_configuration(enclosure['uri'], config)
    print("  Enclosure calibratedMaxPower = %s" % environmental_configuration['calibratedMaxPower'])
except HPOneViewException as e:
    print("  %s" % e.msg['message'])

print("Refresh the enclosure")
try:
    config = {"refreshState": "RefreshPending"}
    enclosure = oneview_client.enclosures.refresh_state(enclosure['uri'], config)
    print("  Done")
except HPOneViewException as e:
    print("  %s" % e.msg['message'])

print("Get the enclosure script")
try:
    script = oneview_client.enclosures.get_script(enclosure['uri'])
    pprint(script)
except HPOneViewException as e:
    print("  %s" % e.msg['message'])

print("Builds the SSO (Single Sign-On) URL parameters for the enclosure")
try:
    sso_url_parameters = oneview_client.enclosures.get_sso(enclosure['uri'], 'Active')
    pprint(sso_url_parameters)
except HPOneViewException as e:
    print("  %s" % e.msg['message'])

# Remove the recently added enclosure
oneview_client.enclosures.remove(enclosure)
print("Enclosure removed successfully")

# Get Statistics with defaults
ENCLOSURE_ID = "09SGH102X6J1"

print("Get enclosure statistics")
try:
    enclosure_statistics = oneview_client.enclosures.get_utilization(ENCLOSURE_ID)
    pprint(enclosure_statistics)
except HPOneViewException as e:
    print(e.msg['message'])

# Get Statistics specifying parameters
print("Get enclosure statistics")
try:
    enclosure_statistics = oneview_client.enclosures.get_utilization(ENCLOSURE_ID,
                                                                     fields='AveragePower',
                                                                     filter='startDate=2016-05-30T03:29:42.000Z',
                                                                     view='day')
    pprint(enclosure_statistics)
except HPOneViewException as e:
    print(e.msg['message'])
