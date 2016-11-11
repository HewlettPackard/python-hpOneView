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

from hpOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file
from hpOneView import extract_id_from_uri

config = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

_client = OneViewClient(config)

# Getting the first 5 alerts
print("\nGetting the first 5 alerts")
alerts = _client.alerts.get_all(0, 5)
for alert in alerts:
    print("uri: '%s' | type: '%s' | alertState: '%s'" % (alert['uri'], alert['type'], alert['alertState']))

# Get a specific alert (first of the list that was obtained in previous item)
print("\nGet a specific alert")
id_alert_by_id = extract_id_from_uri(alerts[0]['uri'])
print("Find id == %s" % id_alert_by_id)
alert_by_id = _client.alerts.get(id_alert_by_id)
print("uri: '%s' | alertState: '%s'" % (alert_by_id['uri'], alert_by_id['alertState']))

# Get by Uri
print("Find uri == %s" % (alert['uri']))
alert_by_uri = _client.alerts.get(alert['uri'])
print("uri: '%s' | alertState: '%s'" % (alert_by_uri['uri'], alert_by_uri['alertState']))

# Find first alert by state
print("\nGet first alert by state: Active")
alert_by_state = _client.alerts.get_by('alertState', 'Active')[0]
print("Found alert by state: '%s' | uri: '%s'" % (alert_by_state["alertState"], alert_by_state["uri"]))

# Update state alert
print("\nUpdate state alert")
alert_to_update = {
    'uri': alert_by_state['uri'],
    'alertState': 'Cleared',
}
alert_updated = _client.alerts.update(alert_to_update)
print("Update alert successfully.\n uri = '%s' | alertState = '%s'" %
      (alert_updated['uri'], alert_updated['alertState']))

# Filter by state
print("\nGet all alerts filtering by alertState")
alerts = _client.alerts.get_all(filter="\"alertState='Locked'\"", view="day", count=10)
for alert in alerts:
    print("'%s' | type: '%s' | alertState: '%s'" % (alert['uri'], alert['type'], alert['alertState']))

# Delete the alert
print("\nDelete an alert")
_client.alerts.delete(alert_by_id)
print("Successfully deleted alert")

# # Deletes the AlertChangeLog item identified by ID
# print("Deletes alert change log")
# _client.alerts.delete_alert_change_log('8')
