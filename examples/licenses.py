# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2018) Hewlett Packard Enterprise Development LP
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

from config_loader import try_load_from_file
from hpOneView.oneview_client import OneViewClient
from pprint import pprint

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

# Example license Key
# ACDE B9MA H9PY CHW3 U7B5 HWW5 Y9JL KMPL B89H MZVU DXAU 2CSM GHTG L762 KQL7 EG5M KJVT D5KM AFVW TT5J F77K NXWW BPSM YF26 28JS EWTZ X36Q
# M5G7 WZJL HH5Q L975 SNJT 288F ADT2 LK44 56UG V8MC 2K9X 7KG2 F6AD EMVA 9GEB 95Y6 XBM3 HVDY LBSS PU24 KEWY JSJC FPZC 2JJE
# ZLAB\"24R2-02192-002 T1111A HP_OneView_w/o_iLO_Explicit_Feature J4E8IAMANEON\"

options = {
    "key": "<your license Key>",
    "type": "LicenseV500"
}

# Add a License
license = oneview_client.licenses.create(options)
print("\n\nLicense added '%s' successfully.\n" % license['key'])

# Get all licenses
print("\n\n\n\n **********   Displaying all the Licenses loaded on the appliance:  ********** \n\n\n\n")
licenses = oneview_client.licenses.get_all()
pprint(licenses)

# Get License by ID
uri = license['uri']
print uri
print("\n License fetched by ID is: \n")
license = oneview_client.licenses.get_by_id(uri)
pprint(license)

# Delete License by ID
print ("\n\n   ********** Delete the license by ID:  **********")
print uri
oneview_client.licenses.delete(uri)

print("\n Check if the license is Deleted: \n")
lic = oneview_client.licenses.get_by_id(uri)
pprint(lic)
