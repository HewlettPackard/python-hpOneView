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

# This resource is only available on HPE Synergy

config = {
    "ip": "172.16.102.164",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Get all, with defaults
print("Get all SAS Interconnects")
all_sas_interconnects = oneview_client.sas_interconnects.get_all()
pprint(all_sas_interconnects)

# Get the first 10 records
print("\nGet the first ten SAS Interconnects")
sas_interconnects_limited = oneview_client.sas_interconnects.get_all(0, 10)
pprint(sas_interconnects_limited)

if all_sas_interconnects:
    sas_interconnect_uri = all_sas_interconnects[0]['uri']

    # Get by Id
    try:
        print("\nGet a SAS Interconnect by id")
        interconnect_id = sas_interconnect_uri.rsplit('/')[-1]
        sas_interconnect_by_id = oneview_client.sas_interconnects.get(id_or_uri=interconnect_id)
        pprint(sas_interconnect_by_id)
    except HPOneViewException as e:
        print(e.msg)

    # Get by Uri
    print("\nGet a SAS Interconnect by uri")
    sas_interconnect_by_uri = oneview_client.sas_interconnects.get(id_or_uri=sas_interconnect_uri)
    pprint(sas_interconnect_by_uri)

    if sas_interconnect_by_uri["powerState"] == 'Off':
        print("\nTurn on power for SAS interconnect %s" % sas_interconnect_by_uri['name'])
        oneview_client.sas_interconnects.patch(
            id_or_uri=sas_interconnect_uri,
            operation='replace',
            path='/powerState',
            value='On'
        )
        print("Done!")

    print("\nRefresh a SAS interconnect")
    oneview_client.sas_interconnects.refresh_state(
        id_or_uri=sas_interconnect_uri,
        configuration={"refreshState": "RefreshPending"}
    )
    print("Done!")

    print("\nTurn 'On' UID light on SAS interconnect %s" % sas_interconnect_by_uri['name'])
    oneview_client.sas_interconnects.patch(
        id_or_uri=sas_interconnect_uri,
        operation='replace',
        path='/uidState',
        value='On'
    )
    print("Done!")

    print("\nSoft Reset SAS interconnect %s" % sas_interconnect_by_uri['name'])
    oneview_client.sas_interconnects.patch(
        id_or_uri=sas_interconnect_uri,
        operation='replace',
        path='/softResetState',
        value='Reset'
    )
    print("Done!")

    print("\nReset SAS interconnect %s" % sas_interconnect_by_uri['name'])
    oneview_client.sas_interconnects.patch(
        id_or_uri=sas_interconnect_uri,
        operation='replace',
        path='/hardResetState',
        value='Reset'
    )
    print("Done!")

    print("\nTurn off power for SAS interconnect %s" % sas_interconnect_by_uri['name'])
    oneview_client.sas_interconnects.patch(
        id_or_uri=sas_interconnect_uri,
        operation='replace',
        path='/powerState',
        value='Off'
    )
    print("Done!")
