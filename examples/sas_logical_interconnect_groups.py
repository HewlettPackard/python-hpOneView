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
from config_loader import try_load_from_file

# This example works only with the API version 300 or higher

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

# The Interconnect Type URI which is permitted to form SAS interconnect map must be defined to run this example
permittedInterconnectTypeUri = '/rest/sas-interconnect-types/Synergy12GbSASConnectionModule'

# Create a SAS Logical Interconnect Group
data = {
    "name": "Test SAS Logical Interconnect Group",
    "state": "Active",
    "interconnectMapTemplate": {
        "interconnectMapEntryTemplates": [{
            "logicalLocation": {
                "locationEntries": [
                    {
                        "type": "Bay",
                        "relativeValue": 1
                    }, {
                        "type": "Enclosure",
                        "relativeValue": 1
                    }
                ]
            },
            "enclosureIndex": 1,
            "permittedInterconnectTypeUri": permittedInterconnectTypeUri
        }, {
            "logicalLocation": {
                "locationEntries": [
                    {
                        "type": "Bay",
                        "relativeValue": 4
                    }, {
                        "type": "Enclosure",
                        "relativeValue": 1
                    }
                ]
            },
            "enclosureIndex": 1,
            "permittedInterconnectTypeUri": permittedInterconnectTypeUri
        }]
    },
    "enclosureType": "SY12000",
    "enclosureIndexes": [1],
    "interconnectBaySet": 1
}
sas_lig_created = oneview_client.sas_logical_interconnect_groups.create(data)
print("SAS Logical Interconnect Group '{name}' created successfully.\n  uri = '{uri}'".format(**sas_lig_created))

# Get all SAS Logical Interconnect Groups
print("Get all SAS Logical Interconnect Groups")
sas_ligs = oneview_client.sas_logical_interconnect_groups.get_all()
for sas_lig in sas_ligs:
    print("   '{name}' at uri: {uri}".format(**sas_lig))

# Get a SAS Logical Interconnect Group by URI
print("Get a SAS Logical Interconnect Group by URI")
sas_lig_found_by_uri = oneview_client.sas_logical_interconnect_groups.get(sas_lig_created['uri'])
pprint(sas_lig_found_by_uri)

# Get a SAS Logical Interconnect Group by name
print("Get a SAS Logical Interconnect Group by name")
sas_lig_found_by_name = oneview_client.sas_logical_interconnect_groups.get_by('name', data['name'])
print("   '{name}' at uri: {uri}".format(**sas_lig_found_by_name[0]))

# Update the SAS Logical Interconnect Group
print("Update the SAS Logical Interconnect Group")
resource_to_update = sas_lig_created.copy()
resource_to_update['name'] = 'Test SAS Logical Interconnect Group - Renamed'

sas_lig_updated = oneview_client.sas_logical_interconnect_groups.update(resource_to_update)
pprint(sas_lig_updated)

# Delete the SAS Logical Interconnect Group
oneview_client.sas_logical_interconnect_groups.delete(sas_lig_updated)
print("SAS Logical Interconnect Group deleted successfully")
