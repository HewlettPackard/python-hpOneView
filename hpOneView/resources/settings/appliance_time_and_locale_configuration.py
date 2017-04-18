# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2017) Hewlett Packard Enterprise Development LP
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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

from hpOneView.resources.resource import ResourceClient


class ApplianceTimeAndLocaleConfiguration(object):
    """
    ApplianceTimeAndLocaleConfiguration API client.

    """
    URI = '/rest/appliance/configuration/time-locale'

    DEFAULT_VALUES = {
        '200': {"type": "TimeAndLocale"},
        '300': {"type": "TimeAndLocale"}
    }

    def __init__(self, con):
        self._client = ResourceClient(con, self.URI)

    def get(self):
        """
        Gets the appliance time and locale configuration.

        Returns:
            dict: ApplianceTimeAndLocaleConfiguration
        """
        return self._client.get(self.URI)

    def update(self, resource, timeout=-1):
        """
        Updates the appliance time and locale configuration.

        Args:
            resource (dict): Object to update.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Updated appliance time and locale configuration.

        """
        return self._client.create(resource, timeout=timeout, default_values=self.DEFAULT_VALUES)
