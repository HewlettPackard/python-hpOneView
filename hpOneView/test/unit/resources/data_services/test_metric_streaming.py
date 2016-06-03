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
from hpOneView.resources.data_services.metric_streaming import MetricStreaming
from hpOneView.resources.resource import ResourceClient


class MetricStreamingTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._metrics = MetricStreaming(self.connection)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_capability_called_once(self, mock_get):
        self._metrics.get_capability()
        mock_get.assert_called_once_with("/rest/metrics/capability")

    @mock.patch.object(ResourceClient, 'get')
    def test_get_configuration_called_once(self, mock_get):
        self._metrics.get_configuration()
        mock_get.assert_called_once_with("/rest/metrics/configuration")

    @mock.patch.object(ResourceClient, 'basic_update')
    def test_update_should_use_given_values(self, mock_update):
        configuration = {
            "sourceTypeList": [
                {
                    "sourceType": "/rest/power-devices",
                    "sampleIntervalInSeconds": "300",
                    "frequencyOfRelayInSeconds": "3600"
                }
            ]
        }
        configuration_rest_call = configuration.copy()
        mock_update.return_value = configuration

        self._metrics.update_configuration(configuration)
        mock_update.assert_called_once_with(configuration_rest_call, "/rest/metrics/configuration")
