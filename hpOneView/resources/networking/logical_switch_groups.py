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


from hpOneView.resources.resource import Resource, ResourcePatchMixin


class LogicalSwitchGroups(ResourcePatchMixin, Resource):
    """
    Logical Switch Groups API client.

    Note:
        This resource is only available on C7000 enclosures.

    """
    URI = '/rest/logical-switch-groups'

    DEFAULT_VALUES = {
        '200': {"type": "logical-switch-group"},
        '300': {"type": "logical-switch-groupV300"},
        '500': {"type": "logical-switch-groupV300"},
        '600': {"type": "logical-switch-groupV4"},
        '800': {"type": "logical-switch-groupV4"}
    }

    def __init__(self, connection, data=None):
        super(LogicalSwitchGroups, self).__init__(connection, data)
