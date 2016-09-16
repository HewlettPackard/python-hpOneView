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

import io
import unittest

import mock

from hpOneView.connection import connection
from hpOneView.oneview_client import OneViewClient
from hpOneView.resources.data_services.metric_streaming import MetricStreaming
from hpOneView.resources.facilities.power_devices import PowerDevices
from hpOneView.resources.facilities.racks import Racks
from hpOneView.resources.fc_sans.managed_sans import ManagedSANs
from hpOneView.resources.fc_sans.san_managers import SanManagers
from hpOneView.resources.fc_sans.endpoints import Endpoints
from hpOneView.resources.networking.fc_networks import FcNetworks
from hpOneView.resources.networking.fcoe_networks import FcoeNetworks
from hpOneView.resources.networking.interconnect_link_topologies import InterconnectLinkTopologies
from hpOneView.resources.networking.interconnects import Interconnects
from hpOneView.resources.networking.logical_interconnect_groups import LogicalInterconnectGroups
from hpOneView.resources.networking.logical_interconnects import LogicalInterconnects
from hpOneView.resources.networking.logical_switches import LogicalSwitches
from hpOneView.resources.networking.logical_switch_groups import LogicalSwitchGroups
from hpOneView.resources.networking.uplink_sets import UplinkSets
from hpOneView.resources.facilities.datacenters import Datacenters
from hpOneView.resources.servers.server_profile_templates import ServerProfileTemplate
from hpOneView.resources.servers.server_profiles import ServerProfiles
from hpOneView.resources.uncategorized.unmanaged_devices import UnmanagedDevices
from hpOneView.resources.storage.storage_volume_attachments import StorageVolumeAttachments
from hpOneView.resources.storage.storage_volume_templates import StorageVolumeTemplates
from hpOneView.resources.storage.volumes import Volumes
from tests.test_utils import mock_builtin


class OneViewClientTest(unittest.TestCase):
    def __mock_file_open(self, json_config_content):
        # Simulates a TextIOWrapper (file output)
        return io.StringIO(json_config_content)

    @mock.patch.object(connection, 'login')
    def setUp(self, mock_login):
        super(OneViewClientTest, self).setUp()

        config = {"ip": "172.16.102.59",
                  "proxy": "127.0.0.1:3128",
                  "credentials": {
                      "authLoginDomain": "",
                      "userName": "administrator",
                      "password": ""}}

        self._oneview = OneViewClient(config)

    def test_raise_error_invalid_proxy(self):
        config = {"ip": "172.16.102.59",
                  "proxy": "3128",
                  "credentials": {
                      "authLoginDomain": "",
                      "userName": "administrator",
                      "password": ""}}

        try:
            OneViewClient(config)
        except ValueError as e:
            self.assertTrue("Proxy" in e.args[0])
        else:
            self.fail()

    @mock.patch.object(connection, 'login')
    @mock.patch(mock_builtin('open'))
    def test_from_json_file(self, mock_open, mock_login):
        json_config_content = u"""{
          "ip": "172.16.102.59",
          "credentials": {
            "userName": "administrator",
            "authLoginDomain": "",
            "password": ""
          }
        }"""
        mock_open.return_value = self.__mock_file_open(json_config_content)
        oneview_client = OneViewClient.from_json_file("config.json")

        self.assertIsInstance(oneview_client, OneViewClient)
        self.assertEqual("172.16.102.59", oneview_client.connection.get_host())

    @mock.patch.object(connection, 'login')
    @mock.patch(mock_builtin('open'))
    def test_default_api_version(self, mock_open, mock_login):
        json_config_content = u"""{
          "ip": "172.16.102.59",
          "credentials": {
            "userName": "administrator",
            "authLoginDomain": "",
            "password": ""
          }
        }"""
        mock_open.return_value = self.__mock_file_open(json_config_content)
        oneview_client = OneViewClient.from_json_file("config.json")

        self.assertEqual(200, oneview_client.connection._apiVersion)

    @mock.patch.object(connection, 'login')
    @mock.patch(mock_builtin('open'))
    def test_configured_api_version(self, mock_open, mock_login):
        json_config_content = u"""{
          "ip": "172.16.102.59",
          "api_version": 300,
          "credentials": {
            "userName": "administrator",
            "authLoginDomain": "",
            "password": ""
          }
        }"""
        mock_open.return_value = self.__mock_file_open(json_config_content)
        oneview_client = OneViewClient.from_json_file("config.json")

        self.assertEqual(300, oneview_client.connection._apiVersion)

    def test_fc_networks_has_right_type(self):
        self.assertIsInstance(self._oneview.fc_networks, FcNetworks)

    def test_fc_networks_has_value(self):
        self.assertIsNotNone(self._oneview.fc_networks)

    def test_lazy_loading_fc_networks(self):
        fcn = self._oneview.fc_networks
        self.assertEqual(fcn, self._oneview.fc_networks)

    def test_connection_type(self):
        self.assertIsInstance(self._oneview.connection, connection)

    def test_fcoe_networks_has_right_type(self):
        self.assertIsInstance(self._oneview.fcoe_networks, FcoeNetworks)

    def test_fcoe_networks_has_value(self):
        self.assertIsNotNone(self._oneview.fcoe_networks)

    def test_lazy_loading_fcoe_networks(self):
        fcn = self._oneview.fcoe_networks
        self.assertEqual(fcn, self._oneview.fcoe_networks)

    def test_metric_streaming_has_right_type(self):
        self.assertIsInstance(self._oneview.metric_streaming, MetricStreaming)

    def test_metric_streaming_has_value(self):
        self.assertIsNotNone(self._oneview.metric_streaming)

    def test_lazy_loading_enclosure_groups(self):
        enclosure_groups = self._oneview.enclosure_groups
        self.assertEqual(enclosure_groups, self._oneview.enclosure_groups)

    def test_lazy_loading_tasks(self):
        tasks = self._oneview.tasks
        self.assertEqual(tasks, self._oneview.tasks)

    def test_lazy_loading_connection_templates(self):
        connection_templates = self._oneview.connection_templates
        self.assertEqual(connection_templates, self._oneview.connection_templates)

    def test_lazy_loading_switch_types(self):
        switch_types = self._oneview.switch_types
        self.assertEqual(switch_types, self._oneview.switch_types)

    def test_lazy_loading_network_sets(self):
        network_sets = self._oneview.network_sets
        self.assertEqual(network_sets, self._oneview.network_sets)

    def test_lazy_loading_fabrics(self):
        fabrics = self._oneview.fabrics
        self.assertEqual(fabrics, self._oneview.fabrics)

    def test_lazy_loading_metric_streaming(self):
        metric = self._oneview.metric_streaming
        self.assertEqual(metric, self._oneview.metric_streaming)

    def test_lazy_loading_enclosures(self):
        enclosures = self._oneview.enclosures
        self.assertEqual(enclosures, self._oneview.enclosures)

    def test_lazy_loading_switches(self):
        switches = self._oneview.switches
        self.assertEqual(switches, self._oneview.switches)

    def test_lazy_loading_ethernet_networks(self):
        ethernet_networks = self._oneview.ethernet_networks
        self.assertEqual(ethernet_networks, self._oneview.ethernet_networks)

    def test_lazy_loading_server_hardware(self):
        server_hardware = self._oneview.server_hardware
        self.assertEqual(server_hardware, self._oneview.server_hardware)

    def test_interconnect_link_topologies_has_right_type(self):
        self.assertIsInstance(self._oneview.interconnect_link_topologies, InterconnectLinkTopologies)

    def test_interconnect_link_topologies_has_value(self):
        self.assertIsNotNone(self._oneview.interconnect_link_topologies)

    def test_lazy_loading_interconnect_link_topologies(self):
        interconnect_link_topologies = self._oneview.interconnect_link_topologies
        self.assertEqual(interconnect_link_topologies, self._oneview.interconnect_link_topologies)

    def test_interconnects_has_right_type(self):
        self.assertIsInstance(self._oneview.interconnects, Interconnects)

    def test_interconnects_has_value(self):
        self.assertIsNotNone(self._oneview.interconnects)

    def test_lazy_loading_interconnects(self):
        interconnects = self._oneview.interconnects
        self.assertEqual(interconnects, self._oneview.interconnects)

    def test_lazy_loading_connections(self):
        connections = self._oneview.connections
        self.assertEqual(connections, self._oneview.connections)

    def test_lazy_loading_server_hardware_types(self):
        server_hardware_types = self._oneview.server_hardware_types
        self.assertEqual(server_hardware_types, self._oneview.server_hardware_types)

    def test_lazy_loading_id_pools_vsn_ranges(self):
        id_pools_vsn_ranges = self._oneview.id_pools_vsn_ranges
        self.assertEqual(id_pools_vsn_ranges, self._oneview.id_pools_vsn_ranges)

    def test_lazy_loading_id_pools_vmac_ranges(self):
        id_pools_vmac_ranges = self._oneview.id_pools_vmac_ranges
        self.assertEqual(id_pools_vmac_ranges, self._oneview.id_pools_vmac_ranges)

    def test_lazy_loading_id_pools_vwwn_ranges(self):
        id_pools_vwwn_ranges = self._oneview.id_pools_vwwn_ranges
        self.assertEqual(id_pools_vwwn_ranges, self._oneview.id_pools_vwwn_ranges)

    def test_lazy_loading_logical_enclosures(self):
        logical_enclosures = self._oneview.logical_enclosures
        self.assertEqual(logical_enclosures, self._oneview.logical_enclosures)

    def test_lazy_loading_interconnect_types(self):
        interconnect_types = self._oneview.interconnect_types
        self.assertEqual(interconnect_types, self._oneview.interconnect_types)

    def test_lazy_loading_logical_downlinks(self):
        logical_downlinks = self._oneview.logical_downlinks
        self.assertEqual(logical_downlinks, self._oneview.logical_downlinks)

    def test_lazy_loading_storage_systems(self):
        storage_systems = self._oneview.storage_systems
        self.assertEqual(storage_systems, self._oneview.storage_systems)

    def test_lazy_loading_storage_pools(self):
        storage_pools = self._oneview.storage_pools
        self.assertEqual(storage_pools, self._oneview.storage_pools)

    def test_lazy_loading_firmware_drivers(self):
        firmware_drivers = self._oneview.firmware_drivers
        self.assertEqual(firmware_drivers, self._oneview.firmware_drivers)

    def test_lazy_loading_firmware_bundles(self):
        firmware_bundles = self._oneview.firmware_bundles
        self.assertEqual(firmware_bundles, self._oneview.firmware_bundles)

    def test_power_devices_has_right_type(self):
        self.assertIsInstance(self._oneview.power_devices, PowerDevices)

    def test_power_devices_has_value(self):
        self.assertIsNotNone(self._oneview.power_devices)

    def test_lazy_loading_power_devices(self):
        power_devices = self._oneview.power_devices
        self.assertEqual(power_devices, self._oneview.power_devices)

    def test_racks_has_right_type(self):
        self.assertIsInstance(self._oneview.racks, Racks)

    def test_racks_has_value(self):
        self.assertIsNotNone(self._oneview.racks)

    def test_lazy_loading_racks(self):
        racks = self._oneview.racks
        self.assertEqual(racks, self._oneview.racks)

    def test_san_managers_has_right_type(self):
        self.assertIsInstance(self._oneview.san_managers, SanManagers)

    def test_san_managers_has_value(self):
        self.assertIsNotNone(self._oneview.san_managers)

    def test_lazy_loading_san_managers(self):
        san_managers = self._oneview.san_managers
        self.assertEqual(san_managers, self._oneview.san_managers)

    def test_endpoints_has_right_type(self):
        self.assertIsInstance(self._oneview.endpoints, Endpoints)

    def test_endpoints_has_value(self):
        self.assertIsNotNone(self._oneview.endpoints)

    def test_lazy_loading_endpoints(self):
        endpoints = self._oneview.endpoints
        self.assertEqual(endpoints, self._oneview.endpoints)

    def test_logical_interconnect_groups_has_right_type(self):
        self.assertIsInstance(self._oneview.logical_interconnect_groups, LogicalInterconnectGroups)

    def test_logical_interconnect_groups_has_value(self):
        self.assertIsNotNone(self._oneview.logical_interconnect_groups)

    def test_lazy_loading_logical_interconnect_groups(self):
        logical_interconnect_groups = self._oneview.logical_interconnect_groups
        self.assertEqual(logical_interconnect_groups, self._oneview.logical_interconnect_groups)

    def test_logical_switch_groups_has_right_type(self):
        self.assertIsInstance(self._oneview.logical_switch_groups, LogicalSwitchGroups)

    def test_logical_switch_groups_has_value(self):
        self.assertIsNotNone(self._oneview.logical_switch_groups)

    def test_lazy_loading_logical_switch_groups(self):
        logical_switch_groups = self._oneview.logical_switch_groups
        self.assertEqual(logical_switch_groups, self._oneview.logical_switch_groups)

    def test_logical_switches_has_right_type(self):
        self.assertIsInstance(self._oneview.logical_switches, LogicalSwitches)

    def test_lazy_loading_logical_switches(self):
        logical_switches = self._oneview.logical_switches
        self.assertEqual(logical_switches, self._oneview.logical_switches)

    def test_logical_interconnects_has_right_type(self):
        self.assertIsInstance(self._oneview.logical_interconnects, LogicalInterconnects)

    def test_logical_interconnects_has_value(self):
        self.assertIsNotNone(self._oneview.logical_interconnects)

    def test_lazy_loading_logical_interconnects(self):
        logical_interconnects = self._oneview.logical_interconnects
        self.assertEqual(logical_interconnects, self._oneview.logical_interconnects)

    def test_storage_volume_templates_has_right_type(self):
        self.assertIsInstance(self._oneview.storage_volume_templates, StorageVolumeTemplates)

    def test_storage_volume_templates_has_value(self):
        self.assertIsNotNone(self._oneview.storage_volume_templates)

    def test_lazy_loading_storage_volume_templates(self):
        storage_volume_templates = self._oneview.storage_volume_templates
        self.assertEqual(storage_volume_templates, self._oneview.storage_volume_templates)

    def test_storage_volume_attachments_has_right_type(self):
        self.assertIsInstance(self._oneview.storage_volume_attachments, StorageVolumeAttachments)

    def test_storage_volume_attachments_has_value(self):
        self.assertIsNotNone(self._oneview.storage_volume_attachments)

    def test_lazy_loading_storage_volume_attachments(self):
        storage_volume_attachments = self._oneview.storage_volume_attachments
        self.assertEqual(storage_volume_attachments, self._oneview.storage_volume_attachments)

    def test_uplink_sets_has_right_type(self):
        self.assertIsInstance(self._oneview.uplink_sets, UplinkSets)

    def test_uplink_sets_has_value(self):
        self.assertIsNotNone(self._oneview.uplink_sets)

    def test_lazy_loading_uplink_sets(self):
        copy_uplink_sets = self._oneview.uplink_sets
        self.assertEqual(copy_uplink_sets, self._oneview.uplink_sets)

    def test_unmanaged_devices_has_right_type(self):
        self.assertIsInstance(self._oneview.unmanaged_devices, UnmanagedDevices)

    def test_volumes_has_right_type(self):
        self.assertIsInstance(self._oneview.volumes, Volumes)

    def test_volumes_has_value(self):
        self.assertIsNotNone(self._oneview.volumes)

    def test_lazy_loading_volumes(self):
        copy_volumes = self._oneview.volumes
        self.assertEqual(copy_volumes, self._oneview.volumes)

    def test_server_profile_templates_has_right_type(self):
        self.assertIsInstance(self._oneview.server_profile_templates, ServerProfileTemplate)

    def test_server_profile_templates_has_value(self):
        self.assertIsNotNone(self._oneview.server_profile_templates)

    def test_lazy_loading_server_profile_templates(self):
        server_profile_templates = self._oneview.server_profile_templates
        self.assertEqual(server_profile_templates, self._oneview.server_profile_templates)

    def test_server_profiles_has_right_type(self):
        self.assertIsInstance(self._oneview.server_profiles, ServerProfiles)

    def test_server_profiles_has_value(self):
        self.assertIsNotNone(self._oneview.server_profiles)

    def test_lazy_loading_server_profiles(self):
        server_profiles = self._oneview.server_profiles
        self.assertEqual(server_profiles, self._oneview.server_profiles)

    def test_datacenters_has_right_type(self):
        self.assertIsInstance(self._oneview.datacenters, Datacenters)

    def test_lazy_loading_datacenters(self):
        datacenters = self._oneview.datacenters
        self.assertEqual(datacenters, self._oneview.datacenters)

    def test_managed_sans_has_right_type(self):
        self.assertIsInstance(self._oneview.managed_sans, ManagedSANs)

    def test_lazy_loading_managed_sans(self):
        managed_sans = self._oneview.managed_sans
        self.assertEqual(managed_sans, self._oneview.managed_sans)
