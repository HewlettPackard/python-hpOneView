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

import unittest

import mock

from hpOneView.connection import connection
from hpOneView.exceptions import HPOneViewException
from hpOneView.resources.settings.firmware_bundles import FirmwareBundles
from hpOneView.resources.task_monitor import TaskMonitor


class FirmwareBundlesTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._firmware_bundles = FirmwareBundles(self.connection)

    @mock.patch.object(TaskMonitor, 'wait_for_task')
    @mock.patch.object(connection, 'post_multipart')
    def test_upload(self, mock_upload, mock_wait_task):
        firmware_path = "test/SPPgen9snap6.2015_0405.81.iso"
        response = mock.MagicMock(status=200)

        body = {
            "category": "tasks",
            "type": "TaskResourceV2",
            "associatedResource": {
                "resourceUri": "/rest/associatedresourceuri"
            }}

        mock_upload.return_value = response, body
        mock_wait_task.return_value = {}

        self._firmware_bundles.upload(firmware_path)
        mock_upload.assert_called_once_with('/rest/firmware-bundles', None, firmware_path,
                                            'SPPgen9snap6.2015_0405.81.iso')

        mock_wait_task.assert_called_once_with(body, -1)

    @mock.patch.object(TaskMonitor, 'wait_for_task')
    @mock.patch.object(connection, 'post_multipart')
    def test_upload_should_raise_exception(self, mock_upload, mock_wait_task):
        firmware_path = "test/SPPgen9snap6.2015_0405.81.iso"

        response = mock.MagicMock(status=400)

        body = {"message": "The file you are attempting to upload is empty."}

        mock_upload.return_value = response, body

        try:
            self._firmware_bundles.upload(firmware_path)
        except HPOneViewException as e:
            self.assertEqual(e.msg, "The file you are attempting to upload is empty.")
            mock_wait_task.assert_not_called()
        else:
            self.fail("Expected exception was not raised")
