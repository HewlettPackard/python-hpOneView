# -*- coding: utf-8 -*-
###
# (C) Copyright (2016) Hewlett Packard Enterprise Development LP
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

from hpOneView.oneview_client import OneViewClient
from hpOneView.common import make_migration_information
from hpOneView.common import print_entity
from hpOneView.exceptions import HPOneViewTaskError
from config_loader import try_load_from_file
from pprint import PrettyPrinter

import ssl
ssl.PROTOCOL_TLSv1_2=ssl.PROTOCOL_TLSv1

config = \
{
    "ip": "172.16.102.59",
    "credentials":
    {
        "userName": "Administrator",
        "password": ""
    },
    "enclosure_hostname": "172.178.209.32",
    "enclosure_username": "Administrator",
    "enclosure_password": "",
    "vcmUsername": "Administrator",
    "vcmPassword": "",
    "enclosure_group_uri": None
}

pp = PrettyPrinter()

#Try load config from a file (if there is a config file)
config = try_load_from_file(config)

#Obtain the master OneView client
oneview_client = OneViewClient(config)

#Create the dict that VC Migration Manager requires to start the process
migrationInformation = make_migration_information(config['enclosure_hostname'], config['enclosure_username'], config['enclosure_password'], config['vcmUsername'], config['vcmPassword'], enclosureGroupUri=config['enclosure_group_uri'])

#Start a migration by first creating a compatibility report
print("Create a compatibility report for enclosure '%s'." % migrationInformation['credentials']['oaIpAddress'])
compatibility_report = oneview_client.vc_migration_manager.test_compatibility(migrationInformation)
print("Complete.  Created a compatibility report for enclosure '%s'.\n  uri = '%s'" % (compatibility_report['credentials']['oaIpAddress'], compatibility_report['uri']))

#We got the compatibility report as part of the previous call, but one may need to get it later on
print("Get the '%s' compatibility report." % compatibility_report['credentials']['oaIpAddress'])
compatibility_report = oneview_client.vc_migration_manager.get_migration_report(compatibility_report['uri'])
print("Complete.  Obtained the compatibility report for '%s'.\n  Here is the compatibility report:" % compatibility_report['credentials']['oaIpAddress'])
pp.pprint(compatibility_report)

#One would now resolve all the critical issues and however many lesser severity issues found in the compatibility report before continuing
#Now is the time to initiate the migration
print("Attempting to migrate enclosure '%s'.  The migration state before is '%s'.  This could take a while." % (compatibility_report['credentials']['oaIpAddress'], compatibility_report['migrationState']))
try:
    compatibility_report = oneview_client.vc_migration_manager.migrate(compatibility_report['uri'])
    print("Complete.  Migration state afterward is '%s'." % compatibility_report['migrationState'])
except HPOneViewTaskError:
    print("Failure.  The enclosure failed to migrate.  Perhaps there was a critical issue that was unresolved before migrating?")

#One now may decide to delete the compatibility report if they so choose
print("Deleting the compatibility report for '%s'." % compatibility_report['credentials']['oaIpAddress'])
successful_deletion = oneview_client.vc_migration_manager.delete(compatibility_report['uri'])
print("Complete.  Deletion was successful for compatibility report '%s'?  %s." % (compatibility_report['credentials']['oaIpAddress'], successful_deletion))
