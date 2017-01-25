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

import unittest

import mock

from hpOneView.connection import connection
from hpOneView.resources.storage.storage_systems import StorageSystems
from hpOneView.resources.resource import ResourceClient


class StorageSystemsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._storage_systems = StorageSystems(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._storage_systems.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._storage_systems.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        storage_systems_id = "TXQ1010306"
        self._storage_systems.get(storage_systems_id)
        mock_get.assert_called_once_with(storage_systems_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        storage_systems_uri = "/rest/storage-systems/TXQ1010306"
        self._storage_systems.get(storage_systems_uri)
        mock_get.assert_called_once_with(storage_systems_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_host_types_called_once(self, mock_get):
        storage_systems_host_types_uri = "/rest/storage-systems/host-types"
        self._storage_systems.get_host_types()
        mock_get.assert_called_once_with(storage_systems_host_types_uri)

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_managed_ports_called_once_with_uri(self, mock_get):
        storage_systems_uri = "/rest/storage-systems/TXQ1010306"
        storage_systems_managed_ports_uri = "/rest/storage-systems/TXQ1010306/managedPorts"
        self._storage_systems.get_managed_ports(storage_systems_uri)
        mock_get.assert_called_once_with(storage_systems_managed_ports_uri)

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_managed_ports_called_once_with_id(self, mock_get):
        storage_systems_id = "TXQ1010306"
        storage_systems_managed_ports_uri = "/rest/storage-systems/TXQ1010306/managedPorts"
        self._storage_systems.get_managed_ports(storage_systems_id)
        mock_get.assert_called_once_with(storage_systems_managed_ports_uri)

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_managed_ports_called_once_with_uri_and_port_id(self, mock_get):
        storage_systems_uri = "/rest/storage-systems/TXQ1010306"
        port_id = "C862833E-907C-4124-8841-BDC75444CF76"
        storage_systems_managed_ports_uri = \
            "/rest/storage-systems/TXQ1010306/managedPorts/C862833E-907C-4124-8841-BDC75444CF76"
        self._storage_systems.get_managed_ports(storage_systems_uri, port_id)
        mock_get.assert_called_once_with(storage_systems_managed_ports_uri)

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_managed_ports_called_once_with_id_and_port_id(self, mock_get):
        storage_systems_id = "TXQ1010306"
        port_id = "C862833E-907C-4124-8841-BDC75444CF76"
        storage_systems_managed_ports_uri = \
            "/rest/storage-systems/TXQ1010306/managedPorts/C862833E-907C-4124-8841-BDC75444CF76"
        self._storage_systems.get_managed_ports(storage_systems_id, port_id)
        mock_get.assert_called_once_with(storage_systems_managed_ports_uri)

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_managed_ports_called_once_with_uri_and_port_uri(self, mock_get):
        storage_systems_uri = "/rest/storage-systems/TXQ1010306"
        port_uri = \
            "/rest/storage-systems/TXQ1010306/managedPorts/C862833E-907C-4124-8841-BDC75444CF76"
        storage_systems_managed_ports_uri = \
            "/rest/storage-systems/TXQ1010306/managedPorts/C862833E-907C-4124-8841-BDC75444CF76"
        self._storage_systems.get_managed_ports(storage_systems_uri, port_uri)
        mock_get.assert_called_once_with(storage_systems_managed_ports_uri)

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_managed_ports_called_once_with_id_and_port_uri(self, mock_get):
        storage_systems_id = "TXQ1010306"
        port_uri = \
            "/rest/storage-systems/TXQ1010306/managedPorts/C862833E-907C-4124-8841-BDC75444CF76"
        storage_systems_managed_ports_uri = \
            "/rest/storage-systems/TXQ1010306/managedPorts/C862833E-907C-4124-8841-BDC75444CF76"
        self._storage_systems.get_managed_ports(storage_systems_id, port_uri)
        mock_get.assert_called_once_with(storage_systems_managed_ports_uri)

    @mock.patch.object(ResourceClient, 'create')
    def test_add_called_once_with_defaults(self, mock_create):
        storage_system = {
            "ip_hostname": "example.com",
            "username": "username",
            "password": "password"
        }
        self._storage_systems.add(storage_system)
        mock_create.assert_called_once_with(storage_system, timeout=-1)

    @mock.patch.object(ResourceClient, 'create')
    def test_add_called_once(self, mock_create):
        storage_system = {
            "ip_hostname": "example.com",
            "username": "username",
            "password": "password"
        }
        self._storage_systems.add(storage_system, 70)
        mock_create.assert_called_once_with(storage_system, timeout=70)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_storage_pools_called_once_with_uri(self, mock_get):
        storage_systems_uri = "/rest/storage-systems/TXQ1010306"
        storage_systems_managed_ports_uri = "/rest/storage-systems/TXQ1010306/storage-pools"
        self._storage_systems.get_storage_pools(storage_systems_uri)
        mock_get.assert_called_once_with(storage_systems_managed_ports_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_storage_pools_called_once_with_id(self, mock_get):
        storage_systems_id = "TXQ1010306"
        storage_systems_managed_ports_uri = "/rest/storage-systems/TXQ1010306/storage-pools"
        self._storage_systems.get_storage_pools(storage_systems_id)
        mock_get.assert_called_once_with(storage_systems_managed_ports_uri)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once_with_defaults(self, update):
        storage_system = {
            "type": "StorageSystemV3",
            "credentials": {
                "ip_hostname": "example.com",
                "username": "username"
            },
            "name": "StoreServ1",
        }
        self._storage_systems.update(storage_system)
        update.assert_called_once_with(storage_system, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_update):
        storage_system = {
            "type": "StorageSystemV3",
            "credentials": {
                "ip_hostname": "example.com",
                "username": "username"
            },
            "name": "StoreServ1",
        }
        self._storage_systems.update(storage_system, 70)
        mock_update.assert_called_once_with(storage_system, timeout=70)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._storage_systems.remove(id, force=True, timeout=50)

        mock_delete.assert_called_once_with(id, force=True, timeout=50)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove_called_once_with_defaults(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._storage_systems.remove(id)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._storage_systems.get_by("name", "test name")

        mock_get_by.assert_called_once_with("name", "test name")

    @mock.patch.object(ResourceClient, 'get_by_name')
    def test_get_by_name_called_once(self, mock_get_by):
        self._storage_systems.get_by_name("test name")

        mock_get_by.assert_called_once_with(name="test name")

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_by_ip_hostname_find_value(self, get_all):
        get_all.return_value = [
            {"credentials": {
                "ip_hostname": "10.0.0.0",
                "username": "username"}},
            {"credentials": {
                "ip_hostname": "20.0.0.0",
                "username": "username"}},
        ]

        result = self._storage_systems.get_by_ip_hostname("20.0.0.0")
        get_all.assert_called_once()
        self.assertEqual(
            {"credentials": {
                "ip_hostname": "20.0.0.0",
                "username": "username"}}, result)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_by_ip_hostname_value_not_found(self, get_all):
        get_all.return_value = [
            {"credentials": {
                "ip_hostname": "10.0.0.0",
                "username": "username"}},
            {"credentials": {
                "ip_hostname": "20.0.0.0",
                "username": "username"}},
        ]

        result = self._storage_systems.get_by_ip_hostname("30.0.0.0")
        get_all.assert_called_once()
        self.assertIsNone(result)
