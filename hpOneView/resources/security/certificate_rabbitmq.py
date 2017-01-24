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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()


from hpOneView.resources.resource import ResourceClient


class CertificateRabbitMQ(object):
    URI = '/rest/certificates/client/rabbitmq'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def generate(self, information, timeout=-1):
        """
        Generates a self signed certificate or an internal CA signed certificate for RabbitMQ clients.

        Args:
            information (dict): Information to generate the certificate for RabbitMQ clients.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: RabbitMQ certificate generated
        """
        return self._client.create(information, timeout=timeout)

    def get(self, alias_name):
        """
        Retrieves the base-64 encoded certificate associated with the RabbitMQ user.

        Args:
            alias_name: Key pair associated with the RabbitMQ

        Returns:
            dict: RabbitMQ certificate
        """
        return self._client.get(alias_name)

    def get_key_pair(self, alias_name):
        """
        Retrieves the public and private key pair associated with the specified alias name.

        Args:
            alias_name: Key pair associated with the RabbitMQ

        Returns:
            dict: RabbitMQ certificate
        """
        uri = self.URI + "/keypair/" + alias_name
        return self._client.get(uri)

    def get_keys(self, alias_name, key_format):
        """
        Retrieves the contents of PKCS12 file in the format specified.
        This PKCS12 formatted file contains both the certificate as well as the key file data.
        Valid key formats are Base64 and PKCS12.

        Args:
            alias_name: Key pair associated with the RabbitMQ
            key_format: Valid key formats are Base64 and PKCS12.
        Returns:
            dict: RabbitMQ certificate
        """
        uri = self.URI + "/keys/" + alias_name + "?format=" + key_format
        return self._client.get(uri)
