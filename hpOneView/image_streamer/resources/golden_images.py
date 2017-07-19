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
from hpOneView.resources.task_monitor import TaskMonitor
from urllib.parse import quote


class GoldenImages(object):
    URI = '/rest/golden-images'

    def __init__(self, con):
        self._client = ResourceClient(con, self.URI)
        self._task_monitor = TaskMonitor(con)
        self.__default_values = {
            'type': 'GoldenImage',
        }

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Retrieves a list of Golden Image resources as per the specified parameters.

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
            list: A list of Golden Images.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def create(self, resource, timeout=-1):
        """
        Creates a Golden Image resource from the deployed OS Volume as per the attributes specified.

        Args:
            resource (dict): Object to create.
            timeout:
                Timeout in seconds. Waits for task completion by default. The timeout does not abort the operation
                in OneView, it just stops waiting for its completion.

        Returns:
            dict: Golden Image created.
        """
        data = self.__default_values.copy()
        data.update(resource)
        return self._client.create(data, timeout=timeout)

    def upload(self, file_path, golden_image_info):
        """
        Adds a Golden Image resource from the file that is uploaded from a local drive. Only the .zip format file can
        be used for the upload.

        Args:
            file_path (str): File name to upload.
            golden_image_info (dict): Golden Image information.

        Returns:
            dict: Golden Image.
        """
        uri = "{0}?name={1}&description={2}".format(self.URI,
                                                    quote(golden_image_info.get('name', '')),
                                                    quote(golden_image_info.get('description', '')))

        return self._client.upload(file_path, uri)

    def download_archive(self, id_or_uri, file_path):
        """
        Download the details of the Golden Image capture logs, which has been archived based on the specific attribute
        ID.

        Args:
            id_or_uri: ID or URI of the Golden Image.
            file_path (str): File name to save the archive.

        Returns:
            bool: Success.
        """
        uri = self.URI + "/archive/" + extract_id_from_uri(id_or_uri)
        return self._client.download(uri, file_path)

    def download(self, id_or_uri, file_path):
        """
        Downloads the content of the selected Golden Image as per the specified attributes.

        Args:
            id_or_uri: ID or URI of the Golden Image.
            file_path(str): Destination file path.

        Returns:
            bool: Successfully downloaded.
        """
        uri = self.URI + "/download/" + extract_id_from_uri(id_or_uri)
        return self._client.download(uri, file_path)

    def get(self, id_or_uri):
        """
        Retrieves the overview details of the selected Golden Image as per the specified attributes.

        Args:
            id_or_uri: ID or URI of the Golden Image.

        Returns:
            dict: The Golden Image.
        """
        return self._client.get(id_or_uri)

    def update(self, resource, timeout=-1):
        """
        Updates the properties of the Golden Image.

        Args:
            resource (dict): Object to update.
            timeout:
                Timeout in seconds. Waits for task completion by default. The timeout does not abort the operation
                in OneView, it just stops waiting for its completion.

        Returns:
            dict: Updated resource.

        """
        return self._client.update(resource, timeout=timeout)

    def delete(self, resource, force=False, timeout=-1):
        """
        Deletes the Golden Image specified.

        Args:
            resource: dict object to delete
            force:
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Waits for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates if the resource was successfully deleted.

        """
        return self._client.delete(resource, force=force, timeout=timeout)

    def get_by(self, field, value):
        """
        Gets all Golden Images that match the filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of Golden Images.
        """
        return self._client.get_by(field, value)
