# -*- coding: utf-8 -*-
###
# (C) Copyright (2016-2017) Hewlett Packard Enterprise Development LP
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

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()

from hpOneView.resources.resource import ResourceClient


class MigratableVcDomains(object):
    """
    The migratable VC domains resource provides methods for migrating Virtual Connect (VC)
    enclosures into the appliance. The operations are testing compatibility of a VC
    managed enclosure, retrieving a compatibility report, deleting a
    compatibility report and migrating a VC managed enclosure into the appliance.

    """

    URI = '/rest/migratable-vc-domains'

    def __init__(self, connection):
        self._connection = connection
        self._client = ResourceClient(connection, self.URI)

    @staticmethod
    def make_migration_information(oaIpAddress, oaUsername, oaPassword, vcmUsername, vcmPassword,
                                   iloLicenseType='OneView', enclosureGroupUri=None):
        return {
            'credentials': {
                'oaIpAddress': oaIpAddress,
                'oaUsername': oaUsername,
                'oaPassword': oaPassword,
                'vcmUsername': vcmUsername,
                'vcmPassword': vcmPassword,
                'type': 'EnclosureCredentials'
            },
            'iloLicenseType': iloLicenseType,
            'enclosureGroupUri': enclosureGroupUri,
            'type': 'migratable-vc-domains',
            'category': 'migratable-vc-domains'
        }

    def test_compatibility(self, migrationInformation, timeout=-1):
        """
        Creates a migration report for an enclosure with a Virtual Connect domain.

        Args:
           migrationInformation: A dict specifying the enclosure, OA username, OA password, VCM username, and VCM
               password among other things.  Use make_migration_information to easily create this dict.
           timeout: Timeout in seconds.  Waits for task completion by default.  The timeout does not abort the task in
               OneView; just stops waiting for its completion.

        Returns: dict: a migration report.
        """

        return self._client.create(migrationInformation, timeout=timeout)

    def get_migration_report(self, id_or_uri):
        """
        Returns a migration report that has previously been generated.

        Args:
            id_or_uri: ID or URI of the migration report.

        Returns: dict: a migration report.
        """

        return self._client.get(id_or_uri)

    def migrate(self, id_or_uri, timeout=-1):
        """
        Initiates a migration of an enclosure specified by the ID or URI of a migration report.

        Args:
            id_or_uri: ID or URI of the migration report.
            timeout: Timeout in seconds.  Waits for task completion by default.  The timeout does not abort the task in
                OneView; just stops waiting for its completion.

        Returns: dict: a migration report.
        """

        # create the special payload to tell the VC Migration Manager to migrate the VC domain
        migrationInformation = {
            'migrationState': 'Migrated',
            'type': 'migratable-vc-domains',
            'category': 'migratable-vc-domains'
        }

        # call build_uri manually since .update(...) doesn't do it and the URI is not to be included in the body when
        # requesting a migration
        complete_uri = self._client.build_uri(id_or_uri)

        return self._client.update(migrationInformation, uri=complete_uri, timeout=timeout)

    def delete(self, id_or_uri, timeout=-1):
        """
        Deletes a migration report.

        Args:
            id_or_uri: ID or URI of the migration report.
            timeout: Timeout in seconds.  Waits for task completion by default.  The timeout does not abort the task in
                OneView; just stops waiting for its completion.

        Returns: bool: Indicates if the migration report was successfully deleted.
        """

        return self._client.delete(id_or_uri, timeout=timeout)
