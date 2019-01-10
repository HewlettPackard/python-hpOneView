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
from hpOneView.resources.settings.appliance_device_snmp_v3_users import ApplianceDeviceSNMPv3Users
from hpOneView.resources.resource import ResourceClient


class ApplianceDeviceSNMPv3UsersTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._snmp_v3_users = ApplianceDeviceSNMPv3Users(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get):
        self._snmp_v3_users.get_all()
        mock_get.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        resource = {
            'type': 'Users',
            'userName': 'testUser1',
            'securityLevel': 'Authentication and privacy',
            'authenticationProtocol': 'SHA512',
            'authenticationPassphrase': 'authPass',
            'privacyProtocol': 'AES-256',
            'privacyPassphrase': '1234567812345678'
        }
        self._snmp_v3_users.create(resource)
        mock_create.assert_called_once_with(resource, timeout=-1, uri=None)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._snmp_v3_users.get('0ca1b9e9-3c30-405f-b450-abd36730aa38')

        mock_get.assert_called_once_with('0ca1b9e9-3c30-405f-b450-abd36730aa38')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/appliance/snmpv3-trap-forwarding/users/0ca1b9e9-3c30-405f-b450-abd36730aa38'
        self._snmp_v3_users.get(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_uri_called_once(self, mock_create):
        uri = '/rest/appliance/snmpv3-trap-forwarding/users/0ca1b9e9-3c30-405f-b450-abd36730aa38'
        self._snmp_v3_users.get_by('uri', uri)
        mock_create.assert_called_once_with('uri', uri)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_create):
        resource = {
            'authenticationPassphrase': 'newAuthPass',
            'privacyPassphrase': 8765432187654321,
            'uri': '/rest/appliance/snmpv3-trap-forwarding/users/0ca1b9e9-3c30-405f-b450-abd36730aa38'
        }
        self._snmp_v3_users.update(resource)
        mock_create.assert_called_once_with(resource, timeout=-1)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_create):
        id_or_uri = '/rest/appliance/snmpv3-trap-forwarding/users/0ca1b9e9-3c30-405f-b450-abd36730aa38'
        self._snmp_v3_users.delete(id_or_uri)
        mock_create.assert_called_once_with(id_or_uri, timeout=-1)
