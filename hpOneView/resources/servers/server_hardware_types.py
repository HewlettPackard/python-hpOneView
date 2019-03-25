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

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library


standard_library.install_aliases()


from hpOneView.resources.resource import Resource, ensure_resource_client


class ServerHardwareTypes(Resource):
    """
    The server hardware types resource is a representation/abstraction of a physical server managed by the appliance.
    It defines capabilities and settings that can be used in a server profile.

    """
    URI = '/rest/server-hardware-types'

    def __init__(self, connection, data=None):
        super(ServerHardwareTypes, self).__init__(connection, data)

    @ensure_resource_client
    def update(self, data, timeout=-1, force=False):
        """
        Updates one or more attributes for a server hardware type resource.
        Args:
            data (dict): Object to update.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
            force: Flag to force the operation.
        Returns:
            dict: Updated server hardware type.
        """
        uri = self.data["uri"]
        self.data = self._helper.update(data, uri=uri, timeout=timeout, force=force)

        return self
