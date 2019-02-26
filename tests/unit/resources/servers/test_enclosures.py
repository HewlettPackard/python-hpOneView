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
from hpOneView.resources.servers.enclosures import Enclosures
from hpOneView.resources.resource import (Resource, ResourceHelper, ResourcePatchMixin,
                                          ResourceZeroBodyMixin, ResourceUtilizationMixin)


class EnclosuresTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._enclosures = Enclosures(self.connection)
        self._enclosures.data = {'uri': '/rest/enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32'}

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'
        scope_uris = 'rest/scopes/cd237b60-09e2-45c4-829e-082e318a6d2a'

        self._enclosures.get_all(2, 500, filter, sort=sort, scope_uris=scope_uris)
        mock_get_all.assert_called_once_with(start=2, count=500, filter=filter, sort=sort, scope_uris=scope_uris)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default_values(self, mock_get_all):
        self._enclosures.get_all(0, -1)
        mock_get_all.assert_called_once_with(count=-1, start=0, filter='', sort='', scope_uris='')

    @mock.patch.object(Resource, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._enclosures.get_by('name', 'OneViewSDK-Test-Enclosure')
        mock_get_by.assert_called_once_with('name', 'OneViewSDK-Test-Enclosure')

    @mock.patch.object(Enclosures, 'get_by_hostname')
    def test_get_by_hostname_called_one(self, mock_get_by_hostname):
        self._enclosures.get_by_hostname('host_name')
        mock_get_by_hostname.assert_called_once_with('host_name')

    @mock.patch.object(Enclosures, 'get_all')
    def test_get_by_hostname_return_with_no_host(self, mock_get_all):
        mock_get_all.return_value = []
        actual_return = self._enclosures.get_by_hostname('host_name')
        expected_return = None
        self.assertEqual(actual_return, expected_return)

    @mock.patch.object(Enclosures, 'get_all')
    def test_get_by_hostname_return_with_primary_ip(self, mock_get_all):
        enclosure = {'activeOaPreferredIP': '1.1.1.1', "name": "En1"}
        mock_get_all.return_value = [enclosure]
        actual_return = self._enclosures.get_by_hostname('1.1.1.1')
        expected_return = enclosure
        self.assertEqual(actual_return.data, expected_return)

    @mock.patch.object(Enclosures, 'get_all')
    def test_get_by_hostname_return_with_standby_ip(self, mock_get_all):
        enclosure = {'standbyOaPreferredIP': '1.1.1.1', "name": "En1"}
        mock_get_all.return_value = [enclosure]
        actual_return = self._enclosures.get_by_hostname('1.1.1.1')
        expected_return = enclosure
        self.assertEqual(actual_return.data, expected_return)

    @mock.patch.object(Resource, 'create')
    def test_add_called_once(self, mock_create):
        information = {
            'enclosureGroupUri': '/rest/enclosure-groups/id-enclosure-group'
        }
        mock_create.return_value = {}

        self._enclosures.add(information)
        mock_create.assert_called_once_with(data=information.copy(), timeout=-1)

    @mock.patch.object(Resource, 'get_by_uri')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/enclosures/3518be0e-17c1-4189-8f81-83f3724f6155'

        self._enclosures.get_by_uri(uri)
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourcePatchMixin, 'patch_request')
    def test_patch_should_use_user_defined_values(self, mock_patch, ensure_resource_data):
        mock_patch.return_value = {}

        self._enclosures.patch('replace', '/name', 'new_name', timeout=1)
        print (self._enclosures.data)
        mock_patch.assert_called_once_with('/rest/enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32',
                                           body=[{u'path': '/name', u'value': 'new_name', u'op': 'replace'}],
                                           custom_headers=None, timeout=1)

    @mock.patch.object(Resource, 'delete')
    def test_remove_called_once(self, mock_delete):
        self._enclosures.remove(force=False)
        mock_delete.assert_called_once_with(force=False)

    @mock.patch.object(Resource, 'delete')
    def test_remove_called_once_with_force(self, mock_delete):
        self._enclosures.remove(force=True)
        mock_delete.assert_called_once_with(force=True)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceZeroBodyMixin, 'update_with_zero_body')
    def test_update_configuration_by_uri(self, mock_update_with_zero_body, ensure_resource_data):
        self._enclosures.update_configuration()
        uri = "{}/configuration".format(self._enclosures.data['uri'])
        mock_update_with_zero_body.assert_called_once_with(uri=uri, timeout=-1)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_environmental_configuration_by_uri(self, mock_get, ensure_resource_data):
        uri_rest_call = '/rest/enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32/environmentalConfiguration'

        self._enclosures.get_environmental_configuration()
        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_environmental_configuration_by_id(self, mock_get, ensure_resource_data):
        uri_rest_call = '/rest/enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32/environmentalConfiguration'

        self._enclosures.get_environmental_configuration()
        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'do_put')
    def test_update_environmental_configuration_by_uri(self, mock_put, ensure_resource_data):
        uri_rest_call = '/rest/enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32/environmentalConfiguration'
        configuration = {"calibratedMaxPower": 2500}
        configuration_rest_call = configuration.copy()

        self._enclosures.update_environmental_configuration(configuration, timeout=-1)
        mock_put.assert_called_once_with(uri_rest_call, configuration_rest_call, -1, None)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'do_put')
    def test_refresh_state_by_uri(self, mock_put, ensure_resource_data):
        uri_rest_call = '/rest/enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32/refreshState'
        configuration = {"refreshState": "RefreshPending"}
        configuration_rest_call = configuration.copy()

        self._enclosures.refresh_state(configuration)
        mock_put.assert_called_once_with(uri_rest_call, configuration_rest_call, -1, None)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_script_by_uri(self, mock_get, ensure_resource_data):
        uri_rest_call = '/rest/enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32/script'

        self._enclosures.get_script()
        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_sso_by_uri(self, mock_get, ensure_resource_data):
        uri_rest_call = '/rest/enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32/sso?role=Active'

        self._enclosures.get_sso('Active')
        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceUtilizationMixin, 'get_utilization')
    def test_get_utilization_with_all_args(self, mock_get_utilization):
        self._enclosures.get_utilization('09USE7335NW3', fields='AmbientTemperature,AveragePower,PeakPower',
                                         filter='startDate=2016-05-30T03:29:42.361Z',
                                         refresh=True, view='day')

        mock_get_utilization.assert_called_once_with('09USE7335NW3', fields='AmbientTemperature,AveragePower,PeakPower',
                                                     filter='startDate=2016-05-30T03:29:42.361Z',
                                                     refresh=True, view='day')

    @mock.patch.object(ResourceUtilizationMixin, 'get_utilization')
    def test_get_utilization_by_uri_with_defaults(self, mock_get):
        self._enclosures.get_utilization('/rest/enclosures/09USE7335NW3')
        mock_get.assert_called_once_with('/rest/enclosures/09USE7335NW3')

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'do_post')
    def test_generate_csr(self, mock_post, ensure_resource_data):
        bay_number = 1
        uri_rest_call = '/rest/enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32/https/certificaterequest?bayNumber=%d' % (bay_number)
        csr_data = {
            'type': 'CertificateDtoV2',
            'organization': 'Acme Corp.',
            'organizationalUnit': 'IT',
            'locality': 'Townburgh',
            'state': 'Mississippi',
            'country': 'US',
            'email': 'admin@example.com'
        }
        headers = {'Content-Type': 'application/json'}

        self._enclosures.generate_csr(csr_data, bay_number=bay_number)
        mock_post.assert_called_once_with(uri_rest_call, csr_data, -1, headers)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_csr(self, mock_get, ensure_resource_data):
        bay_number = 1
        uri_rest_call = '/rest/enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32/https/certificaterequest?bayNumber=%d' % (bay_number)

        self._enclosures.get_csr(bay_number=bay_number)
        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(Resource, 'ensure_resource_data')
    @mock.patch.object(ResourceHelper, 'do_put')
    def test_import_certificate(self, mock_put, ensure_resource_data):
        bay_number = 1
        uri_rest_call = '/rest/enclosures/ad28cf21-8b15-4f92-bdcf-51cb2042db32/https/certificaterequest?bayNumber=%d' % (bay_number)
        certificate_data = {
            'type': 'CertificateDataV2',
            'base64Data': '-----BEGIN CERTIFICATE----- encoded data here -----END CERTIFICATE-----'
        }
        headers = {'Content-Type': 'application/json'}

        self._enclosures.import_certificate(certificate_data, bay_number=bay_number)
        mock_put.assert_called_once_with(uri_rest_call, certificate_data, -1, headers)
