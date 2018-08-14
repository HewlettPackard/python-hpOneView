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
from hpOneView.exceptions import HPOneViewException, HPOneViewTaskError
from config_loader import try_load_from_file

# This example is compatible only for C7000 enclosures

config = {
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    },
    "enclosure_group_uri": "",
    "enclosure_hostname": "",
    "enclosure_username": "",
    "enclosure_password": "",
}

# Declare a CA signed certificate file path.
certificate_file = ""

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

# The hostname, enclosure group URI, username, and password must be set on the configuration file
options = {
    "name": "Encl1-Updated-Updated-Updated",
    "enclosureGroupUri": config['enclosure_group_uri'],
    "hostname": config['enclosure_hostname'],
    "username": config['enclosure_username'],
    "password": config['enclosure_password'],
    "licensingIntent": "OneView"
}

# Get OneView client
oneview_client = OneViewClient(config)

# Add an enclosure
try:
    # This will return an enclosure object
    enclosure = oneview_client.enclosures.add(options)
    print("Added enclosure '{name}'.\n  URI = '{uri}'".format(**enclosure.data))
except HPOneViewTaskError, e:
    print(e)
    # Get the reosurce by name
    enclosure = oneview_client.enclosures.get_by_name(options['name'])

# Perform a patch operation on the enclosure, replacing name of the enclosure
enclosure_name = "Encl1-Updated"
print("Updating the enclosure to have a name of " + enclosure_name)
enclosure.patch('replace', '/name', enclosure_name)
print("  Done.\n  URI = '{uri}', name = {name}".format(**enclosure.data))

# Get by URI
print("Find an enclosure by URI")
enclosure = enclosure.get_by_uri(enclosure.data['uri'])
pprint(enclosure.data)

# Get all enclosures
print("Get all enclosures")
enclosures = enclosure.get_all()
for enc in enclosures:
    print('  {name}'.format(**enc))

# Update configuration
print("Reapplying the appliance's configuration on the enclosure")
try:
    enclosure.update_configuration()
    print("  Done.")
except HPOneViewException as e:
    print(e.msg)

print("Retrieve the environmental configuration data for the enclosure")
try:
    environmental_configuration = enclosure.get_environmental_configuration()
    print("  Enclosure calibratedMaxPower = {calibratedMaxPower}".format(**environmental_configuration))
except HPOneViewException as e:
    print(e.msg)

# Refresh the enclosure
print("Refreshing the enclosure")
try:
    refresh_state = {"refreshState": "RefreshPending"}
    enclosure.refresh_state(refresh_state)
    print("  Done")
except HPOneViewException as e:
    print(e.msg)

# Get the enclosure script
print("Get the enclosure script")
try:
    script = enclosure.get_script()
    pprint(script)
except HPOneViewException as e:
    print(e.msg)

# Buid the SSO URL parameters
print("Build the SSO (Single Sign-On) URL parameters for the enclosure")
try:
    sso_url_parameters = enclosure.get_sso('Active')
    pprint(sso_url_parameters)
except HPOneViewException as e:
    print(e.msg)

# Get Statistics specifying parameters
print("Get the enclosure statistics")
try:
    enclosure_statistics = enclosure.get_utilization(fields='AveragePower',
                                                     filter='startDate=2016-06-30T03:29:42.000Z',
                                                     view='day')
    pprint(enclosure_statistics)
except HPOneViewException as e:
    print(e.msg)

# Create a Certificate Signing Request (CSR) for the enclosure.
bay_number = 1  # Required for C7000 enclosure
csr_data = {
    "type": "CertificateDtoV2",
    "organization": "",
    "organizationalUnit": "",
    "locality": "",
    "state": "",
    "country": "",
    "commonName": ""
}
try:
    enclosure.generate_csr(csr_data, bay_number=bay_number)
    print("Generated CSR for the enclosure.")
except HPOneViewException as e:
    print(e.msg)

# Get the certificate Signing Request (CSR) that was generated by previous POST.
try:
    csr = enclosure.get_csr(bay_number=bay_number)
    with open('enclosure.csr', 'w') as csr_file:
            csr_file.write(csr["base64Data"])
    print("Saved CSR(generated by previous POST) to 'enclosure.csr' file")
except HPOneViewException as e:
    print(e.msg)

try:
    # Get Enclosure by scope_uris
    if oneview_client.api_version >= 600:
        enclosures_by_scope_uris = enclosure.get_all(scope_uris="\"'/rest/scopes/3bb0c754-fd38-45af-be8a-4d4419de06e9'\"")
        if len(enclosures_by_scope_uris) > 0:
            print("Found %d Enclosures" % (len(enclosures_by_scope_uris)))
            i = 0
            while i < len(enclosures_by_scope_uris):
                print("Found Enclosures by scope_uris: '%s'.\n  uri = '%s'" % (enclosures_by_scope_uris[i]['name'], enclosures_by_scope_uris[i]['uri']))
                i += 1
            pprint(enclosures_by_scope_uris)
        else:
            print("No Enclosures Group found.")
except HPOneViewException as e:
    print(e.msg)

# Import a CA signed certificate to the enclosure.
try:
    # This action requires a certificate(CA signed) file path to be declared.
    if certificate_file:
        with open(certificate_file, "r") as file_object:
            certificate = file_object.read()

        certificate_data = {
            "type": "CertificateDataV2",
            "base64Data": certificate
        }

        enclosure.import_certificate(certificate_data, enclosure.data['uri'], bay_number=bay_number)
        print("Imported Signed Certificate  to the enclosure.")
except HPOneViewException as e:
    print(e.msg)

# Remove the recently added enclosure
enclosure.remove()
print("Enclosure removed successfully")
