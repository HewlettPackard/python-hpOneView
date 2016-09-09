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
from hpOneView.resources.facilities.datacenters import Datacenters
from hpOneView.resources.resource import ResourceClient


class DatacenterTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._datacenters = Datacenters(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._datacenters.get_all(2, 500, filter=filter, sort=sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort, query='')

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._datacenters.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='', query='')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        datacenter_id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._datacenters.get(datacenter_id)
        mock_get.assert_called_once_with(datacenter_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        datacenter_uri = "/rest/datacenters/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._datacenters.get(datacenter_uri)
        mock_get.assert_called_once_with(datacenter_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_visual_content_called_once_when_datacenter_uri_provided(self, mock_get):
        datacenter_uri = "/rest/datacenters/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        uri = "/rest/datacenters/f0a0a113-ec97-41b4-83ce-d7c92b900e7c/visualContent"
        self._datacenters.get_visual_content(datacenter_uri)
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_visual_content_called_once_when_datacenter_id_provided(self, mock_get):
        datacenter_id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        uri = "/rest/datacenters/f0a0a113-ec97-41b4-83ce-d7c92b900e7c/visualContent"
        self._datacenters.get_visual_content(datacenter_id)
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._datacenters.get_by("name", "test name")

        mock_get_by.assert_called_once_with("name", "test name")

    @mock.patch.object(ResourceClient, 'create')
    def test_add_called_once_with_defaults(self, mock_create):
        datacenter = {
            "name": "MyDatacenter"
        }
        self._datacenters.add(datacenter)
        mock_create.assert_called_once_with(datacenter, timeout=-1)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        datacenter = {
            "name": "MyDatacenter"
        }
        self._datacenters.add(datacenter, 70)
        mock_create.assert_called_once_with(datacenter, timeout=70)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once_with_defaults(self, update):
        datacenter = {
            "id": "4b4b87e2-eea8-4c90-8eca-b92eaaeecfff",
            "name": "MyDatacenter"

        }
        self._datacenters.update(datacenter)
        update.assert_called_once_with(datacenter, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_update):
        datacenter = {
            "id": "4b4b87e2-eea8-4c90-8eca-b92eaaeecfff",
            "name": "MyDatacenter"
        }
        self._datacenters.update(datacenter, 70)
        mock_update.assert_called_once_with(datacenter, timeout=70)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._datacenters.remove(id, force=True, timeout=50)

        mock_delete.assert_called_once_with(id, force=True, timeout=50)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove_called_once_with_defaults(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._datacenters.remove(id)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'delete_all')
    def test_remove_all_called_once(self, mock_delete):
        self._datacenters.remove_all(filter="name matches '%1'", force=True, timeout=50)

        mock_delete.assert_called_once_with(filter="name matches '%1'", force=True, timeout=50)

    @mock.patch.object(ResourceClient, 'delete_all')
    def test_remove_all_called_once_with_defaults(self, mock_delete):
        self._datacenters.remove_all(filter="name matches '%'")

        mock_delete.assert_called_once_with(filter="name matches '%'", force=False, timeout=-1)
