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

config = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": "123456"
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# A Uri for a backup to restore must be set to run this example
uri_of_backup_to_restore = "/rest/backups/example_backup_2017-04-25_195515"

# Start a restore
print("Starting a restore")
options = {
    "uriOfBackupToRestore": uri_of_backup_to_restore
}
restore = oneview_client.restores.restore(options)
pprint(restore)

# Get all restores
print("Get all Restores")
restores = oneview_client.restores.get_all()
pprint(restores)

# Get by
print("\nGet a Restore by hostName equals to '{}'".format(restore['hostName']))
restore_by_host_name = oneview_client.restores.get_by("hostName", restore['hostName'])
pprint(restore_by_host_name)

# Get by URI
print("\nGet a Restore by URI")
restore_by_uri = oneview_client.restores.get(restore['uri'])
pprint(restore_by_uri)

# Get Restore Failure
print("\nRetrieving Restore Failure")
failures = oneview_client.restores.get_failure()
pprint(failures)
