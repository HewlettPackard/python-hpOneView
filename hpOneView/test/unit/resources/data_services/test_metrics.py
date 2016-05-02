from unittest import TestCase

import mock

from hpOneView.resources.data_services.metrics import Metrics
from hpOneView.test.test_utils import load_stub


class TestMetrics(TestCase):

    configuration = load_stub("update_metrics_configuration.json")

    def test_update_metrics_configuration(self):
        connection = mock.Mock()
        connection.put.return_value = None, self.configuration

        metrics_client = Metrics(connection)
        response = metrics_client.update_configuration(self.configuration)

        connection.put.assert_called_once_with(Metrics.RESOURCE_URI, self.configuration)
        self.assertEquals(self.configuration, response)

