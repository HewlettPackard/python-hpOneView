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

from urllib.parse import quote
from hpOneView.common import get_members
from hpOneView.activity import activity
from hpOneView.exceptions import HPOneViewUnknownType


class ResourceClient(object):
    """
    This class implements common functions for HpOneView API rest
    """

    def __init__(self, con, uri):
        self._connection = con
        self._uri = uri
        self._activity = activity(con)

    def get_members(self, uri):
        # TODO: common is deprecated, refactor get_members implementation
        return get_members(self._connection.get(uri))

    def get_all(self, start=0, count=-1, filter='', query='', sort='', view=''):
        """
        the use of optional parameters are described here:
        http://h17007.www1.hpe.com/docs/enterprise/servers/oneview2.0/cic-api/en/api-docs/current/index.html

        Known issues:
            - Pass "'" inside a parameter is not supported by One View API

        Returns: a dictionary with requested data

        """
        if filter:
            filter = "&filter=" + quote(filter)

        if query:
            query = "&query=" + quote(query)

        if sort:
            sort = "&sort=" + quote(sort)

        if view:
            view = "&view=" + quote(view)

        uri = "{0}?start={1}&count={2}{3}{4}{5}{6}".format(self._uri, start, count, filter, query, sort, view)
        return self.get_members(uri)

    def delete(self, resource, force=False, blocking=True, verbose=False, timeout=60):
        if isinstance(resource, dict):
            if 'uri' in resource and resource['uri']:
                uri = resource['uri']
            else:
                raise HPOneViewUnknownType('Unknown object type')
        else:
            uri = self._uri + "/" + resource

        if force:
            uri += '?force=True'

        task, body = self._connection.delete(uri)
        if blocking:
            task = self._activity.wait4task(task, tout=timeout, verbose=verbose)

        return task

    def get_schema(self):
        return self._connection.get(self._uri + '/schema')

    def get(self, id):
        return self._connection.get(self._uri + '/' + id)

    def update(self, resource, blocking=True):
        task, body = self._connection.put(resource['uri'], resource)
        if blocking:
            return self.__wait_for_task(task, 60)
        return task

    def create(self, resource, blocking=True):
        task, entity = self._connection.post(self._uri, resource)
        if blocking:
            return self.__wait_for_task(task, 60)
        return task

    def __wait_for_task(self, task, tout=60):
        task = self._activity.wait4task(task, tout=tout, verbose=False)
        if 'type' in task and task['type'].startswith('Task'):
            resource = self._activity.get_task_associated_resource(task)
            entity = self._connection.get(resource['resourceUri'])
            return entity

    def get_by(self, field, value):
        """
        This function uses get_all passing a filter
        The search is case insensitive
        Args:
            field: field name to filter
            value: value to filter

        Returns: dict

        """
        filter = filter = "\"'{0}'='{1}'\"".format(field, value)
        return self.get_all(filter=filter)
