from unittest import TestCase

import mock

from hpOneView.common import uri
from hpOneView.connection import connection
from hpOneView.test.test_utils import load_stub
from hpOneView.resources.networking.interconnects import Interconnects



class InterconnectsTest(TestCase):

    def setUp(self):
        super(InterconnectsTest, self).setUp()
        self.host = 'http://1.2.3.4'
        self.connection = connection(self.host)
        self.interconnect = Interconnects(self.connection)

    @mock.patch.object(connection, 'get')
    def test_get_interconnects_statistics_request(self, mock_get):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        url = (uri['ic'] + '/{id}/statistics').format(id=id)
        self.interconnect.get_interconnects_statistics(id=id)
        mock_get.assert_called_once_with(url)

    @mock.patch.object(connection, 'get')
    def test_get_interconnects_statistics_response(self, mock_get):
        id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
        stub = load_stub('get_interconnects_statistics_client_teste.json')

        expected_dict = stub
        mock_response = mock.Mock()
        mock_response.json = stub
        mock_get.return_value = mock_response

        response_dict = self.interconnect.get_interconnects_statistics(id=id)

        self.assertEqual(response_dict.json, expected_dict)
