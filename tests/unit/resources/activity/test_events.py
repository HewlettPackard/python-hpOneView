# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2017) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

from unittest import TestCase

import mock

from hpOneView.connection import connection
from hpOneView.resources.activity.events import Events
from hpOneView.resources.resource import ResourceClient


class EventsTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._client = Events(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all(self, mock_get):
        self._client.get_all(filter="name='name'",
                             sort='name:ascending',
                             view='day')
        mock_get.assert_called_once_with(count=-1,
                                         filter="name='name'",
                                         query='', sort='name:ascending', start=0, view='day')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_specific(self, mock_get):
        self._client.get('/rest/events/fake_uri')
        mock_get.assert_called_once_with('/rest/events/fake_uri')

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._client.get_by('eventTypeID', 'hp.justATest')
        mock_get_by.assert_called_once_with('eventTypeID', 'hp.justATest')

    @mock.patch.object(ResourceClient, 'create')
    def test_create_should_use_given_values(self, mock_create):
        resource = {
            "description": "This is a very simple test event",
            "serviceEventSource": True,
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
                "isThisVarbindData": False,
                "varBindOrderIndex": -1}]
        }
        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self._client.create(resource, 30)
        mock_create.assert_called_once_with(resource_rest_call, timeout=30,
                                            default_values=self._client.DEFAULT_VALUES)
