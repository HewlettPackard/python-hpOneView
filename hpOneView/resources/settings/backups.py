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

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()


from hpOneView.resources.resource import ResourceClient


class Backups(object):
    """
    Backups API client.
    """

    URI = '/rest/backups'

    def __init__(self, con):
        self._client = ResourceClient(con, self.URI)

    def get_all(self):
        """
        Retrieves the details for any current appliance backup. Only one backup file is present on the appliance at any
        time.

        Returns:
            list: A list of Backups.
        """
        return self._client.get_collection(self.URI)

    def get(self, id_or_uri):
        """
        Gets the details of the specified backup.

        Args:
            id_or_uri: ID or URI of the backup

        Returns:
            dict: Details of the specified backup.
        """
        return self._client.get(id_or_uri)

    def create(self, timeout=-1):
        """
        Starts backing up the appliance. After completion, the backup file must be downloaded and saved off-appliance.
        Appliance backups can be started at any time, and do not require any special setup to prepare the appliance for
        the backup.

        Args:
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Details of the created backup.

        """
        return self._client.create_with_zero_body(timeout=timeout)

    def download(self, id_or_uri, file_path):
        """
        Downloads a backup archive previously created on the appliance. Uploaded backup files cannot be downloaded.

        Args:
            id_or_uri: ID or URI of the Artifact Bundle.
            file_path(str): Destination file path.

        Returns:
            bool: Successfully downloaded.
        """
        return self._client.download(id_or_uri, file_path)

    def upload(self, file_path):
        """
        Uploads an appliance backup file in preparation of a restore. Any existing backup on the appliance is removed.

        After the backup file is uploaded and validated, its details are returned. The URI of the backup can be used to
        start a restore.

        Args:
            file_path (str): The local backup filepath

        Returns:
            dict: Details of the uploaded backup.
        """
        return self._client.upload(file_path)

    def get_config(self):
        """
        Retrieves the details of the backup configuration for the remote server and automatic backup schedule.

        Args:
            id_or_uri: ID or URI of the backup

        Returns:
            dict: Details of the backup configuration for the remote server and automatic backup schedule.
        """
        return self._client.get('config')

    def update_config(self, config, timeout=-1):
        """
        Updates the remote server configuration and the automatic backup schedule for backup.

        Args:
            config (dict): Object to update.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Backup details.

        """
        return self._client.update(config, uri=self.URI + "/config", timeout=timeout)

    def update_remote_archive(self, save_uri, timeout=-1):
        """
        Saves a backup of the appliance to a previously-configured remote location.

        Args:
            save_uri (dict): The URI for saving the backup to a previously configured location.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Backup details.

        """
        return self._client.update_with_zero_body(uri=save_uri, timeout=timeout)
