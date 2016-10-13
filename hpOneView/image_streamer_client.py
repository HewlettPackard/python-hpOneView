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
"""
image_streamer_client.py
~~~~~~~~~~~~~~~~~~

This module implements a common client for HPE Image Streamer REST API.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

__title__ = 'Image Streamer Client'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP'
__license__ = 'MIT'
__status__ = 'Development'

import json

from hpOneView.connection import connection
from hpOneView.resources.image_streamer.plan_scripts import PlanScripts


IMAGE_STREAMER_CLIENT_INVALID_PROXY = 'Invalid Proxy format'
IMAGE_STREAMER_DEFAULT_API_VERSION = 300


class ImageStreamerClient(object):
    def __init__(self, config):
        self.__connection = connection(config["ip"], config.get('api_version', IMAGE_STREAMER_DEFAULT_API_VERSION))
        self.__set_proxy(config)
        self.__connection.login(config["credentials"])
        self.__plan_scripts = None
        

    @classmethod
    def from_json_file(cls, file_name):
        """
        Construct ImageStreamerClient using a json file.

        Args:
            file_name: json full path.

        Returns:
            ImageStreamerClient:
        """
        with open(file_name) as json_data:
            config = json.load(json_data)

        return cls(config)

    def __set_proxy(self, config):
        """
        Set proxy if needed
        Args:
            config: Config dict
        """
        if "proxy" in config and config["proxy"]:
            proxy = config["proxy"]
            splitted = proxy.split(':')
            if len(splitted) != 2:
                raise ValueError(IMAGE_STREAMER_CLIENT_INVALID_PROXY)

            proxy_host = splitted[0]
            proxy_port = int(splitted[1])
            self.__connection.set_proxy(proxy_host, proxy_port)

    @property
    def api_version(self):
        """
        Gets the Image Streamer API Version.

        Returns:
            int: API Version.
        """
        return self.__connection._apiVersion

    @property
    def connection(self):
        """
        Gets the underlying HPE Image Streamer connection used by the ImageStreamerClient.

        Returns:
            connection:
        """
        return self.__connection

    @property
    def plan_scripts(self):
        """
        Gets the Plan Scripts API client.

        Returns:
            PlanScripts:
        """
        if not self.__plan_scripts:
            self.__plan_scripts = PlanScripts(self.__connection)
        return self.__plan_scripts
