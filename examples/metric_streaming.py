# -*- coding: utf-8 -*-

from pprint import pprint

from config_loader import try_load_from_file
from hpOneView.oneview_client import OneViewClient

config = {
    "ip": "172.16.102.59",
    "credentials": {
        "authLoginDomain": "",
        "userName": "administrator",
        "password": ""
    }
}
# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

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

# Configure metric relay for server-hardware, enclosures and power-devices.
print("Configure metric streaming")
updated_metrics_configuration = oneview_client.metric_streaming.update_configuration(metrics_configuration)
pprint(updated_metrics_configuration)

# Get current relay configuration
print("Get current configuration")
current_configuration = oneview_client.metric_streaming.get_configuration()
pprint(current_configuration)

# Gets the list of all supported metrics and resource types.
print("Gets the list of all supported metrics and resource types")
supported_metrics = oneview_client.metric_streaming.get_capability()
pprint(supported_metrics)
