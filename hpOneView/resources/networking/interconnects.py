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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

__title__ = 'Interconnects'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2016) Hewlett Packard Enterprise ' \
                ' Development LP'
__license__ = 'MIT'
__status__ = 'Development'

from hpOneView.resources.resource import ResourceClient


class Interconnects(object):
    URI = '/rest/interconnects'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_statistics(self, interconnect_id, port_name=''):
        """
        Gets the statistics from an interconnect.

        Args:
            interconnect_id: The interconnect id
            port_name (str): A specific port name of an interconnect

        Returns:
             dict: The statistics for the interconnect that matches id
        """
        uri = "/rest/interconnects/%s/statistics" % interconnect_id

        if port_name:
            uri = uri + "/" + port_name

        return self._client.get(uri)

    def get_subport_statistics(self, interconnect_id, port_name, subport_number):
        """
        Gets the subport statistics on an interconnect.

        Args:
            interconnect_id: The interconnect id
            port_name (str): A specific port name of an interconnect
            subport_number (int): The subport

        Returns:
             dict: The statistics for the interconnect that matches id, port_name and subport_number
        """
        uri = "/rest/interconnects/%s/statistics/%s/subport/%i" % (interconnect_id, port_name, subport_number)
        return self._client.get(uri)
