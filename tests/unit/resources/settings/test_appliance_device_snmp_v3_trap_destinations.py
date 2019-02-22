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
from hpOneView.resources.settings.appliance_device_snmp_v3_trap_destinations import ApplianceDeviceSNMPv3TrapDestinations
from hpOneView.resources.resource import ResourceClient


class ApplianceDeviceSNMPv3TrapDestinationsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._snmp_v3_trap_dest = ApplianceDeviceSNMPv3TrapDestinations(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get):
        self._snmp_v3_trap_dest.get_all()
        mock_get.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        resource = {
            'type': 'Destination',
            'destinationAddress': '1.1.1.1',
            'port': 162,
            'userId': '6b9c6f7b-7a24-4514-b9c9-0c31e086c170'
        }
        self._snmp_v3_trap_dest.create(resource)
        mock_create.assert_called_once_with(resource, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._snmp_v3_trap_dest.get('86731e55-6837-44cf-a5c5-f0392920da7e')

        mock_get.assert_called_once_with('86731e55-6837-44cf-a5c5-f0392920da7e')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/appliance/snmpv3-trap-forwarding/destinations/86731e55-6837-44cf-a5c5-f0392920da7e'
        self._snmp_v3_trap_dest.get(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_uri_called_once(self, mock_create):
        uri = '/rest/appliance/snmpv3-trap-forwarding/destinations/86731e55-6837-44cf-a5c5-f0392920da7e'
        self._snmp_v3_trap_dest.get_by('uri', uri)
        mock_create.assert_called_once_with('uri', uri)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_create):
        resource = {
            'destinationAddress': '1.1.9.9',
        }
        self._snmp_v3_trap_dest.update(resource)
        mock_create.assert_called_once_with(resource, timeout=-1)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_create):
        id_or_uri = '/rest/appliance/snmpv3-trap-forwarding/destinations/86731e55-6837-44cf-a5c5-f0392920da7e'
        self._snmp_v3_trap_dest.delete(id_or_uri)
        mock_create.assert_called_once_with(id_or_uri, timeout=-1)
