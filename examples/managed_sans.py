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

imported_san = None
internally_managed_san = None

# You must set the value of the WWN to run the API 300 example
wwn = ''

# Get all, with defaults
print("Get all Managed SANs")
managed_sans = oneview_client.managed_sans.get_all()

if managed_sans:
    for managed_san in managed_sans:
        print('  Name: {name} - Manager: {deviceManagerName} - Imported: {imported}'.format(**managed_san))
        if managed_san['imported']:
            imported_san = managed_san
        else:
            internally_managed_san = managed_san

    # Get a Managed SAN by name
    print("Get a Managed SAN by name")
    managed_san_by_name = oneview_client.managed_sans.get_by_name(managed_san['name'])
    pprint(managed_san_by_name)

    # Get a Managed SAN by URI
    print("Get a Managed SAN by URI")
    managed_san_by_uri = oneview_client.managed_sans.get(managed_san['uri'])
    pprint(managed_san_by_uri)

    if internally_managed_san:
        # Update the Managed SAN's publicAttributes
        print("Update the Internally Managed SAN's publicAttributes")
        public_attributes = {
            "publicAttributes": [{
                "name": "MetaSan",
                "value": "Neon SAN",
                "valueType": "String",
                "valueFormat": "None"
            }]
        }
        san_response_update_attr = oneview_client.managed_sans.update(internally_managed_san['uri'], public_attributes)
        pprint(san_response_update_attr)

        # Update the Managed SAN's policy
        print("Update the Internally Managed SAN's policy")
        policy = {
            "sanPolicy": {
                "zoningPolicy": "SingleInitiatorAllTargets",
                "zoneNameFormat": "{hostName}_{initiatorWwn}",
                "enableAliasing": True,
                "initiatorNameFormat": "{hostName}_{initiatorWwn}",
                "targetNameFormat": "{storageSystemName}_{targetName}",
                "targetGroupNameFormat": "{storageSystemName}_{targetGroupName}"
            }
        }
        san_response_police_update = oneview_client.managed_sans.update(internally_managed_san['uri'], policy)
        pprint(san_response_police_update)

    if imported_san:
        # Refresh the Managed SAN
        print("Refresh the Imported Managed SAN")
        refresh_config = {
            "refreshState": "RefreshPending"
        }
        san_response_refresh = oneview_client.managed_sans.update(imported_san['uri'], refresh_config)
        pprint(san_response_refresh)

        # Create a SAN endpoints CSV file
        print("Create a SAN endpoints CSV file")
        csv_file_response = oneview_client.managed_sans.create_endpoints_csv_file(imported_san['uri'])
        pprint(csv_file_response)

        # Retrieve the endpoints for a SAN
        print("Get the list of endpoints in the Imported Managed SAN")
        endpoints = oneview_client.managed_sans.get_endpoints(imported_san['uri'])
        pprint(endpoints)

        # Create an unexpected zoning report
        print("Create an unexpected zoning report")
        issues_response = oneview_client.managed_sans.create_issues_report(imported_san['uri'])
        pprint(issues_response)

else:
    print("No Managed SANs found.")

# This method is available for API version 300 or later
if oneview_client.api_version >= 300:
    # Retrieves an association between the provided WWN and the SAN (if any) on which it resides
    print("\nGet a list of associations between provided WWNs and the SANs on which they reside")
    wwns = oneview_client.managed_sans.get_wwn(wwn)
    pprint(wwns)
