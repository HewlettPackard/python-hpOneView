# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2019) Hewlett Packard Enterprise Development LP
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


from hpOneView.resources.resource import Resource


class ConnectionTemplates(Resource):
    """
    Connection Templates API client.

    """
    URI = '/rest/connection-templates'

    DEFAULT_VALUES = {
        '200': {"type": "connection-template"},
        '300': {"type": "connection-template"},
        '500': {"type": "connection-template"},
        '600': {"type": "connection-template"},
        '800': {"type": "connection-template"}
    }

    def __init__(self, connection, data=None):
        super(ConnectionTemplates, self).__init__(connection, data)

    def get_default(self):
        """
        Gets the default network connection template. This is the default connection template used
        for construction of networks. Its value is copied when a new connection template is made.

        Returns:
            dict:
        """
        uri = self.URI + "/defaultConnectionTemplate"
        return self._helper.do_get(uri)
