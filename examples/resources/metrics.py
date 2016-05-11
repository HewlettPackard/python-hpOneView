from pprint import pprint

from hpOneView.oneview_client import OneViewClient

config = {"ip": "127.0.0.1",
          "credentials": {
              "authLoginDomain": "",
              "userName": "administrator",
              "password": "password"}}

one_view_client = OneViewClient(config)

metrics_configuration = {
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

updated_metrics_configuration = one_view_client.metrics.update_configuration(metrics_configuration)
pprint(updated_metrics_configuration)
