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
import io

from tests.test_utils import mock_builtin
from hpOneView.connection import connection
from hpOneView.oneview_client import OneViewClient
from hpOneView.resources.data_services.metric_streaming import MetricStreaming
from hpOneView.resources.facilities.power_devices import PowerDevices
from hpOneView.resources.networking.fc_networks import FcNetworks
from hpOneView.resources.networking.fcoe_networks import FcoeNetworks
from hpOneView.resources.networking.interconnects import Interconnects


class OneViewClientTest(unittest.TestCase):
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

        # Simulates a TextIOWrapper (file output)
        output = io.StringIO(json_config_content)
        mock_open.return_value = output

        oneview_client = OneViewClient.from_json_file("config.json")

        self.assertIsInstance(oneview_client, OneViewClient)
        self.assertEqual("172.16.102.59", oneview_client.connection.get_host())

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

    def test_lazy_loading_tasks(self):
        tasks = self._oneview.tasks
        self.assertEqual(tasks, self._oneview.tasks)

    def test_lazy_loading_metric_streaming(self):
        metric = self._oneview.metric_streaming
        self.assertEqual(metric, self._oneview.metric_streaming)

    def test_lazy_loading_enclosures(self):
        enclosures = self._oneview.enclosures
        self.assertEqual(enclosures, self._oneview.enclosures)

    def test_lazy_loading_switches(self):
        switches = self._oneview.switches
        self.assertEqual(switches, self._oneview.switches)

    def test_lazy_loading_server_hardware(self):
        server_hardware = self._oneview.server_hardware
        self.assertEqual(server_hardware, self._oneview.server_hardware)

    def test_interconnects_has_right_type(self):
        self.assertIsInstance(self._oneview.interconnects, Interconnects)

    def test_interconnects_has_value(self):
        self.assertIsNotNone(self._oneview.interconnects)

    def test_lazy_loading_interconnects(self):
        interconnects = self._oneview.interconnects
        self.assertEqual(interconnects, self._oneview.interconnects)

    def test_power_devices_has_right_type(self):
        self.assertIsInstance(self._oneview.power_devices, PowerDevices)

    def test_power_devices_has_value(self):
        self.assertIsNotNone(self._oneview.power_devices)

    def test_lazy_loading_power_devices(self):
        power_devices = self._oneview.power_devices
        self.assertEqual(power_devices, self._oneview.power_devices)
