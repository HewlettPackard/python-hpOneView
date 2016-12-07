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

from hpOneView.image_streamer.image_streamer_client import ImageStreamerClient
from hpOneView.image_streamer.resources.plan_scripts import PlanScripts
from hpOneView.image_streamer.resources.golden_images import GoldenImages
from hpOneView.image_streamer.resources.build_plans import BuildPlans
from hpOneView.image_streamer.resources.os_volumes import OsVolumes
from hpOneView.image_streamer.resources.deployment_plans import DeploymentPlans


class ImageStreamerClientTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.session_id = 'LTU1NzIzMDMxMjIxcsgLtu5d6Q_oydNqaO2oWuZz5Xj7L7cc'
        self._client = ImageStreamerClient(self.host, self.session_id, 300)

    def test_connection_has_right_host(self):
        self.assertEqual(self._client.connection.get_host(), self.host)

    def test_connection_has_right_session_id(self):
        self.assertEqual(self._client.connection.get_session_id(), self.session_id)

    def test_connection_has_session(self):
        self.assertEqual(self._client.connection.get_session(), True)

    def test_golden_images_has_right_type(self):
        self.assertIsInstance(self._client.golden_images, GoldenImages)

    def test_golden_images_lazy_loading(self):
        resource = self._client.golden_images
        self.assertEqual(resource, self._client.golden_images)

    def test_plan_scripts_has_right_type(self):
        self.assertIsInstance(self._client.plan_scripts, PlanScripts)

    def test_plan_scripts_lazy_loading(self):
        resource = self._client.plan_scripts
        self.assertEqual(resource, self._client.plan_scripts)

    def test_build_plans_has_right_type(self):
        self.assertIsInstance(self._client.build_plans, BuildPlans)

    def test_build_plans_lazy_loading(self):
        resource = self._client.build_plans
        self.assertEqual(resource, self._client.build_plans)

    def test_os_volumes_has_right_type(self):
        self.assertIsInstance(self._client.os_volumes, OsVolumes)

    def test_os_volumes_lazy_loading(self):
        resource = self._client.os_volumes
        self.assertEqual(resource, self._client.os_volumes)

    def test_deployment_plans_has_right_type(self):
        self.assertIsInstance(self._client.deployment_plans, DeploymentPlans)

    def test_deployment_plans_lazy_loading(self):
        resource = self._client.deployment_plans
        self.assertEqual(resource, self._client.deployment_plans)
