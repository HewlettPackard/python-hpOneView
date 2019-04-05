# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2019) Hewlett Packard Enterprise Development LP
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

enclosure_groups = oneview_client.enclosure_groups
enclosures = oneview_client.enclosures
logical_enclosures = oneview_client.logical_enclosures

# The valid enclosure URIs need to be inserted sorted by URI
# The number of enclosure URIs must be equal to the enclosure count in the enclosure group
options = dict(
    enclosureUris=[],
    enclosureGroupUri="",
    forceInstallFirmware=False,
    name="LogicalEnclosure2"
)

# Get all logical enclosures
print("Get all logical enclosures")
logical_enclosures_all = logical_enclosures.get_all()
for enc in logical_enclosures_all:
    print('   %s' % enc['name'])

# Get first logical enclosure
logical_enclosure_all = logical_enclosures.get_all()
if logical_enclosure_all:
    logical_enclosure = logical_enclosure_all[0]
    print("Found logical enclosure '{}' at\n   uri: '{}'".format(
        logical_enclosure['name'], logical_enclosure['uri']))

    # Get logical enclosure by uri
    logical_enclosure = logical_enclosures.get_by_uri(logical_enclosure['uri'])
    print("Got logical enclosure '{}' by\n   uri: '{}'".format(
        logical_enclosure.data['name'], logical_enclosure.data['uri']))

# Get Logical Enclosure by scope_uris
if oneview_client.api_version >= 600:
    le_by_scope_uris = logical_enclosures.get_all(scope_uris="\"'/rest/scopes/cd237b60-09e2-45c4-829e-082e318a6d2a'\"")
    if len(le_by_scope_uris) > 0:
        print("Got Logical Enclosure by scope_uris: '%s'.\n  uri = '%s'" % (le_by_scope_uris[0]['name'], le_by_scope_uris[0]['uri']))
        pprint(le_by_scope_uris)
    else:
        print("No Logical Enclosure found by scope_uris")

# Get Logical Enclosure by name
logical_enclosure = logical_enclosures.get_by_name(options["name"])
if not logical_enclosure:
    # Get enclosure group for creating logical enclosure
    enclosure_groups_all = enclosure_groups.get_all()
    first_enclosure_groups = enclosure_groups_all[0]
    options["enclosureGroupUri"] = first_enclosure_groups["uri"]
    enclosure_count = first_enclosure_groups["enclosureCount"]

    # Get enclosures
    enclosures_all = enclosures.get_all()
    enclosure_uris = []
    for i in range(0, enclosure_count):
        enclosure_uris.append(enclosures_all[i]["uri"])
    options["enclosureUris"] = sorted(enclosure_uris)

    # Create a logical enclosure
    # This method is only available on HPE Synergy.
    logical_enclosure = logical_enclosures.create(options)
    print("Created logical enclosure'%s' successfully.\n  uri = '%s'" % (
        logical_enclosure['name'],
        logical_enclosure['uri'])
    )

# Update the logical enclosure name
print("Update the logical enclosure to have a name of '%s'" %
      options["name"])
resource = logical_enclosure.data.copy()
previous_name = resource["name"]
resource["name"] = resource["name"] + "-Renamed"
logical_enclosure.update(resource)
print("   Done. uri: '%s', 'name': '%s'" %
      (logical_enclosure.data['uri'], logical_enclosure.data['name']))

print("Reset name")
resource["name"] = previous_name
logical_enclosure.update(resource)
print("   Done. uri: '%s', 'name': '%s'" %
      (logical_enclosure.data['uri'],
       logical_enclosure.data['name']))

# Update configuration
print("Reapply the appliance's configuration to the logical enclosure")
logical_enclosure.update_configuration()
print("   Done.")

# Update and get script
print("Update script")
script = "# TEST COMMAND"
logical_enclosure_updated = logical_enclosure.update_script(
    logical_enclosure.data['uri'], script)
print("   updated script: '{}'".format(
    logical_enclosure.get_script()))

# Create support dumps
print("Generate support dump")
info = {
    "errorCode": "MyDump16",
    "encrypt": True,
    "excludeApplianceDump": False
}
support_dump = logical_enclosure.generate_support_dump(info)
print("   Done")

# update from group
print("Update from group")
logical_enclosure_updated = logical_enclosure.update_from_group()
print("   Done")

if oneview_client.api_version >= 300:
    if logical_enclosure:
        print("Update firmware for a logical enclosure with the logical-interconnect validation set as true.")

        logical_enclosure_updated = logical_enclosure.patch(
            operation="replace",
            path="/firmware",
            value={
                "firmwareBaselineUri": "/rest/firmware-drivers/SPP_2018_06_20180709_for_HPE_Synergy_Z7550-96524",
                "firmwareUpdateOn": "EnclosureOnly",
                "forceInstallFirmware": "true",
                "validateIfLIFirmwareUpdateIsNonDisruptive": "true",
                "logicalInterconnectUpdateMode": "Orchestrated",
                "updateFirmwareOnUnmanagedInterconnect": "true"
            },
            custom_headers={"if-Match": "*"}
        )
        pprint(logical_enclosure_updated.data)

# Delete the logical enclosure created
# This method is only available on HPE Synergy.
logical_enclosure.delete()
print("Delete logical enclosure")
