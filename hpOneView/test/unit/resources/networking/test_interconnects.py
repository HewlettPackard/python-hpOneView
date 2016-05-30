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

from hpOneView.connection import connection
from hpOneView.resources.networking.interconnects import Interconnects
from hpOneView.resources.resource import ResourceClient


class InterconnectsTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._interconnects = Interconnects(self.connection)

    @mock.patch.object(ResourceClient, 'get_by_uri')
    def test_get_statistics(self, mock_get_by_uri):
        self._interconnects.get_statistics('3518be0e-17c1-4189-8f81-83f3724f6155')

        uri = '/rest/interconnects/3518be0e-17c1-4189-8f81-83f3724f6155/statistics'

        mock_get_by_uri.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get_by_uri')
    def test_get_statistics_with_port_name(self, mock_get_by_uri):
        self._interconnects.get_statistics('3518be0e-17c1-4189-8f81-83f3724f6155', 'd1')

        uri = '/rest/interconnects/3518be0e-17c1-4189-8f81-83f3724f6155/statistics/d1'

        mock_get_by_uri.assert_called_once_with(uri)
