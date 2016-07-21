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
from hpOneView.resources.servers.server_hardware import ServerHardware
from hpOneView.resources.resource import ResourceClient


class ServerHardwareTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._server_hardware = ServerHardware(self.connection)

    @mock.patch.object(ResourceClient, 'get_utilization')
    def test_get_utilization_with_all_args(self, mock_get_utilization):
        self._server_hardware.get_utilization('09USE7335NW3', fields='AmbientTemperature,AveragePower,PeakPower',
                                              filter='startDate=2016-05-30T03:29:42.361Z',
                                              refresh=True, view='day')

        mock_get_utilization.assert_called_once_with('09USE7335NW3', fields='AmbientTemperature,AveragePower,PeakPower',
                                                     filter='startDate=2016-05-30T03:29:42.361Z',
                                                     refresh=True, view='day')

    @mock.patch.object(ResourceClient, 'get_utilization')
    def test_get_utilization_with_defaults(self, mock_get):
        self._server_hardware.get_utilization('09USE7335NW3')

        mock_get.assert_called_once_with(
            '09USE7335NW3', fields=None, filter=None, refresh=False, view=None)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._server_hardware.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default_values(self, mock_get_all):
        self._server_hardware.get_all()

        mock_get_all.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'get_by')
    def test_get_by_called_once(self, mock_get_by):
        self._server_hardware.get_by('name', 'OneViewSDK-Test-Rack-Server')

        mock_get_by.assert_called_once_with(
            'name', 'OneViewSDK-Test-Rack-Server')

    @mock.patch.object(ResourceClient, 'create')
    def test_add_called_once(self, mock_create):
        information = {
            "licensingIntent": "OneView",
            "configurationState": "Managed"
        }
        mock_create.return_value = {}

        self._server_hardware.add(information)
        mock_create.assert_called_once_with(information.copy(), timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._server_hardware.get('3518be0e-17c1-4189-8f81-83f3724f6155')

        mock_get.assert_called_once_with(
            '3518be0e-17c1-4189-8f81-83f3724f6155')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_with_uri_called_once(self, mock_get):
        uri = '/rest/server-hardware/3518be0e-17c1-4189-8f81-83f3724f6155'
        self._server_hardware.get(uri)

        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove_called_once(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._server_hardware.remove(id, force=False)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'delete')
    def test_remove_called_once_with_force(self, mock_delete):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        self._server_hardware.remove(id, force=True)

        mock_delete.assert_called_once_with(id, force=True, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_bios_by_uri(self, mock_get):
        uri_server_hardware = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32/bios'

        self._server_hardware.get_bios(uri_server_hardware)

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_bios_by_id(self, mock_get):
        id_server_hardware = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32/bios'

        self._server_hardware.get_bios(id_server_hardware)

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_environmental_configuration_by_uri(self, mock_get):
        uri_server_hardware = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32/environmentalConfiguration'

        self._server_hardware.get_environmental_configuration(
            uri_server_hardware)

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_environmental_configuration_by_id(self, mock_get):
        id_server_hardware = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32/environmentalConfiguration'

        self._server_hardware.get_environmental_configuration(
            id_server_hardware)

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_environmental_configuration_by_uri(self, mock_update):
        uri_server_hardware = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32/environmentalConfiguration'
        configuration = {"calibratedMaxPower": 2500}
        configuration_rest_call = configuration.copy()

        self._server_hardware.update_environmental_configuration(
            configuration, uri_server_hardware, timeout=-1)

        mock_update.assert_called_once_with(
            configuration_rest_call, uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_environmental_configuration_by_id(self, mock_update):
        id_server_hardware = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32/environmentalConfiguration'
        configuration = {"calibratedMaxPower": 2500}
        configuration_rest_call = configuration.copy()

        self._server_hardware.update_environmental_configuration(
            configuration, id_server_hardware, timeout=-1)

        mock_update.assert_called_once_with(
            configuration_rest_call, uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_ilo_sso_url_by_url(self, mock_get):
        uri_server_hardware = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32/iloSsoUrl'

        self._server_hardware.get_ilo_sso_url(uri_server_hardware)

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_ilo_sso_url_by_id(self, mock_get):
        id_server_hardware = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32/iloSsoUrl'

        self._server_hardware.get_ilo_sso_url(id_server_hardware)

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_java_remote_console_by_url(self, mock_get):
        uri_server_hardware = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32/javaRemoteConsoleUrl'

        self._server_hardware.get_java_remote_console_url(uri_server_hardware)

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_java_remote_console_by_id(self, mock_get):
        id_server_hardware = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32/javaRemoteConsoleUrl'

        self._server_hardware.get_java_remote_console_url(id_server_hardware)

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceClient, 'update')
    def test_refresh_state_by_uri(self, mock_update):
        uri_server_hardware = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32/refreshState'
        configuration = {"refreshState": "RefreshPending"}
        configuration_rest_call = configuration.copy()

        self._server_hardware.refresh_state(
            configuration, uri_server_hardware, timeout=-1)

        mock_update.assert_called_once_with(
            configuration_rest_call, uri=uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_refresh_state_by_id(self, mock_update):
        id_server_hardware = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32/refreshState'
        configuration = {"refreshState": "RefreshPending"}
        configuration_rest_call = configuration.copy()

        self._server_hardware.refresh_state(
            configuration, id_server_hardware, timeout=-1)

        mock_update.assert_called_once_with(
            configuration_rest_call, uri=uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_power_state_by_uri(self, mock_update):
        uri_server_hardware = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32/powerState'
        configuration = {
            "powerState": "Off",
            "powerControl": "MomentaryPress"
        }
        configuration_rest_call = configuration.copy()

        self._server_hardware.update_power_state(
            configuration, uri_server_hardware)

        mock_update.assert_called_once_with(
            configuration_rest_call, uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_power_state_by_id(self, mock_update):
        id_server_hardware = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32/powerState'
        configuration = {
            "powerState": "Off",
            "powerControl": "MomentaryPress"
        }
        configuration_rest_call = configuration.copy()

        self._server_hardware.update_power_state(
            configuration, id_server_hardware, -1)

        mock_update.assert_called_once_with(
            configuration_rest_call, uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_remote_console_url_by_url(self, mock_get):
        uri_server_hardware = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32/remoteConsoleUrl'

        self._server_hardware.get_remote_console_url(uri_server_hardware)

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_remote_console_url_by_id(self, mock_get):
        id_server_hardware = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32/remoteConsoleUrl'

        self._server_hardware.get_remote_console_url(id_server_hardware)

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceClient, 'update_with_zero_body')
    def test_update_mp_firware_version_called_once(self, mock_get):
        id_server_hardware = '/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32'

        self._server_hardware.update_mp_firware_version(id_server_hardware)

        mock_get.assert_called_once_with('/rest/server-hardware/ad28cf21-8b15-4f92-bdcf-51cb2042db32/mpFirmwareVersion',
                                         -1)
