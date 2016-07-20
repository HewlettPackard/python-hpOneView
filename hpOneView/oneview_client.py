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
"""
oneview_client.py
~~~~~~~~~~~~

This module implements a common client for HPE OneView REST API
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

__title__ = 'OneViewClient'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2016) Hewlett Packard Enterprise ' \
                ' Development LP'
__license__ = 'MIT'
__status__ = 'Development'

import json

from hpOneView.connection import connection
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
from hpOneView.resources.servers.enclosures import Enclosures
from hpOneView.resources.servers.logical_enclosures import LogicalEnclosures
from hpOneView.resources.servers.enclosure_groups import EnclosureGroups
from hpOneView.resources.servers.server_hardware import ServerHardware
from hpOneView.resources.servers.server_hardware_types import ServerHardwareTypes
from hpOneView.resources.servers.id_pools_vsn_ranges import IdPoolsVsnRanges
from hpOneView.resources.servers.id_pools_vmac_ranges import IdPoolsVmacRanges
from hpOneView.resources.servers.id_pools_vwwn_ranges import IdPoolsVwwnRanges
from hpOneView.resources.networking.interconnects import Interconnects
from hpOneView.resources.networking.interconnect_types import InterconnectTypes
from hpOneView.resources.networking.logical_downlinks import LogicalDownlinks
from hpOneView.resources.facilities.power_devices import PowerDevices
from hpOneView.resources.networking.logical_interconnects import LogicalInterconnects
from hpOneView.resources.networking.logical_interconnect_groups import LogicalInterconnectGroups
from hpOneView.resources.networking.logical_switch_groups import LogicalSwitchGroups
from hpOneView.resources.storage.storage_systems import StorageSystems
from hpOneView.resources.storage.storage_pools import StoragePools
from hpOneView.resources.storage.storage_volume_templates import StorageVolumeTemplates
from hpOneView.resources.storage.storage_volume_attachments import StorageVolumeAttachments
from hpOneView.resources.settings.firmware_drivers import FirmwareDrivers
from hpOneView.resources.settings.firmware_bundles import FirmwareBundles

ONEVIEW_CLIENT_INVALID_PROXY = 'Invalid Proxy format'


class OneViewClient(object):

    def __init__(self, config):
        self.__connection = connection(config["ip"], config.get('api_version', 200))
        self.__set_proxy(config)
        self.__connection.login(config["credentials"])
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
        self.__enclosures = None
        self.__logical_enclosures = None
        self.__enclosure_groups = None
        self.__metric_streaming = None
        self.__server_hardware = None
        self.__server_hardware_types = None
        self.__id_pools_vsn_ranges = None
        self.__id_pools_vmac_ranges = None
        self.__id_pools_vwwn_ranges = None
        self.__interconnects = None
        self.__interconnect_types = None
        self.__power_devices = None
        self.__logical_interconnects = None
        self.__logical_interconnect_groups = None
        self.__logical_switch_groups = None
        self.__logical_downlinks = None
        self.__storage_systems = None
        self.__storage_pools = None
        self.__storage_volume_templates = None
        self.__storage_volume_attachments = None
        self.__firmware_drivers = None
        self.__firmware_bundles = None
        # TODO: Implement: con.set_trusted_ssl_bundle(args.cert)

    @classmethod
    def from_json_file(cls, file_name):
        """
        Construct OneViewClient using a json file

        Args:
            file_name: json full path

        Returns: OneViewClient

        """
        with open(file_name) as json_data:
            config = json.load(json_data)

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

            self.__connection.set_proxy(splitted[0], splitted[1])

    @property
    def connection(self):
        return self.__connection

    @property
    def connections(self):
        if not self.__connections:
            self.__connections = Connections(
                self.__connection)
        return self.__connections

    @property
    def connection_templates(self):
        if not self.__connection_templates:
            self.__connection_templates = ConnectionTemplates(
                self.__connection)
        return self.__connection_templates

    @property
    def fc_networks(self):
        if not self.__fc_networks:
            self.__fc_networks = FcNetworks(self.__connection)
        return self.__fc_networks

    @property
    def fcoe_networks(self):
        if not self.__fcoe_networks:
            self.__fcoe_networks = FcoeNetworks(self.__connection)
        return self.__fcoe_networks

    @property
    def ethernet_networks(self):
        if not self.__ethernet_networks:
            self.__ethernet_networks = EthernetNetworks(self.__connection)
        return self.__ethernet_networks

    @property
    def fabrics(self):
        if not self.__fabrics:
            self.__fabrics = Fabrics(self.__connection)
        return self.__fabrics

    @property
    def network_sets(self):
        if not self.__network_sets:
            self.__network_sets = NetworkSets(self.__connection)
        return self.__network_sets

    @property
    def server_hardware(self):
        if not self.__server_hardware:
            self.__server_hardware = ServerHardware(self.__connection)
        return self.__server_hardware

    @property
    def server_hardware_types(self):
        if not self.__server_hardware_types:
            self.__server_hardware_types = ServerHardwareTypes(
                self.__connection)
        return self.__server_hardware_types

    @property
    def id_pools_vsn_ranges(self):
        if not self.__id_pools_vsn_ranges:
            self.__id_pools_vsn_ranges = IdPoolsVsnRanges(
                self.__connection)
        return self.__id_pools_vsn_ranges

    @property
    def id_pools_vmac_ranges(self):
        if not self.__id_pools_vmac_ranges:
            self.__id_pools_vmac_ranges = IdPoolsVmacRanges(
                self.__connection)
        return self.__id_pools_vmac_ranges

    @property
    def id_pools_vwwn_ranges(self):
        if not self.__id_pools_vwwn_ranges:
            self.__id_pools_vwwn_ranges = IdPoolsVwwnRanges(
                self.__connection)
        return self.__id_pools_vwwn_ranges

    @property
    def switches(self):
        if not self.__switches:
            self.__switches = Switches(self.__connection)
        return self.__switches

    @property
    def switch_types(self):
        if not self.__switch_types:
            self.__switch_types = SwitchTypes(self.__connection)
        return self.__switch_types

    @property
    def logical_switch_groups(self):
        if not self.__logical_switch_groups:
            self.__logical_switch_groups = LogicalSwitchGroups(
                self.__connection)
        return self.__logical_switch_groups

    @property
    def tasks(self):
        if not self.__tasks:
            self.__tasks = Tasks(self.__connection)
        return self.__tasks

    @property
    def enclosure_groups(self):
        if not self.__enclosure_groups:
            self.__enclosure_groups = EnclosureGroups(self.__connection)
        return self.__enclosure_groups

    @property
    def enclosures(self):
        if not self.__enclosures:
            self.__enclosures = Enclosures(self.__connection)
        return self.__enclosures

    @property
    def logical_enclosures(self):
        if not self.__logical_enclosures:
            self.__logical_enclosures = LogicalEnclosures(self.__connection)
        return self.__logical_enclosures

    @property
    def metric_streaming(self):
        if not self.__metric_streaming:
            self.__metric_streaming = MetricStreaming(self.__connection)
        return self.__metric_streaming

    @property
    def interconnects(self):
        if not self.__interconnects:
            self.__interconnects = Interconnects(self.__connection)
        return self.__interconnects

    @property
    def interconnect_types(self):
        if not self.__interconnect_types:
            self.__interconnect_types = InterconnectTypes(self.__connection)
        return self.__interconnect_types

    @property
    def logical_interconnect_groups(self):
        if not self.__logical_interconnect_groups:
            self.__logical_interconnect_groups = LogicalInterconnectGroups(
                self.__connection)
        return self.__logical_interconnect_groups

    @property
    def logical_interconnects(self):
        if not self.__logical_interconnects:
            self.__logical_interconnects = LogicalInterconnects(
                self.__connection)
        return self.__logical_interconnects

    @property
    def logical_downlinks(self):
        if not self.__logical_downlinks:
            self.__logical_downlinks = LogicalDownlinks(
                self.__connection)
        return self.__logical_downlinks

    @property
    def power_devices(self):
        if not self.__power_devices:
            self.__power_devices = PowerDevices(self.__connection)
        return self.__power_devices

    @property
    def storage_systems(self):
        if not self.__storage_systems:
            self.__storage_systems = StorageSystems(self.__connection)
        return self.__storage_systems

    @property
    def storage_pools(self):
        if not self.__storage_pools:
            self.__storage_pools = StoragePools(self.__connection)
        return self.__storage_pools

    @property
    def storage_volume_templates(self):
        if not self.__storage_volume_templates:
            self.__storage_volume_templates = StorageVolumeTemplates(self.__connection)
        return self.__storage_volume_templates

    @property
    def storage_volume_attachments(self):
        if not self.__storage_volume_attachments:
            self.__storage_volume_attachments = StorageVolumeAttachments(self.__connection)
        return self.__storage_volume_attachments

    @property
    def firmware_drivers(self):
        if not self.__firmware_drivers:
            self.__firmware_drivers = FirmwareDrivers(self.__connection)
        return self.__firmware_drivers

    @property
    def firmware_bundles(self):
        if not self.__firmware_bundles:
            self.__firmware_bundles = FirmwareBundles(self.__connection)
        return self.__firmware_bundles
