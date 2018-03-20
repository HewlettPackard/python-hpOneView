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
from hpOneView.image_streamer.resources.deployment_plans import DeploymentPlans
from hpOneView.resources.resource import ResourceClient


class DeploymentPlansTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._client = DeploymentPlans(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._client.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default_values(self, mock_get_all):
        self._client.get_all()

        mock_get_all.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._client.get_by('name', 'Deployment Plan Name')

        mock_get_by.assert_called_once_with('name', 'Deployment Plan Name')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._client.get('3518be0e-17c1-4189-8f81-83f3724f6155')

        mock_get.assert_called_once_with('3518be0e-17c1-4189-8f81-83f3724f6155')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/deployment-plans/3518be0e-17c1-4189-8f81-83f3724f6155'
        self._client.get(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once_with_default_type(self, mock_create):
        information = {
            "name": "Deployment Plan Name",
        }
        mock_create.return_value = {}

        self._client.create(information)

        expected_data = {
            "type": "OEDeploymentPlan",
            "name": "Deployment Plan Name",
        }
        mock_create.assert_called_once_with(expected_data, timeout=-1)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once_with_provided_type(self, mock_create):
        information = {
            "type": "OEDeploymentPlan",
            "name": "Deployment Plan Name",
        }
        expected_data = information.copy()
        mock_create.return_value = {}

        self._client.create(information)
        mock_create.assert_called_once_with(expected_data, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_update):
        information = {
            "type": "OEDeploymentPlan",
            "name": "Deployment Plan Name",
            "description": "Description of the deployment plan",
        }
        expected_data = information.copy()
        mock_update.return_value = {}

        self._client.update(information)
        mock_update.assert_called_once_with(expected_data, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_osdp_called_once(self, mock_get_osdp):
        self._client.get_osdp('3518be0e-17c1-4189-8f81-83f3724f6155')

        expected_uri = '/rest/deployment-plans/3518be0e-17c1-4189-8f81-83f3724f6155/osdp'
        mock_get_osdp.assert_called_once_with(expected_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_usedby_called_once(self, mock_get_usedby):
        self._client.get_usedby('3518be0e-17c1-4189-8f81-83f3724f6155')

        expected_uri = '/rest/deployment-plans/3518be0e-17c1-4189-8f81-83f3724f6155/usedby'
        mock_get_usedby.assert_called_once_with(expected_uri)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._client.delete(id, force=False)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once_with_force(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._client.delete(id, force=True)

        mock_delete.assert_called_once_with(id, force=True, timeout=-1)
