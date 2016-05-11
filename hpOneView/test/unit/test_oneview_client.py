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

import mock
import unittest

from hpOneView.oneview_client import OneViewClient
from hpOneView.connection import connection
from hpOneView.resources.networking.fc_networks import FcNetworks
from hpOneView.resources.networking.interconnects import Interconnects
from hpOneView.resources.data_services.metrics import Metrics


class OneViewClientTest(unittest.TestCase):
    @mock.patch.object(connection, 'login')
    def setUp(self, mock_login):
        super(OneViewClientTest, self).setUp()

        config = {"ip": "172.16.102.59",
                  "credentials": {
                      "authLoginDomain": "",
                      "userName": "administrator",
                      "password": ""}}

        self._one_view = OneViewClient(config)

    def test_fc_networks_has_right_type(self):
        self.assertIsInstance(self._one_view.fc_networks, FcNetworks)

    def test_fc_networks_has_value(self):
        self.assertIsNotNone(self._one_view.fc_networks)

    def test_lazy_loading_fc_networks(self):
        fcn = self._one_view.fc_networks
        self.assertEqual(fcn, self._one_view.fc_networks)

    def test_interconnects_has_right_type(self):
        self.assertIsInstance(self._one_view.interconnects, Interconnects)

    def test_interconnects_has_value(self):
        self.assertIsNotNone(self._one_view.interconnects)

    def test_lazy_loading_interconnects(self):
        fcn = self._one_view.interconnects
        self.assertEqual(fcn, self._one_view.interconnects)

    def test_metrics_has_right_type(self):
        self.assertIsInstance(self._one_view.metrics, Metrics)

    def test_metrics_has_value(self):
        self.assertIsNotNone(self._one_view.metrics)

    def test_lazy_loading_metrics(self):
        fcn = self._one_view.metrics
        self.assertEqual(fcn, self._one_view.metrics)
