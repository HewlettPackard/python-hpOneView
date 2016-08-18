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
from hpOneView.resources.resource import ResourceClient
from hpOneView.resources.fc_sans.managed_sans import ManagedSANs

TIMEOUT = -1


class ManagedSANsTest(TestCase):
    def setUp(self):
        host = '127.0.0.1'
        http_connection = connection(host)
        self._resource = ManagedSANs(http_connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all(self, mock_get_all):
        query_filter = "name EQ 'TestName'"
        sort = 'name:ascending'

        self._resource.get_all(start=2, count=500, query=query_filter, sort=sort)
        mock_get_all.assert_called_once_with(start=2, count=500, query=query_filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_by_name_should_return_san_manager_when_found(self, mock_get_all):
        mock_get_all.return_value = [
            {"name": "SAN1_0", "uri": "/rest/fc-sans/managed-sans/280FF951-F007-478F-AC29-E4655FC76DDC"},
            {"name": "SAN1_1", "uri": "/rest/fc-sans/managed-sans/6fee02f3-b7c7-42bd-a528-04341e16bad6"}
        ]
        managed_san = self._resource.get_by_name("SAN1_1")

        expected_result = {"name": "SAN1_1", "uri": "/rest/fc-sans/managed-sans/6fee02f3-b7c7-42bd-a528-04341e16bad6"}
        self.assertEqual(managed_san, expected_result)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_by_name_should_return_null_when_not_found(self, mock_get_all):
        mock_get_all.return_value = [
            {"name": "SAN1_0", "uri": "/rest/fc-sans/managed-sans/280FF951-F007-478F-AC29-E4655FC76DDC"},
            {"name": "SAN1_1", "uri": "/rest/fc-sans/managed-sans/6fee02f3-b7c7-42bd-a528-04341e16bad6"}
        ]
        managed_san = self._resource.get_by_name("SAN1_3")

        self.assertIsNone(managed_san)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id(self, mock_get):
        id = "280FF951-F007-478F-AC29-E4655FC76DDC"

        self._resource.get(id)
        mock_get.assert_called_once_with(id_or_uri=id)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_with_uri(self, mock_update):
        uri = "/rest/fc-sans/managed-sans/280FF951-F007-478F-AC29-E4655FC76DDC"
        data = {"attributes": "values"}

        self._resource.update(uri, data)

        mock_update.assert_called_once_with(data, timeout=-1, uri=uri)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_with_id(self, mock_update):
        uri = "/rest/fc-sans/managed-sans/280FF951-F007-478F-AC29-E4655FC76DDC"
        data = {"attributes": "values"}

        self._resource.update("280FF951-F007-478F-AC29-E4655FC76DDC", data)

        mock_update.assert_called_once_with(data, timeout=-1, uri=uri)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_endpoints_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        managed_san_id = '280FF951-F007-478F-AC29-E4655FC76DDC'
        uri = '/rest/fc-sans/managed-sans/280FF951-F007-478F-AC29-E4655FC76DDC/endpoints/'

        self._resource.get_endpoints(managed_san_id, 2, 500, filter, sort)
        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort, uri=uri)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_endpoints_called_once_with_default(self, mock_get_all):
        managed_san_id = '280FF951-F007-478F-AC29-E4655FC76DDC'
        uri = '/rest/fc-sans/managed-sans/280FF951-F007-478F-AC29-E4655FC76DDC/endpoints/'
        self._resource.get_endpoints(managed_san_id)
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='', uri=uri)

    @mock.patch.object(ResourceClient, 'create_with_zero_body')
    def test_create_endpoints_csv_file_called_once_when_id_provided(self, mock_create_with_zero_body):
        id = '280FF951-F007-478F-AC29-E4655FC76DDC'

        self._resource.create_endpoints_csv_file(id)

        expected_uri = '/rest/fc-sans/managed-sans/280FF951-F007-478F-AC29-E4655FC76DDC/endpoints/'
        mock_create_with_zero_body.assert_called_once_with(uri=expected_uri, timeout=-1)

    @mock.patch.object(ResourceClient, 'create_with_zero_body')
    def test_create_endpoints_csv_file_called_once_when_uri_provided(self, mock_create_with_zero_body):
        uri = "/rest/fc-sans/managed-sans/280FF951-F007-478F-AC29-E4655FC76DDC"

        self._resource.create_endpoints_csv_file(uri)

        expected_uri = '/rest/fc-sans/managed-sans/280FF951-F007-478F-AC29-E4655FC76DDC/endpoints/'
        mock_create_with_zero_body.assert_called_once_with(uri=expected_uri, timeout=-1)

    @mock.patch.object(ResourceClient, 'create_report')
    def test_create_issues_report_called_once_when_id_provided(self, mock_create_report):
        id = '280FF951-F007-478F-AC29-E4655FC76DDC'

        self._resource.create_issues_report(id)

        expected_uri = '/rest/fc-sans/managed-sans/280FF951-F007-478F-AC29-E4655FC76DDC/issues/'
        mock_create_report.assert_called_once_with(uri=expected_uri, timeout=-1)

    @mock.patch.object(ResourceClient, 'create_report')
    def test_create_issues_report_called_once_when_uri_provided(self, mock_create_report):
        uri = "/rest/fc-sans/managed-sans/280FF951-F007-478F-AC29-E4655FC76DDC"

        self._resource.create_issues_report(uri)

        expected_uri = '/rest/fc-sans/managed-sans/280FF951-F007-478F-AC29-E4655FC76DDC/issues/'
        mock_create_report.assert_called_once_with(uri=expected_uri, timeout=-1)
