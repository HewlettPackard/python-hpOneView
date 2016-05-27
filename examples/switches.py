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

# Get Statistics
print("Get a switch statistics")
try:
    switch_statistics = oneview_client.switches.get_statistics("aa94cd9e-6e63-4ac7-b7ae-8dfe77474aed")
    pprint(switch_statistics)
except HPOneViewException as e:
    print(e.msg['message'])

# Get Statistics with port_name
print("Get a switch statistics with portName")
try:
    switch_statistics = oneview_client.switches.get_statistics("aa94cd9e-6e63-4ac7-b7ae-8dfe77474aed", "X1")
    pprint(switch_statistics)
except HPOneViewException as e:
    print(e.msg['message'])