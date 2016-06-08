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

# Get all, with default values
print("Get all enclosures")
enclosures = oneview_client.enclosures.get_all()
pprint(enclosures)

# Find an enclosure by name
print("Get enclosure by name")
enclosures = oneview_client.enclosures.get_by('name', 'OneViewSDK-Test-Enclosure')
if len(enclosures) > 0:
    enclosure = enclosures[0]
    print("Found enclosure by name: '%s'.\n  uri = '%s'" % (enclosure['name'], enclosure['uri']))
else:
    print("Enclosure not found.")

# Get Statistics with defaults
ENCLOSURE_ID = "09SGH102X6J1"

print("Get enclosure statistics")
try:
    enclosure_statistics = oneview_client.enclosures.get_utilization(ENCLOSURE_ID)
    pprint(enclosure_statistics)
except HPOneViewException as e:
    print(e.msg['message'])

# Get Statistics specifying parameters
print("Get enclosure statistics")
try:
    enclosure_statistics = oneview_client.enclosures.get_utilization(ENCLOSURE_ID,
                                                                     fields='AveragePower',
                                                                     filter='startDate=2016-05-30T03:29:42.000Z',
                                                                     view='day')
    pprint(enclosure_statistics)
except HPOneViewException as e:
    print(e.msg['message'])
