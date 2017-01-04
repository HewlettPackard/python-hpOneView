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
from hpOneView.resources.resource import ResourceClient
from hpOneView.resources.security.certificate_rabbitmq import CertificateRabbitMQ


class CertificateRabbitMQTest(TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._certificate_rabbitmq = CertificateRabbitMQ(self.connection)

    @mock.patch.object(ResourceClient, 'create')
    def test_generate_called_once_with_defaults(self, mock_create):
        information = {
            "commonName": "default",
            "type": "RabbitMqClientCertV2"
        }
        self._certificate_rabbitmq.generate(information)
        mock_create.assert_called_once_with(information, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_alias_name_called_once(self, mock_get):
        alias_name = 'default'
        self._certificate_rabbitmq.get_alias_name(alias_name)
        uri = "/rest/certificates/client/rabbitmq/" + alias_name
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_key_pair_called_once(self, mock_get):
        alias_name = 'default'
        self._certificate_rabbitmq.get_key_pair(alias_name)
        uri = "/rest/certificates/client/rabbitmq/keypair/" + alias_name
        mock_get.assert_called_once_with(uri)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_keys_called_once(self, mock_get):
        alias_name = 'default'
        key_format = 'Base64'
        self._certificate_rabbitmq.get_keys(alias_name, key_format)
        uri = "/rest/certificates/client/rabbitmq/keys/" + alias_name + "?format=" + key_format
        mock_get.assert_called_once_with(uri)
