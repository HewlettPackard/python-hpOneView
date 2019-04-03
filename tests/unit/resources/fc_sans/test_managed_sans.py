# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2019) Hewlett Packard Enterprise Development LP
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
from hpOneView.resources.resource import Resource, ResourceHelper
from hpOneView.resources.fc_sans.managed_sans import ManagedSANs

TIMEOUT = -1


class ManagedSANsTest(TestCase):
    def setUp(self):
        host = '127.0.0.1'
        http_connection = connection(host)
        self._resource = ManagedSANs(http_connection)
        self.uri = "/rest/fc-sans/managed-sans/280FF951-F007-478F-AC29-E4655FC76DDC"
        self._resource.data = {"uri": self.uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all(self, mock_get_all):
        query_filter = "name EQ 'TestName'"
        sort = 'name:ascending'

        self._resource.get_all(start=2, count=500, query=query_filter, sort=sort)
        mock_get_all.assert_called_once_with(start=2, count=500, query=query_filter, sort=sort)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_name_should_return_san_manager_when_found(self, mock_get_all):
        mock_get_all.return_value = [
            {"name": "SAN1_0", "uri": "/rest/fc-sans/managed-sans/280FF951-F007-478F-AC29-E4655FC76DDC"},
            {"name": "SAN1_1", "uri": "/rest/fc-sans/managed-sans/6fee02f3-b7c7-42bd-a528-04341e16bad6"}
        ]
        managed_san = self._resource.get_by_name("SAN1_1")

        expected_result = {"name": "SAN1_1", "uri": "/rest/fc-sans/managed-sans/6fee02f3-b7c7-42bd-a528-04341e16bad6"}
        self.assertEqual(managed_san.data, expected_result)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_name_should_return_null_when_not_found(self, mock_get_all):
        mock_get_all.return_value = [
            {"name": "SAN1_0", "uri": "/rest/fc-sans/managed-sans/280FF951-F007-478F-AC29-E4655FC76DDC"},
            {"name": "SAN1_1", "uri": "/rest/fc-sans/managed-sans/6fee02f3-b7c7-42bd-a528-04341e16bad6"}
        ]
        managed_san = self._resource.get_by_name("SAN1_3")

        self.assertIsNone(managed_san)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update(self, mock_update, mock_ensure_client_data):
        uri = self._resource.data["uri"]
        data = {"attributes": "values"}

        self._resource.update(data)
        data["uri"] = uri
        mock_update.assert_called_once_with(data, uri, False, -1, None)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_endpoints_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        uri = '{}/endpoints/'.format(self._resource.data["uri"])

        self._resource.get_endpoints(2, 500, filter, sort)
        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort, uri=uri)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_endpoints_called_once_with_default(self, mock_get_all):
        uri = '{}/endpoints/'.format(self._resource.data["uri"])
        self._resource.get_endpoints()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='', uri=uri)

    @mock.patch.object(ResourceHelper, 'do_post')
    def test_create_endpoints_csv_file_called_once_when_id_provided(self, mock_do_post):
        self._resource.create_endpoints_csv_file()

        expected_uri = '{}/endpoints/'.format(self._resource.data["uri"])
        mock_do_post.assert_called_once_with(expected_uri, {}, -1, None)

    @mock.patch.object(ResourceHelper, 'do_post')
    def test_create_endpoints_csv_file_called_once_when_uri_provided(self, mock_do_post):
        self._resource.create_endpoints_csv_file()

        expected_uri = '{}/endpoints/'.format(self._resource.data["uri"])
        mock_do_post.assert_called_once_with(expected_uri, {}, -1, None)

    @mock.patch.object(ResourceHelper, 'create_report')
    def test_create_issues_report_called_once(self, mock_create_report):
        self._resource.create_issues_report()

        expected_uri = '{}/issues/'.format(self._resource.data["uri"])
        mock_create_report.assert_called_once_with(expected_uri, -1)

    @mock.patch.object(ResourceHelper, 'create_report')
    def test_create_issues_report_called_once_when_uri_provided(self, mock_create_report):
        self._resource.create_issues_report()

        expected_uri = '{}/issues/'.format(self._resource.data["uri"])
        mock_create_report.assert_called_once_with(expected_uri, -1)
