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

# To run this example you must define a SAS Logical Interconnect id
sas_logical_interconnect_id = "16b2990f-944a-449a-a78f-004d8b4e6824"

# To install the firmware driver you must define the firmware_driver_uri
firmware_driver_uri = "/rest/firmware-drivers/SPPgen9snap6_2016_0405_87"

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Get by ID
print("Get a SAS Logical Interconnect by ID")
sas_logical_interconnect = oneview_client.sas_logical_interconnects.get(sas_logical_interconnect_id)
pprint(sas_logical_interconnect)

# Get installed firmware
print("Get the installed firmware for a SAS Logical Interconnect that matches the specified ID.")
firmware = oneview_client.sas_logical_interconnects.get_firmware(sas_logical_interconnect_id)
pprint(firmware)

# # Install the firmware to a SAS Logical Interconnect (time-consuming operation)
# print("Install the firmware to a SAS Logical Interconnect that matches the specified ID.")
# firmware_to_install = {
#     "command": "Update",
#     "force": "false",
#     "sppUri": firmware_driver_uri
# }
# installed_firmware = oneview_client.sas_logical_interconnects.update_firmware(firmware_to_install,
#                                                                               sas_logical_interconnect_id)
# pprint(installed_firmware)

# Get all SAS Logical Interconnects
print("Get all SAS Logical Interconnects")
logical_interconnects = oneview_client.sas_logical_interconnects.get_all()
for sas_logical_interconnect in logical_interconnects:
    print('  Name: {name}'.format(**sas_logical_interconnect))

sas_logical_interconnect = logical_interconnects[0]

# Re-applies the configuration on the SAS Logical Interconnect
print("Re-applies the configuration on the SAS Logical Interconnect")
sas_logical_interconnect = oneview_client.sas_logical_interconnects.update_configuration(
    sas_logical_interconnect['uri'])
print("  Done.")

# Return the SAS Logical Interconnect to a consistent state
print("Return the SAS Logical Interconnect to a consistent state")
sas_logical_interconnect = oneview_client.sas_logical_interconnects.update_compliance(sas_logical_interconnect['uri'])
print("  Done. The current consistency state is {consistencyStatus}.".format(**sas_logical_interconnect))

# Return the SAS Logical Interconnect list to a consistent state
print("Return the SAS Logical Interconnect list to a consistent state")
compliance_uris = [
    "/rest/sas-logical-interconnects/" + sas_logical_interconnect_id
]
sas_logical_interconnect = oneview_client.sas_logical_interconnects.update_compliance_all(compliance_uris)
print("  Done. The current consistency state is {consistencyStatus}.".format(**sas_logical_interconnect))

# # Replace Drive Enclosure (This example only works with real hardware)
# print("Replacing Drive Enclosure")
# drive_replacement = {
#     "oldSerialNumber": "S46016710000J4524YPT",
#     "newSerialNumber": "S46016710001J4524YPT"
# }
# drive_replacement_output = oneview_client.sas_logical_interconnects.replace_drive_enclosure(
#     drive_replacement,
#     sas_logical_interconnect['uri'])
# pprint(drive_replacement_output)
