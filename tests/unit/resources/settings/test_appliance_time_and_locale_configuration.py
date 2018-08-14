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

import unittest

import mock

from hpOneView.connection import connection
from hpOneView.resources.settings.appliance_time_and_locale_configuration import ApplianceTimeAndLocaleConfiguration
from hpOneView.resources.resource import ResourceClient


class ApplianceTimeAndLocaleConfigurationTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._time_and_locale = ApplianceTimeAndLocaleConfiguration(self.connection)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        self._time_and_locale.get()
        mock_get.assert_called_once_with('/rest/appliance/configuration/time-locale')

    @mock.patch.object(ResourceClient, 'create')
    def test_update_called_once(self, mock_create):
        resource = {
            'dateTime': '2020-02-27T7:55:00.000Z',
            'locale': 'en_US.UTF-8',
            'localeDisplayName': 'English (United States)',
            'ntpServers': ['127.0.0.1'],
            'timezone': 'UTC',
            'uri': None
        }
        self._time_and_locale.update(resource)
        mock_create.assert_called_once_with(resource, force=False, timeout=-1, default_values=self._time_and_locale.DEFAULT_VALUES)
