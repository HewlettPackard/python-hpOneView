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

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    },
    "api_version": 800
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)
connection_templates = oneview_client.connection_templates

# The name and ID of an existent Connection Template must be set to run this example
connection_template_name = 'defaultConnectionTemplate'

# Get all connection templates
print("Get all connection templates")
con_templates = connection_templates.get_all()
pprint(con_templates)

# Get all sorting by name descending
print("Get all connection templates sorting by name")
con_templates_sorted = connection_templates.get_all(sort='name:descending')
pprint(con_templates_sorted)

# Get default template
print("Get default connection template")
con_template_default = connection_templates.get_default()
pprint(con_template_default)

# Get by name
print("Get a connection_template by name")
con_template_byname = connection_templates.get_by_name(connection_template_name)
pprint(con_template_byname.data)

# Update the connection_template retrieved in the last operation
print("Update the retrieved connection_template typicalBandwidth")
template_byname = con_template_byname.data.copy()
template_byname['bandwidth']['typicalBandwidth'] = 5000
con_template_updated = con_template_byname.update(template_byname)
pprint(con_template_updated.data)
