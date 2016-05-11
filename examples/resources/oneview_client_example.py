# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import range
from future import standard_library

standard_library.install_aliases()

from hpOneView.oneview_client import OneViewClient

# example
config = {"ip": "172.16.102.59",
          "credentials": {
              "authLoginDomain": "",
              "userName": "administrator",
              "password": ""}}

ov = OneViewClient(config)

ov.fc_networks.get_all()
