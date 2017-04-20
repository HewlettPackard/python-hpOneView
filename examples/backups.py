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
from hpOneView.exceptions import HPOneViewException
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

# Create a new appliance backup
print("\n## Create a new appliance backup")
backup_details = oneview_client.backups.create()
pprint(backup_details)

filename = backup_details['id']

# Download the backup archive
print("\n## Download the previously created backup archive")
response = oneview_client.backups.download(backup_details['downloadUri'], filename)
print(response)

# Upload the backup archive
print("\n## Upload the previously downloaded backup archive")
backup_details = oneview_client.backups.upload(filename)
pprint(backup_details)

# Get by URI
print("\n## Find recently created backup by URI")
backup_by_uri = oneview_client.backups.get(backup_details['uri'])
pprint(backup_by_uri)

# Get all backups
print("\n## Get all backups")
backups = oneview_client.backups.get_all()
pprint(backups)

# Get the details of the backup configuration
print("\n## Get the details of the backup configuration for the remote server and automatic backup schedule")
config = oneview_client.backups.get_config()
pprint(config)

# Update the backup configuration
try:
    print("\n## Update the backup configuration")
    config['scheduleTime'] = '23:00'
    updated_config = oneview_client.backups.update_config(config)
    pprint(updated_config)
except HPOneViewException as e:
    print(e.msg)

# Save the backup file to a previously-configured remote location
try:
    print("\n## Save the backup file to a previously-configured remote location")
    backup_details = oneview_client.backups.update_remote_archive(backup_details['saveUri'])
    pprint(backup_details)
except HPOneViewException as e:
    print(e.msg)
