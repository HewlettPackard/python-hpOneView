from pprint import pprint

from hpOneView.connection import connection
from hpOneView.resources.data_services.metrics import Metrics

credential = dict(
    userName='Administrator',
    password='password'
)
one_view_connection = connection('127.0.0.1')
one_view_connection.login(credential)

configuration = {
    "sourceTypeList": [
        {
            "sourceType": "/rest/power-devices",
            "sampleIntervalInSeconds": "300",
            "frequencyOfRelayInSeconds": "3600"
        },
        {
            "sourceType": "/rest/enclosures",
            "sampleIntervalInSeconds": "600",
            "frequencyOfRelayInSeconds": "3600"
        },
        {
            "sourceType": "/rest/server-hardware",
            "sampleIntervalInSeconds": "600",
            "frequencyOfRelayInSeconds": "1800"
        },
    ]
}

metrics = Metrics(one_view_connection)
updated_metrics_configuration = metrics.update_configuration(configuration)
pprint(updated_metrics_configuration)
