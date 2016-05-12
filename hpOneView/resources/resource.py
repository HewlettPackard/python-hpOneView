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

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()

__title__ = 'fc-networks'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2016) Hewlett Packard Enterprise ' \
                ' Development LP'
__license__ = 'MIT'
__status__ = 'Development'

from hpOneView.common import get_members
from hpOneView.activity import activity


class ResourceClient(object):
    def __init__(self, con, uri):
        self._connection = con
        self._uri = uri
        self._activity = activity(con)

    def get_members(self, uri):
        return get_members(self._connection.get(uri))

    def get_all(self, start=0, count=9999999, filter='', sort=''):
        uri = "{0}?start={1}&count={2}{3}{4}".format(self._uri, start, count, filter, sort)
        return self.get_members(uri)

    def delete(self, obj, blocking=True, verbose=False):

        if obj is dict:
            uri = dict['uri']
        else:
            uri = self._uri + "/" + obj

        task, body = self._connection.delete(uri)
        if blocking:
            task = self._activity.wait4task(task, verbose=verbose)
        return task

    def get_schema(self):
        return self._connection.get(self._uri + '/schema')

    def get(self, id):
        return self._connection.get(self._uri + '/' + id)

    def update(self, dict, blocking=True, verbose=False, timeout=60):
        # TODO: Create uri suffix
        task, body = self._connection.put(self._uri + '/' + id, dict)
        if blocking is True:
            task = self._activity.wait4task(task, tout=timeout, verbose=verbose)
        return task
