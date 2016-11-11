# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
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
from hpOneView.resources.activity.alerts import Alerts
from hpOneView.resources.resource import ResourceClient


class AlertsTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._client = Alerts(self.connection)

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
        self._client.get('35323930-4936-4450-5531-303153474820')
        mock_get.assert_called_once_with('35323930-4936-4450-5531-303153474820')

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._client.get_by('alertState', 'Active')
        mock_get_by.assert_called_once_with('alertState', 'Active')

    @mock.patch.object(ResourceClient, 'update')
    def test_update_should_fail_when_no_uri_is_provided(self, mock_update):
        resource = {
            'alertState': 'Cleared',
            'assignedToUser': 'Paul',
            'alertUrgency': 'None',
            'notes': 'Problem fixed',
            'eTag': '2014-03-28T04:40:06.831Z'
        }
        self.assertRaises(ValueError, self._client.update, resource)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_should_use_given_values_by_resource_uri(self, mock_update):
        resource = {
            'uri': '/rest/alerts/26',
            'alertState': 'Cleared',
            'assignedToUser': 'Paul',
            'alertUrgency': 'None',
            'notes': 'Problem fixed',
            'eTag': '2014-03-28T04:40:06.831Z'
        }
        self._client.update(resource.copy(), '/rest/alerts/26')
        resource_test = resource.copy()
        del resource_test["uri"]
        mock_update.assert_called_once_with(resource=resource_test, timeout=-1, uri='/rest/alerts/26')

    @mock.patch.object(ResourceClient, 'update')
    def test_update_should_use_given_values_by_uri_param(self, mock_update):
        resource = {
            'alertState': 'Cleared',
            'assignedToUser': 'Paul',
            'alertUrgency': 'None',
            'notes': 'Problem fixed',
            'eTag': '2014-03-28T04:40:06.831Z'
        }
        self._client.update(resource, '/rest/alerts/26')
        mock_update.assert_called_once_with(resource=resource.copy(), timeout=-1, uri='/rest/alerts/26')

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = '35323930-4936-4450-5531-303153474820'
        self._client.delete(id)
        mock_delete.assert_called_once_with(id)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_alert_change_log_called_once(self, mock_delete):
        id = '35323930-4936-4450-5531-303153474820'
        self._client.delete_alert_change_log(id)
        mock_delete.assert_called_once_with({'uri': '/rest/alerts/AlertChangeLog/35323930-4936-4450-5531-303153474820'})
