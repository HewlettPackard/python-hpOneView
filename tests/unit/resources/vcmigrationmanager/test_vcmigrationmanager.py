# -*- coding: utf-8 -*-
###
# (C) Copyright (2016) Hewlett Packard Enterprise Development LP
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
from hpOneView.resources.vcmigrationmanager.vcmigrationmanager import VcMigrationManager
from hpOneView.resources.resource import ResourceClient
from hpOneView.common import make_migration_information


class VcMigrationManagerTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self.vcmigrationmanager = VcMigrationManager(self.connection)

    @mock.patch.object(ResourceClient, 'create')
    def test_test_compatibility(self, mock_create):
        timeoutValue = 26
        
        migrationInformation = make_migration_information('192.168.9.32', 'Administrator', 'password', 'Administrator', 'password', enclosureGroupUri='/rest/enclosure-groups/uri')

        self.vcmigrationmanager.test_compatibility(migrationInformation, timeout=timeoutValue)

        mock_create.assert_called_once_with(migrationInformation, timeout=timeoutValue)
    
    @mock.patch.object(ResourceClient, 'create')
    def test_test_compatibility_default(self, mock_create):
        timeoutValue = 26
        
        migrationInformation = make_migration_information('192.168.9.32', 'Administrator', 'password', 'Administrator', 'password', enclosureGroupUri='/rest/enclosure-groups/uri')

        self.vcmigrationmanager.test_compatibility(migrationInformation)

        mock_create.assert_called_once_with(migrationInformation, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_migration_report(self, mock_get):
        uri = '/rest/migratable-vc-domains/uri'
    
        self.vcmigrationmanager.get_migration_report(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'update')
    def test_migrate_with_full_uri(self, mock_update):
        migrationInformation = \
        {
            'migrationState': 'Migrated',
            'type': 'migratable-vc-domains',
            'category': 'migratable-vc-domains'
        }
        uriValue = '/rest/migratable-vc-domains/uri'
        timeoutValue = 26
    
        self.vcmigrationmanager.migrate(uriValue, timeout=26)

        mock_update.assert_called_once_with(migrationInformation, uri=uriValue, timeout=26)
    
    @mock.patch.object(ResourceClient, 'update')
    def test_migrate_with_id(self, mock_update):
        migrationInformation = \
        {
            'migrationState': 'Migrated',
            'type': 'migratable-vc-domains',
            'category': 'migratable-vc-domains'
        }
        id = 'uri'
        uriValue = '/rest/migratable-vc-domains/' + id
        timeoutValue = 26
    
        self.vcmigrationmanager.migrate(id, timeout=26)

        mock_update.assert_called_once_with(migrationInformation, uri=uriValue, timeout=26)
    
    @mock.patch.object(ResourceClient, 'update')
    def test_migrate_default(self, mock_update):
        migrationInformation = \
        {
            'migrationState': 'Migrated',
            'type': 'migratable-vc-domains',
            'category': 'migratable-vc-domains'
        }
        uriValue = '/rest/migratable-vc-domains/uri'
    
        self.vcmigrationmanager.migrate(uriValue)

        mock_update.assert_called_once_with(migrationInformation, uri=uriValue, timeout=-1)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete(self, mock_delete):
        timeoutValue = 26
        uriValue = '/rest/migratable-vc-domains/uri'
        
        self.vcmigrationmanager.delete(uriValue, timeout=timeoutValue)
        
        mock_delete.assert_called_once_with(uriValue, timeout=timeoutValue)
    
    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_default(self, mock_delete):
        timeoutValue = 26
        uriValue = '/rest/migratable-vc-domains/uri'
        
        self.vcmigrationmanager.delete(uriValue)
        
        mock_delete.assert_called_once_with(uriValue, timeout=-1)
