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

# Get all
print("\nGet all SAS logical JBOD attachments")
sas_logical_jbod_attachments = oneview_client.sas_logical_jbod_attachments.get_all()
pprint(sas_logical_jbod_attachments)

if sas_logical_jbod_attachments:
    # Get by URI
    print("\nGet a SAS logical JBOD attachment by URI")
    uri = sas_logical_jbod_attachments[0]['uri']
    sas_logical_jbod_attachment_by_uri = oneview_client.sas_logical_jbod_attachments.get(uri)
    pprint(sas_logical_jbod_attachment_by_uri)

    # Get by name
    print("\nGet a SAS logical JBOD attachment by name")
    name = sas_logical_jbod_attachments[0]['name']
    sas_logical_jbod_attachment_by_name = oneview_client.sas_logical_jbod_attachments.get_by('name', name)
    pprint(sas_logical_jbod_attachment_by_name)
