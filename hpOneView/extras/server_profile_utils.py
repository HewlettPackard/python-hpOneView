#!/usr/bin/python

###
# Copyright (2017) Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###
from hpOneView.extras.mergers import merge_list_by_key
from hpOneView.exceptions import HPOneViewResourceNotFound
from copy import deepcopy
from collections import OrderedDict


class Keys(object):
    ID = 'id'
    NAME = 'name'
    DEVICE_SLOT = 'deviceSlot'
    CONNECTIONS = 'connections'
    OS_DEPLOYMENT = 'osDeploymentSettings'
    OS_DEPLOYMENT_URI = 'osDeploymentPlanUri'
    ATTRIBUTES = 'osCustomAttributes'
    SAN = 'sanStorage'
    VOLUMES = 'volumeAttachments'
    PATHS = 'storagePaths'
    CONN_ID = 'connectionId'
    BOOT = 'boot'
    BIOS = 'bios'
    BOOT_MODE = 'bootMode'
    LOCAL_STORAGE = 'localStorage'
    SAS_LOGICAL_JBODS = 'sasLogicalJBODs'
    CONTROLLERS = 'controllers'
    LOGICAL_DRIVES = 'logicalDrives'
    SAS_LOGICAL_JBOD_URI = 'sasLogicalJBODUri'
    SAS_LOGICAL_JBOD_ID = 'sasLogicalJBODId'
    MODE = 'mode'
    MAC_TYPE = 'macType'
    MAC = 'mac'
    SERIAL_NUMBER_TYPE = 'serialNumberType'
    UUID = 'uuid'
    SERIAL_NUMBER = 'serialNumber'
    DRIVE_NUMBER = 'driveNumber'
    WWPN_TYPE = 'wwpnType'
    WWNN = 'wwnn'
    WWPN = 'wwpn'
    LUN_TYPE = 'lunType'
    LUN = 'lun'


class ServerProfileMerger(object):
    def merge_data(self, resource, data):
        merged_data = deepcopy(resource)
        merged_data.update(data)

        merged_data = self._merge_bios_and_boot(merged_data, resource, data)
        merged_data = self._merge_connections(merged_data, resource, data)
        merged_data = self._merge_san_storage(merged_data, data, resource)
        merged_data = self._merge_os_deployment_settings(merged_data, resource, data)
        merged_data = self._merge_local_storage(merged_data, resource, data)

        return merged_data

    def _merge_bios_and_boot(self, merged_data, resource, data):
        if self._should_merge(data, resource, key=Keys.BIOS):
            merged_data = self._merge_dict(merged_data, resource, data, key=Keys.BIOS)
        if self._should_merge(data, resource, key=Keys.BOOT):
            merged_data = self._merge_dict(merged_data, resource, data, key=Keys.BOOT)
        if self._should_merge(data, resource, key=Keys.BOOT_MODE):
            merged_data = self._merge_dict(merged_data, resource, data, key=Keys.BOOT_MODE)
        return merged_data

    def _merge_connections(self, merged_data, resource, data):
        if self._should_merge(data, resource, key=Keys.CONNECTIONS):
            existing_connections = resource[Keys.CONNECTIONS]
            params_connections = data[Keys.CONNECTIONS]
            merged_data[Keys.CONNECTIONS] = merge_list_by_key(existing_connections, params_connections, key=Keys.ID)

            # merge Boot from Connections
            merged_data = self._merge_connections_boot(merged_data, resource)
        return merged_data

    def _merge_connections_boot(self, merged_data, resource):
        existing_connection_map = {x[Keys.ID]: x.copy() for x in resource[Keys.CONNECTIONS]}
        for merged_connection in merged_data[Keys.CONNECTIONS]:
            conn_id = merged_connection[Keys.ID]
            existing_conn_has_boot = conn_id in existing_connection_map and Keys.BOOT in existing_connection_map[
                conn_id]
            if existing_conn_has_boot and Keys.BOOT in merged_connection:
                current_connection = existing_connection_map[conn_id]
                boot_settings_merged = deepcopy(current_connection[Keys.BOOT])
                boot_settings_merged.update(merged_connection[Keys.BOOT])
                merged_connection[Keys.BOOT] = boot_settings_merged
        return merged_data

    def _merge_san_storage(self, merged_data, data, resource):
        if self._removed_data(data, resource, key=Keys.SAN):
            merged_data[Keys.SAN] = dict(volumeAttachments=[], manageSanStorage=False)
        elif self._should_merge(data, resource, key=Keys.SAN):
            merged_data = self._merge_dict(merged_data, resource, data, key=Keys.SAN)

            # Merge Volumes from SAN Storage
            merged_data = self._merge_san_volumes(merged_data, resource, data)
        return merged_data

    def _merge_san_volumes(self, merged_data, resource, data):
        if self._should_merge(data[Keys.SAN], resource[Keys.SAN], key=Keys.VOLUMES):
            existing_volumes = resource[Keys.SAN][Keys.VOLUMES]
            params_volumes = data[Keys.SAN][Keys.VOLUMES]
            merged_volumes = merge_list_by_key(existing_volumes, params_volumes, key=Keys.ID)
            merged_data[Keys.SAN][Keys.VOLUMES] = merged_volumes

            # Merge Paths from SAN Storage Volumes
            merged_data = self._merge_san_storage_paths(merged_data, resource)
        return merged_data

    def _merge_san_storage_paths(self, merged_data, resource):

        existing_volumes_map = OrderedDict([(i[Keys.ID], i) for i in resource[Keys.SAN][Keys.VOLUMES]])
        merged_volumes = merged_data[Keys.SAN][Keys.VOLUMES]
        for merged_volume in merged_volumes:
            volume_id = merged_volume[Keys.ID]
            if volume_id in existing_volumes_map:
                if Keys.PATHS in merged_volume and Keys.PATHS in existing_volumes_map[volume_id]:
                    existent_paths = existing_volumes_map[volume_id][Keys.PATHS]

                    paths_from_merged_volume = merged_volume[Keys.PATHS]

                    merged_paths = merge_list_by_key(existent_paths, paths_from_merged_volume, key=Keys.CONN_ID)

                    merged_volume[Keys.PATHS] = merged_paths
        return merged_data

    def _merge_os_deployment_settings(self, merged_data, resource, data):
        if self._should_merge(data, resource, key=Keys.OS_DEPLOYMENT):
            merged_data = self._merge_dict(merged_data, resource, data, key=Keys.OS_DEPLOYMENT)

            # Merge Custom Attributes from OS Deployment Settings
            merged_data = self._merge_os_deployment_custom_attr(merged_data, resource, data)
        return merged_data

    def _merge_os_deployment_custom_attr(self, merged_data, resource, data):
        from hpOneView.extras.comparators import resource_compare_list

        if Keys.ATTRIBUTES in data[Keys.OS_DEPLOYMENT]:
            existing_os_deployment = resource[Keys.OS_DEPLOYMENT]
            params_os_deployment = data[Keys.OS_DEPLOYMENT]
            merged_os_deployment = merged_data[Keys.OS_DEPLOYMENT]

            if self._removed_data(params_os_deployment, existing_os_deployment, key=Keys.ATTRIBUTES):
                merged_os_deployment[Keys.ATTRIBUTES] = params_os_deployment[Keys.ATTRIBUTES]
            else:
                existing_attributes = existing_os_deployment[Keys.ATTRIBUTES]
                params_attributes = params_os_deployment[Keys.ATTRIBUTES]

                if resource_compare_list(existing_attributes, params_attributes):
                    merged_os_deployment[Keys.ATTRIBUTES] = existing_attributes

        return merged_data

    def _merge_local_storage(self, merged_data, resource, data):
        if self._removed_data(data, resource, key=Keys.LOCAL_STORAGE):
            merged_data[Keys.LOCAL_STORAGE] = dict(sasLogicalJBODs=[], controllers=[])
        elif self._should_merge(data, resource, key=Keys.LOCAL_STORAGE):
            # Merge SAS Logical JBODs from Local Storage
            merged_data = self._merge_sas_logical_jbods(merged_data, resource, data)
            # Merge Controllers from Local Storage
            merged_data = self._merge_controllers(merged_data, resource, data)
        return merged_data

    def _merge_sas_logical_jbods(self, merged_data, resource, data):
        if self._should_merge(data[Keys.LOCAL_STORAGE], resource[Keys.LOCAL_STORAGE], key=Keys.SAS_LOGICAL_JBODS):
            existing_items = resource[Keys.LOCAL_STORAGE][Keys.SAS_LOGICAL_JBODS]
            provided_items = merged_data[Keys.LOCAL_STORAGE][Keys.SAS_LOGICAL_JBODS]
            merged_jbods = merge_list_by_key(existing_items,
                                             provided_items,
                                             key=Keys.ID,
                                             ignore_when_null=[Keys.SAS_LOGICAL_JBOD_URI])
            merged_data[Keys.LOCAL_STORAGE][Keys.SAS_LOGICAL_JBODS] = merged_jbods
        return merged_data

    def _merge_controllers(self, merged_data, resource, data):
        if self._should_merge(data[Keys.LOCAL_STORAGE], resource[Keys.LOCAL_STORAGE], key=Keys.CONTROLLERS):
            existing_items = resource[Keys.LOCAL_STORAGE][Keys.CONTROLLERS]
            provided_items = merged_data[Keys.LOCAL_STORAGE][Keys.CONTROLLERS]
            merged_controllers = merge_list_by_key(existing_items, provided_items, key=Keys.DEVICE_SLOT)
            merged_data[Keys.LOCAL_STORAGE][Keys.CONTROLLERS] = merged_controllers

            # Merge Drives from Mezzanine and Embedded controllers
            merged_data = self._merge_controller_drives(merged_data, resource)
        return merged_data

    def _merge_controller_drives(self, merged_data, resource):
        for current_controller in merged_data[Keys.LOCAL_STORAGE][Keys.CONTROLLERS][:]:
            for existing_controller in resource[Keys.LOCAL_STORAGE][Keys.CONTROLLERS][:]:
                same_slot = current_controller.get(Keys.DEVICE_SLOT) == existing_controller.get(Keys.DEVICE_SLOT)
                same_mode = existing_controller.get(Keys.MODE) == existing_controller.get(Keys.MODE)
                if same_slot and same_mode and current_controller[Keys.LOGICAL_DRIVES]:

                    key_merge = self._define_key_to_merge_drives(current_controller)

                    if key_merge:
                        merged_drives = merge_list_by_key(existing_controller[Keys.LOGICAL_DRIVES],
                                                          current_controller[Keys.LOGICAL_DRIVES],
                                                          key=key_merge)
                        current_controller[Keys.LOGICAL_DRIVES] = merged_drives
        return merged_data

    def _define_key_to_merge_drives(self, controller):
        has_name = True
        has_logical_jbod_id = True
        for drive in controller[Keys.LOGICAL_DRIVES]:
            if not drive.get(Keys.NAME):
                has_name = False
            if not drive.get(Keys.SAS_LOGICAL_JBOD_ID):
                has_logical_jbod_id = False

        if has_name:
            return Keys.NAME
        elif has_logical_jbod_id:
            return Keys.SAS_LOGICAL_JBOD_ID
        return None

    def _removed_data(self, data, resource, key):
        return key in data and not data[key] and key in resource

    def _should_merge(self, data, resource, key):
        data_has_value = key in data and data[key]
        existing_resource_has_value = key in resource and resource[key]
        return data_has_value and existing_resource_has_value

    def _merge_dict(self, merged_data, resource, data, key):
        if resource[key]:
            merged_dict = deepcopy(resource[key])
            merged_dict.update(deepcopy(data[key]))
        merged_data[key] = merged_dict
        return merged_data


class ServerProfileReplaceNamesByUris(object):
    SERVER_PROFILE_OS_DEPLOYMENT_NOT_FOUND = 'OS Deployment Plan not found: '
    SERVER_PROFILE_ENCLOSURE_GROUP_NOT_FOUND = 'Enclosure Group not found: '
    SERVER_PROFILE_NETWORK_NOT_FOUND = 'Network not found: '
    SERVER_HARDWARE_TYPE_NOT_FOUND = 'Server Hardware Type not found: '
    VOLUME_NOT_FOUND = 'Volume not found: '
    STORAGE_POOL_NOT_FOUND = 'Storage Pool not found: '
    STORAGE_SYSTEM_NOT_FOUND = 'Storage System not found: '
    INTERCONNECT_NOT_FOUND = 'Interconnect not found: '
    FIRMWARE_DRIVER_NOT_FOUND = 'Firmware Driver not found: '
    SAS_LOGICAL_JBOD_NOT_FOUND = 'SAS logical JBOD not found: '
    ENCLOSURE_NOT_FOUND = 'Enclosure not found: '

    def replace(self, oneview_client, data):
        self.oneview_client = oneview_client
        self.__replace_os_deployment_name_by_uri(data)
        self.__replace_enclosure_group_name_by_uri(data)
        self.__replace_networks_name_by_uri(data)
        self.__replace_server_hardware_type_name_by_uri(data)
        self.__replace_volume_attachment_names_by_uri(data)
        self.__replace_enclosure_name_by_uri(data)
        self.__replace_interconnect_name_by_uri(data)
        self.__replace_firmware_baseline_name_by_uri(data)
        self.__replace_sas_logical_jbod_name_by_uri(data)

    def __replace_name_by_uri(self, data, attr_name, message, resource_client):
        attr_uri = attr_name.replace("Name", "Uri")
        if attr_name in data:
            name = data.pop(attr_name)
            resource_by_name = resource_client.get_by('name', name)
            if not resource_by_name:
                raise HPOneViewResourceNotFound(message + name)
            data[attr_uri] = resource_by_name[0]['uri']

    def __replace_os_deployment_name_by_uri(self, data):
        if Keys.OS_DEPLOYMENT in data and data[Keys.OS_DEPLOYMENT]:
            self.__replace_name_by_uri(data[Keys.OS_DEPLOYMENT], 'osDeploymentPlanName',
                                       self.SERVER_PROFILE_OS_DEPLOYMENT_NOT_FOUND,
                                       self.oneview_client.os_deployment_plans)

    def __replace_enclosure_group_name_by_uri(self, data):
        self.__replace_name_by_uri(data, 'enclosureGroupName', self.SERVER_PROFILE_ENCLOSURE_GROUP_NOT_FOUND,
                                   self.oneview_client.enclosure_groups)

    def __replace_networks_name_by_uri(self, data):
        if Keys.CONNECTIONS in data and data[Keys.CONNECTIONS]:
            for connection in data[Keys.CONNECTIONS]:
                if 'networkName' in connection:
                    name = connection.pop('networkName', None)
                    connection['networkUri'] = self.__get_network_by_name(name)['uri']

    def __replace_server_hardware_type_name_by_uri(self, data):
        self.__replace_name_by_uri(data, 'serverHardwareTypeName', self.SERVER_HARDWARE_TYPE_NOT_FOUND,
                                   self.oneview_client.server_hardware_types)

    def __replace_volume_attachment_names_by_uri(self, data):
        volume_attachments = (data.get('sanStorage') or {}).get('volumeAttachments') or []
        if len(volume_attachments) > 0:
            for volume in volume_attachments:
                self.__replace_name_by_uri(volume, 'volumeName', self.VOLUME_NOT_FOUND, self.oneview_client.volumes)
                self.__replace_name_by_uri(volume, 'volumeStoragePoolName', self.STORAGE_POOL_NOT_FOUND,
                                           self.oneview_client.storage_pools)
                self.__replace_name_by_uri(volume, 'volumeStorageSystemName', self.STORAGE_SYSTEM_NOT_FOUND,
                                           self.oneview_client.storage_systems)

    def __replace_enclosure_name_by_uri(self, data):
        self.__replace_name_by_uri(data, 'enclosureName', self.ENCLOSURE_NOT_FOUND, self.oneview_client.enclosures)

    def __replace_interconnect_name_by_uri(self, data):
        connections = data.get('connections') or []
        if len(connections) > 0:
            for connection in connections:
                self.__replace_name_by_uri(connection, 'interconnectName', self.INTERCONNECT_NOT_FOUND,
                                           self.oneview_client.interconnects)

    def __replace_firmware_baseline_name_by_uri(self, data):
        firmware = data.get('firmware') or {}
        self.__replace_name_by_uri(firmware, 'firmwareBaselineName', self.FIRMWARE_DRIVER_NOT_FOUND,
                                   self.oneview_client.firmware_drivers)

    def __replace_sas_logical_jbod_name_by_uri(self, data):
        sas_logical_jbods = (data.get('localStorage') or {}).get('sasLogicalJBODs') or []
        if len(sas_logical_jbods) > 0:
            for jbod in sas_logical_jbods:
                self.__replace_name_by_uri(jbod, 'sasLogicalJBODName', self.SAS_LOGICAL_JBOD_NOT_FOUND,
                                           self.oneview_client.sas_logical_jbods)

    def __get_network_by_name(self, name):
        fc_networks = self.oneview_client.fc_networks.get_by('name', name)
        if fc_networks:
            return fc_networks[0]

        ethernet_networks = self.oneview_client.ethernet_networks.get_by('name', name)
        if not ethernet_networks:
            raise HPOneViewResourceNotFound(self.SERVER_PROFILE_NETWORK_NOT_FOUND + name)
        return ethernet_networks[0]
