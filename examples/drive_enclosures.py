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

# This resource is only available on HPE Synergy

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

print("Get all drive enclosures")
drive_enclosures = oneview_client.drive_enclosures.get_all()
pprint(drive_enclosures)

if drive_enclosures:

    first_drive_enclosure = drive_enclosures[0]
    drive_enclosure_uri = first_drive_enclosure["uri"]

    print("\nGet the drive enclosure by URI")
    drive_enclosure_by_uri = oneview_client.drive_enclosures.get(drive_enclosure_uri)
    pprint(drive_enclosure_by_uri)

    product_name = first_drive_enclosure['productName']

    print("\nGet the drive enclosure by product name")
    drive_enclosure_by_product_name = oneview_client.drive_enclosures.get_by('productName', product_name)
    pprint(drive_enclosure_by_product_name)

    print("\nGet the drive enclosure port map")
    port_map = oneview_client.drive_enclosures.get_port_map(drive_enclosure_uri)
    pprint(port_map)

    print("\nRefresh the drive enclosure")
    refresh_config = dict(refreshState="RefreshPending")
    refreshed_drive_enclosure = oneview_client.drive_enclosures.refresh_state(drive_enclosure_uri, refresh_config)
    pprint(refreshed_drive_enclosure)

    print("\nPower off a drive enclosure")
    drive_enclosure_powered_off = oneview_client.drive_enclosures.patch(
        id_or_uri=drive_enclosure_uri,
        operation="replace",
        path="/powerState",
        value="Off"
    )
    pprint(drive_enclosure_powered_off)
