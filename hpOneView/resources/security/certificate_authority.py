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


class CertificateAuthority(object):
    """
    Certificate Authority API client.
    """

    URI = '/rest/certificates/ca'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get(self):
        """
        Retrieves the certificate of the internal CA in the form of a string.

        Returns:
            str: The Internal CA Certificate.
        """
        return self._client.get(self.URI)

    def get_crl(self):
        """
        Retrieves the contents of the CRL file maintained by the internal CA; in Base-64 encoded format, in the form
        of a string.

        Returns:
            str: The Certificate Revocation List
        """
        crl_url = self.URI + "/crl"
        return self._client.get(crl_url)

    def delete(self, alias_name, timeout=-1):
        """
        Revokes a certificate signed by the internal CA. If client certificate to be revoked is RabbitMQ_readonly,
        then the internal CA root certificate, RabbitMQ client certificate and RabbitMQ server certificate will be
        regenerated. This will invalidate the previous version of RabbitMQ client certificate and the RabbitMQ server
        will be restarted to read the latest certificates.

        Args:
            alias_name (str): Alias name.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.
        """
        uri = self.URI + "/" + alias_name
        return self._client.delete(uri, timeout=timeout)
