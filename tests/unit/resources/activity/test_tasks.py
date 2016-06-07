# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###

from unittest import TestCase

import mock

from hpOneView.connection import connection
from hpOneView.resources.activity.tasks import Tasks
from hpOneView.resources.resource import ResourceClient


class TasksTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._client = Tasks(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all(self, mock_get):
        self._client.get_all(fields='parentTaskUri,owner,name',
                             filter="\"taskState='Running'&filter=associatedResource.resourceCatgory='appliance'\"",
                             sort='name:ascending',
                             view='day')

        mock_get.assert_called_once_with(count=-1, fields='parentTaskUri,owner,name',
                                         filter='"taskState=\'Running\'&filter=associatedResource'
                                                '.resourceCatgory=\'appliance\'"',
                                         query='', sort='name:ascending', start=0, view='day')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_specific(self, mock_get):
        self._client.get('35323930-4936-4450-5531-303153474820')
        mock_get.assert_called_once_with('35323930-4936-4450-5531-303153474820')
