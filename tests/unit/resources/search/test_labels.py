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

import unittest

import mock

from hpOneView.connection import connection
from hpOneView.resources.search.labels import Labels
from hpOneView.resources.resource import ResourceClient


class LabelsTest(unittest.TestCase):

    RESOURCE_LABEL = dict(
        uri="/rest/labels/resources/rest/resource/uri",
        resourceUri="/rest/resource/uri",
        type="ResourceLabels",
        category="the-resource-category",
        created="2014-03-31T02:08:27.884Z",
        modified="2014-03-31T02:08:27.884Z",
        eTag=None,
        labels=[
            dict(name="new label", uri=None),
            dict(name="old label", uri="/rest/labels/3")
        ]
    )

    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._resource = Labels(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._resource.get_all(2, 500, filter, sort)
        mock_get_all.assert_called_once_with(start=2, count=500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_called_once(self, mock_get):
        label_uri = "/rest/labels/2"
        self._resource.get(id_or_uri=label_uri)
        mock_get.assert_called_once_with(id_or_uri=label_uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_resource(self, mock_get):
        resource_uri = "/rest/enclosures/09SGH100X6J1"
        self._resource.get_by_resource(resource_uri=resource_uri)

        expected_uri = Labels.URI + Labels.RESOURCES_PATH + '/' + resource_uri
        mock_get.assert_called_once_with(id_or_uri=expected_uri)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_called_once(self, mock_create):
        resource = dict(
            resourceUri="/rest/enclosures/09SGH100X6J1",
            labels=["labelSample2", "enclosureDemo"]
        )

        self._resource.create(resource=resource)

        expected_uri = Labels.URI + Labels.RESOURCES_PATH
        mock_create.assert_called_once_with(uri=expected_uri, resource=resource)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_called_once(self, mock_update):
        self._resource.update(resource=self.RESOURCE_LABEL)
        mock_update.assert_called_once_with(resource=self.RESOURCE_LABEL)

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        self._resource.delete(resource=self.RESOURCE_LABEL)
        mock_delete.assert_called_once_with(resource=self.RESOURCE_LABEL, timeout=-1)
