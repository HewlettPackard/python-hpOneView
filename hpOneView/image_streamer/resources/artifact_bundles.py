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


from hpOneView.resources.resource import ResourceClient, extract_id_from_uri


class ArtifactBundles(object):

    URI = '/rest/artifact-bundles'
    DEPLOYMENT_GROUPS_URI = '/rest/deployment-groups/'
    BACKUPS_PATH = '/rest/artifact-bundles/backups'
    BACKUP_ARCHIVE_PATH = '/rest/artifact-bundles/backups/archive'
    STOP_CREATION_PATH = '/stopArtifactCreate'
    DOWNLOAD_PATH = '/rest/artifact-bundles/download'

    DEFAULT_VALUES = {
        '300': {"type": "ArtifactsBundle"}
    }

    def __init__(self, con):
        self._client = ResourceClient(con, self.URI)
        self.__default_values = {
            'type': 'ArtifactsBundle',
        }

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a list of Artifacts Bundle based on optional sorting and filtering, and constrained by start and count
        parameters.

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all items.

                The actual number of items in the response might differ from the requested
                count if the sum of start and count exceeds the total number of items.
            filter (list or str):
                A general filter/query string to narrow the list of items returned. The
                default is no filter; all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.

        Returns:
            list: A list of Artifacts Bundle.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def get(self, id_or_uri):
        """
        Retrieves the overview details for the selected Artifact Bundle as per the selected attributes.

        Args:
            id_or_uri: ID or URI of the Artifact Bundle.

        Returns:
            dict: The Artifact Bundle.
        """
        return self._client.get(id_or_uri)

    def get_by(self, field, value):
        """
        Gets all of the Artifacts Bundle resources that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: The Artifacts Bundle.
        """
        return self._client.get_by(field, value)

    def get_by_name(self, name):
        """
        Gets an Artifact Bundle by name.

        Args:
            name: Name of the Artifact Bundle.

        Returns:
            dict: The Artifact Bundle.
        """
        return self._client.get_by_name(name)

    def get_all_backups(self):
        """
        Get all Backups for Artifact Bundle.

        Returns:
            list: A list of Backups for Artifacts Bundle.
        """
        return self._client.get_collection(id_or_uri=self.BACKUPS_PATH)

    def get_backup(self, id_or_uri):
        """
        Get the details for the backup from an Artifact Bundle.

        Args:
            id_or_uri: ID or URI of the Artifact Bundle.

        Returns:
            Dict: Backup for an Artifacts Bundle.
        """
        uri = self.BACKUPS_PATH + '/' + extract_id_from_uri(id_or_uri)
        return self._client.get(id_or_uri=uri)

    def download_archive_artifact_bundle(self, id_or_uri, file_path):
        """
        Downloads an archive for the Artifact Bundle.

        Args:
            id_or_uri: ID or URI of the Artifact Bundle.
            file_path(str): Destination file path.

        Returns:
            bool: Successfully downloaded.
        """

        uri = self.BACKUP_ARCHIVE_PATH + '/' + extract_id_from_uri(id_or_uri)
        return self._client.download(uri, file_path)

    def download_artifact_bundle(self, id_or_uri, file_path):
        """
        Download the Artifact Bundle.

        Args:
            id_or_uri: ID or URI of the Artifact Bundle.
            file_path(str): Destination file path.

        Returns:
            bool: Successfully downloaded.
        """
        uri = self.DOWNLOAD_PATH + '/' + extract_id_from_uri(id_or_uri)
        return self._client.download(uri, file_path)

    def create_backup(self, resource, timeout=-1):
        """
        Creates a backup bundle with all the artifacts present on the appliance. At any given point only one backup
        bundle will exist on the appliance.

        Args:
            resource (dict): Deployment Group to create the backup.
            timeout:
                Timeout in seconds. Waits for task completion by default. The timeout does not abort the operation in
                OneView, it just stops waiting for its completion.

        Returns:
            dict: A Deployment Group associated with the Artifact Bundle backup.
        """
        return self._client.create(resource, uri=self.BACKUPS_PATH, timeout=timeout)

    def upload_bundle_from_file(self, file_path):
        """
        Restore an Artifact Bundle from a backup file.

        Args:
            file_path (str): The File Path to restore the Artifact Bundle.

        Returns:
            dict: Artifact bundle.
        """
        return self._client.upload(file_path)

    def upload_backup_bundle_from_file(self, file_path, deployment_groups_id_or_uri):
        """
        Restore an Artifact Bundle from a backup file.

        Args:
            file_path (str): The File Path to restore the Artifact Bundle.
            deployment_groups_id_or_uri: ID or URI of the Deployment Groups.

        Returns:
            dict: Deployment group.
        """
        deployment_groups_uri = deployment_groups_id_or_uri

        if self.DEPLOYMENT_GROUPS_URI not in deployment_groups_id_or_uri:
            deployment_groups_uri = self.DEPLOYMENT_GROUPS_URI + deployment_groups_id_or_uri

        uri = self.BACKUP_ARCHIVE_PATH + "?deploymentGrpUri=" + deployment_groups_uri

        return self._client.upload(file_path, uri)

    def create(self, resource, timeout=-1):
        """
        Creates an Artifact Bundle.

        Args:
            resource (dict): Object to create.
            timeout:
                Timeout in seconds. Waits for task completion by default. The timeout does not abort the operation
                in OneView, it just stops waiting for its completion.

        Returns:
            dict: Created resource.
        """
        return self._client.create(resource, timeout=timeout)

    def delete(self, resource, timeout=-1):
        """
        Deletes an Artifact Bundle.

        Args:
            resource(str, dict):
                Accept either the resource id  or the entire resource.
            timeout:
                Timeout in seconds. Waits for task completion by default. The timeout does not abort the operation in
                OneView, it just stops waiting for its completion.

        Returns:
            bool: Indicates if the resource was successfully deleted.
        """
        return self._client.delete(resource, timeout=timeout)

    def update(self, resource, timeout=-1):
        """
        Updates only name for the Artifact Bundle.

        Args:
            resource (dict): Object to update.
            timeout:
                Timeout in seconds. Waits for task completion by default. The timeout does not abort the operation
                in OneView, it just stops waiting for its completion.

        Returns:
            dict: Updated resource.
        """
        return self._client.update(resource, timeout=timeout, default_values=self.DEFAULT_VALUES)

    def extract_bundle(self, resource, timeout=-1):
        """
        Extracts the existing bundle on the appliance and creates all the artifacts.

        Args:
            resource (dict): Artifact Bundle to extract.
            timeout:
                Timeout in seconds. Waits for task completion by default. The timeout does not abort the operation in
                OneView, it just stops waiting for its completion.

        Returns:
            dict: The Artifact Bundle.
        """
        return self._client.update(resource, timeout=timeout, custom_headers={"Content-Type": "text/plain"})

    def extract_backup_bundle(self, resource, timeout=-1):
        """
        Extracts the existing backup bundle on the appliance and creates all the artifacts.

        Args:
            resource (dict): Deployment Group to extract.
            timeout:
                Timeout in seconds. Waits for task completion by default. The timeout does not abort the operation in
                OneView, it just stops waiting for its completion.

        Returns:
            dict: A Deployment Group associated with the Artifact Bundle backup.
        """
        return self._client.update(resource, uri=self.BACKUP_ARCHIVE_PATH, timeout=timeout)

    def stop_artifact_creation(self, id_or_uri, task_uri):
        """
        Stops creation of the selected Artifact Bundle.

        Args:
            id_or_uri: ID or URI of the Artifact Bundle.
            task_uri: Task URI associated with the Artifact Bundle.

        Returns:
            string:
        """
        data = {
            "taskUri": task_uri
        }

        uri = self.URI + '/' + extract_id_from_uri(id_or_uri) + self.STOP_CREATION_PATH

        return self._client.update(data, uri=uri)
