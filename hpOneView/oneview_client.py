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
from hpOneView.resources.networking.fc_networks import FcNetworks
from hpOneView.resources.networking.fcoe_networks import FcoeNetworks
from hpOneView.resources.data_services.metric_streaming import MetricStreaming
from hpOneView.resources.networking.switches import Switches
from hpOneView.resources.activity.tasks import Tasks
from hpOneView.resources.servers.enclosures import Enclosures
from hpOneView.resources.servers.server_hardware import ServerHardware
from hpOneView.resources.networking.interconnects import Interconnects
from hpOneView.resources.facilities.power_devices import PowerDevices

ONEVIEW_CLIENT_INVALID_PROXY = 'Invalid Proxy format'


class OneViewClient(object):
    def __init__(self, config):
        self.__config = config
        self.__connection = connection(config["ip"])
        self.__set_proxy(config)
        self.__connection.login(config["credentials"])
        self.__fc_networks = None
        self.__fcoe_networks = None
        self.__switches = None
        self.__tasks = None
        self.__enclosures = None
        self.__metric_streaming = None
        self.__server_hardware = None
        self.__interconnects = None
        self.__power_devices = None
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
    def server_hardware(self):
        if not self.__server_hardware:
            self.__server_hardware = ServerHardware(self.__connection)
        return self.__server_hardware

    @property
    def switches(self):
        if not self.__switches:
            self.__switches = Switches(self.__connection)
        return self.__switches

    @property
    def tasks(self):
        if not self.__tasks:
            self.__tasks = Tasks(self.__connection)
        return self.__tasks

    @property
    def enclosures(self):
        if not self.__enclosures:
            self.__enclosures = Enclosures(self.__connection)
        return self.__enclosures

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
    def power_devices(self):
        if not self.__power_devices:
            self.__power_devices = PowerDevices(self.__connection)
        return self.__power_devices
