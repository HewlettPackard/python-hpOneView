# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
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
from hpOneView.resources.networking.logical_interconnects import LogicalInterconnects
from hpOneView.resources.resource import ResourceClient


class LogicalInterconnectsTest(unittest.TestCase):

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._logical_interconnect = LogicalInterconnects(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._logical_interconnect.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once_with_default(self, mock_get_all):
        self._logical_interconnect.get_all()
        mock_get_all.assert_called_once_with(0, -1, filter='', sort='')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_id_called_once(self, mock_get):
        logical_interconnect_id = "f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._logical_interconnect.get(logical_interconnect_id)
        mock_get.assert_called_once_with(logical_interconnect_id)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_uri_called_once(self, mock_get):
        logical_interconnect_uri = "/rest/logical-interconnects/f0a0a113-ec97-41b4-83ce-d7c92b900e7c"
        self._logical_interconnect.get(logical_interconnect_uri)
        mock_get.assert_called_once_with(logical_interconnect_uri)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_by_name_return_logical_interconnect_when_exists(self, mock_get_all):
        mock_get_all.return_value = [
            {"name": "Logical Interconnect 1", "uri": "/path/to/logical/interconnect/1"},
            {"name": "Logical Interconnect 2", "uri": "/path/to/logical/interconnect/2"}
        ]
        logical_interconnect = self._logical_interconnect.get_by_name("Logical Interconnect 1")

        self.assertEqual(logical_interconnect,
                         {"name": "Logical Interconnect 1", "uri": "/path/to/logical/interconnect/1"})

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_by_name_return_null_when_logical_interconnect_not_exist(self, mock_get_all):
        mock_get_all.return_value = [
            {"name": "Logical Interconnect 1", "uri": "/path/to/logical/interconnect/1"},
            {"name": "Logical Interconnect 2", "uri": "/path/to/logical/interconnect/2"}
        ]
        logical_interconnect = self._logical_interconnect.get_by_name("another name")

        self.assertIsNone(logical_interconnect)

    @mock.patch.object(ResourceClient, 'update_with_zero_body')
    def test_update_compliance_by_uri(self, mock_update_with_zero_body):
        logical_interconnect_uri = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/compliance'

        self._logical_interconnect.update_compliance(logical_interconnect_uri)

        mock_update_with_zero_body.assert_called_once_with(uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceClient, 'update_with_zero_body')
    def test_update_compliance_by_id(self, mock_update_with_zero_body):
        mock_update_with_zero_body.return_value = {}
        logical_interconnect_id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/compliance'

        self._logical_interconnect.update_compliance(logical_interconnect_id)

        mock_update_with_zero_body.assert_called_once_with(uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_ethernet_settings_by_uri(self, mock_update):
        logical_interconnect_uri = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/ethernetSettings'
        configuration = {"enableNetworkLoopProtection": True}
        configuration_rest_call = configuration.copy()

        self._logical_interconnect.update_ethernet_settings(logical_interconnect_uri, configuration)

        mock_update.assert_called_once_with(configuration_rest_call, uri=uri_rest_call, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_ethernet_settings_by_id(self, mock_update):
        logical_interconnect_id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/ethernetSettings'
        configuration = {"enableNetworkLoopProtection": True}
        configuration_rest_call = configuration.copy()

        self._logical_interconnect.update_ethernet_settings(logical_interconnect_id, configuration)

        mock_update.assert_called_once_with(configuration_rest_call, uri=uri_rest_call, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_ethernet_settings_with_force(self, mock_update):
        logical_interconnect_id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'

        self._logical_interconnect.update_ethernet_settings(logical_interconnect_id, {}, force=True)

        mock_update.assert_called_once_with(mock.ANY, uri=mock.ANY, force=True, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_internal_networks_by_uri(self, mock_update):
        logical_interconnect_uri = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/internalNetworks'
        network_uri_list = ['/rest/ethernet-networks/123s4s', '/rest/ethernet-networks/335d']

        self._logical_interconnect.update_internal_networks(logical_interconnect_uri, network_uri_list)

        mock_update.assert_called_once_with(network_uri_list, uri=uri_rest_call, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_internal_networks_by_id(self, mock_update):
        logical_interconnect_id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/internalNetworks'
        network_uri_list = ['/rest/ethernet-networks/123s4s', '/rest/ethernet-networks/335d']

        self._logical_interconnect.update_internal_networks(logical_interconnect_id, network_uri_list)

        mock_update.assert_called_once_with(network_uri_list, uri=uri_rest_call, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_internal_networks_with_force(self, mock_update):
        self._logical_interconnect.update_internal_networks("abc123", [], force=True)

        mock_update.assert_called_once_with(mock.ANY, uri=mock.ANY, force=True, timeout=-1)

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_internal_vlans_by_uri(self, mock_get_collection):
        logical_interconnect_uri = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/internalVlans'

        self._logical_interconnect.get_internal_vlans(logical_interconnect_uri)

        mock_get_collection.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_internal_vlans_by_id(self, mock_get_collection):
        logical_interconnect_id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/internalVlans'

        self._logical_interconnect.get_internal_vlans(logical_interconnect_id)

        mock_get_collection.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_settings_by_uri(self, mock_update):
        logical_interconnect_uri = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/settings'
        settings = {
            "type": "type",
            "ethernetSettings": {
                "type": "ethernet-type",
                "macRefreshInterval": "5"
            }
        }
        settings_rest_call = settings.copy()

        self._logical_interconnect.update_settings(logical_interconnect_uri, settings)

        mock_update.assert_called_once_with(settings_rest_call, uri=uri_rest_call, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_settings_by_id(self, mock_update):
        logical_interconnect_id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/settings'
        settings = {
            "type": "type",
            "ethernetSettings": {
                "type": "ethernet-type",
                "macRefreshInterval": "5"
            }
        }
        settings_rest_call = settings.copy()

        self._logical_interconnect.update_settings(logical_interconnect_id, settings)

        mock_update.assert_called_once_with(settings_rest_call, uri=uri_rest_call, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_settings_with_force(self, mock_update):
        self._logical_interconnect.update_settings("abc123", {}, force=True)

        mock_update.assert_called_once_with(mock.ANY, uri=mock.ANY, force=True, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_settings_with_default_values(self, mock_update):
        settings = {
            "ethernetSettings": {
                "macRefreshInterval": "5"
            }
        }
        settings_with_default_values = {
            "type": "InterconnectSettingsV3",
            "ethernetSettings": {
                "type": "EthernetInterconnectSettingsV3",
                "macRefreshInterval": "5"
            }
        }
        self._logical_interconnect.update_settings("abc123", settings)

        mock_update.assert_called_once_with(settings_with_default_values, uri=mock.ANY, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'update_with_zero_body')
    def test_update_configuration_by_uri(self, mock_update_with_zero_body):
        logical_interconnect_uri = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/configuration'

        self._logical_interconnect.update_configuration(logical_interconnect_uri)

        mock_update_with_zero_body.assert_called_once_with(uri=uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceClient, 'update_with_zero_body')
    def test_update_configuration_by_id(self, mock_update_with_zero_body):
        logical_interconnect_id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/configuration'

        self._logical_interconnect.update_configuration(logical_interconnect_id)

        mock_update_with_zero_body.assert_called_once_with(uri=uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_unassigned_uplink_ports_by_uri(self, mock_get_collection):
        logical_interconnect_uri = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = logical_interconnect_uri + '/unassignedUplinkPortsForPortMonitor'

        self._logical_interconnect.get_unassigned_uplink_ports(logical_interconnect_uri)

        mock_get_collection.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_unassigned_uplink_ports_by_id(self, mock_get_collection):
        logical_interconnect_id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        logical_interconnect_uri = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = logical_interconnect_uri + '/unassignedUplinkPortsForPortMonitor'

        self._logical_interconnect.get_unassigned_uplink_ports(logical_interconnect_id)

        mock_get_collection.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_port_monitor_by_uri(self, mock_get):
        uri_logical_interconnect = '/rest/logical-interconnects/be227eaf-3810-4b8a-b9ba-0af4479a9fe2'
        uri_rest_call = uri_logical_interconnect + '/port-monitor'

        self._logical_interconnect.get_port_monitor(uri_logical_interconnect)

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_port_monitor_by_id(self, mock_get):
        logical_interconnect_id = 'be227eaf-3810-4b8a-b9ba-0af4479a9fe2'
        uri_logical_interconnect = '/rest/logical-interconnects/be227eaf-3810-4b8a-b9ba-0af4479a9fe2'
        uri_rest_call = uri_logical_interconnect + '/port-monitor'

        self._logical_interconnect.get_port_monitor(logical_interconnect_id)

        mock_get.assert_called_once_with(uri_rest_call)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_port_monitor_by_uri(self, mock_update):
        logical_interconnect_uri = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/port-monitor'
        monitor_data = {
            "analyzerPort": {
                "portUri": "/rest/interconnects/76ad8f4b-b01b-d2ac31295c19/ports/76ad8f4b-6f13:X1",
                "portMonitorConfigInfo": "AnalyzerPort"
            },
            "enablePortMonitor": True,
            "type": "port-monitor",
            "monitoredPorts": [{
                "portUri": "/rest/interconnects/76ad8f4b-b01b-d2ac31295c19/ports/76ad8f4b-6f13:X1",
                "portMonitorConfigInfo": "MonitoredBoth"
            }]
        }
        port_monitor_rest_call = monitor_data.copy()

        self._logical_interconnect.update_port_monitor(logical_interconnect_uri, monitor_data)

        mock_update.assert_called_once_with(port_monitor_rest_call, uri=uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_port_monitor_by_id(self, mock_update):
        logical_interconnect_id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        uri_rest_call = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/port-monitor'
        monitor_data = {
            "analyzerPort": {
                "portUri": "/rest/interconnects/76ad8f4b-b01b-d2ac31295c19/ports/76ad8f4b-6f13:X1",
                "portMonitorConfigInfo": "AnalyzerPort"
            },
            "enablePortMonitor": True,
            "type": "port-monitor",
            "monitoredPorts": [{
                "portUri": "/rest/interconnects/76ad8f4b-b01b-d2ac31295c19/ports/76ad8f4b-6f13:X1",
                "portMonitorConfigInfo": "MonitoredBoth"
            }]
        }
        port_monitor_rest_call = monitor_data.copy()

        self._logical_interconnect.update_port_monitor(logical_interconnect_id, monitor_data)

        mock_update.assert_called_once_with(port_monitor_rest_call, uri=uri_rest_call, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_telemetry_configuration_by_uri(self, mock_get):
        uri_telemetry_configuration = '/rest/logical-interconnects/091c597d-5c68-45e5-ba40-5d69a1da8f90/' \
                                      'telemetry-configurations/dead0c9c-54db-4683-b402-48c2e86fe278'

        self._logical_interconnect.get_telemetry_configuration(uri_telemetry_configuration)

        mock_get.assert_called_once_with(uri_telemetry_configuration)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_interconnect_called_once(self, mock_create):
        location_entries = {"locationEntries": [{"type": "Bay", "value": "1"}]}

        self._logical_interconnect.create_interconnect(location_entries.copy(), timeout=-1)

        mock_create.assert_called_once_with(location_entries,
                                            uri="/rest/logical-interconnects/locations/interconnects",
                                            timeout=-1)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_interconnect_called_once(self, mock_delete):
        self._logical_interconnect.delete_interconnect(enclosure_uri="/rest/enclosures/09SGH100X6J1",
                                                       bay=3, timeout=-1)

        expected_uri = "/rest/logical-interconnects/locations/interconnects" \
                       "?location=Enclosure:/rest/enclosures/09SGH100X6J1,Bay:3"
        mock_delete.assert_called_once_with(expected_uri, timeout=-1)

    @mock.patch.object(ResourceClient, 'build_uri')
    @mock.patch.object(ResourceClient, 'get')
    def test_get_firmware(self, mock_get, mock_build_uri):
        logical_interconnect_id = '3518be0e-17c1-4189-8f81-83f3724f6155'

        logical_interconnect_uri = "/rest/logical-interconnects/" + logical_interconnect_id
        mock_build_uri.return_value = logical_interconnect_uri

        expected_uri = logical_interconnect_uri + "/firmware"

        self._logical_interconnect.get_firmware(logical_interconnect_id)
        mock_get.assert_called_once_with(expected_uri)

    @mock.patch.object(ResourceClient, 'build_uri')
    @mock.patch.object(ResourceClient, 'update')
    def test_install_firmware(self, mock_update, mock_build_uri):
        logical_interconnect_id = '3518be0e-17c1-4189-8f81-83f3724f6155'

        fake_firmware = dict(
            command="Update",
            sppUri="/rest/firmware-drivers/Service_0Pack_0for_0ProLiant"
        )

        logical_interconnect_uri = "/rest/logical-interconnects/" + logical_interconnect_id
        mock_build_uri.return_value = logical_interconnect_uri

        expected_uri = logical_interconnect_uri + "/firmware"

        self._logical_interconnect.install_firmware(fake_firmware, logical_interconnect_id)
        mock_update.assert_called_once_with(fake_firmware, expected_uri)

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_forwarding_information_base_by_id(self, mock_get_collection):
        filter = 'name=TestName'
        logical_interconnect_id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'

        self._logical_interconnect.get_forwarding_information_base(logical_interconnect_id, filter)

        expected_uri = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/forwarding-information-base'
        mock_get_collection.assert_called_once_with(expected_uri, filter=filter)

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_forwarding_information_base_by_uri(self, mock_get_collection):
        filter = 'name=TestName'
        logical_interconnect_uri = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32'

        self._logical_interconnect.get_forwarding_information_base(logical_interconnect_uri, filter)

        expected_uri = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/forwarding-information-base'
        mock_get_collection.assert_called_once_with(expected_uri, filter=filter)

    @mock.patch.object(ResourceClient, 'get_collection')
    def test_get_forwarding_information_base_when_no_filtering(self, mock_get_collection):
        self._logical_interconnect.get_forwarding_information_base("ad28cf21")

        mock_get_collection.assert_called_once_with(mock.ANY, filter='')

    @mock.patch.object(ResourceClient, 'create_with_zero_body')
    def test_create_interconnect_called_once_when_id_provided(self, mock_create_with_zero_body):
        logical_interconnect_id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'

        self._logical_interconnect.create_forwarding_information_base(logical_interconnect_id)

        expected_uri = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/forwarding-information-base'
        mock_create_with_zero_body.assert_called_once_with(uri=expected_uri, timeout=-1)

    @mock.patch.object(ResourceClient, 'create_with_zero_body')
    def test_create_interconnect_called_once_when_uri_provided(self, mock_create_with_zero_body):
        logical_interconnect_uri = "/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32"

        self._logical_interconnect.create_forwarding_information_base(logical_interconnect_uri)

        expected_uri = '/rest/logical-interconnects/ad28cf21-8b15-4f92-bdcf-51cb2042db32/forwarding-information-base'
        mock_create_with_zero_body.assert_called_once_with(uri=expected_uri, timeout=-1)
