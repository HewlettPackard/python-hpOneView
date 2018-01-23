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

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)
try:
    # The valid enclosure URIs need to be inserted sorted by URI
    # The number of enclosure URIs must be equal to the enclosure count in the enclosure group
    options = dict(
        enclosureUris=[],
        enclosureGroupUri="",
        forceInstallFirmware=False,
        name="LogicalEnclosure2",
        initialScopeUris=["/rest/scopes/cd237b60-09e2-45c4-829e-082e318a6d2a", "/rest/scopes/e9dde1f2-69d5-461b-871d-1790aebbc519"]
    )

    # Get enclosure group for creating logical enclosure
    enclosure_groups = oneview_client.enclosure_groups.get_all()
    first_enclosure_groups = enclosure_groups[0]
    options["enclosureGroupUri"] = first_enclosure_groups["uri"]
    enclosure_count = first_enclosure_groups["enclosureCount"]

    # Get enclosures
    enclosures = oneview_client.enclosures.get_all()
    enclosure_uris = []
    for i in range(0, enclosure_count):
        enclosure_uris.append(enclosures[i]["uri"])
    options["enclosureUris"] = enclosure_uris

    # Create a logical enclosure
    # This method is only available on HPE Synergy.
    logical_enclosure_created = oneview_client.logical_enclosures.create(options)
    print("Created logical enclosure'%s' successfully.\n  uri = '%s'" % (
        logical_enclosure_created['name'],
        logical_enclosure_created['uri'])
    )

    # Delete the logical enclosure created
    # This method is only available on HPE Synergy.
    oneview_client.logical_enclosures.delete(logical_enclosure_created)
    print("Delete logical enclosure")
except HPOneViewException as e:
    print(e.msg)

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
        "5a136d8e-d44a-42f9-bf28-5c93a93f8663")
    print("Got logical enclosure '{}' by id: '5a136d8e-d44a-42f9-bf28-5c93a93f8663'\n   uri: '{}'".format(
        logical_enclosure_by_id['name'], logical_enclosure_by_id['uri']))
except HPOneViewException as e:
    print(e.msg)

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
    print(e.msg)
# Get Logical Enclosure by scope_uris
if oneview_client.api_version == 600:
    le_by_scope_uris = oneview_client.logical_enclosures.get_all(scope_uris="\"'/rest/scopes/cd237b60-09e2-45c4-829e-082e318a6d2a'\"")
    if len(le_by_scope_uris) > 0:
        print("Got Logical Enclosure by scope_uris: '%s'.\n  uri = '%s'" % (le_by_scope_uris[0]['name'], le_by_scope_uris[0]['uri']))
        pprint(le_by_scope_uris)
    else:
        print("No Logical Enclosure found by scope_uris")

# Update configuration
print("Reapply the appliance's configuration to the logical enclosure")
try:
    oneview_client.logical_enclosures.update_configuration(
        logical_enclosure['uri'])
    print("   Done.")
except HPOneViewException as e:
    print(e.msg)

# update and get script
print("Update script")
try:
    script = "# TEST COMMAND"
    logical_enclosure = oneview_client.logical_enclosures.update_script(
        logical_enclosure['uri'], script)
    print("   updated script: '{}'".format(
        oneview_client.logical_enclosures.get_script(logical_enclosure['uri'])))
except HPOneViewException as e:
    print("  %s" % e.msg)

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
    print("  %s" % e.msg)

# Get all logical enclosures
print("Get all logical enclosures")
logical_enclosures = oneview_client.logical_enclosures.get_all()
for enc in logical_enclosures:
    print('   %s' % enc['name'])

if oneview_client.api_version >= 300:

    if logical_enclosures:

        print("Update firmware for a logical enclosure with the logical-interconnect validation set as true.")

        logical_enclosure = logical_enclosures[0]

        logical_enclosure_updated = oneview_client.logical_enclosures.patch(
            id_or_uri=logical_enclosure["uri"],
            operation="replace",
            path="/firmware",
            value={
                "firmwareBaselineUri": "/rest/firmware-drivers/spp-2017_04_0-SPP2017040_2017_0420_14",
                "firmwareUpdateOn": "EnclosureOnly",
                "forceInstallFirmware": "true",
                "validateIfLIFirmwareUpdateIsNonDisruptive": "true",
                "logicalInterconnectUpdateMode": "Orchestrated",
                "updateFirmwareOnUnmanagedInterconnect": "true"
            }
        )

        pprint(logical_enclosure_updated)
