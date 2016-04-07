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

	@mock.patch.object(connection, 'get')
	def test_get_logical_interconnects(self, mock_get):
		self.networking.get_lis()
		mock_get.assert_called_once_with(uri['li'])
		mock_get.reset_mock()

		# Testing with filter
		filter = '?start=0&count=10'
		self.networking.get_lis(filter=filter)
		mock_get.assert_called_once_with(uri['li'] + filter)

	@mock.patch.object(connection, 'put')
	def test_correct_lis(self, mock_put):
		uris = [uuid.uuid4().hex, uuid.uuid4().hex, uuid.uuid4().hex]
		mock_put.return_value = (None, None)
		request = {'uris': uris}

		# passing blocking as False because we just want to test the uri.
		self.networking.correct_lis(uris, blocking=False)
		mock_put.assert_called_once_with(uri['li'] + '/compliance', request)

	@mock.patch.object(connection, 'post')
	def test_create_li(self, mock_post):
		location_entries = [uuid.uuid4().hex, uuid.uuid4().hex]
		mock_post.return_value = (None, None)
		request = {'locationEntries': location_entries}

		# passing blocking as False because we just want to test the uri.
		self.networking.create_li(location_entries, blocking=False)
		mock_post.assert_called_once_with(
			uri['li'] + '/locations/interconnects', request)

	@mock.patch.object(connection, 'delete')
	def test_delete_li(self, mock_delete):
		# the host where the li will be deleted.
		location = self.host
		mock_delete.return_value = (None, None)

		# passing blocking as False because we just want to test the uri.
		self.networking.delete_li(location, blocking=False)
		mock_delete.assert_called_once_with(
			uri['li'] + '/locations/interconnects?location=' + location)

	@mock.patch.object(connection, 'get')
	def test_get_logical_interconnects_schema(self, mock_get):
		self.networking.get_li_schema()
		mock_get.assert_called_once_with(uri['li'] + '/schema')

	@mock.patch.object(connection, 'get')
	def test_get_logical_interconnects_by_id(self, mock_get):
		id = uuid.uuid4().hex
		self.networking.get_li_by_id(id)
		mock_get.assert_called_once_with(uri['li'] + '/' + id)

	@mock.patch.object(connection, 'put')
	def test_correct_li_by_id(self, mock_put):
		id = uuid.uuid4().hex
		mock_put.return_value = (None, None)

		# passing blocking as False because we just want to test the uri.
		self.networking.correct_li_by_id(id, blocking=False)
		correct_li_uri = uri['li'] + '/{id}/compliance'
		mock_put.assert_called_once_with(correct_li_uri.format(id=id), {})

	@mock.patch.object(connection, 'put')
	def test_update_ethernet_interconnected_settings(self, mock_put):
		id = uuid.uuid4().hex
		mock_put.return_value = (None, None)
		settings_test = {"interconnectType": "Ethernet",
                         "igmpIdleTimeoutInterval": 200,
                         "macRefreshInterval": 10,
                         "name": "ES-882901476",
                         "created": "2015-08-21T21:48:01.096Z",
                         "enableRichTLV": 'false',
                         "uri": "/rest/logical-interconnects/ID/ethernetSettings",
                         "enableNetworkLoopProtection": True,
                         "enableFastMacCacheFailover": True,
                         "modified": "2015-08-21T21:48:01.099Z",
                         "enableIgmpSnooping": True,
                         "enablePauseFloodProtection": True,
                         "dependentResourceUri": "/rest/logical-interconnects/ID",
                         "type": "EthernetInterconnectSettingsV3",
                         "id": "9b1380ee-a0bb-4388-af35-2c5a05e84c47"}

		# passing blocking as False because we just want to test the uri.
		self.networking.update_ethernet_interconnected_settings(
			id, settings_test, blocking=False)
		correct_li_uri = uri['li'] + '/{id}/ethernetSettings'
		mock_put.assert_called_once_with(correct_li_uri.format(id=id),
			                             settings_test)

	@mock.patch.object(connection, 'get')
	def test_get_logical_interconnect_firmware(self, mock_get):
		id = uuid.uuid4().hex
		self.networking.get_li_firmware(id)

		li_firmware_uri = uri['li'] + '/{id}/firmware'
		mock_get.assert_called_once_with(li_firmware_uri.format(id=id))

if __name__ == '__main__':
	unittest.main()
