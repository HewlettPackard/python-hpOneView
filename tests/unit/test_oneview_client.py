# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2019) Hewlett Packard Enterprise Development LP
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
from hpOneView.resources.security.certificate_authority import CertificateAuthority
from hpOneView.resources.data_services.metric_streaming import MetricStreaming
from hpOneView.resources.facilities.power_devices import PowerDevices
from hpOneView.resources.facilities.racks import Racks
from hpOneView.resources.fc_sans.managed_sans import ManagedSANs
from hpOneView.resources.fc_sans.san_managers import SanManagers
from hpOneView.resources.fc_sans.endpoints import Endpoints
from hpOneView.resources.settings.backups import Backups
from hpOneView.resources.settings.restores import Restores
from hpOneView.resources.settings.scopes import Scopes
from hpOneView.resources.networking.fc_networks import FcNetworks
from hpOneView.resources.networking.fcoe_networks import FcoeNetworks
from hpOneView.resources.networking.interconnect_link_topologies import InterconnectLinkTopologies
from hpOneView.resources.networking.interconnects import Interconnects
from hpOneView.resources.networking.logical_interconnect_groups import LogicalInterconnectGroups
from hpOneView.resources.networking.logical_interconnects import LogicalInterconnects
from hpOneView.resources.networking.logical_switches import LogicalSwitches
from hpOneView.resources.networking.logical_switch_groups import LogicalSwitchGroups
from hpOneView.resources.servers.migratable_vc_domains import MigratableVcDomains
from hpOneView.resources.networking.uplink_sets import UplinkSets
from hpOneView.resources.networking.sas_interconnects import SasInterconnects
from hpOneView.resources.networking.sas_logical_interconnect_groups import SasLogicalInterconnectGroups
from hpOneView.resources.networking.sas_logical_interconnects import SasLogicalInterconnects
from hpOneView.resources.networking.sas_interconnect_types import SasInterconnectTypes
from hpOneView.resources.facilities.datacenters import Datacenters
from hpOneView.resources.servers.server_profile_templates import ServerProfileTemplate
from hpOneView.resources.servers.server_profiles import ServerProfiles
from hpOneView.resources.servers.id_pools import IdPools
from hpOneView.resources.servers.id_pools_ranges import IdPoolsRanges
from hpOneView.resources.servers.id_pools_ipv4_ranges import IdPoolsIpv4Ranges
from hpOneView.resources.servers.id_pools_ipv4_subnets import IdPoolsIpv4Subnets
from hpOneView.resources.uncategorized.unmanaged_devices import UnmanagedDevices
from hpOneView.resources.storage.sas_logical_jbods import SasLogicalJbods
from hpOneView.resources.storage.storage_volume_attachments import StorageVolumeAttachments
from hpOneView.resources.storage.storage_volume_templates import StorageVolumeTemplates
from hpOneView.resources.storage.volumes import Volumes
from hpOneView.resources.storage.drive_enclosures import DriveEnclosures
from hpOneView.resources.storage.sas_logical_jbod_attachments import SasLogicalJbodAttachments
from hpOneView.resources.security.login_details import LoginDetails
from hpOneView.resources.networking.internal_link_sets import InternalLinkSets
from hpOneView.resources.search.index_resources import IndexResources
from hpOneView.resources.search.labels import Labels
from hpOneView.resources.uncategorized.os_deployment_plans import OsDeploymentPlans
from hpOneView.resources.uncategorized.os_deployment_servers import OsDeploymentServers
from hpOneView.resources.activity.alerts import Alerts
from hpOneView.resources.activity.events import Events
from hpOneView.resources.security.certificate_rabbitmq import CertificateRabbitMQ
from hpOneView.resources.security.roles import Roles
from hpOneView.resources.security.users import Users
from hpOneView.resources.settings.appliance_device_read_community import ApplianceDeviceReadCommunity
from hpOneView.resources.settings.appliance_device_snmp_v1_trap_destinations import ApplianceDeviceSNMPv1TrapDestinations
from hpOneView.resources.settings.appliance_device_snmp_v3_trap_destinations import ApplianceDeviceSNMPv3TrapDestinations
from hpOneView.resources.settings.appliance_device_snmp_v3_users import ApplianceDeviceSNMPv3Users
from hpOneView.resources.settings.appliance_node_information import ApplianceNodeInformation
from hpOneView.resources.settings.appliance_time_and_locale_configuration import ApplianceTimeAndLocaleConfiguration
from hpOneView.resources.settings.versions import Versions
from tests.test_utils import mock_builtin
from hpOneView.resources.settings.licenses import Licenses

OS_ENVIRON_CONFIG_MINIMAL = {
    'ONEVIEWSDK_IP': '172.16.100.199',
    'ONEVIEWSDK_USERNAME': 'admin',
    'ONEVIEWSDK_PASSWORD': 'secret123'
}

OS_ENVIRON_CONFIG_MINIMAL_WITH_SESSIONID = {
    'ONEVIEWSDK_IP': '172.16.100.199',
    'ONEVIEWSDK_SESSIONID': '123'
}

OS_ENVIRON_CONFIG_FULL = {
    'ONEVIEWSDK_IP': '172.16.100.199',
    'ONEVIEWSDK_IMAGE_STREAMER_IP': '172.172.172.172',
    'ONEVIEWSDK_USERNAME': 'admin',
    'ONEVIEWSDK_PASSWORD': 'secret123',
    'ONEVIEWSDK_API_VERSION': '201',
    'ONEVIEWSDK_AUTH_LOGIN_DOMAIN': 'authdomain',
    'ONEVIEWSDK_PROXY': '172.16.100.195:9999',
    'ONEVIEWSDK_CONNECTION_TIMEOUT': '20'
}

OS_ENVIRON_CONFIG_FULL_WITH_SESSIONID = {
    'ONEVIEWSDK_IP': '172.16.100.199',
    'ONEVIEWSDK_IMAGE_STREAMER_IP': '172.172.172.172',
    'ONEVIEWSDK_USERNAME': 'admin',
    'ONEVIEWSDK_PASSWORD': 'secret123',
    'ONEVIEWSDK_SESSIONID': '123',
    'ONEVIEWSDK_API_VERSION': '201',
    'ONEVIEWSDK_PROXY': '172.16.100.195:9999',
    'ONEVIEWSDK_CONNECTION_TIMEOUT': '20'

}


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
    def test_from_json_file_with_sessionID(self, mock_open, mock_login):
        json_config_content = u"""{
          "ip": "172.16.102.59",
          "credentials": {
            "userName": "administrator",
            "authLoginDomain": "",
            "password": "",
            "sessionID": "123"
          }
        }"""
        mock_open.return_value = self.__mock_file_open(json_config_content)
        oneview_client = OneViewClient.from_json_file("config.json")

        self.assertIsInstance(oneview_client, OneViewClient)
        self.assertEqual("172.16.102.59", oneview_client.connection.get_host())

    @mock.patch.object(connection, 'login')
    @mock.patch(mock_builtin('open'))
    def test_from_json_file_with_only_sessionID(self, mock_open, mock_login):
        json_config_content = u"""{
          "ip": "172.16.102.59",
          "credentials": {
            "sessionID": "123"
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

        self.assertEqual(300, oneview_client.connection._apiVersion)
        self.assertEqual(300, oneview_client.api_version)

    @mock.patch.object(connection, 'login')
    @mock.patch(mock_builtin('open'))
    def test_configured_api_version(self, mock_open, mock_login):
        json_config_content = u"""{
          "ip": "172.16.102.59",
          "api_version": 200,
          "credentials": {
            "userName": "administrator",
            "authLoginDomain": "",
            "password": ""
          }
        }"""
        mock_open.return_value = self.__mock_file_open(json_config_content)
        oneview_client = OneViewClient.from_json_file("config.json")

        self.assertEqual(200, oneview_client.connection._apiVersion)
        self.assertEqual(200, oneview_client.api_version)

    @mock.patch.object(connection, 'login')
    @mock.patch.object(connection, 'set_proxy')
    @mock.patch.dict('os.environ', OS_ENVIRON_CONFIG_MINIMAL)
    def test_from_minimal_environment_variables(self, mock_set_proxy, mock_login):
        oneview_client = OneViewClient.from_environment_variables()

        mock_login.assert_called_once_with(dict(userName='admin',
                                                password='secret123',
                                                authLoginDomain='',
                                                sessionID=''))
        mock_set_proxy.assert_not_called()
        self.assertEqual(300, oneview_client.connection._apiVersion)

    @mock.patch.object(connection, 'login')
    @mock.patch.object(connection, 'set_proxy')
    @mock.patch.dict('os.environ', OS_ENVIRON_CONFIG_MINIMAL_WITH_SESSIONID)
    def test_from_minimal_environment_variables_with_sessionID(self, mock_set_proxy, mock_login):
        oneview_client = OneViewClient.from_environment_variables()

        mock_login.assert_called_once_with(dict(userName='',
                                                password='',
                                                authLoginDomain='',
                                                sessionID='123'))
        mock_set_proxy.assert_not_called()
        self.assertEqual(300, oneview_client.connection._apiVersion)

    @mock.patch.object(connection, 'login')
    @mock.patch.object(connection, 'set_proxy')
    @mock.patch.dict('os.environ', OS_ENVIRON_CONFIG_FULL)
    def test_from_full_environment_variables(self, mock_set_proxy, mock_login):
        oneview_client = OneViewClient.from_environment_variables()

        mock_login.assert_called_once_with(dict(userName='admin',
                                                password='secret123',
                                                authLoginDomain='authdomain',
                                                sessionID=''))
        mock_set_proxy.assert_called_once_with('172.16.100.195', 9999)

        self.assertEqual(201, oneview_client.connection._apiVersion)
        self.assertEqual(oneview_client.create_image_streamer_client().connection.get_host(),
                         OS_ENVIRON_CONFIG_FULL['ONEVIEWSDK_IMAGE_STREAMER_IP'])

    @mock.patch.object(connection, 'login')
    @mock.patch.object(connection, 'set_proxy')
    @mock.patch.dict('os.environ', OS_ENVIRON_CONFIG_FULL_WITH_SESSIONID)
    def test_from_full_environment_variables_with_sessionID(self, mock_set_proxy, mock_login):
        oneview_client = OneViewClient.from_environment_variables()

        mock_login.assert_called_once_with(dict(userName='admin',
                                                password='secret123',
                                                authLoginDomain='',
                                                sessionID='123'))
        mock_set_proxy.assert_called_once_with('172.16.100.195', 9999)

        self.assertEqual(201, oneview_client.connection._apiVersion)
        self.assertEqual(oneview_client.create_image_streamer_client().connection.get_host(),
                         OS_ENVIRON_CONFIG_FULL_WITH_SESSIONID['ONEVIEWSDK_IMAGE_STREAMER_IP'])

    @mock.patch.dict('os.environ', OS_ENVIRON_CONFIG_FULL)
    @mock.patch.object(OneViewClient, '__init__')
    def test_from_environment_variables_is_passing_right_arguments_to_the_constructor(self, mock_cls):
        mock_cls.return_value = None
        OneViewClient.from_environment_variables()
        mock_cls.assert_called_once_with({'api_version': 201,
                                          'proxy': '172.16.100.195:9999',
                                          'timeout': '20',
                                          'ip': '172.16.100.199',
                                          'ssl_certificate': '',
                                          'image_streamer_ip': '172.172.172.172',
                                          'credentials':
                                              {'userName': 'admin',
                                               'password': 'secret123',
                                               'authLoginDomain': 'authdomain',
                                               'sessionID': ''}})

    @mock.patch.dict('os.environ', OS_ENVIRON_CONFIG_FULL_WITH_SESSIONID)
    @mock.patch.object(OneViewClient, '__init__')
    def test_from_environment_variables_is_passing_right_arguments_to_the_constructor_with_sessionID(self, mock_cls):
        mock_cls.return_value = None
        OneViewClient.from_environment_variables()
        mock_cls.assert_called_once_with({'api_version': 201,
                                          'proxy': '172.16.100.195:9999',
                                          'timeout': '20',
                                          'ip': '172.16.100.199',
                                          'image_streamer_ip': '172.172.172.172',
                                          'ssl_certificate': '',
                                          'credentials':
                                              {'userName': 'admin',
                                               'password': 'secret123',
                                               'authLoginDomain': '',
                                               'sessionID': '123'}})

    @mock.patch.dict('os.environ', OS_ENVIRON_CONFIG_MINIMAL_WITH_SESSIONID)
    @mock.patch.object(OneViewClient, '__init__')
    def test_from_environment_variables_is_passing_right_arguments_to_the_constructor_with_only_sessionID(self, mock_cls):
        mock_cls.return_value = None
        OneViewClient.from_environment_variables()
        mock_cls.assert_called_once_with({'api_version': 300,
                                          'proxy': '',
                                          'timeout': None,
                                          'ip': '172.16.100.199',
                                          'image_streamer_ip': '',
                                          'ssl_certificate': '',
                                          'credentials':
                                              {'userName': '',
                                               'password': '',
                                               'authLoginDomain': '',
                                               'sessionID': '123'}})

    @mock.patch.object(connection, 'login')
    def test_create_image_streamer_client_without_image_streamer_ip(self, mock_login):

        config = {"ip": "172.16.102.59",
                  "credentials": {
                      "userName": "administrator",
                      "password": "password"}}

        client = OneViewClient(config)
        client.connection.set_session_id('123')

        i3s = client.create_image_streamer_client()

        self.assertEqual(i3s.connection.get_session_id(), client.connection.get_session_id())
        self.assertEqual(i3s.connection._apiVersion, client.api_version)
        self.assertEqual(i3s.connection.get_host(), None)
        self.assertEqual(client.connection.get_host(), "172.16.102.59")

    @mock.patch.object(connection, 'login')
    def test_create_image_streamer_client_with_image_streamer_ip(self, mock_login):

        config = {"ip": "172.16.102.59",
                  "image_streamer_ip": "172.16.102.50",
                  "credentials": {
                      "userName": "administrator",
                      "password": "password"}}

        client = OneViewClient(config)
        client.connection.set_session_id('124')

        i3s = client.create_image_streamer_client()

        self.assertEqual(i3s.connection.get_session_id(), client.connection.get_session_id())
        self.assertEqual(i3s.connection._apiVersion, client.api_version)
        self.assertEqual(i3s.connection.get_host(), "172.16.102.50")
        self.assertEqual(client.connection.get_host(), "172.16.102.59")

    def test_fc_networks_has_right_type(self):
        self.assertIsInstance(self._oneview.fc_networks, FcNetworks)

    def test_fc_networks_has_value(self):
        self.assertIsNotNone(self._oneview.fc_networks)

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

    def test_should_return_new_connection_templates_obj(self):
        self.assertNotEqual(self._oneview.connection_templates, self._oneview.connection_templates)

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

    def test_lazy_loading_switches(self):
        switches = self._oneview.switches
        self.assertEqual(switches, self._oneview.switches)

    def test_should_return_new_ethernet_networks_obj(self):
        self.assertNotEqual(self._oneview.ethernet_networks, self._oneview.ethernet_networks)

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

    def test_sas_interconnect_types_has_right_type(self):
        self.assertIsInstance(self._oneview.sas_interconnect_types, SasInterconnectTypes)

    def test_lazy_loading_sas_interconnect_types(self):
        sas_interconnect_types = self._oneview.sas_interconnect_types
        self.assertEqual(sas_interconnect_types, self._oneview.sas_interconnect_types)

    def test_interconnects_has_right_type(self):
        self.assertIsInstance(self._oneview.interconnects, Interconnects)

    def test_interconnects_has_value(self):
        self.assertIsNotNone(self._oneview.interconnects)

    def test_lazy_loading_interconnects(self):
        interconnects = self._oneview.interconnects
        self.assertEqual(interconnects, self._oneview.interconnects)

    def test_certificate_authority_has_right_type(self):
        self.assertIsInstance(self._oneview.certificate_authority, CertificateAuthority)

    def test_certificate_authority_has_value(self):
        self.assertIsNotNone(self._oneview.certificate_authority)

    def test_lazy_loading_certificate_authority(self):
        certificates = self._oneview.certificate_authority
        self.assertEqual(certificates, self._oneview.certificate_authority)

    def test_lazy_loading_connections(self):
        connections = self._oneview.connections
        self.assertEqual(connections, self._oneview.connections)

    def test_lazy_loading_server_hardware_types(self):
        server_hardware_types = self._oneview.server_hardware_types
        self.assertEqual(server_hardware_types, self._oneview.server_hardware_types)

    def test_lazy_loading_id_pools_vsn_ranges(self):
        id_pools_vsn_ranges = self._oneview.id_pools_vsn_ranges
        self.assertEqual(id_pools_vsn_ranges, self._oneview.id_pools_vsn_ranges)

    def test_id_pools_vsn_ranges_has_right_type(self):
        self.assertIsInstance(self._oneview.id_pools_vsn_ranges, IdPoolsRanges)

    def test_id_pools_vsn_ranges_has_right_value(self):
        self.assertEqual('/rest/id-pools/vsn/ranges', self._oneview.id_pools_vsn_ranges._client._uri)

    def test_lazy_loading_id_pools_vmac_ranges(self):
        id_pools_vmac_ranges = self._oneview.id_pools_vmac_ranges
        self.assertEqual(id_pools_vmac_ranges, self._oneview.id_pools_vmac_ranges)

    def test_id_pools_vmac_ranges_has_right_type(self):
        self.assertIsInstance(self._oneview.id_pools_vmac_ranges, IdPoolsRanges)

    def test_id_pools_vmac_ranges_has_right_value(self):
        self.assertEqual('/rest/id-pools/vmac/ranges', self._oneview.id_pools_vmac_ranges._client._uri)

    def test_lazy_loading_id_pools_vwwn_ranges(self):
        id_pools_vwwn_ranges = self._oneview.id_pools_vwwn_ranges
        self.assertEqual(id_pools_vwwn_ranges, self._oneview.id_pools_vwwn_ranges)

    def test_id_pools_vwwn_ranges_has_right_type(self):
        self.assertIsInstance(self._oneview.id_pools_vwwn_ranges, IdPoolsRanges)

    def test_id_pools_vwwn_ranges_has_right_value(self):
        self.assertEqual('/rest/id-pools/vwwn/ranges', self._oneview.id_pools_vwwn_ranges._client._uri)

    def test_id_pools_ipv4_ranges_has_right_type(self):
        self.assertIsInstance(self._oneview.id_pools_ipv4_ranges, IdPoolsIpv4Ranges)

    def test_id_pools_ipv4_ranges_lazy_loading(self):
        id_pools_ipv4_ranges = self._oneview.id_pools_ipv4_ranges
        self.assertEqual(id_pools_ipv4_ranges, self._oneview.id_pools_ipv4_ranges)

    def test_id_pools_ipv4_subnets_has_right_type(self):
        self.assertIsInstance(self._oneview.id_pools_ipv4_subnets, IdPoolsIpv4Subnets)

    def test_id_pools_ipv4_subnets_lazy_loading(self):
        id_pools_ipv4_subnets = self._oneview.id_pools_ipv4_subnets
        self.assertEqual(id_pools_ipv4_subnets, self._oneview.id_pools_ipv4_subnets)

    def test_id_pools_has_right_type(self):
        self.assertIsInstance(self._oneview.id_pools, IdPools)

    def test_id_pools_lazy_loading(self):
        id_pools = self._oneview.id_pools
        self.assertEqual(id_pools, self._oneview.id_pools)

    def test_lazy_loading_logical_enclosures(self):
        logical_enclosures = self._oneview.logical_enclosures
        self.assertEqual(logical_enclosures, self._oneview.logical_enclosures)

    def test_should_return_new_interconnect_types_obj(self):
        self.assertNotEqual(self._oneview.interconnect_types, self._oneview.interconnect_types)

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

    def test_migratable_vc_domains_has_right_type(self):
        self.assertIsInstance(self._oneview.migratable_vc_domains, MigratableVcDomains)

    def test_migratable_vc_domains_lazy_loading(self):
        migratable_vc_domains = self._oneview.migratable_vc_domains
        self.assertEqual(migratable_vc_domains, self._oneview.migratable_vc_domains)

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

    def test_roles_has_right_type(self):
        self.assertIsInstance(self._oneview.roles, Roles)

    def test_roles_lazy_loading(self):
        roles = self._oneview.roles
        self.assertEqual(roles, self._oneview.roles)

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

    def test_logical_switch_groups_return(self):
        self.assertNotEqual(self._oneview.logical_switch_groups,
                            self._oneview.logical_switch_groups)

    def test_logical_switches_has_right_type(self):
        self.assertIsInstance(self._oneview.logical_switches, LogicalSwitches)

    def test_lazy_loading_logical_switches(self):
        logical_switches = self._oneview.logical_switches
        self.assertEqual(logical_switches, self._oneview.logical_switches)

    def test_logical_interconnects_has_right_type(self):
        self.assertIsInstance(self._oneview.logical_interconnects, LogicalInterconnects)

    def test_logical_interconnects_has_value(self):
        self.assertIsNotNone(self._oneview.logical_interconnects)

    def test_logical_interconnects_return(self):
        self.assertNotEqual(self._oneview.logical_interconnects,
                            self._oneview.logical_interconnects)

    def test_sas_logical_interconnects_has_right_type(self):
        self.assertIsInstance(self._oneview.sas_logical_interconnects, SasLogicalInterconnects)

    def test_lazy_loading_sas_logical_interconnects(self):
        sas_logical_interconnects = self._oneview.sas_logical_interconnects
        self.assertEqual(sas_logical_interconnects, self._oneview.sas_logical_interconnects)

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

    def test_should_return_new_uplink_sets_obj(self):
        self.assertNotEqual(self._oneview.uplink_sets, self._oneview.uplink_sets)

    def test_uplink_sets_has_right_type(self):
        self.assertIsInstance(self._oneview.uplink_sets, UplinkSets)

    def test_uplink_sets_has_value(self):
        self.assertIsNotNone(self._oneview.uplink_sets)

    def test_backups_has_right_type(self):
        self.assertIsInstance(self._oneview.backups, Backups)

    def test_lazy_loading_backups(self):
        copy_backups = self._oneview.backups
        self.assertEqual(copy_backups, self._oneview.backups)

    def test_restores_has_right_type(self):
        self.assertIsInstance(self._oneview.restores, Restores)

    def test_lazy_loading_restores(self):
        copy_restores = self._oneview.restores
        self.assertEqual(copy_restores, self._oneview.restores)

    def test_scopes_has_right_type(self):
        self.assertIsInstance(self._oneview.scopes, Scopes)

    def test_lazy_loading_scopes(self):
        copy_scopes = self._oneview.scopes
        self.assertEqual(copy_scopes, self._oneview.scopes)

    def test_sas_logical_interconnect_groups_has_right_type(self):
        self.assertIsInstance(self._oneview.sas_logical_interconnect_groups, SasLogicalInterconnectGroups)

    def test_lazy_loading_sas_logical_interconnect_groups(self):
        sas_logical_interconnect_groups = self._oneview.sas_logical_interconnect_groups
        self.assertEqual(sas_logical_interconnect_groups, self._oneview.sas_logical_interconnect_groups)

    def test_login_details_has_right_type(self):
        self.assertIsInstance(self._oneview.login_details, LoginDetails)

    def test_lazy_loading_login_details(self):
        login_details = self._oneview.login_details
        self.assertEqual(login_details, self._oneview.login_details)

    def test_licenses_has_right_type(self):
        self.assertIsInstance(self._oneview.licenses, Licenses)

    def test_unmanaged_devices_has_right_type(self):
        self.assertIsInstance(self._oneview.unmanaged_devices, UnmanagedDevices)

    def test_volumes_has_right_type(self):
        self.assertIsInstance(self._oneview.volumes, Volumes)

    def test_volumes_has_value(self):
        self.assertIsNotNone(self._oneview.volumes)

    def test_lazy_loading_volumes(self):
        copy_volumes = self._oneview.volumes
        self.assertEqual(copy_volumes, self._oneview.volumes)

    def test_sas_logical_jbod_attachments_right_type(self):
        self.assertIsInstance(self._oneview.sas_logical_jbod_attachments, SasLogicalJbodAttachments)

    def test_lazy_loading_sas_logical_jbod_attachments(self):
        sas_logical_jbod_attachments = self._oneview.sas_logical_jbod_attachments
        self.assertEqual(sas_logical_jbod_attachments, self._oneview.sas_logical_jbod_attachments)

    def test_server_profile_templates_has_right_type(self):
        self.assertIsInstance(self._oneview.server_profile_templates, ServerProfileTemplate)

    def test_server_profile_templates_has_value(self):
        self.assertIsNotNone(self._oneview.server_profile_templates)

    def test_server_profile_templates_return(self):
        self.assertNotEqual(self._oneview.server_profile_templates,
                            self._oneview.server_profile_templates)

    def test_server_profiles_has_right_type(self):
        self.assertIsInstance(self._oneview.server_profiles, ServerProfiles)

    def test_server_profiles_has_value(self):
        self.assertIsNotNone(self._oneview.server_profiles)

    def test_server_profiles_return(self):
        self.assertNotEqual(self._oneview.server_profiles,
                            self._oneview.server_profiles)

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

    def test_sas_interconnects_has_right_type(self):
        self.assertIsInstance(self._oneview.sas_interconnects, SasInterconnects)

    def test_lazy_loading_sas_interconnects(self):
        sas_interconnects = self._oneview.sas_interconnects
        self.assertEqual(sas_interconnects, self._oneview.sas_interconnects)

    def test_drive_enclosure_has_right_type(self):
        self.assertIsInstance(self._oneview.drive_enclosures, DriveEnclosures)

    def test_lazy_loading_drive_enclosure(self):
        drive_enclosures = self._oneview.drive_enclosures
        self.assertEqual(drive_enclosures, self._oneview.drive_enclosures)

    def test_sas_logical_jbods_has_right_type(self):
        self.assertIsInstance(self._oneview.sas_logical_jbods, SasLogicalJbods)

    def test_lazy_loading_sas_logical_jbods(self):
        sas_logical_jbods = self._oneview.sas_logical_jbods
        self.assertEqual(sas_logical_jbods, self._oneview.sas_logical_jbods)

    def test_internal_link_sets_has_right_type(self):
        self.assertIsInstance(self._oneview.internal_link_sets, InternalLinkSets)

    def test_lazy_loading_internal_link_sets(self):
        internal_links = self._oneview.internal_link_sets
        self.assertEqual(internal_links, self._oneview.internal_link_sets)

    def test_index_resources_has_right_type(self):
        self.assertIsInstance(self._oneview.index_resources, IndexResources)

    def test_lazy_loading_index_resources(self):
        index_resources = self._oneview.index_resources
        self.assertEqual(index_resources, self._oneview.index_resources)

    def test_labels_has_right_type(self):
        self.assertIsInstance(self._oneview.labels, Labels)

    def test_lazy_loading_labels(self):
        labels = self._oneview.labels
        self.assertEqual(labels, self._oneview.labels)

    def test_alerts_has_right_type(self):
        self.assertIsInstance(self._oneview.alerts, Alerts)

    def test_lazy_loading_alerts(self):
        alerts = self._oneview.alerts
        self.assertEqual(alerts, self._oneview.alerts)

    def test_events_has_right_type(self):
        self.assertIsInstance(self._oneview.events, Events)

    def test_lazy_loading_events(self):
        events = self._oneview.events
        self.assertEqual(events, self._oneview.events)

    def test_os_deployment_plans_has_right_type(self):
        self.assertIsInstance(self._oneview.os_deployment_plans, OsDeploymentPlans)

    def test_os_deployment_plans_return(self):
        self.assertNotEqual(self._oneview.os_deployment_plans,
                            self._oneview.os_deployment_plans)

    def test_os_deployment_servers_has_right_type(self):
        self.assertIsInstance(self._oneview.os_deployment_servers, OsDeploymentServers)

    def test_lazy_loading_os_deployment_servers(self):
        os_deployment_servers = self._oneview.os_deployment_servers
        self.assertEqual(os_deployment_servers, self._oneview.os_deployment_servers)

    def test_certificate_rabbitmq_has_right_type(self):
        self.assertIsInstance(self._oneview.certificate_rabbitmq, CertificateRabbitMQ)

    def test_lazy_loading_certificate_rabbitmq(self):
        certificate_rabbitmq = self._oneview.certificate_rabbitmq
        self.assertEqual(certificate_rabbitmq, self._oneview.certificate_rabbitmq)

    def test_users_has_right_type(self):
        self.assertIsInstance(self._oneview.users, Users)

    def test_lazy_loading_users(self):
        user = self._oneview.users
        self.assertEqual(user, self._oneview.users)

    def test_appliance_device_read_community_has_right_type(self):
        self.assertIsInstance(self._oneview.appliance_device_read_community,
                              ApplianceDeviceReadCommunity)

    def test_lazy_loading_appliance_device_read_community(self):
        appliance_device_read_community = self._oneview.appliance_device_read_community
        self.assertEqual(appliance_device_read_community, self._oneview.appliance_device_read_community)

    def test_appliance_device_device_snmp_v1_trap_destinations_has_right_type(self):
        self.assertIsInstance(self._oneview.appliance_device_snmp_v1_trap_destinations,
                              ApplianceDeviceSNMPv1TrapDestinations)

    def test_lazy_loading_appliance_device_device_snmp_v1_trap_destinations(self):
        appliance_device_snmp_v1_trap_destinations = self._oneview.appliance_device_snmp_v1_trap_destinations
        self.assertEqual(appliance_device_snmp_v1_trap_destinations, self._oneview.appliance_device_snmp_v1_trap_destinations)

    def test_appliance_device_device_snmp_v3_trap_destinations_has_right_type(self):
        self.assertIsInstance(self._oneview.appliance_device_snmp_v3_trap_destinations,
                              ApplianceDeviceSNMPv3TrapDestinations)

    def test_lazy_loading_appliance_device_device_snmp_v3_trap_destinations(self):
        appliance_device_snmp_v3_trap_destinations = self._oneview.appliance_device_snmp_v3_trap_destinations
        self.assertEqual(appliance_device_snmp_v3_trap_destinations, self._oneview.appliance_device_snmp_v3_trap_destinations)

    def test_appliance_device_device_snmp_v3_users_has_right_type(self):
        self.assertIsInstance(self._oneview.appliance_device_snmp_v3_users,
                              ApplianceDeviceSNMPv3Users)

    def test_lazy_loading_appliance_device_device_snmp_v3_users(self):
        appliance_device_snmp_v3_users = self._oneview.appliance_device_snmp_v3_users
        self.assertEqual(appliance_device_snmp_v3_users, self._oneview.appliance_device_snmp_v3_users)

    def test_appliance_node_information_has_right_type(self):
        self.assertIsInstance(self._oneview.appliance_node_information,
                              ApplianceNodeInformation)

    def test_lazy_loading_appliance_node_information(self):
        appliance_node_information = self._oneview.appliance_node_information
        self.assertEqual(appliance_node_information, self._oneview.appliance_node_information)

    def test_appliance_time_and_locale_configuration_has_right_type(self):
        self.assertIsInstance(self._oneview.appliance_time_and_locale_configuration,
                              ApplianceTimeAndLocaleConfiguration)

    def test_lazy_loading_appliance_time_and_locale_configuration(self):
        appliance_time_and_locale_configuration = self._oneview.appliance_time_and_locale_configuration
        self.assertEqual(appliance_time_and_locale_configuration, self._oneview.appliance_time_and_locale_configuration)

    def test_should_get_appliance_current_version_and_minimum_version(self):
        self.assertIsInstance(self._oneview.versions,
                              Versions)

    def test_lazy_loading_appliance_version_information(self):
        versions = self._oneview.versions
        self.assertEqual(versions, self._oneview.versions)
