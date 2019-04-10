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
from hpOneView.resources.servers.server_profiles import ServerProfiles
from hpOneView.resources.resource import (Resource, ResourceHelper,
                                          ResourcePatchMixin, ResourceSchemaMixin)

TIMEOUT = -1


class ServerProfilesTest(TestCase):
    def setUp(self):
        host = '127.0.0.1'
        http_connection = connection(host)
        self._resource = ServerProfiles(http_connection)
        self.uri = "/rest/server-profiles/4ff2327f-7638-4b66-ad9d-283d4940a4ae"
        self._resource.data = {"uri": self.uri}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all(self, mock_get_all):
        query_filter = 'name=TestName'
        sort = 'name:ascending'

        self._resource.get_all(start=2, count=500, filter=query_filter, sort=sort)
        mock_get_all.assert_called_once_with(start=2, count=500, filter=query_filter, sort=sort)

    @mock.patch.object(ResourceHelper, 'create')
    def test_create(self, mock_create):
        template = dict(name="Server Profile Test")

        expected_template = template.copy()
        default_values = self._resource._get_default_values()
        expected_template.update(default_values)

        self._resource.create(template, timeout=TIMEOUT)
        mock_create.assert_called_once_with(expected_template, force='', timeout=TIMEOUT)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'update')
    def test_update(self, mock_update, mock_ensure_client):
        template = dict(name="Server Profile Test", macType="Virtual",
                        enclosureUri='/rest/fake', enclosureBay=3)

        expected_template = dict(name="Server Profile Test", macType="Virtual")
        expected_template["uri"] = self.uri

        self._resource.update(template)
        mock_update.assert_called_once_with(expected_template, self.uri, '', -1)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_delete(self, mock_delete):
        self._resource.delete(timeout=TIMEOUT)
        mock_delete.assert_called_once_with(self.uri, custom_headers=None,
                                            timeout=TIMEOUT, force=False)

    @mock.patch.object(ResourcePatchMixin, 'patch_request')
    def test_patch(self, mock_pacth):
        self._resource.patch("replace", "/templateCompliance", "Compliant")
        mock_pacth.assert_called_once_with(self.uri, body=[{'path': '/templateCompliance',
                                                            'op': 'replace',
                                                            'value': 'Compliant'}],
                                           custom_headers=None, timeout=-1)

    @mock.patch.object(ResourceHelper, 'delete_all')
    def test_delete_all(self, delete_all):
        query_filter = 'name=TestName'

        self._resource.delete_all(filter=query_filter, force=True, timeout=60)
        delete_all.assert_called_once_with(filter=query_filter, force=True, timeout=60)

    @mock.patch.object(ResourceSchemaMixin, 'get_schema')
    def test_get_schema(self, get_schema):
        self._resource.get_schema()
        get_schema.assert_called_once()

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_compliance_preview(self, mock_get):
        uri = "{}/compliance-preview".format(self.uri)

        self._resource.get_compliance_preview()
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_profile_ports(self, mock_get):
        uri = "/rest/server-profiles/profile-ports" \
              "?enclosureGroupUri=/rest/enclosure-groups/a0f1c07b-f811-4c85-8e38-ac5ec34ea2f4" \
              "&serverHardwareTypeUri=/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226"

        server_hardware_type_uri = "/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226"
        enclosure_group_uri = "/rest/enclosure-groups/a0f1c07b-f811-4c85-8e38-ac5ec34ea2f4"

        self._resource.get_profile_ports(enclosureGroupUri=enclosure_group_uri,
                                         serverHardwareTypeUri=server_hardware_type_uri)
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_messages(self, mock_get):
        uri = "{}/messages".format(self.uri)

        self._resource.get_messages()
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_transformation(self, mock_get):
        uri = "{}/transformation" \
              "?enclosureGroupUri=/rest/enclosure-groups/a0f1c07b-f811-4c85-8e38-ac5ec34ea2f4" \
              "&serverHardwareTypeUri=/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226".format(self.uri)

        server_hardware_type_uri = "/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226"
        enclosure_group_uri = "/rest/enclosure-groups/a0f1c07b-f811-4c85-8e38-ac5ec34ea2f4"

        self._resource.get_transformation(enclosureGroupUri=enclosure_group_uri,
                                          serverHardwareTypeUri=server_hardware_type_uri)
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_available_networks(self, mock_get):
        uri = "/rest/server-profiles/available-networks" \
              "?enclosureGroupUri=/rest/enclosure-groups/a0f1c07b-f811-4c85-8e38-ac5ec34ea2f4" \
              "&serverHardwareTypeUri=/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226"

        server_hardware_type_uri = "/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226"
        enclosure_group_uri = "/rest/enclosure-groups/a0f1c07b-f811-4c85-8e38-ac5ec34ea2f4"

        self._resource.get_available_networks(enclosureGroupUri=enclosure_group_uri,
                                              serverHardwareTypeUri=server_hardware_type_uri)
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_available_servers(self, mock_get):
        uri = "/rest/server-profiles/available-servers" \
              "?enclosureGroupUri=/rest/enclosure-groups/a0f1c07b-f811-4c85-8e38-ac5ec34ea2f4" \
              "&serverHardwareTypeUri=/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226"

        server_hardware_type_uri = "/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226"
        enclosure_group_uri = "/rest/enclosure-groups/a0f1c07b-f811-4c85-8e38-ac5ec34ea2f4"

        self._resource.get_available_servers(enclosureGroupUri=enclosure_group_uri,
                                             serverHardwareTypeUri=server_hardware_type_uri)
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_available_storage_system(self, mock_get):
        uri = "/rest/server-profiles/available-storage-system" \
              "?enclosureGroupUri=/rest/enclosure-groups/a0f1c07b-f811-4c85-8e38-ac5ec34ea2f4" \
              "&serverHardwareTypeUri=/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226"

        server_hardware_type_uri = "/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226"
        enclosure_group_uri = "/rest/enclosure-groups/a0f1c07b-f811-4c85-8e38-ac5ec34ea2f4"

        self._resource.get_available_storage_system(enclosureGroupUri=enclosure_group_uri,
                                                    serverHardwareTypeUri=server_hardware_type_uri)
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_available_storage_systems(self, mock_get):
        uri = "/rest/server-profiles/available-storage-systems" \
              "?enclosureGroupUri=/rest/enclosure-groups/a0f1c07b-f811-4c85-8e38-ac5ec34ea2f4" \
              "&serverHardwareTypeUri=/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226"

        server_hardware_type_uri = "/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226"
        enclosure_group_uri = "/rest/enclosure-groups/a0f1c07b-f811-4c85-8e38-ac5ec34ea2f4"

        self._resource.get_available_storage_systems(enclosureGroupUri=enclosure_group_uri,
                                                     serverHardwareTypeUri=server_hardware_type_uri)
        mock_get.assert_called_once_with(start=0, count=-1, filter='', sort='', uri=uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_available_targets(self, mock_get):
        uri = "/rest/server-profiles/available-targets" \
              "?enclosureGroupUri=/rest/enclosure-groups/a0f1c07b-f811-4c85-8e38-ac5ec34ea2f4" \
              "&serverHardwareTypeUri=/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226"

        server_hardware_type_uri = "/rest/server-hardware-types/C8DEF9A6-9586-465E-A951-3070988BC226"
        enclosure_group_uri = "/rest/enclosure-groups/a0f1c07b-f811-4c85-8e38-ac5ec34ea2f4"

        self._resource.get_available_targets(enclosureGroupUri=enclosure_group_uri,
                                             serverHardwareTypeUri=server_hardware_type_uri)
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_new_profile_template(self, mock_get):
        uri = "{}/new-profile-template".format(self.uri)

        self._resource.get_new_profile_template()
        mock_get.assert_called_once_with(uri)
