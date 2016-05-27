# -*- coding: utf-8 -*-

from pprint import pprint
from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException

config = {
    "ip": "172.16.102.59",
    "credentials": {
        "authLoginDomain": "",
        "userName": "administrator",
        "password": ""
    }
}

oneview_client = OneViewClient(config)

# Get by Uri
print("Get a switch statistics")
try:
    switch_statistics = oneview_client.switches.get_statistics("aa94cd9e-6e63-4ac7-b7ae-8dfe77474aed")
    pprint(switch_statistics)
except HPOneViewException as e:
    print(e.msg['message'])
