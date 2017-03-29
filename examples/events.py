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

from hpOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file
# from hpOneView import extract_id_from_uri
# from pprint import pprint

config = {
    "ip": "172.16.101.230",
    "credentials": {
        "userName": "administrator",
        "password": "rainforest"
    }
}

options = {
    "type": "EventResourceV3",
    "description": "This is a very simple test event",
    "serviceEventSource": "true",
    "serviceEventDetails": {
        "caseId": "1234",
        "primaryContact": "contactDetails",
        "remoteSupportState": "Submitted"
    },
    "severity": "OK",
    "healthCategory": "PROCESSOR",
    "eventTypeID": "hp.justATest",
    "rxTime": "2012-05-14T20:23:56.688Z",
    "urgency": "None",
    "eventDetails":
    [{"eventItemName": "ipv4Address",
        "eventItemValue": "198.51.100.5",
        "isThisVarbindData": "false",
        "varBindOrderIndex": -1}]
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

_client = OneViewClient(config)

# Getting the first 5 events
print("\nGetting the first 5 events:")
events = _client.events.get_all(0, 5)
for event in events:
    print("eventTypeID: '%s' | description: %s " % (event['description'], event['eventTypeID']))

# Create an Event
event = _client.events.create(options)
print("\nCreated event successfully.\n  uri = '%s'" % (event['uri']))

# # Get by Uri
print("\nFind uri == %s" % ('/rest/events/24'))
event_by_uri = _client.events.get('/rest/events/24')
print("uri: '%s' | eventTypeID: '%s' \n" % (event_by_uri['uri'], event_by_uri['eventTypeID']))

# # Filter by state
print("\nGet all events filtering by eventTypeID")
events = _client.events.get_all(filter="\"eventTypeID='StatusPoll.EnclosureStatus'\"", count=10)
for event in events:
    print("uri: '%s' | eventTypeID: '%s'" % (event['uri'], event['eventTypeID']))
