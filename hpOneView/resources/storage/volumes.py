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

INVALID_VOLUME_URI = "When no snapshot uri is provided, volume id or valume uri is required."


class Volumes(object):
    """
    Volumes API client.

    """

    URI = '/rest/storage-volumes'

    DEFAULT_VALUES_SNAPSHOT = {
        '200': {"type": "Snapshot"},
        '300': {"type": "Snapshot"},
        '500': {}
    }

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, filter='', sort=''):
        """
        Gets a paginated collection of managed volumes. The collection is based on optional
        sorting and filtering and is constrained by start and count parameters.

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
            list: A list of managed volumes.
        """
        return self._client.get_all(start, count, filter=filter, sort=sort)

    def get(self, id_or_uri):
        """
        Gets the managed volume.

        Args:
            id_or_uri: Can be either the volume ID or the volume URI.

        Returns:
            Managed volume.
        """
        return self._client.get(id_or_uri)

    def get_by(self, field, value):
        """
        Gets all managed volumes that matches the given filter.

        The search is case-insensitive.

        Args:
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: A list of managed volumes.
        """
        return self._client.get_by(field, value)

    def create(self, resource, timeout=-1):
        """
        Creates or adds a volume.

        There are six different methods to create the volume:

          1) Common = Storage System + Storage Pool
          2) Template = Storage Volume Template
          3) Common with snapshots = Storage System + Storage Pool + Snapshot Pool
          4) Management = Storage System + wwn
          5) Management by name = Storage System + Storage System Volume Name
          6) Snapshot = Snapshot Pool + Storage Pool + Snapshot.

          NOTE: Use numbers 4 and 5 to add a volume for management; it does not create new volumes.

        Args:
            resource (dict):
                Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Created or added resource.
        """
        return self._client.create(resource, timeout=timeout)

    def add_from_existing(self, resource, timeout=-1):
        """
        Adds a volume that already exists in the Storage system

        Args:
            resource (dict):
                Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Added resource.
        """
        uri = self.URI + "/from-existing"
        return self._client.create(resource, uri=uri, timeout=timeout)

    def create_from_snapshot(self, data, timeout=-1):
        """
        Creates a new volume on the storage system from a snapshot of a volume.
        A volume template must also be specified when creating a volume from a snapshot.

        The global setting "StorageVolumeTemplateRequired" controls whether or
        not root volume templates can be used to provision volumes.
        The value of this setting defaults to "false".
        If the value is set to "true", then only templates with an "isRoot" value of "false"
        can be used to provision a volume.

        Args:
            data (dict):
                Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Created data.
        """
        uri = self.URI + "/from-snapshot"
        return self._client.create(data, uri=uri, timeout=timeout)

    def update(self, resource, force=False, timeout=-1):
        """
        Updates properties of a volume.

        Reverts a volume to the specified snapshot.

        Args:
            resource (dict): Object to update.
            force:
                If set to true, the operation completes despite any problems with network connectivity or errors on
                the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stops waiting for its completion.

        Returns:
            Updated resource.
        """
        return self._client.update(resource, timeout=timeout, force=force)

    def delete(self, resource, force=False, export_only=None, suppress_device_updates=None, timeout=-1):
        """
        Deletes a managed volume.

        Args:
            resource (dict):
                Object to delete.
            force:
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.
            export_only:
                Valid prior to API500. By default, volumes will be deleted from OneView, and storage system.
                To delete the volume from OneView only, you must set its value to True.
                Setting its value to False has the same behavior as the default behavior.
            suppress_device_updates:
                Valid API500 onwards. By default, volumes will be deleted from OneView, and storage system.
                To delete the volume from OneView only, you must set its value to True.
                Setting its value to False has the same behavior as the default behavior.

        Returns:
            bool: Indicates if the volume was successfully deleted.
        """
        custom_headers = {'If-Match': '*'}
        if 'uri' in resource:
            uri = resource['uri']
        else:
            uri = self._client.build_uri(resource)
        if suppress_device_updates:
            uri += '?suppressDeviceUpdates=true'
        if export_only:
            custom_headers['exportOnly'] = True
        return self._client.delete(uri, force=force, timeout=timeout, custom_headers=custom_headers)

    def __build_volume_snapshot_uri(self, volume_id_or_uri=None, snapshot_id_or_uri=None):
        if snapshot_id_or_uri and "/" in snapshot_id_or_uri:
            return snapshot_id_or_uri
        else:
            if not volume_id_or_uri:
                raise ValueError(INVALID_VOLUME_URI)
            volume_uri = self._client.build_uri(volume_id_or_uri)
            return volume_uri + "/snapshots/" + str(snapshot_id_or_uri or '')

    def get_snapshots(self, volume_id_or_uri, start=0, count=-1, filter='', sort=''):
        """
        Gets all snapshots of a volume. Returns a list of snapshots based on optional sorting and filtering, and
        constrained by start and count parameters.

        Args:
            volume_id_or_uri:
                Can be either the volume id or the volume uri.
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
            list: A list of snapshots.
        """
        uri = self.__build_volume_snapshot_uri(volume_id_or_uri)
        return self._client.get_all(start, count, filter=filter, sort=sort, uri=uri)

    def create_snapshot(self, volume_id_or_uri, snapshot, timeout=-1):
        """
        Creates a snapshot for the specified volume.

        Args:
            volume_id_or_uri:
                Can be either the volume ID or the volume URI.
            snapshot (dict):
                Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        Returns:
            dict: Storage volume.
        """
        uri = self.__build_volume_snapshot_uri(volume_id_or_uri)

        return self._client.create(snapshot, uri=uri, timeout=timeout, default_values=self.DEFAULT_VALUES_SNAPSHOT)

    def get_snapshot(self, snapshot_id_or_uri, volume_id_or_uri=None):
        """
        Gets a snapshot of a volume.

        Args:
            volume_id_or_uri:
                Can be either the volume ID or the volume URI. It is optional if it is passed a snapshot URI,
                but required if it passed a snapshot ID.
            snapshot_id_or_uri:
                Can be either the snapshot ID or the snapshot URI.

        Returns:
            dict: The snapshot.
        """
        uri = self.__build_volume_snapshot_uri(volume_id_or_uri, snapshot_id_or_uri)
        return self._client.get(uri)

    def delete_snapshot(self, resource, force=False, timeout=-1):
        """
        Deletes a snapshot from OneView and the storage system.

        Args:
            resource (dict): Object to remove.
            force (bool):
                 If set to true, the operation completes despite any problems with
                 network connectivity or errors on the resource itself. The default is false.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Details of associated volume.

        """
        headers = {'If-Match': '*'}
        return self._client.delete(resource, force=force, timeout=timeout, custom_headers=headers)

    def get_snapshot_by(self, volume_id_or_uri, field, value):
        """
        Gets all snapshots that match the filter.

        The search is case-insensitive.

        Args:
            volume_id_or_uri: Can be either the volume id or the volume uri.
            field: Field name to filter.
            value: Value to filter.

        Returns:
            list: Snapshots
        """
        uri = self.__build_volume_snapshot_uri(volume_id_or_uri)
        return self._client.get_by(field, value, uri=uri)

    def get_extra_managed_storage_volume_paths(self, start=0, count=-1, filter='', sort=''):
        """
        Gets the list of extra managed storage volume paths.

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
            list: A list of extra managed storage volume paths.
        """
        uri = self.URI + '/repair?alertFixType=ExtraManagedStorageVolumePaths'
        return self._client.get_all(start, count, filter=filter, sort=sort, uri=uri)

    def repair(self, volume_id_or_uri, timeout=-1):
        """
        Removes extra presentations from a specified volume on the storage system.

        Args:
            volume_id_or_uri:
                Can be either the volume id or the volume uri.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation in
                OneView, just stops waiting for its completion.

        Returns:
            dict: Storage volume.
        """
        data = {
            "type": "ExtraManagedStorageVolumePaths",
            "resourceUri": self._client.build_uri(volume_id_or_uri)
        }
        custom_headers = {'Accept-Language': 'en_US'}
        uri = self.URI + '/repair'
        return self._client.create(data, uri=uri, timeout=timeout, custom_headers=custom_headers)

    def get_attachable_volumes(self, start=0, count=-1, filter='', query='', sort=''):
        """
        Gets the volumes that are connected on the specified networks based on the storage system port's expected
        network connectivity.

        A volume is attachable if it satisfies either of the following conditions:
            * The volume is shareable.
            * The volume not shareable and not attached.

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
            query:
                A general query string to narrow the list of resources returned. The default
                is no query; all resources are returned.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.

        Returns:
            list: A list of attachable volumes that the appliance manages.
        """
        uri = self.URI + '/attachable-volumes'
        return self._client.get_all(start, count, filter=filter, query=query, sort=sort, uri=uri)
