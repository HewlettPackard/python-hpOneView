from pprint import pprint

from hpOneView.oneview_client import OneViewClient

config = {"ip": "127.0.0.1",
          "credentials": {
              "authLoginDomain": "",
              "userName": "administrator",
              "password": "password"}}

one_view_client = OneViewClient(config)
interconnects_id = 'ad28cf21-8b15-4f92-bdcf-51cb2042db32'
statistics = one_view_client.interconnects.get_statistics(interconnects_id)
pprint(statistics)
