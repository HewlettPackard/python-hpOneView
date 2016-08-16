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

# Get all, with defaults
print("Get all Managed SANs")
managed_sans = oneview_client.managed_sans.get_all()

if managed_sans:
    for managed_san in managed_sans:
        print('  Name: {name} - Manager: {deviceManagerName}'.format(**managed_san))
        if managed_san['imported']:
            imported_san = managed_san
        else:
            internally_managed_san = managed_san

    # Get all, with defaults
    print("Get a Managed SANs by Name")
    managed_san_by_id = oneview_client.managed_sans.get_by_name(managed_san['name'])
    pprint(managed_san_by_id)

    # Get all, with defaults
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

else:
    print("No Managed SANs found.")
