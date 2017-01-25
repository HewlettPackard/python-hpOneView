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

from config_loader import try_load_from_file
from hpOneView.exceptions import HPOneViewException
from hpOneView.oneview_client import OneViewClient

config = {
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

certificate_ca_signed_client = {
    "commonName": "default",
    "type": "RabbitMqClientCertV2"
}

certificate_self_signed_client = {
    "commonName": "any",
    "signedCert": "false",
    "type": "RabbitMqClientCertV2"
}


# Generate a CA Signed Certificate
print('Generate a CA Signed Certificate')
try:
    response = oneview_client.certificate_rabbitmq.generate(certificate_ca_signed_client)
    pprint(response)
except HPOneViewException as e:
    print (e.msg)
    if e.oneview_response:
        print e.oneview_response.get('recommendedActions')


# Generate a Self Signed Certificate
print('\nGenerate a Self Signed Certificate')
try:
    response = oneview_client.certificate_rabbitmq.generate(certificate_self_signed_client)
    pprint(response)
except HPOneViewException as e:
    print (e.msg)
    if e.oneview_response:
        print e.oneview_response.get('recommendedActions')


# Get by Alias Name
print('\nGet by Alias Name')
response = oneview_client.certificate_rabbitmq.get('default')
pprint(response)


# Get a Key Pair
print('\nGet a Key Pair')
response = oneview_client.certificate_rabbitmq.get_key_pair('default')
pprint(response)


# Get Keys in Base64 format
print('\nGet Keys in Base64 format')
response = oneview_client.certificate_rabbitmq.get_keys('default', 'Base64')
pprint(response)


# Get Keys in PKCS12 format
print('\nGet Keys in PKCS12 format')
response = oneview_client.certificate_rabbitmq.get_keys('default', 'PKCS12')
pprint(response)
