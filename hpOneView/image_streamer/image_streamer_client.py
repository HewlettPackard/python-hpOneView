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

from hpOneView.connection import connection
from hpOneView.image_streamer.resources.plan_scripts import PlanScripts
from hpOneView.image_streamer.resources.build_plans import BuildPlans


class ImageStreamerClient(object):
    def __init__(self, ip, session_id, api_version):
        self.__connection = connection(ip, api_version)
        self.__connection.set_session_id(session_id)
        self.__plan_scripts = None
        self.__build_plans = None

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

    @property
    def build_plans(self):
        """
        Gets the Build Plans API client.

        Returns:
            BuildPlans:
        """
        if not self.__build_plans:
            self.__build_plans = BuildPlans(self.__connection)
        return self.__build_plans
