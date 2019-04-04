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
from hpOneView.resources.servers.server_hardware import ServerHardware
from hpOneView.resources.resource import (ResourceHelper,
                                          ResourceUtilizationMixin,
                                          ResourcePatchMixin)


class ServerHardwareTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._server_hardware = ServerHardware(self.connection)
        self.uri = "/rest/server-hardware/1224242424"
        self._server_hardware.data = {"uri": self.uri}

    @mock.patch.object(ResourceUtilizationMixin, 'get_utilization')
    def test_get_utilization_with_all_args(self, mock_get_utilization):
        self._server_hardware.get_utilization(fields='AmbientTemperature,AveragePower,PeakPower',
                                              filter='startDate=2016-05-30T03:29:42.361Z',
                                              refresh=True, view='day')

        mock_get_utilization.assert_called_once_with(fields='AmbientTemperature,AveragePower,PeakPower',
                                                     filter='startDate=2016-05-30T03:29:42.361Z',
                                                     refresh=True, view='day')

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_utilization_with_defaults(self, mock_get):
        self._server_hardware.get_utilization()

        mock_get.assert_called_once_with("{}/utilization".format(self.uri))

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._server_hardware.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(start=2, count=500, filter=filter, sort=sort)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_called_once_with_default_values(self, mock_get_all):
        self._server_hardware.get_all()

        mock_get_all.assert_called_once_with(start=0, count=-1, filter='', sort='')

    @mock.patch.object(ResourceHelper, 'create')
    def test_add_called_once(self, mock_create):
        information = {
            "licensingIntent": "OneView",
            "configurationState": "Managed"
        }
        mock_create.return_value = {}

        self._server_hardware.add(information)
        mock_create.assert_called_once_with(information.copy(), None, -1, None, False)

    @mock.patch.object(ResourceHelper, 'create')
    def test_add_multiple_servers_called_once(self, mock_create):
        information = {
            "licensingIntent": "OneView",
            "configurationState": "Managed"
        }
        mock_create.return_value = {}

        self._server_hardware.add_multiple_servers(information)
        mock_create.assert_called_once_with(information.copy(),
                                            '/rest/server-hardware/discovery',
                                            -1, None, False)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_remove_called_once(self, mock_delete):
        self._server_hardware.remove(force=False)

        mock_delete.assert_called_once_with(self.uri, force=False,
                                            custom_headers=None, timeout=-1)

    @mock.patch.object(ResourceHelper, 'delete')
    def test_remove_called_once_with_force(self, mock_delete):
        self._server_hardware.remove(force=True)

        mock_delete.assert_called_once_with(self.uri, force=True,
                                            custom_headers=None,
                                            timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_bios(self, mock_get):
        uri_rest_call = '{}/bios'.format(self.uri)

        self._server_hardware.get_bios()

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_environmental_configuration(self, mock_get):
        uri_rest_call = '{}/environmentalConfiguration'.format(self.uri)

        self._server_hardware.get_environmental_configuration()

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'update')
    def test_update_environmental_configuration(self, mock_update):
        uri_rest_call = '{}/environmentalConfiguration'.format(self.uri)
        configuration = {"calibratedMaxPower": 2500}
        configuration_rest_call = configuration.copy()

        self._server_hardware.update_environmental_configuration(
            configuration, timeout=-1)

        mock_update.assert_called_once_with(
            configuration_rest_call, uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_ilo_sso_url(self, mock_get):
        uri_rest_call = '{}/iloSsoUrl'.format(self.uri)

        self._server_hardware.get_ilo_sso_url()

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_ilo_sso_url_with_ip(self, mock_get):
        uri_rest_call = '{}/iloSsoUrl?ip=172.16.8.4'.format(self.uri)

        self._server_hardware.get_ilo_sso_url(ip='172.16.8.4')

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_java_remote_console(self, mock_get):
        uri_rest_call = '{}/javaRemoteConsoleUrl'.format(self.uri)

        self._server_hardware.get_java_remote_console_url()

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_java_remote_console_with_ip(self, mock_get):
        uri_rest_call = '{}/javaRemoteConsoleUrl?ip=172.16.8.4'.format(self.uri)

        self._server_hardware.get_java_remote_console_url(ip='172.16.8.4')

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'update')
    def test_refresh_state(self, mock_update):
        uri_rest_call = '{}/refreshState'.format(self.uri)
        configuration = {"refreshState": "RefreshPending"}
        configuration_rest_call = configuration.copy()

        self._server_hardware.refresh_state(
            configuration, timeout=-1)

        mock_update.assert_called_once_with(
            configuration_rest_call, uri=uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceHelper, 'update')
    def test_power_state(self, mock_update):
        uri_rest_call = '{}/powerState'.format(self.uri)
        configuration = {
            "powerState": "Off",
            "powerControl": "MomentaryPress"
        }
        configuration_rest_call = configuration.copy()

        self._server_hardware.update_power_state(configuration)

        mock_update.assert_called_once_with(
            configuration_rest_call, uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_remote_console_url(self, mock_get):
        uri_rest_call = '{}/remoteConsoleUrl'.format(self.uri)

        self._server_hardware.get_remote_console_url()

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_remote_console_url_with_ip(self, mock_get):
        uri_rest_call = '{}/remoteConsoleUrl?ip=172.16.8.4'.format(self.uri)

        self._server_hardware.get_remote_console_url(ip='172.16.8.4')

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceHelper, 'do_put')
    def test_update_mp_firware_version_called_once(self, mock_get):
        self._server_hardware.update_mp_firware_version()
        uri = "{}/mpFirmwareVersion".format(self.uri)
        mock_get.assert_called_once_with(uri, None, -1, None)

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_firmwares_with_defaults(self, mock_get):
        self._server_hardware.get_all_firmwares()

        mock_get.assert_called_once_with(0, -1, '', '', '', '', '',
                                         '/rest/server-hardware/*/firmware')

    @mock.patch.object(ResourceHelper, 'get_all')
    def test_get_all_firmwares_with_all_arguments(self, mock_get):
        self._server_hardware.get_all_firmwares("name='name'", 2, 5, 'query', 'sort')

        mock_get.assert_called_once_with(2, 5, "name='name'",
                                         'query', 'sort',
                                         '', '', '/rest/server-hardware/*/firmware')

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_firmware_by_id(self, mock_get):
        self._server_hardware.get_firmware()

        mock_get.assert_called_once_with('{}/firmware'.format(self.uri))

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_firmware_by_uri(self, mock_get):
        self._server_hardware.get_firmware()

        mock_get.assert_called_once_with('{}/firmware'.format(self.uri))

    @mock.patch.object(ResourcePatchMixin, 'patch_request')
    def test_patch_called_once(self, mock_patch):
        self._server_hardware.patch('replace', '/uidState', 'On')

        mock_patch.assert_called_once_with(self.uri,
                                           body=[{'op': 'replace',
                                                  'path': '/uidState',
                                                  'value': 'On'}],
                                           custom_headers=None,
                                           timeout=-1)

    @mock.patch.object(ResourceHelper, 'do_get')
    def test_get_physical_server_hardware(self, mock_get):
        uri_rest_call = '{}/physicalServerHardware'.format(self.uri)

        self._server_hardware.get_physical_server_hardware()

        mock_get.assert_called_once_with(uri_rest_call)
