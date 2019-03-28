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

# This resource is only available on HPE Synergy

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
sas_logical_interconnects = oneview_client.sas_logical_interconnects
firmware_driver_uri = None

# Get all SAS Logical Interconnects
print("\nGet all SAS Logical Interconnects")
logical_interconnects = sas_logical_interconnects.get_all()
for sas_logical_interconnect in logical_interconnects:
    print('  Name: {name}'.format(**sas_logical_interconnect))

name = logical_interconnects[0]['name']
sas_logical_interconnect = sas_logical_interconnects.get_by_name(name)

# Re-applies the configuration on the SAS Logical Interconnect
print("\nRe-applies the configuration on the SAS Logical Interconnect")
sas_logical_interconnect.update_configuration()
print("\n  Done.")

# Return the SAS Logical Interconnect to a consistent state
print("\nReturn the SAS Logical Interconnect to a consistent state")
sas_logical_interconnect.update_compliance()
print("\n  Done. The current consistency state is {consistencyStatus}.".format(**sas_logical_interconnect.data))

# Return the SAS Logical Interconnect list to a consistent state
print("\nReturn the SAS Logical Interconnect list to a consistent state")
compliance_uris = [logical_interconnects[0]['uri']]
sas_logical_interconnect.update_compliance_all(compliance_uris)
print("\n  Done. The current consistency state is {consistencyStatus}.".format(**sas_logical_interconnect.data))

# Replace Drive Enclosure (This example only works with real hardware)
print("\nReplacing Drive Enclosure")
drive_replacement = {
    "oldSerialNumber": "S46016710000J4524YPT",
    "newSerialNumber": "S46016710001J4524YPT"
}
drive_replacement_output = sas_logical_interconnect.replace_drive_enclosure(drive_replacement)
pprint(drive_replacement_output)

# Get installed firmware
print("\nGet the installed firmware for a SAS Logical Interconnect that matches the specified ID.")
firmware = sas_logical_interconnect.get_firmware()
pprint(firmware)

# Install the firmware to a SAS Logical Interconnect (time-consuming operation)
print("\nInstall the firmware to a SAS Logical Interconnect that matches the specified ID.")
firmware_to_install = {
    "command": "Update",
    "force": "false",
    "sppUri": firmware_driver_uri
}
installed_firmware = sas_logical_interconnect.update_firmware(firmware_to_install)
pprint(installed_firmware)
