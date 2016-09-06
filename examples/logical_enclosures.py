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

oneview_client = OneViewClient(config)

# Get first logical enclosure
logical_enclosure = oneview_client.logical_enclosures.get_all()[0]
print("Found logical enclosure '{}' at\n   uri: '{}'".format(
    logical_enclosure['name'], logical_enclosure['uri']))

# Update the logical enclosure name
logical_enclosure_name = logical_enclosure['name']
logical_enclosure['name'] = logical_enclosure_name + "-updated"
print("Update the logical enclosure to have a name of '%s'" %
      logical_enclosure['name'])
logical_enclosure = oneview_client.logical_enclosures.update(logical_enclosure)
print("   Done. uri: '%s', 'name': '%s'" %
      (logical_enclosure['uri'], logical_enclosure['name']))
print("Reset name")
logical_enclosure['name'] = logical_enclosure_name
logical_enclosure = oneview_client.logical_enclosures.update(logical_enclosure)
print("   Done.")

# Get logical enclosure by id
try:
    logical_enclosure_by_id = oneview_client.logical_enclosures.get(
        "acb17b89-6724-4602-818a-1ee20ed4ec60")
    print("Got logical enclosure '{}' by id: 'acb17b89-6724-4602-818a-1ee20ed4ec60'\n   uri: '{}'".format(
        logical_enclosure_by_id['name'], logical_enclosure_by_id['uri']))
except HPOneViewException as e:
    print(e.msg['message'])

# Get logical enclosure by uri
logical_enclosure = oneview_client.logical_enclosures.get(
    logical_enclosure['uri'])
print("Got logical enclosure '{}' by\n   uri: '{}'".format(
    logical_enclosure['name'], logical_enclosure['uri']))
pprint(logical_enclosure)

# Get logical enclosure by name
try:
    logical_enclosure_by_name = oneview_client.logical_enclosures.get_by('name', logical_enclosure['name'])[0]
    print("Got logical enclosure by name '{name}'\n   uri: '{uri}'".format(**logical_enclosure_by_name))
except HPOneViewException as e:
    print(e.msg['message'])

# Update configuration
print("Reapply the appliance's configuration to the logical enclosure")
try:
    oneview_client.logical_enclosures.update_configuration(
        logical_enclosure['uri'])
    print("   Done.")
except HPOneViewException as e:
    print(e.msg['message'])

# update and get script
print("Update script")
script = "# TEST COMMAND"
logical_enclosure = oneview_client.logical_enclosures.update_script(
    logical_enclosure['uri'], script)
print("   updated script: '{}'".format(
    oneview_client.logical_enclosures.get_script(logical_enclosure['uri'])))

# create support dumps
print("Generate support dump")
info = {
    "errorCode": "MyDump16",
    "encrypt": True,
    "excludeApplianceDump": False
}
support_dump = oneview_client.logical_enclosures.generate_support_dump(
    info, logical_enclosure['uri'])
print("   Done")

# update from group
print("Update from group")
try:
    logical_enclosure = oneview_client.logical_enclosures.update_from_group(
        logical_enclosure['uri'])
    print("   Done")
except HPOneViewException as e:
    print("  %s" % e.msg['message'])

# Get all logical enclosures
print("Get all logical enclosures")
logical_enclosures = oneview_client.logical_enclosures.get_all()
for enc in logical_enclosures:
    print('   %s' % enc['name'])
