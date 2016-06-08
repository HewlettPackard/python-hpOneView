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
from hpOneView.resources.facilities.power_devices import PowerDevices


class PowerDevicesTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._power_devices = PowerDevices(self.connection)

    @mock.patch.object(connection, 'get')
    def test_get_utilization_with_all_args(self, mock_get):
        self._power_devices.get_utilization(
            '35323930-4936-4450-5531-303153474820',
            fields='PeakPower,AveragePower',
            filter='startDate=2016-05-30T03:29:42.361Z,endDate=2016-05-31T03:29:42.361Z',
            refresh=True, view='day')

        expected_uri = '/rest/power-devices/35323930-4936-4450-5531-303153474820/utilization' \
                       '?filter=startDate%3D2016-05-30T03%3A29%3A42.361Z' \
                       '&filter=endDate%3D2016-05-31T03%3A29%3A42.361Z' \
                       '&fields=PeakPower%2CAveragePower' \
                       '&refresh=true&view=day'

        mock_get.assert_called_once_with(expected_uri)

    @mock.patch.object(connection, 'get')
    def test_get_utilization_with_defaults(self, mock_get):
        self._power_devices.get_utilization('35323930-4936-4450-5531-303153474820')

        expected_uri = '/rest/power-devices/35323930-4936-4450-5531-303153474820/utilization'

        mock_get.assert_called_once_with(expected_uri)
