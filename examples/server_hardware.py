# -*- coding: utf-8 -*-

from pprint import pprint
from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException
from config_loader import try_load_from_file

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

# Get Statistics with defaults
print("Get server-hardware statistics")
try:
    server_utilization = oneview_client.server_hardware.get_utilization("37333036-3831-584D-5131-303030333037")
    pprint(server_utilization)
except HPOneViewException as e:
    print(e.msg['message'])

# Get Statistics specifying parameters
print("Get server-hardware statistics specifying parameters")
try:
    server_utilization = oneview_client.server_hardware.get_utilization("37333036-3831-584D-5131-303030333037",
                                                                        fields='AveragePower',
                                                                        filter='startDate=2016-05-30T03:29:42.000Z',
                                                                        view='day')
    pprint(server_utilization)
except HPOneViewException as e:
    print(e.msg['message'])
