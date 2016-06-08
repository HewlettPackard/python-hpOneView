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
