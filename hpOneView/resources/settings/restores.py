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


class Restores(object):
    """
    Restore API client for initiate a restore of an appliance and to get the status of the restore operation.
    """
    URI = '/rest/restores'

    DEFAULT_VALUES = {
        '200': {"type": "RESTORE"},
        '300': {"type": "RESTORE"}
    }

    def __init__(self, con):
        self._client = ResourceClient(con, self.URI)

    def get_all(self):
        """
        Retrieve the status of any current appliance restore.

        Returns:
            list: A collection of restore status, but there will be at most one restore status. The status for
            the last restore will be returned if there has been a restore.
        """
        return self._client.get_all()

    def get(self, id_or_uri):
        """
        Retrieves the status of the specified restore operation.

        Args:
            id_or_uri: ID or URI of the Restore.

        Returns:
            dict: Restore
        """
        return self._client.get(id_or_uri)

    def get_by(self, field, value):
        """
        Gets all Restores that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of Restores.
        """
        return self._client.get_by(field, value)

    def get_failure(self):
        """
        Retrieves the result of an appliance restore operation after it has completed.

        The restore result remains valid until a user logs in. After a user logs in, the restore result will be reset.
        This rest request will return only the valid result after restore has completed and before a user logs in.


        Returns:
            dict: Restore Result
        """
        uri = self.URI + '/failure'
        return self._client.get(uri)

    def restore(self, resource, timeout=-1):
        """
        Starts a restore operation with the specified backup file. The backup must be uploaded to the appliance
        prior to running this command. Only one restore can run at a time.

        Args:
            resource (dict): Config to restore.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Restore.

        """
        return self._client.create(resource, timeout=timeout, default_values=self.DEFAULT_VALUES)
