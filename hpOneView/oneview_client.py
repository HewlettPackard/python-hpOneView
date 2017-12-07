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
"""
This module implements a common client for HPE OneView REST API.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

import json
import os

from hpOneView.connection import connection
from hpOneView.image_streamer.image_streamer_client import ImageStreamerClient
from hpOneView.resources.security.certificate_authority import CertificateAuthority
from hpOneView.resources.servers.connections import Connections
from hpOneView.resources.networking.fc_networks import FcNetworks
from hpOneView.resources.networking.fcoe_networks import FcoeNetworks
from hpOneView.resources.networking.ethernet_networks import EthernetNetworks
from hpOneView.resources.networking.connection_templates import ConnectionTemplates
from hpOneView.resources.networking.fabrics import Fabrics
from hpOneView.resources.networking.network_sets import NetworkSets
from hpOneView.resources.data_services.metric_streaming import MetricStreaming
from hpOneView.resources.networking.switches import Switches
from hpOneView.resources.networking.switch_types import SwitchTypes
from hpOneView.resources.activity.tasks import Tasks
from hpOneView.resources.settings.restores import Restores
from hpOneView.resources.settings.scopes import Scopes
from hpOneView.resources.servers.enclosures import Enclosures
from hpOneView.resources.servers.logical_enclosures import LogicalEnclosures
from hpOneView.resources.servers.enclosure_groups import EnclosureGroups
from hpOneView.resources.servers.server_hardware import ServerHardware
from hpOneView.resources.servers.server_hardware_types import ServerHardwareTypes
from hpOneView.resources.servers.id_pools_ranges import IdPoolsRanges
from hpOneView.resources.servers.id_pools_ipv4_ranges import IdPoolsIpv4Ranges
from hpOneView.resources.servers.id_pools_ipv4_subnets import IdPoolsIpv4Subnets
from hpOneView.resources.servers.id_pools import IdPools
from hpOneView.resources.networking.interconnects import Interconnects
from hpOneView.resources.networking.interconnect_types import InterconnectTypes
from hpOneView.resources.networking.interconnect_link_topologies import InterconnectLinkTopologies
from hpOneView.resources.networking.sas_interconnect_types import SasInterconnectTypes
from hpOneView.resources.networking.internal_link_sets import InternalLinkSets
from hpOneView.resources.uncategorized.unmanaged_devices import UnmanagedDevices
from hpOneView.resources.networking.logical_downlinks import LogicalDownlinks
from hpOneView.resources.facilities.power_devices import PowerDevices
from hpOneView.resources.facilities.racks import Racks
from hpOneView.resources.facilities.datacenters import Datacenters
from hpOneView.resources.fc_sans.managed_sans import ManagedSANs
from hpOneView.resources.fc_sans.san_managers import SanManagers
from hpOneView.resources.fc_sans.endpoints import Endpoints
from hpOneView.resources.networking.logical_interconnects import LogicalInterconnects
from hpOneView.resources.networking.logical_interconnect_groups import LogicalInterconnectGroups
from hpOneView.resources.networking.sas_logical_interconnects import SasLogicalInterconnects
from hpOneView.resources.networking.logical_switch_groups import LogicalSwitchGroups
from hpOneView.resources.networking.logical_switches import LogicalSwitches
from hpOneView.resources.networking.sas_interconnects import SasInterconnects
from hpOneView.resources.servers.server_profiles import ServerProfiles
from hpOneView.resources.servers.server_profile_templates import ServerProfileTemplate
from hpOneView.resources.storage.sas_logical_jbods import SasLogicalJbods
from hpOneView.resources.storage.storage_systems import StorageSystems
from hpOneView.resources.storage.storage_pools import StoragePools
from hpOneView.resources.storage.storage_volume_templates import StorageVolumeTemplates
from hpOneView.resources.storage.storage_volume_attachments import StorageVolumeAttachments
from hpOneView.resources.storage.drive_enclosures import DriveEnclosures
from hpOneView.resources.settings.firmware_drivers import FirmwareDrivers
from hpOneView.resources.settings.firmware_bundles import FirmwareBundles
from hpOneView.resources.settings.backups import Backups
from hpOneView.resources.storage.volumes import Volumes
from hpOneView.resources.storage.sas_logical_jbod_attachments import SasLogicalJbodAttachments
from hpOneView.resources.networking.uplink_sets import UplinkSets
from hpOneView.resources.servers.migratable_vc_domains import MigratableVcDomains
from hpOneView.resources.networking.sas_logical_interconnect_groups import SasLogicalInterconnectGroups
from hpOneView.resources.search.index_resources import IndexResources
from hpOneView.resources.search.labels import Labels
from hpOneView.resources.activity.alerts import Alerts
from hpOneView.resources.activity.events import Events
from hpOneView.resources.uncategorized.os_deployment_plans import OsDeploymentPlans
from hpOneView.resources.uncategorized.os_deployment_servers import OsDeploymentServers
from hpOneView.resources.security.certificate_rabbitmq import CertificateRabbitMQ
from hpOneView.resources.security.login_details import LoginDetails
from hpOneView.resources.security.roles import Roles
from hpOneView.resources.security.users import Users
from hpOneView.resources.settings.appliance_node_information import ApplianceNodeInformation
from hpOneView.resources.settings.appliance_time_and_locale_configuration import ApplianceTimeAndLocaleConfiguration
from hpOneView.resources.settings.versions import Versions

ONEVIEW_CLIENT_INVALID_PROXY = 'Invalid Proxy format'


class OneViewClient(object):
    DEFAULT_API_VERSION = 300

    def __init__(self, config):
        self.__connection = connection(config["ip"], config.get('api_version', self.DEFAULT_API_VERSION), config.get('ssl_certificate', False),
                                       config.get('timeout'))
        self.__image_streamer_ip = config.get("image_streamer_ip")
        self.__set_proxy(config)
        self.__connection.login(config["credentials"])
        self.__certificate_authority = None
        self.__connections = None
        self.__connection_templates = None
        self.__fc_networks = None
        self.__fcoe_networks = None
        self.__ethernet_networks = None
        self.__fabrics = None
        self.__network_sets = None
        self.__switches = None
        self.__switch_types = None
        self.__tasks = None
        self.__scopes = None
        self.__enclosures = None
        self.__logical_enclosures = None
        self.__enclosure_groups = None
        self.__metric_streaming = None
        self.__server_hardware = None
        self.__server_hardware_types = None
        self.__id_pools_vsn_ranges = None
        self.__id_pools_vmac_ranges = None
        self.__id_pools_vwwn_ranges = None
        self.__id_pools_ipv4_ranges = None
        self.__id_pools_ipv4_subnets = None
        self.__id_pools = None
        self.__interconnects = None
        self.__interconnect_types = None
        self.__interconnect_link_topologies = None
        self.__sas_interconnect_types = None
        self.__internal_link_sets = None
        self.__power_devices = None
        self.__unmanaged_devices = None
        self.__racks = None
        self.__roles = None
        self.__datacenters = None
        self.__san_managers = None
        self.__endpoints = None
        self.__logical_interconnects = None
        self.__sas_logical_interconnects = None
        self.__logical_interconnect_groups = None
        self.__logical_switch_groups = None
        self.__logical_switches = None
        self.__logical_downlinks = None
        self.__restores = None
        self.__server_profiles = None
        self.__server_profile_templates = None
        self.__sas_logical_jbods = None
        self.__storage_systems = None
        self.__storage_pools = None
        self.__storage_volume_templates = None
        self.__storage_volume_attachments = None
        self.__firmware_drivers = None
        self.__firmware_bundles = None
        self.__uplink_sets = None
        self.__volumes = None
        self.__sas_logical_jbod_attachments = None
        self.__managed_sans = None
        self.__migratable_vc_domains = None
        self.__sas_interconnects = None
        self.__index_resources = None
        self.__labels = None
        self.__sas_logical_interconnect_groups = None
        self.__alerts = None
        self.__events = None
        self.__drive_enclures = None
        self.__os_deployment_plans = None
        self.__os_deployment_servers = None
        self.__certificate_rabbitmq = None
        self.__users = None
        self.__appliance_time_and_locale_configuration = None
        self.__appliance_node_information = None
        self.__versions = None
        self.__backups = None
        self.__login_details = None

    @classmethod
    def from_json_file(cls, file_name):
        """
        Construct OneViewClient using a json file.

        Args:
            file_name: json full path.

        Returns:
            OneViewClient:
        """
        with open(file_name) as json_data:
            config = json.load(json_data)

        return cls(config)

    @classmethod
    def from_environment_variables(cls):
        """
        Construct OneViewClient using environment variables.

        Allowed variables: ONEVIEWSDK_IP (required), ONEVIEWSDK_USERNAME (required), ONEVIEWSDK_PASSWORD (required),
        ONEVIEWSDK_AUTH_LOGIN_DOMAIN, ONEVIEWSDK_API_VERSION, ONEVIEWSDK_IMAGE_STREAMER_IP, ONEVIEWSDK_SESSIONID, ONEVIEWSDK_SSL_CERTIFICATE,
        ONEVIEWSDK_CONNECTION_TIMEOUT and ONEVIEWSDK_PROXY.

        Returns:
            OneViewClient:
        """
        ip = os.environ.get('ONEVIEWSDK_IP', '')
        image_streamer_ip = os.environ.get('ONEVIEWSDK_IMAGE_STREAMER_IP', '')
        api_version = int(os.environ.get('ONEVIEWSDK_API_VERSION', OneViewClient.DEFAULT_API_VERSION))
        ssl_certificate = os.environ.get('ONEVIEWSDK_SSL_CERTIFICATE', '')
        username = os.environ.get('ONEVIEWSDK_USERNAME', '')
        auth_login_domain = os.environ.get('ONEVIEWSDK_AUTH_LOGIN_DOMAIN', '')
        password = os.environ.get('ONEVIEWSDK_PASSWORD', '')
        proxy = os.environ.get('ONEVIEWSDK_PROXY', '')
        sessionID = os.environ.get('ONEVIEWSDK_SESSIONID', '')
        timeout = os.environ.get('ONEVIEWSDK_CONNECTION_TIMEOUT')

        config = dict(ip=ip,
                      image_streamer_ip=image_streamer_ip,
                      api_version=api_version,
                      ssl_certificate=ssl_certificate,
                      credentials=dict(userName=username, authLoginDomain=auth_login_domain, password=password, sessionID=sessionID),
                      proxy=proxy, timeout=timeout)

        return cls(config)

    def __set_proxy(self, config):
        """
        Set proxy if needed
        Args:
            config: Config dict
        """
        if "proxy" in config and config["proxy"]:
            proxy = config["proxy"]
            splitted = proxy.split(':')
            if len(splitted) != 2:
                raise ValueError(ONEVIEW_CLIENT_INVALID_PROXY)

            proxy_host = splitted[0]
            proxy_port = int(splitted[1])
            self.__connection.set_proxy(proxy_host, proxy_port)

    @property
    def api_version(self):
        """
        Gets the OneView API Version.

        Returns:
            int: API Version.
        """
        return self.__connection._apiVersion

    @property
    def connection(self):
        """
        Gets the underlying HPE OneView connection used by the OneViewClient.

        Returns:
            connection:
        """
        return self.__connection

    def create_image_streamer_client(self):
        """
        Create the Image Streamer API Client.

        Returns:
            ImageStreamerClient:
        """
        image_streamer = ImageStreamerClient(self.__image_streamer_ip,
                                             self.__connection.get_session_id(),
                                             self.__connection._apiVersion,
                                             self.__connection._sslBundle)

        return image_streamer

    @property
    def certificate_authority(self):
        """
        Gets the Certificate Authority API client.

        Returns:
            CertificateAuthority:
        """
        if not self.__certificate_authority:
            self.__certificate_authority = CertificateAuthority(self.__connection)
        return self.__certificate_authority

    @property
    def connections(self):
        """
        Gets the Connections API client.

        Returns:
            Connections:
        """
        if not self.__connections:
            self.__connections = Connections(
                self.__connection)
        return self.__connections

    @property
    def connection_templates(self):
        """
        Gets the ConnectionTemplates API client.

        Returns:
            ConnectionTemplates:
        """
        if not self.__connection_templates:
            self.__connection_templates = ConnectionTemplates(
                self.__connection)
        return self.__connection_templates

    @property
    def fc_networks(self):
        """
        Gets the FcNetworks API client.

        Returns:
            FcNetworks:
        """
        if not self.__fc_networks:
            self.__fc_networks = FcNetworks(self.__connection)
        return self.__fc_networks

    @property
    def fcoe_networks(self):
        """
        Gets the FcoeNetworks API client.

        Returns:
            FcoeNetworks:
        """
        if not self.__fcoe_networks:
            self.__fcoe_networks = FcoeNetworks(self.__connection)
        return self.__fcoe_networks

    @property
    def ethernet_networks(self):
        """
        Gets the EthernetNetworks API client.

        Returns:
            EthernetNetworks:
        """
        if not self.__ethernet_networks:
            self.__ethernet_networks = EthernetNetworks(self.__connection)
        return self.__ethernet_networks

    @property
    def fabrics(self):
        """
        Gets the Fabrics API client.

        Returns:
            Fabrics:
        """
        if not self.__fabrics:
            self.__fabrics = Fabrics(self.__connection)
        return self.__fabrics

    @property
    def restores(self):
        """
        Gets the Restores API client.

        Returns:
            Restores:
        """
        if not self.__restores:
            self.__restores = Restores(self.__connection)
        return self.__restores

    @property
    def scopes(self):
        """
        Gets the Scopes API client.

        Returns:
            Scopes:
        """
        if not self.__scopes:
            self.__scopes = Scopes(self.__connection)
        return self.__scopes

    @property
    def datacenters(self):
        """
        Gets the Datacenters API client.

        Returns:
            Datacenters:
        """
        if not self.__datacenters:
            self.__datacenters = Datacenters(self.__connection)
        return self.__datacenters

    @property
    def network_sets(self):
        """
        Gets the NetworkSets API client.

        Returns:
            NetworkSets:
        """
        if not self.__network_sets:
            self.__network_sets = NetworkSets(self.__connection)
        return self.__network_sets

    @property
    def server_hardware(self):
        """
        Gets the ServerHardware API client.

        Returns:
            ServerHardware:
        """
        if not self.__server_hardware:
            self.__server_hardware = ServerHardware(self.__connection)
        return self.__server_hardware

    @property
    def server_hardware_types(self):
        """
        Gets the ServerHardwareTypes API client.

        Returns:
            ServerHardwareTypes:
        """
        if not self.__server_hardware_types:
            self.__server_hardware_types = ServerHardwareTypes(
                self.__connection)
        return self.__server_hardware_types

    @property
    def id_pools_vsn_ranges(self):
        """
        Gets the IdPoolsRanges API Client for VSN Ranges.

        Returns:
            IdPoolsRanges:
        """
        if not self.__id_pools_vsn_ranges:
            self.__id_pools_vsn_ranges = IdPoolsRanges('vsn', self.__connection)
        return self.__id_pools_vsn_ranges

    @property
    def id_pools_vmac_ranges(self):
        """
        Gets the IdPoolsRanges API Client for VMAC Ranges.

        Returns:
            IdPoolsRanges:
        """
        if not self.__id_pools_vmac_ranges:
            self.__id_pools_vmac_ranges = IdPoolsRanges('vmac', self.__connection)
        return self.__id_pools_vmac_ranges

    @property
    def id_pools_vwwn_ranges(self):
        """
        Gets the IdPoolsRanges API Client for VWWN Ranges.

        Returns:
            IdPoolsRanges:
        """
        if not self.__id_pools_vwwn_ranges:
            self.__id_pools_vwwn_ranges = IdPoolsRanges('vwwn', self.__connection)
        return self.__id_pools_vwwn_ranges

    @property
    def id_pools_ipv4_ranges(self):
        """
        Gets the IdPoolsIpv4Ranges API client.

        Returns:
            IdPoolsIpv4Ranges:
        """
        if not self.__id_pools_ipv4_ranges:
            self.__id_pools_ipv4_ranges = IdPoolsIpv4Ranges(self.__connection)
        return self.__id_pools_ipv4_ranges

    @property
    def id_pools_ipv4_subnets(self):
        """
        Gets the IdPoolsIpv4Subnets API client.

        Returns:
            IdPoolsIpv4Subnets:
        """
        if not self.__id_pools_ipv4_subnets:
            self.__id_pools_ipv4_subnets = IdPoolsIpv4Subnets(self.__connection)
        return self.__id_pools_ipv4_subnets

    @property
    def id_pools(self):
        """
        Gets the IdPools API client.

        Returns:
            IdPools:
        """
        if not self.__id_pools:
            self.__id_pools = IdPools(self.__connection)
        return self.__id_pools

    @property
    def switches(self):
        """
        Gets the Switches API client.

        Returns:
            Switches:
        """
        if not self.__switches:
            self.__switches = Switches(self.__connection)
        return self.__switches

    @property
    def roles(self):
        """
        Gets the Roles API client.

        Returns:
            Roles:
        """
        if not self.__roles:
            self.__roles = Roles(self.__connection)
        return self.__roles

    @property
    def switch_types(self):
        """
        Gets the SwitchTypes API client.

        Returns:
            SwitchTypes:
        """
        if not self.__switch_types:
            self.__switch_types = SwitchTypes(self.__connection)
        return self.__switch_types

    @property
    def logical_switch_groups(self):
        """
        Gets the LogicalSwitchGroups API client.

        Returns:
            LogicalSwitchGroups:
        """
        if not self.__logical_switch_groups:
            self.__logical_switch_groups = LogicalSwitchGroups(self.__connection)
        return self.__logical_switch_groups

    @property
    def logical_switches(self):
        """
        Gets the LogicalSwitches API client.

        Returns:
            LogicalSwitches:
        """
        if not self.__logical_switches:
            self.__logical_switches = LogicalSwitches(self.__connection)
        return self.__logical_switches

    @property
    def tasks(self):
        """
        Gets the Tasks API client.

        Returns:
            Tasks:
        """
        if not self.__tasks:
            self.__tasks = Tasks(self.__connection)
        return self.__tasks

    @property
    def enclosure_groups(self):
        """
        Gets the EnclosureGroups API client.

        Returns:
            EnclosureGroups:
        """
        if not self.__enclosure_groups:
            self.__enclosure_groups = EnclosureGroups(self.__connection)
        return self.__enclosure_groups

    @property
    def enclosures(self):
        """
        Gets the Enclosures API client.

        Returns:
            Enclosures:
        """
        if not self.__enclosures:
            self.__enclosures = Enclosures(self.__connection)
        return self.__enclosures

    @property
    def logical_enclosures(self):
        """
        Gets the LogicalEnclosures API client.

        Returns:
            LogicalEnclosures:
        """
        if not self.__logical_enclosures:
            self.__logical_enclosures = LogicalEnclosures(self.__connection)
        return self.__logical_enclosures

    @property
    def metric_streaming(self):
        """
        Gets the MetricStreaming API client.

        Returns:
            MetricStreaming:
        """
        if not self.__metric_streaming:
            self.__metric_streaming = MetricStreaming(self.__connection)
        return self.__metric_streaming

    @property
    def interconnects(self):
        """
        Gets the Interconnects API client.

        Returns:
            Interconnects:
        """
        if not self.__interconnects:
            self.__interconnects = Interconnects(self.__connection)
        return self.__interconnects

    @property
    def interconnect_types(self):
        """
        Gets the InterconnectTypes API client.

        Returns:
            InterconnectTypes:
        """
        if not self.__interconnect_types:
            self.__interconnect_types = InterconnectTypes(self.__connection)
        return self.__interconnect_types

    @property
    def interconnect_link_topologies(self):
        """
        Gets the InterconnectLinkTopologies API client.

        Returns:
            InterconnectLinkTopologies:
        """
        if not self.__interconnect_link_topologies:
            self.__interconnect_link_topologies = InterconnectLinkTopologies(self.__connection)
        return self.__interconnect_link_topologies

    @property
    def sas_interconnect_types(self):
        """
        Gets the SasInterconnectTypes API client.

        Returns:
            SasInterconnectTypes:
        """
        if not self.__sas_interconnect_types:
            self.__sas_interconnect_types = SasInterconnectTypes(self.__connection)
        return self.__sas_interconnect_types

    @property
    def internal_link_sets(self):
        """
        Gets the InternalLinkSets API client.

        Returns:
            InternalLinkSets:
        """
        if not self.__internal_link_sets:
            self.__internal_link_sets = InternalLinkSets(self.__connection)
        return self.__internal_link_sets

    @property
    def logical_interconnect_groups(self):
        """
        Gets the LogicalInterconnectGroups API client.

        Returns:
            LogicalInterconnectGroups:
        """
        if not self.__logical_interconnect_groups:
            self.__logical_interconnect_groups = LogicalInterconnectGroups(
                self.__connection)
        return self.__logical_interconnect_groups

    @property
    def logical_interconnects(self):
        """
        Gets the LogicalInterconnects API client.

        Returns:
            LogicalInterconnects:
        """
        if not self.__logical_interconnects:
            self.__logical_interconnects = LogicalInterconnects(
                self.__connection)
        return self.__logical_interconnects

    @property
    def sas_logical_interconnects(self):
        """
        Gets the SasLogicalInterconnects API client.

        Returns:
            SasLogicalInterconnects:
        """
        if not self.__sas_logical_interconnects:
            self.__sas_logical_interconnects = SasLogicalInterconnects(self.__connection)
        return self.__sas_logical_interconnects

    @property
    def logical_downlinks(self):
        """
        Gets the LogicalDownlinks API client.

        Returns:
            LogicalDownlinks:
        """
        if not self.__logical_downlinks:
            self.__logical_downlinks = LogicalDownlinks(
                self.__connection)
        return self.__logical_downlinks

    @property
    def power_devices(self):
        """
        Gets the PowerDevices API client.

        Returns:
            PowerDevices:
        """
        if not self.__power_devices:
            self.__power_devices = PowerDevices(self.__connection)
        return self.__power_devices

    @property
    def unmanaged_devices(self):
        """
        Gets the Unmanaged Devices API client.

        Returns:
            UnmanagedDevices:
        """
        if not self.__unmanaged_devices:
            self.__unmanaged_devices = UnmanagedDevices(self.__connection)
        return self.__unmanaged_devices

    @property
    def racks(self):
        """
        Gets the Racks API client.

        Returns:
            Racks:
        """
        if not self.__racks:
            self.__racks = Racks(self.__connection)
        return self.__racks

    @property
    def san_managers(self):
        """
        Gets the SanManagers API client.

        Returns:
            SanManagers:
        """
        if not self.__san_managers:
            self.__san_managers = SanManagers(self.__connection)
        return self.__san_managers

    @property
    def endpoints(self):
        """
        Gets the Endpoints API client.

        Returns:
            Endpoints:
        """
        if not self.__endpoints:
            self.__endpoints = Endpoints(self.__connection)
        return self.__endpoints

    @property
    def server_profiles(self):
        """
        Gets the ServerProfiles API client.

        Returns:
            ServerProfiles:
        """
        if not self.__server_profiles:
            self.__server_profiles = ServerProfiles(self.__connection)
        return self.__server_profiles

    @property
    def server_profile_templates(self):
        """
        Gets the ServerProfileTemplate API client.

        Returns:
            ServerProfileTemplate:
        """
        if not self.__server_profile_templates:
            self.__server_profile_templates = ServerProfileTemplate(self.__connection)
        return self.__server_profile_templates

    @property
    def storage_systems(self):
        """
        Gets the StorageSystems API client.

        Returns:
            StorageSystems:
        """
        if not self.__storage_systems:
            self.__storage_systems = StorageSystems(self.__connection)
        return self.__storage_systems

    @property
    def storage_pools(self):
        """
        Gets the StoragePools API client.

        Returns:
            StoragePools:
        """
        if not self.__storage_pools:
            self.__storage_pools = StoragePools(self.__connection)
        return self.__storage_pools

    @property
    def storage_volume_templates(self):
        """
        Gets the StorageVolumeTemplates API client.

        Returns:
            StorageVolumeTemplates:
        """
        if not self.__storage_volume_templates:
            self.__storage_volume_templates = StorageVolumeTemplates(self.__connection)
        return self.__storage_volume_templates

    @property
    def storage_volume_attachments(self):
        """
        Gets the StorageVolumeAttachments API client.

        Returns:
            StorageVolumeAttachments:
        """
        if not self.__storage_volume_attachments:
            self.__storage_volume_attachments = StorageVolumeAttachments(self.__connection)
        return self.__storage_volume_attachments

    @property
    def firmware_drivers(self):
        """
        Gets the FirmwareDrivers API client.

        Returns:
            FirmwareDrivers:
        """
        if not self.__firmware_drivers:
            self.__firmware_drivers = FirmwareDrivers(self.__connection)
        return self.__firmware_drivers

    @property
    def firmware_bundles(self):
        """
        Gets the FirmwareBundles API client.

        Returns:
            FirmwareBundles:
        """
        if not self.__firmware_bundles:
            self.__firmware_bundles = FirmwareBundles(self.__connection)
        return self.__firmware_bundles

    @property
    def uplink_sets(self):
        """
        Gets the UplinkSets API client.

        Returns:
            UplinkSets:
        """
        if not self.__uplink_sets:
            self.__uplink_sets = UplinkSets(self.__connection)
        return self.__uplink_sets

    @property
    def volumes(self):
        """
        Gets the Volumes API client.

        Returns:
            Volumes:
        """
        if not self.__volumes:
            self.__volumes = Volumes(self.__connection)
        return self.__volumes

    @property
    def sas_logical_jbod_attachments(self):
        """
        Gets the SAS Logical JBOD Attachments client.

        Returns:
            SasLogicalJbodAttachments:
        """
        if not self.__sas_logical_jbod_attachments:
            self.__sas_logical_jbod_attachments = SasLogicalJbodAttachments(self.__connection)
        return self.__sas_logical_jbod_attachments

    @property
    def managed_sans(self):
        """
        Gets the Managed SANs API client.

        Returns:
            ManagedSANs:
        """
        if not self.__managed_sans:
            self.__managed_sans = ManagedSANs(self.__connection)
        return self.__managed_sans

    @property
    def migratable_vc_domains(self):
        """
        Gets the VC Migration Manager API client.

        Returns:
            MigratableVcDomains:
        """
        if not self.__migratable_vc_domains:
            self.__migratable_vc_domains = MigratableVcDomains(self.__connection)
        return self.__migratable_vc_domains

    @property
    def sas_interconnects(self):
        """
        Gets the SAS Interconnects API client.

        Returns:
            SasInterconnects:
        """
        if not self.__sas_interconnects:
            self.__sas_interconnects = SasInterconnects(self.__connection)
        return self.__sas_interconnects

    @property
    def sas_logical_interconnect_groups(self):
        """
        Gets the SasLogicalInterconnectGroups API client.

        Returns:
            SasLogicalInterconnectGroups:
        """
        if not self.__sas_logical_interconnect_groups:
            self.__sas_logical_interconnect_groups = SasLogicalInterconnectGroups(self.__connection)
        return self.__sas_logical_interconnect_groups

    @property
    def drive_enclosures(self):
        """
        Gets the Drive Enclosures API client.

        Returns:
            DriveEnclosures:
        """
        if not self.__drive_enclures:
            self.__drive_enclures = DriveEnclosures(self.__connection)
        return self.__drive_enclures

    @property
    def sas_logical_jbods(self):
        """
        Gets the SAS Logical JBODs API client.

        Returns:
            SasLogicalJbod:
        """
        if not self.__sas_logical_jbods:
            self.__sas_logical_jbods = SasLogicalJbods(self.__connection)
        return self.__sas_logical_jbods

    @property
    def labels(self):
        """
        Gets the Labels API client.

        Returns:
            Labels:
        """
        if not self.__labels:
            self.__labels = Labels(self.__connection)
        return self.__labels

    @property
    def index_resources(self):
        """
        Gets the Index Resources API client.

        Returns:
            IndexResources:
        """
        if not self.__index_resources:
            self.__index_resources = IndexResources(self.__connection)
        return self.__index_resources

    @property
    def alerts(self):
        """
        Gets the Alerts API client.

        Returns:
            Alerts:
        """
        if not self.__alerts:
            self.__alerts = Alerts(self.__connection)
        return self.__alerts

    @property
    def events(self):
        """
        Gets the Events API client.

        Returns:
            Events:
        """
        if not self.__events:
            self.__events = Events(self.__connection)
        return self.__events

    @property
    def os_deployment_plans(self):
        """
        Gets the Os Deployment Plans API client.

        Returns:
            OsDeploymentPlans:
        """
        if not self.__os_deployment_plans:
            self.__os_deployment_plans = OsDeploymentPlans(self.__connection)
        return self.__os_deployment_plans

    @property
    def os_deployment_servers(self):
        """
        Gets the Os Deployment Servers API client.

        Returns:
            OsDeploymentServers:
        """
        if not self.__os_deployment_servers:
            self.__os_deployment_servers = OsDeploymentServers(self.__connection)
        return self.__os_deployment_servers

    @property
    def certificate_rabbitmq(self):
        """
        Gets the Certificate RabbitMQ API client.

        Returns:
            CertificateRabbitMQ:
        """
        if not self.__certificate_rabbitmq:
            self.__certificate_rabbitmq = CertificateRabbitMQ(self.__connection)
        return self.__certificate_rabbitmq

    @property
    def users(self):
        """
        Gets the Users API client.

        Returns:
            Users:
        """
        if not self.__users:
            self.__users = Users(self.__connection)
        return self.__users

    @property
    def appliance_node_information(self):
        """
        Gets the ApplianceNodeInformation API client.

        Returns:
            ApplianceNodeInformation:
        """
        if not self.__appliance_node_information:
            self.__appliance_node_information = ApplianceNodeInformation(self.__connection)
        return self.__appliance_node_information

    @property
    def appliance_time_and_locale_configuration(self):
        """
        Gets the ApplianceTimeAndLocaleConfiguration API client.

        Returns:
            ApplianceTimeAndLocaleConfiguration:
        """
        if not self.__appliance_time_and_locale_configuration:
            self.__appliance_time_and_locale_configuration = ApplianceTimeAndLocaleConfiguration(self.__connection)
        return self.__appliance_time_and_locale_configuration

    @property
    def versions(self):
        """
        Gets the Version API client.

        Returns:
            Version:
        """
        if not self.__versions:
            self.__versions = Versions(self.__connection)
        return self.__versions

    @property
    def backups(self):
        """
        Gets the Backup API client.

        Returns:
            Backups:
        """
        if not self.__backups:
            self.__backups = Backups(self.__connection)
        return self.__backups

    @property
    def login_details(self):
        """
        Gets the login details

        Returns:
        List of login details
        """
        if not self.__login_details:
            self.__login_details = LoginDetails(self.__connection)
        return self.__login_details
