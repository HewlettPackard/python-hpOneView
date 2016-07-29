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
from hpOneView.resources.servers.server_profile_templates import ServerProfileTemplate
from hpOneView.resources.resource import ResourceClient


class ServerProfileTemplateTest(TestCase):

    def setUp(self):
        host = '127.0.0.1'
        http_connection = connection(host)
        self._resource = ServerProfileTemplate(http_connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all(self, mock_get_all):
        query_filter = 'name=TestName'
        sort = 'name:ascending'

        self._resource.get_all(start=2, count=500, filter=query_filter, sort=sort)
        mock_get_all.assert_called_once_with(start=2, count=500, filter=query_filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id(self, mock_get):
        template_id = "6fee02f3-b7c7-42bd-a528-04341e16bad6"

        self._resource.get(template_id)
        mock_get.assert_called_once_with(id_or_uri=template_id)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_property(self, mock_get_by):
        template_property = "name"
        template_name = "BL460c Gen8 1"

        self._resource.get_by(template_property, template_name)
        mock_get_by.assert_called_once_with(template_property, template_name)

    @mock.patch.object(ResourceClient, 'get_by_name')
    def test_get_by_name(self, mock_get_by_name):
        template_name = "BL460c Gen8 1"

        self._resource.get_by_name(template_name)
        mock_get_by_name.assert_called_once_with(template_name)
