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

# Get Interconnects Statistics
print("Get a interconnect statistics")
try:
    interconnect_statistics = oneview_client.interconnects.get_statistics("ad28cf21-8b15-4f92-bdcf-51cb2042db32")
    pprint(interconnect_statistics['moduleStatistics'])
except HPOneViewException as e:
    print(e.msg['message'])
