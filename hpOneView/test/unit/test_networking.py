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
import uuid

from hpOneView.common import uri
from hpOneView.connection import *
from hpOneView.networking import *


class NetworkingTest(unittest.TestCase):

	def setUp(self):
		super(NetworkingTest, self).setUp()
		self.host = 'http://1.2.3.4'
		self.connection = connection(self.host)
		self.networking = networking(self.connection)

	@mock.patch.object(connection, 'get')
	def test_get_lig_default_settings(self, mock_get):
		self.networking.get_lig_default_settings()
		mock_get.assert_called_once_with(uri['lig'] + '/defaultSettings')

	@mock.patch.object(connection, 'get')
	def test_get_lig_settings(self, mock_get):
		id = uuid.uuid4()
		self.networking.get_lig_settings(id)
		lig_uri = uri['lig'] + '/{id}/settings'
		mock_get.assert_called_once_with(lig_uri.format(id=id))

	@mock.patch.object(connection, 'get')
	def test_get_lig_by_id(self, mock_get):
		id = str(uuid.uuid4())
		self.networking.get_lig_by_id(id)
		mock_get.assert_called_once_with(uri['lig'] + '/' + id)

	@mock.patch.object(connection, 'get')
	def test_get_lig_schema(self, mock_get):
		self.networking.get_lig_schema()
		mock_get.assert_called_once_with(uri['lig'] + '/schema')

	@mock.patch.object(connection, 'get')
	def test_get_logical_downlinks(self, mock_get):
		self.networking.get_logical_downlinks()
		mock_get.assert_called_once_with(uri['ld'])
		mock_get.reset_mock()

		# Testing with filter
		filter = '?start=0&count=10'
		self.networking.get_logical_downlinks(filter=filter)
		mock_get.assert_called_once_with(uri['ld'] + filter)

	@mock.patch.object(connection, 'get')
	def test_get_logical_downlinks_schema(self, mock_get):
		self.networking.get_logical_downlinks_schema()
		mock_get.assert_called_once_with(uri['ld'] + '/schema')

	@mock.patch.object(connection, 'get')
	def test_get_logical_downlinks_without_ethernet(self, mock_get):
		self.networking.get_logical_downlinks_without_ethernet()
		downlinks_uri = uri['ld'] + '/withoutEthernet'
		mock_get.assert_called_once_with(downlinks_uri)
		mock_get.reset_mock()

		# Testing with filter
		filter = '?start=0&count=10'
		self.networking.get_logical_downlinks_without_ethernet(filter=filter)
		mock_get.assert_called_once_with(downlinks_uri + filter)

	@mock.patch.object(connection, 'get')
	def test_get_logical_downlink_by_id(self, mock_get):
		id = str(uuid.uuid4())
		self.networking.get_logical_downlink(id)
		mock_get.assert_called_once_with(uri['ld'] + '/' + id)

	@mock.patch.object(connection, 'get')
	def test_get_logical_downlink_without_ethernet_by_id(self, mock_get):
		id = str(uuid.uuid4())
		self.networking.get_logical_downlink_without_ethernet(id)
		downlink_uri = uri['ld'] + '/{id}/withoutEthernet'
		mock_get.assert_called_once_with(downlink_uri.format(id=id))


if __name__ == '__main__':
	unittest.main()