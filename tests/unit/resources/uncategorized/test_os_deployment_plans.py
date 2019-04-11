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
from hpOneView.resources.resource import ResourceHelper
from hpOneView.resources.uncategorized.os_deployment_plans import OsDeploymentPlans


class OsDeploymentPlansTest(TestCase):
    RESOURCE_ID = "81decf85-0dff-4a5e-8a95-52994eeb6493"
    RESOURCE_URI = "/rest/os-deployment-plans/" + RESOURCE_ID

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._os_deployment_plans = OsDeploymentPlans(self.connection)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._os_deployment_plans.get_all(2, 500, filter=filter, sort=sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort, query='')

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._os_deployment_plans.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='', query='')

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_called_once(self, mock_get_by):
        self._os_deployment_plans.get_by("name", "test name")
        mock_get_by.assert_called_once_with(0, -1, filter='"name=\'test name\'"',
                                            query='', sort='')

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_name_sould_return_none_when_resource_is_not_found(self, mock_get_by):
        mock_get_by.return_value = []
        response = self._os_deployment_plans.get_by_name("test name")
        self.assertEqual(response, None)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_by_name_called_once(self, mock_get_by):
        self._os_deployment_plans.get_by_name("test name")
        mock_get_by.assert_called_once_with(0, -1, filter='"name=\'test name\'"', query='', sort='')
