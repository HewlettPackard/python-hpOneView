# -*- coding: utf-8 -*-
###
# (C) Copyright (2017) Hewlett Packard Enterprise Development LP
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

from unittest import TestCase
from hpOneView.extras.server_profile_utils import ServerProfileReplaceNamesByUris
from hpOneView.extras.server_profile_utils import Keys
from hpOneView.extras.server_profile_utils import ServerProfileMerger
from copy import deepcopy
from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewResourceNotFound
import mock


class ServerProfileReplaceNamesByUrisTest(TestCase):
    SERVER_PROFILE_NAME = "Profile101"
    SERVER_PROFILE_URI = "/rest/server-profiles/94B55683-173F-4B36-8FA6-EC250BA2328B"
    SHT_URI = "/rest/server-hardware-types/94B55683-173F-4B36-8FA6-EC250BA2328B"
    ENCLOSURE_GROUP_URI = "/rest/enclosure-groups/ad5e9e88-b858-4935-ba58-017d60a17c89"
    TEMPLATE_URI = '/rest/server-profile-templates/9a156b04-fce8-40b0-b0cd-92ced1311dda'
    FAKE_SERVER_HARDWARE = {'uri': '/rest/server-hardware/31393736-3831-4753-567h-30335837524E'}

    BASIC_PROFILE = dict(
        name=SERVER_PROFILE_NAME,
        serverHardwareTypeUri=SHT_URI,
        enclosureGroupUri=ENCLOSURE_GROUP_URI,
        uri=SERVER_PROFILE_URI
    )

    def setUp(self):
        patcher_json_file = mock.patch.object(OneViewClient, 'from_json_file')
        self.addCleanup(patcher_json_file.stop)
        self.mock_ov_client = patcher_json_file.start()

    def test_should_replace_os_deployment_name_by_uri(self):
        uri = '/rest/os-deployment-plans/81decf85-0dff-4a5e-8a95-52994eeb6493'

        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data[Keys.OS_DEPLOYMENT] = dict(osDeploymentPlanName="Deployment Plan Name")

        self.mock_ov_client.os_deployment_plans.get_by.return_value = [dict(uri=uri)]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data[Keys.OS_DEPLOYMENT], dict(osDeploymentPlanUri=uri))

    def test_should_fail_when_deployment_plan_not_found(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data[Keys.OS_DEPLOYMENT] = dict(osDeploymentPlanName="Deployment Plan Name")

        self.mock_ov_client.os_deployment_plans.get_by.return_value = []

        expected_error = ServerProfileReplaceNamesByUris.SERVER_PROFILE_OS_DEPLOYMENT_NOT_FOUND + "Deployment Plan Name"

        try:
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)
        except HPOneViewResourceNotFound as e:
            self.assertEqual(e.msg, expected_error)
        else:
            self.fail(msg="Expected Exception was not raised")

    def test_should_replace_enclosure_group_name_by_uri(self):
        uri = '/rest/enclosure-groups/81decf85-0dff-4a5e-8a95-52994eeb6493'

        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['enclosureGroupName'] = "Enclosure Group Name"

        self.mock_ov_client.enclosure_groups.get_by.return_value = [dict(uri=uri)]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data.get('enclosureGroupUri'), uri)
        self.assertFalse(sp_data.get('enclosureGroupName'))

    def test_should_fail_when_enclosure_group_not_found(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['enclosureGroupName'] = "Enclosure Group Name"

        self.mock_ov_client.enclosure_groups.get_by.return_value = []

        message = ServerProfileReplaceNamesByUris.SERVER_PROFILE_ENCLOSURE_GROUP_NOT_FOUND + "Enclosure Group Name"

        try:
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)
        except HPOneViewResourceNotFound as e:
            self.assertEqual(e.msg, message)
        else:
            self.fail(msg="Expected Exception was not raised")

    def test_should_replace_connections_name_by_uri(self):
        conn_1 = dict(name="connection-1", networkUri='/rest/fc-networks/98')
        conn_2 = dict(name="connection-2", networkName='FC Network')
        conn_3 = dict(name="connection-3", networkName='Ethernet Network')

        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data[Keys.CONNECTIONS] = [conn_1, conn_2, conn_3]

        self.mock_ov_client.fc_networks.get_by.side_effect = [[dict(uri='/rest/fc-networks/14')], []]
        self.mock_ov_client.ethernet_networks.get_by.return_value = [dict(uri='/rest/ethernet-networks/18')]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        expected_connections = [dict(name="connection-1", networkUri='/rest/fc-networks/98'),
                                dict(name="connection-2", networkUri='/rest/fc-networks/14'),
                                dict(name="connection-3", networkUri='/rest/ethernet-networks/18')]

        self.assertEqual(sp_data.get(Keys.CONNECTIONS), expected_connections)

    def test_should_fail_when_network_not_found(self):
        conn = dict(name="connection-1", networkName='FC Network')

        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data[Keys.CONNECTIONS] = [conn]

        self.mock_ov_client.fc_networks.get_by.return_value = []
        self.mock_ov_client.ethernet_networks.get_by.return_value = []

        expected_error = ServerProfileReplaceNamesByUris.SERVER_PROFILE_NETWORK_NOT_FOUND + "FC Network"

        try:
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)
        except HPOneViewResourceNotFound as e:
            self.assertEqual(e.msg, expected_error)
        else:
            self.fail(msg="Expected Exception was not raised")

    def test_should_replace_server_hardware_type_name_by_uri(self):
        sht_uri = "/rest/server-hardware-types/BCAB376E-DA2E-450D-B053-0A9AE7E5114C"
        sht = {"name": "SY 480 Gen9 1", "uri": sht_uri}
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['serverHardwareTypeName'] = "SY 480 Gen9 1"

        self.mock_ov_client.server_hardware_types.get_by.return_value = [sht]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data.get('serverHardwareTypeUri'), sht_uri)
        self.assertEqual(sp_data.get('serverHardwareTypeName'), None)

    def test_should_fail_when_server_hardware_type_name_not_found(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['serverHardwareTypeName'] = "SY 480 Gen9 1"

        self.mock_ov_client.server_hardware_types.get_by.return_value = []

        expected_error = ServerProfileReplaceNamesByUris.SERVER_HARDWARE_TYPE_NOT_FOUND + "SY 480 Gen9 1"

        try:
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)
        except HPOneViewResourceNotFound as e:
            self.assertEqual(e.msg, expected_error)
        else:
            self.fail(msg="Expected Exception was not raised")

    def test_should_replace_volume_names_by_uri(self):
        volume1 = {"name": "volume1", "uri": "/rest/storage-volumes/1"}
        volume2 = {"name": "volume2", "uri": "/rest/storage-volumes/2"}
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeName": "volume1"},
                {"id": 2, "volumeName": "volume2"}
            ]
        }
        expected_dict = deepcopy(sp_data)
        expected_dict['sanStorage']['volumeAttachments'][0] = {"id": 1, "volumeUri": "/rest/storage-volumes/1"}
        expected_dict['sanStorage']['volumeAttachments'][1] = {"id": 2, "volumeUri": "/rest/storage-volumes/2"}

        self.mock_ov_client.volumes.get_by.side_effect = [[volume1], [volume2]]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected_dict)

    def test_should_not_replace_when_inform_volume_uri(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeUri": "/rest/storage-volumes/1"},
                {"id": 2, "volumeUri": "/rest/storage-volumes/2"}
            ]
        }
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected_dict)
        self.mock_ov_client.volumes.get_by.assert_not_called()

    def test_should_not_replace_volume_name_when_volume_attachments_is_none(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": None
        }
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected_dict)
        self.mock_ov_client.volumes.get_by.assert_not_called()

    def test_should_not_replace_volume_name_when_san_storage_is_none(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = None
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected_dict)
        self.mock_ov_client.volumes.get_by.assert_not_called()

    def test_should_fail_when_volume_name_not_found(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeName": "volume1"}
            ]}

        expected_error = ServerProfileReplaceNamesByUris.VOLUME_NOT_FOUND + "volume1"
        self.mock_ov_client.volumes.get_by.return_value = []

        try:
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)
        except HPOneViewResourceNotFound as e:
            self.assertEqual(e.msg, expected_error)
        else:
            self.fail(msg="Expected Exception was not raised")

    def test_should_replace_storage_pool_names_by_uri(self):
        pool1 = {"name": "pool1", "uri": "/rest/storage-pools/1"}
        pool2 = {"name": "pool2", "uri": "/rest/storage-pools/2"}
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeStoragePoolName": "pool1"},
                {"id": 2, "volumeStoragePoolName": "pool2"}
            ]
        }
        expected_dict = deepcopy(sp_data)
        expected_dict['sanStorage']['volumeAttachments'][0] = {"id": 1, "volumeStoragePoolUri": "/rest/storage-pools/1"}
        expected_dict['sanStorage']['volumeAttachments'][1] = {"id": 2, "volumeStoragePoolUri": "/rest/storage-pools/2"}

        self.mock_ov_client.storage_pools.get_by.side_effect = [[pool1], [pool2]]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected_dict)

    def test_should_not_replace_when_inform_storage_pool_uri(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeStoragePoolUri": "/rest/storage-volumes/1"},
                {"id": 2, "volumeStoragePoolUri": "/rest/storage-volumes/2"}
            ]
        }
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected_dict)
        self.mock_ov_client.storage_pools.get_by.assert_not_called()

    def test_should_not_replace_storage_pool_name_when_volume_attachments_is_none(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": None
        }
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected_dict)
        self.mock_ov_client.storage_pools.get_by.assert_not_called()

    def test_should_not_replace_storage_pool_name_when_san_storage_is_none(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = None
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected_dict)
        self.mock_ov_client.storage_pools.get_by.assert_not_called()

    def test_should_fail_when_storage_pool_name_not_found(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeStoragePoolName": "pool1"}
            ]
        }

        self.mock_ov_client.storage_pools.get_by.return_value = []

        expected_error = ServerProfileReplaceNamesByUris.STORAGE_POOL_NOT_FOUND + "pool1"

        try:
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)
        except HPOneViewResourceNotFound as e:
            self.assertEqual(e.msg, expected_error)
        else:
            self.fail(msg="Expected Exception was not raised")

    def test_should_replace_storage_system_names_by_uri(self):
        storage_system1 = {"name": "system1", "uri": "/rest/storage-systems/1"}
        storage_system2 = {"name": "system2", "uri": "/rest/storage-systems/2"}
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeStorageSystemName": "system1"},
                {"id": 2, "volumeStorageSystemName": "system2"}
            ]
        }
        expected = deepcopy(sp_data)
        expected['sanStorage']['volumeAttachments'][0] = {"id": 1, "volumeStorageSystemUri": "/rest/storage-systems/1"}
        expected['sanStorage']['volumeAttachments'][1] = {"id": 2, "volumeStorageSystemUri": "/rest/storage-systems/2"}

        self.mock_ov_client.storage_systems.get_by.side_effect = [[storage_system1], [storage_system2]]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected)

    def test_should_not_replace_when_inform_storage_system_uri(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeStorageSystemUri": "/rest/storage-systems/1"},
                {"id": 2, "volumeStorageSystemUri": "/rest/storage-systems/2"}
            ]
        }
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected_dict)
        self.mock_ov_client.storage_systems.get_by.assert_not_called()

    def test_should_not_replace_storage_system_name_when_volume_attachments_is_none(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": None
        }
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected_dict)
        self.mock_ov_client.storage_systems.get_by.assert_not_called()

    def test_should_not_replace_storage_system_name_when_san_storage_is_none(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = None
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected_dict)
        self.mock_ov_client.storage_systems.get_by.assert_not_called()

    def test_should_fail_when_storage_system_name_not_found(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['sanStorage'] = {
            "volumeAttachments": [
                {"id": 1, "volumeStorageSystemName": "system1"}
            ]
        }

        self.mock_ov_client.storage_systems.get_by.return_value = []

        expected_error = ServerProfileReplaceNamesByUris.STORAGE_SYSTEM_NOT_FOUND + "system1"

        try:
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)
        except HPOneViewResourceNotFound as e:
            self.assertEqual(e.msg, expected_error)
        else:
            self.fail(msg="Expected Exception was not raised")

    def test_should_replace_enclosure_name_by_uri(self):
        uri = "/rest/enclosures/09SGH100X6J1"
        enclosure = {"name": "Enclosure-474", "uri": uri}
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['enclosureName'] = "Enclosure-474"

        self.mock_ov_client.enclosures.get_by.return_value = [enclosure]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data.get('enclosureUri'), uri)
        self.assertEqual(sp_data.get('enclosureName'), None)

    def test_should_fail_when_enclosure_name_not_found(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['enclosureName'] = "Enclosure-474"

        self.mock_ov_client.enclosures.get_by.return_value = []

        expected_error = ServerProfileReplaceNamesByUris.ENCLOSURE_NOT_FOUND + "Enclosure-474"

        try:
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)
        except HPOneViewResourceNotFound as e:
            self.assertEqual(e.msg, expected_error)
        else:
            self.fail(msg="Expected Exception was not raised")

    def test_should_replace_interconnect_name_by_uri(self):
        interconnect1 = {"name": "interconnect1", "uri": "/rest/interconnects/1"}
        interconnect2 = {"name": "interconnect2", "uri": "/rest/interconnects/2"}
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['connections'] = [
            {"id": 1, "interconnectName": "interconnect1"},
            {"id": 2, "interconnectName": "interconnect2"}
        ]

        expected = deepcopy(sp_data)
        expected['connections'][0] = {"id": 1, "interconnectUri": "/rest/interconnects/1"}
        expected['connections'][1] = {"id": 2, "interconnectUri": "/rest/interconnects/2"}

        self.mock_ov_client.interconnects.get_by.side_effect = [[interconnect1], [interconnect2]]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected)

    def test_should_not_replace_when_inform_interconnect_uri(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['connections'] = [
            {"id": 1, "interconnectUri": "/rest/interconnects/1"},
            {"id": 2, "interconnectUri": "/rest/interconnects/2"}
        ]

        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected_dict)
        self.mock_ov_client.interconnects.get_by.assert_not_called()

    def test_should_not_replace_interconnect_name_when_connections_is_none(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['connections'] = None
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected_dict)
        self.mock_ov_client.interconnects.get_by.assert_not_called()

    def test_should_fail_when_interconnect_name_not_found(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['connections'] = [{"id": 1, "interconnectName": "interconnect1"}]

        self.mock_ov_client.interconnects.get_by.return_value = None

        expected_error = ServerProfileReplaceNamesByUris.INTERCONNECT_NOT_FOUND + "interconnect1"
        try:
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)
        except HPOneViewResourceNotFound as e:
            self.assertEqual(e.msg, expected_error)
        else:
            self.fail(msg="Expected Exception was not raised")

    def test_should_replace_firmware_baseline_name_by_uri(self):
        firmware_driver = {"name": "firmwareName001", "uri": "/rest/firmware-drivers/1"}
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['firmware'] = {"firmwareBaselineName": "firmwareName001"}

        expected = deepcopy(sp_data)
        expected['firmware'] = {"firmwareBaselineUri": "/rest/firmware-drivers/1"}

        self.mock_ov_client.firmware_drivers.get_by.return_value = [firmware_driver]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected)

    def test_should_not_replace_when_inform_firmware_baseline_uri(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['firmware'] = {"firmwareBaselineUri": "/rest/firmware-drivers/1"}

        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected_dict)
        self.mock_ov_client.firmware_drivers.get_by.assert_not_called()

    def test_should_not_replace_firmware_baseline_name_when_firmware_is_none(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['firmware'] = None
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected_dict)
        self.mock_ov_client.firmware_drivers.get_by.assert_not_called()

    def test_should_fail_when_firmware_baseline_name_not_found(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['firmware'] = {"firmwareBaselineName": "firmwareName001"}

        self.mock_ov_client.firmware_drivers.get_by.return_value = None

        expected_error = ServerProfileReplaceNamesByUris.FIRMWARE_DRIVER_NOT_FOUND + "firmwareName001"

        try:
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)
        except HPOneViewResourceNotFound as e:
            self.assertEqual(e.msg, expected_error)
        else:
            self.fail(msg="Expected Exception was not raised")

    def test_should_replace_sas_logical_jbod_names_by_uris(self):
        sas_logical_jbod1 = {"name": "jbod1", "uri": "/rest/sas-logical-jbods/1"}
        sas_logical_jbod2 = {"name": "jbod2", "uri": "/rest/sas-logical-jbods/2"}
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['localStorage'] = {
            "sasLogicalJBODs": [
                {"id": 1, "sasLogicalJBODName": "jbod1"},
                {"id": 2, "sasLogicalJBODName": "jbod2"}
            ]
        }
        expected = deepcopy(sp_data)
        expected['localStorage']['sasLogicalJBODs'][0] = {"id": 1, "sasLogicalJBODUri": "/rest/sas-logical-jbods/1"}
        expected['localStorage']['sasLogicalJBODs'][1] = {"id": 2, "sasLogicalJBODUri": "/rest/sas-logical-jbods/2"}

        self.mock_ov_client.sas_logical_jbods.get_by.side_effect = [[sas_logical_jbod1], [sas_logical_jbod2]]

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected)

    def test_should_not_replace_when_inform_sas_logical_jbod_uris(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['localStorage'] = {
            "sasLogicalJBODs": [
                {"id": 1, "sasLogicalJBODUri": "/rest/sas-logical-jbods/1"},
                {"id": 2, "sasLogicalJBODUri": "/rest/sas-logical-jbods/2"}
            ]
        }
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected_dict)
        self.mock_ov_client.sas_logical_jbods.get_by.assert_not_called()

    def test_should_not_replace_sas_logical_jbod_names_when_jbod_list_is_none(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['localStorage'] = {
            "sasLogicalJBODs": None
        }
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected_dict)
        self.mock_ov_client.sas_logical_jbods.get_by.assert_not_called()

    def test_should_not_replace_sas_logical_jbod_names_when_local_storage_is_none(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['localStorage'] = None
        expected_dict = deepcopy(sp_data)

        ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)

        self.assertEqual(sp_data, expected_dict)
        self.mock_ov_client.sas_logical_jbods.get_by.assert_not_called()

    def test_should_fail_when_sas_logical_jbod_name_not_found(self):
        sp_data = deepcopy(self.BASIC_PROFILE)
        sp_data['localStorage'] = {
            "sasLogicalJBODs": [
                {"id": 1, "sasLogicalJBODName": "jbod1"}
            ]
        }

        self.mock_ov_client.sas_logical_jbods.get_by.return_value = []

        expected_error = ServerProfileReplaceNamesByUris.SAS_LOGICAL_JBOD_NOT_FOUND + "jbod1"

        try:
            ServerProfileReplaceNamesByUris().replace(self.mock_ov_client, sp_data)
        except HPOneViewResourceNotFound as e:
            self.assertEqual(e.msg, expected_error)
        else:
            self.fail(msg="Expected Exception was not raised")


class ServerProfileMergerTest(TestCase):
    SERVER_PROFILE_NAME = "Profile101"

    CREATED_BASIC_PROFILE = dict(
        affinity="Bay",
        bios=dict(manageBios=False, overriddenSettings=[]),
        boot=dict(manageBoot=False, order=[]),
        bootMode=dict(manageMode=False, mode=None, pxeBootPolicy=None),
        category="server-profile-templates",
        enclosureGroupUri="/rest/enclosure-groups/ad5e9e88-b858-4935-ba58-017d60a17c89",
        name=SERVER_PROFILE_NAME,
        serialNumber='VCGGU8800W',
        serialNumberType="Virtual",
        serverHardwareTypeUri="/rest/server-hardware-types/94B55683-173F-4B36-8FA6-EC250BA2328B",
        serverHardwareUri='/rest/server-hardware/37333036-3831-76jh-4831-303658389766',
        status="OK",
        type="ServerProfileV5",
        uri="/rest/server-profiles/57d3af2a-b6d2-4446-8645-f38dd808ea490",
        serverProfileTemplateUri='/rest/server-profile-templates/9a156b04-fce8-40b0-b0cd-92ced1311dda',
        templateCompliance='Compliant',
        wwnType="Virtual"
    )

    FAKE_SERVER_HARDWARE = {'uri': '/rest/server-hardware/31393736-3831-4753-567h-30335837524E'}

    BOOT_CONN = dict(priority="NotBootable", chapLevel="none")

    CONNECTION_1 = dict(id=1, name="connection-1", mac="E2:4B:0D:30:00:29", boot=BOOT_CONN)
    CONNECTION_2 = dict(id=2, name="connection-2", mac="E2:4B:0D:30:00:2A", boot=BOOT_CONN)

    CONNECTION_1_WITH_WWPN = dict(name="connection-1", wwpnType="Virtual",
                                  wwnn="10:00:3a:43:88:50:00:01", wwpn="10:00:3a:43:88:50:00:00")
    CONNECTION_2_WITH_WWPN = dict(name="connection-2", wwpnType="Physical",
                                  wwnn="10:00:3a:43:88:50:00:03", wwpn="10:00:3a:43:88:50:00:02")

    CONN_1_NO_MAC_BASIC_BOOT = dict(id=1, name="connection-1", boot=dict(priority="NotBootable"))
    CONN_2_NO_MAC_BASIC_BOOT = dict(id=2, name="connection-2", boot=dict(priority="NotBootable"))

    PATH_1 = dict(isEnabled=True, connectionId=1, storageTargets=["20:00:00:02:AC:00:08:D6"])
    PATH_2 = dict(isEnabled=True, connectionId=2, storageTargetType="Auto")

    VOLUME_1 = dict(id=1, volumeUri="/rest/volume/id1", lun=123, lunType="Auto", storagePaths=[PATH_1, PATH_2])
    VOLUME_2 = dict(id=2, volumeUri="/rest/volume/id2", lun=345, lunType="Auto", storagePaths=[])

    SAN_STORAGE = dict(hostOSType="Windows 2012 / WS2012 R2",
                       volumeAttachments=[VOLUME_1, VOLUME_2])

    OS_CUSTOM_ATTRIBUTES = [dict(name="hostname", value="newhostname"),
                            dict(name="username", value="administrator")]

    OS_DEPLOYMENT_SETTINGS = dict(osDeploymentPlanUri="/rest/os-deployment-plans/81decf85-0dff-4a5e-8a95-52994eeb6493",
                                  osVolumeUri="/rest/deployed-targets/a166c84a-4964-4f20-b4ba-ef2f154b8596",
                                  osCustomAttributes=OS_CUSTOM_ATTRIBUTES)

    SAS_LOGICAL_JBOD_1 = dict(id=1, deviceSlot="Mezz 1", name="jbod-1", driveTechnology="SasHdd", status="OK",
                              sasLogicalJBODUri="/rest/sas-logical-jbods/3128c9e6-e3de-43e7-b196-612707b54967")

    SAS_LOGICAL_JBOD_2 = dict(id=2, deviceSlot="Mezz 1", name="jbod-2", driveTechnology="SataHdd", status="Pending")

    DRIVES_CONTROLLER_EMBEDDED = [dict(driveNumber=1, name="drive-1", raidLevel="RAID1", bootable=False,
                                       sasLogicalJBODId=None),
                                  dict(driveNumber=2, name="drive-2", raidLevel="RAID1", bootable=False,
                                       sasLogicalJBODId=None)]

    CONTROLLER_EMBEDDED = dict(deviceSlot="Embedded", mode="RAID", initialize=False, importConfiguration=True,
                               logicalDrives=DRIVES_CONTROLLER_EMBEDDED)

    DRIVES_CONTROLLER_MEZZ_1 = [dict(name=None, raidLevel="RAID1", bootable=False, sasLogicalJBODId=1),
                                dict(name=None, raidLevel="RAID1", bootable=False, sasLogicalJBODId=2)]
    CONTROLLER_MEZZ_1 = dict(deviceSlot="Mezz 1", mode="RAID", initialize=False, importConfiguration=True,
                             logicalDrives=DRIVES_CONTROLLER_MEZZ_1)

    INDEX_EMBED = 1
    INDEX_MEZZ = 0

    profile_with_san_storage = CREATED_BASIC_PROFILE.copy()
    profile_with_san_storage[Keys.CONNECTIONS] = [CONNECTION_1, CONNECTION_2]
    profile_with_san_storage[Keys.SAN] = SAN_STORAGE

    profile_with_os_deployment = CREATED_BASIC_PROFILE.copy()
    profile_with_os_deployment[Keys.OS_DEPLOYMENT] = OS_DEPLOYMENT_SETTINGS

    profile_with_local_storage = CREATED_BASIC_PROFILE.copy()
    profile_with_local_storage[Keys.LOCAL_STORAGE] = dict()
    profile_with_local_storage[Keys.LOCAL_STORAGE][Keys.SAS_LOGICAL_JBODS] = [SAS_LOGICAL_JBOD_2, SAS_LOGICAL_JBOD_1]
    profile_with_local_storage[Keys.LOCAL_STORAGE][Keys.CONTROLLERS] = [CONTROLLER_MEZZ_1, CONTROLLER_EMBEDDED]

    def setUp(self):
        patcher_json_file = mock.patch.object(OneViewClient, 'from_json_file')
        self.addCleanup(patcher_json_file.stop)
        self.mock_ov_client = patcher_json_file.start()

        self.mock_ov_client.server_hardware.get_by.return_value = [self.FAKE_SERVER_HARDWARE]
        self.mock_ov_client.server_hardware.update_power_state.return_value = {}
        self.mock_ov_client.server_profiles.update.return_value = deepcopy(self.profile_with_san_storage)

    def test_merge_when_connections_have_new_item(self):
        connection_added = dict(id=3, name="new-connection")
        data = dict(name="Profile101",
                    connections=[self.CONN_1_NO_MAC_BASIC_BOOT.copy(),
                                 self.CONN_2_NO_MAC_BASIC_BOOT.copy(),
                                 connection_added.copy()])
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_connections = [self.CONNECTION_1.copy(), self.CONNECTION_2.copy(), connection_added]
        self.assertEqual(merged_data[Keys.CONNECTIONS], expected_connections)

    def test_merge_when_connections_have_removed_item(self):
        data = dict(name="Profile101",
                    connections=[self.CONNECTION_1.copy()])
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_connections = [self.CONNECTION_1]
        self.assertEqual(merged_data[Keys.CONNECTIONS], expected_connections)

    def test_merge_when_connections_have_changed_item(self):
        connection_2_renamed = dict(id=2, name="connection-2-renamed", boot=dict(priority="NotBootable"))
        data = dict(name="Profile101",
                    connections=[self.CONNECTION_1.copy(), connection_2_renamed.copy()])
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        connection_2_merged = dict(id=2, name="connection-2-renamed", mac="E2:4B:0D:30:00:2A", boot=self.BOOT_CONN)
        expected_connections = [self.CONNECTION_1.copy(), connection_2_merged.copy()]
        self.assertEqual(merged_data[Keys.CONNECTIONS], expected_connections)

    def test_merge_when_connection_list_is_removed(self):
        data = dict(name="Profile101",
                    connections=[])
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        self.assertFalse(merged_data[Keys.CONNECTIONS])

    def test_merge_when_connection_list_is_null(self):
        data = dict(name="Profile101",
                    connections=None)
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        self.assertFalse(merged_data[Keys.CONNECTIONS])

    def test_merge_when_connection_list_not_provided(self):
        data = dict(name="Profile101")

        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_connections = [self.CONNECTION_1.copy(), self.CONNECTION_2.copy()]
        self.assertEqual(merged_data[Keys.CONNECTIONS], expected_connections)

    def test_merge_when_existing_connection_list_is_null(self):
        data = dict(name="Profile101",
                    connections=[self.CONNECTION_1.copy(), self.CONNECTION_2.copy()])

        resource = deepcopy(self.profile_with_san_storage)
        resource[Keys.CONNECTIONS] = None

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_connections = [self.CONNECTION_1.copy(), self.CONNECTION_2.copy()]
        self.assertEqual(merged_data[Keys.CONNECTIONS], expected_connections)

    def test_merge_when_san_storage_is_equals(self):
        data = dict(name="Profile101",
                    connections=[self.CONNECTION_1.copy(), self.CONNECTION_2.copy()])
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        self.assertEqual(merged_data, resource)

    def test_merge_when_san_storage_has_changes(self):
        data = dict(name="Profile101",
                    sanStorage=deepcopy(self.SAN_STORAGE))
        data[Keys.SAN].pop('hostOSType')
        data[Keys.SAN]['newField'] = "123"
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_san_storage = deepcopy(self.SAN_STORAGE)
        expected_san_storage['newField'] = "123"
        self.assertEqual(merged_data[Keys.SAN], expected_san_storage)

    def test_merge_when_san_storage_is_removed_from_profile_with_san(self):
        data = dict(name="Profile101",
                    sanStorage=None)
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_san_storage = dict(manageSanStorage=False,
                                    volumeAttachments=[])
        self.assertEqual(merged_data[Keys.SAN], expected_san_storage)

    def test_merge_when_san_storage_is_removed_from_basic_profile(self):
        data = dict(name="Profile101",
                    sanStorage=None,
                    newField="123")
        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        self.assertFalse(merged_data[Keys.SAN])

    def test_merge_when_san_storage_not_provided(self):
        data = dict(name="Profile101")
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        self.assertEqual(merged_data[Keys.SAN], resource[Keys.SAN])

    def test_merge_when_existing_san_storage_is_null(self):
        data = dict(name="Profile101",
                    sanStorage=deepcopy(self.SAN_STORAGE))
        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        self.assertEqual(merged_data[Keys.SAN], self.SAN_STORAGE)

    def test_merge_when_volume_attachments_are_removed(self):
        data = dict(name="Profile101",
                    sanStorage=deepcopy(self.SAN_STORAGE))
        data[Keys.SAN][Keys.VOLUMES] = None
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        self.assertFalse(merged_data[Keys.SAN][Keys.VOLUMES])

    def test_merge_when_volume_attachments_has_changes(self):
        data = dict(name="Profile101",
                    sanStorage=deepcopy(self.SAN_STORAGE))
        data[Keys.SAN][Keys.VOLUMES][0]['newField'] = "123"
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_volumes = [deepcopy(self.VOLUME_1), deepcopy(self.VOLUME_2)]
        expected_volumes[0]['newField'] = "123"
        self.assertEqual(merged_data[Keys.SAN][Keys.VOLUMES], expected_volumes)

    def test_merge_when_storage_paths_has_changes(self):
        data = dict(name="Profile101",
                    sanStorage=deepcopy(self.SAN_STORAGE))
        data[Keys.SAN][Keys.VOLUMES][0][Keys.PATHS][1]['newField'] = "123"
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)
        merged_volumes = merged_data[Keys.SAN].get(Keys.VOLUMES)

        expected_paths_storage_1 = [deepcopy(self.PATH_1), deepcopy(self.PATH_2)]
        expected_paths_storage_1[1]['newField'] = "123"
        self.assertEqual(expected_paths_storage_1, merged_volumes[0][Keys.PATHS])
        self.assertEqual([], merged_volumes[1][Keys.PATHS])

    def test_merge_should_add_storage_path(self):
        profile = deepcopy(self.profile_with_san_storage)
        path3 = dict(isEnabled=True, connectionId=3, storageTargetType="Auto")
        profile[Keys.SAN][Keys.VOLUMES][0][Keys.PATHS].append(deepcopy(path3))

        resource = deepcopy(self.profile_with_san_storage)
        merged_data = ServerProfileMerger().merge_data(resource, profile)

        expected_paths = [self.PATH_1, self.PATH_2, path3]

        self.assertEqual(expected_paths, merged_data[Keys.SAN][Keys.VOLUMES][0][Keys.PATHS])

    def test_merge_when_storage_paths_are_removed(self):
        data = dict(name="Profile101",
                    sanStorage=deepcopy(self.SAN_STORAGE))
        data[Keys.SAN][Keys.VOLUMES][0][Keys.PATHS] = []
        resource = deepcopy(self.profile_with_san_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)
        merged_volumes = merged_data[Keys.SAN].get(Keys.VOLUMES)

        self.assertEqual([], merged_volumes[1][Keys.PATHS])

    def test_merge_when_bios_has_changes(self):
        data = dict(name="Profile101")
        data[Keys.BIOS] = dict(newField="123")
        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_bios = dict(manageBios=False, overriddenSettings=[], newField="123")
        self.assertEqual(merged_data[Keys.BIOS], expected_bios)

    def test_merge_when_bios_is_null(self):
        data = dict(name="Profile101")
        data[Keys.BIOS] = None

        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        self.assertFalse(merged_data[Keys.BIOS])

    def test_merge_when_bios_not_provided(self):
        data = dict(name="Profile101")
        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_bios = dict(manageBios=False, overriddenSettings=[])
        self.assertEqual(merged_data[Keys.BIOS], expected_bios)

    def test_merge_when_existing_bios_is_null(self):
        data = dict(name="Profile101")
        data[Keys.BIOS] = dict(newField="123")
        resource = deepcopy(self.CREATED_BASIC_PROFILE)
        resource[Keys.BIOS] = None

        merged_data = ServerProfileMerger().merge_data(resource, data)

        self.assertEqual(merged_data[Keys.BIOS], dict(newField="123"))

    def test_merge_when_boot_has_changes(self):
        data = dict(name="Profile101")
        data[Keys.BOOT] = dict(newField="123")
        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_boot = dict(manageBoot=False, order=[], newField="123")
        self.assertEqual(merged_data[Keys.BOOT], expected_boot)

    def test_merge_when_boot_is_null(self):
        data = dict(name="Profile101")
        data[Keys.BOOT] = None

        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        self.assertFalse(merged_data[Keys.BOOT])

    def test_merge_when_boot_not_provided(self):
        data = dict(name="Profile101")
        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_boot = dict(manageBoot=False, order=[])
        self.assertEqual(merged_data[Keys.BOOT], expected_boot)

    def test_merge_when_existing_boot_is_null(self):
        data = dict(name="Profile101")
        data[Keys.BOOT] = dict(newField="123")
        resource = deepcopy(self.CREATED_BASIC_PROFILE)
        resource[Keys.BOOT] = None

        merged_data = ServerProfileMerger().merge_data(resource, data)

        self.assertEqual(merged_data[Keys.BOOT], dict(newField="123"))

    def test_merge_when_boot_mode_has_changes(self):
        data = dict(name="Profile101")
        data[Keys.BOOT_MODE] = dict(newField="123")
        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_boot_mode = dict(manageMode=False, mode=None, pxeBootPolicy=None, newField="123")
        self.assertEqual(merged_data[Keys.BOOT_MODE], expected_boot_mode)

    def test_merge_when_boot_mode_is_null(self):
        data = dict(name="Profile101")
        data[Keys.BOOT_MODE] = None

        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        self.assertFalse(merged_data[Keys.BOOT_MODE])

    def test_merge_when_boot_mode_not_provided(self):
        data = dict(name="Profile101")
        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_boot_mode = dict(manageMode=False, mode=None, pxeBootPolicy=None)
        self.assertEqual(merged_data[Keys.BOOT_MODE], expected_boot_mode)

    def test_merge_when_existing_boot_mode_is_null(self):
        data = dict(name="Profile101")
        data[Keys.BOOT_MODE] = dict(newField="123")
        resource = deepcopy(self.CREATED_BASIC_PROFILE)
        resource[Keys.BOOT_MODE] = None

        merged_data = ServerProfileMerger().merge_data(resource, data)

        self.assertEqual(merged_data[Keys.BOOT_MODE], dict(newField="123"))

    def test_merge_when_os_deployment_is_equals(self):
        data = dict(name="Profile101",
                    osDeploymentSettings=deepcopy(self.OS_DEPLOYMENT_SETTINGS))
        resource = deepcopy(self.profile_with_os_deployment)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        self.assertEqual(merged_data, resource)

    def test_merge_when_os_deployment_has_changes(self):
        data = dict(name="Profile101",
                    osDeploymentSettings=deepcopy(self.OS_DEPLOYMENT_SETTINGS))
        data[Keys.OS_DEPLOYMENT]['osDeploymentPlanUri'] = "/rest/os-deployment-plans/other-id"
        resource = deepcopy(self.profile_with_os_deployment)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_os_deployment = deepcopy(self.OS_DEPLOYMENT_SETTINGS)
        expected_os_deployment['osDeploymentPlanUri'] = "/rest/os-deployment-plans/other-id"
        self.assertEqual(merged_data[Keys.OS_DEPLOYMENT], expected_os_deployment)

    def test_merge_when_os_deployment_not_provided(self):
        data = dict(name="Profile101")

        resource = deepcopy(self.profile_with_os_deployment)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_os_deployment = resource[Keys.OS_DEPLOYMENT]
        self.assertEqual(merged_data[Keys.OS_DEPLOYMENT], expected_os_deployment)

    def test_merge_when_existing_os_deployment_settings_are_null(self):
        data = dict(name="Profile101",
                    osDeploymentSettings=deepcopy(self.OS_DEPLOYMENT_SETTINGS))

        resource = deepcopy(self.profile_with_os_deployment)
        resource[Keys.OS_DEPLOYMENT] = None

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_os_deployment = deepcopy(self.OS_DEPLOYMENT_SETTINGS)
        self.assertEqual(merged_data[Keys.OS_DEPLOYMENT], expected_os_deployment)

    def test_merge_when_custom_attributes_have_changes(self):
        data = dict(name="Profile101",
                    osDeploymentSettings=deepcopy(self.OS_DEPLOYMENT_SETTINGS))
        data[Keys.OS_DEPLOYMENT][Keys.ATTRIBUTES][0]['hostname'] = 'updatedhostname'
        resource = deepcopy(self.profile_with_os_deployment)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_os_deployment = deepcopy(self.OS_DEPLOYMENT_SETTINGS)
        expected_os_deployment[Keys.ATTRIBUTES][0]['hostname'] = 'updatedhostname'
        self.assertEqual(merged_data[Keys.OS_DEPLOYMENT], expected_os_deployment)

    def test_merge_when_custom_attributes_have_new_item(self):
        new_item = dict(name="password", value="secret123")
        data = dict(name="Profile101",
                    osDeploymentSettings=deepcopy(self.OS_DEPLOYMENT_SETTINGS))
        data[Keys.OS_DEPLOYMENT][Keys.ATTRIBUTES].append(new_item.copy())

        resource = deepcopy(self.profile_with_os_deployment)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_os_deployment = deepcopy(self.OS_DEPLOYMENT_SETTINGS)
        expected_os_deployment[Keys.ATTRIBUTES].append(new_item.copy())
        self.assertEqual(merged_data[Keys.OS_DEPLOYMENT], expected_os_deployment)

    def test_merge_when_custom_attributes_have_removed_item(self):
        data = dict(name="Profile101",
                    osDeploymentSettings=deepcopy(self.OS_DEPLOYMENT_SETTINGS))
        data[Keys.OS_DEPLOYMENT][Keys.ATTRIBUTES].pop()
        resource = deepcopy(self.profile_with_os_deployment)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_os_deployment = deepcopy(self.OS_DEPLOYMENT_SETTINGS)
        expected_os_deployment[Keys.ATTRIBUTES].pop()
        self.assertEqual(merged_data[Keys.OS_DEPLOYMENT], expected_os_deployment)

    def test_merge_when_custom_attributes_are_equals_with_different_order(self):
        data = dict(name="Profile101",
                    osDeploymentSettings=deepcopy(self.OS_DEPLOYMENT_SETTINGS))
        first_attr = data[Keys.OS_DEPLOYMENT][Keys.ATTRIBUTES][0]
        second_attr = data[Keys.OS_DEPLOYMENT][Keys.ATTRIBUTES][1]
        data[Keys.OS_DEPLOYMENT][Keys.ATTRIBUTES][0] = second_attr
        data[Keys.OS_DEPLOYMENT][Keys.ATTRIBUTES][1] = first_attr
        resource = deepcopy(self.profile_with_os_deployment)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        self.assertEqual(merged_data, deepcopy(self.profile_with_os_deployment))

    def test_merge_when_custom_attributes_have_different_values_and_order(self):
        data = dict(name="Profile101",
                    osDeploymentSettings=deepcopy(self.OS_DEPLOYMENT_SETTINGS))

        first_attr = data[Keys.OS_DEPLOYMENT][Keys.ATTRIBUTES][0]
        second_attr = data[Keys.OS_DEPLOYMENT][Keys.ATTRIBUTES][1]

        first_attr['value'] = 'newValue'
        data[Keys.OS_DEPLOYMENT][Keys.ATTRIBUTES][0] = second_attr
        data[Keys.OS_DEPLOYMENT][Keys.ATTRIBUTES][1] = first_attr
        resource = deepcopy(self.profile_with_os_deployment)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_os_attributes = [dict(name="username", value="administrator"),
                                  dict(name="hostname", value="newValue")]
        expected_os_deployment = deepcopy(self.OS_DEPLOYMENT_SETTINGS)
        expected_os_deployment[Keys.ATTRIBUTES] = expected_os_attributes
        self.assertEqual(merged_data[Keys.OS_DEPLOYMENT], expected_os_deployment)

    def test_merge_when_custom_attributes_are_removed(self):
        data = dict(name="Profile101",
                    osDeploymentSettings=deepcopy(self.OS_DEPLOYMENT_SETTINGS))
        data[Keys.OS_DEPLOYMENT][Keys.ATTRIBUTES] = None
        resource = deepcopy(self.profile_with_os_deployment)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_os_deployment = deepcopy(self.OS_DEPLOYMENT_SETTINGS)
        expected_os_deployment[Keys.ATTRIBUTES] = None
        self.assertEqual(merged_data[Keys.OS_DEPLOYMENT], expected_os_deployment)

    def test_merge_when_existing_custom_attributes_are_null(self):
        data = dict(name="Profile101",
                    osDeploymentSettings=deepcopy(self.OS_DEPLOYMENT_SETTINGS))
        resource = deepcopy(self.profile_with_os_deployment)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_attributes = deepcopy(self.OS_DEPLOYMENT_SETTINGS).get(Keys.ATTRIBUTES)
        self.assertEqual(merged_data[Keys.OS_DEPLOYMENT].get(Keys.ATTRIBUTES), expected_attributes)

    def test_merge_when_local_storage_removed(self):
        data = dict(name="Profile101",
                    localStorage=None)
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        self.assertEqual(merged_data[Keys.LOCAL_STORAGE], dict(sasLogicalJBODs=[], controllers=[]))

    def test_merge_when_local_storage_is_null_and_existing_server_profile_is_basic(self):
        data = dict(name="Profile101",
                    localStorage=None)
        resource = deepcopy(self.CREATED_BASIC_PROFILE)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        self.assertFalse(merged_data[Keys.LOCAL_STORAGE])

    def test_merge_when_sas_logical_jbods_have_new_item(self):
        sas_logical_jbod_added = dict(id=3, deviceSlot="Mezz 1", name="new-sas-logical-jbod", driveTechnology="SataHdd")
        data = dict(name="Profile101",
                    localStorage=dict(sasLogicalJBODs=[self.SAS_LOGICAL_JBOD_2.copy(),
                                                       self.SAS_LOGICAL_JBOD_1.copy(),
                                                       sas_logical_jbod_added.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_sas_logical_jbods = [self.SAS_LOGICAL_JBOD_2.copy(),
                                      self.SAS_LOGICAL_JBOD_1.copy(),
                                      sas_logical_jbod_added]
        self.assertEqual(merged_data[Keys.LOCAL_STORAGE][Keys.SAS_LOGICAL_JBODS], expected_sas_logical_jbods)

    def test_merge_when_sas_logical_jbods_have_removed_item(self):
        data = dict(name="Profile101",
                    localStorage=dict(sasLogicalJBODs=[self.SAS_LOGICAL_JBOD_1.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_sas_logical_jbods = [self.SAS_LOGICAL_JBOD_1.copy()]
        self.assertEqual(merged_data[Keys.LOCAL_STORAGE][Keys.SAS_LOGICAL_JBODS], expected_sas_logical_jbods)

    def test_merge_when_sas_logical_jbods_have_changed_item(self):
        item_2_changed = dict(id=2, numPhysicalDrives=2)
        data = dict(name="Profile101",
                    localStorage=dict(sasLogicalJBODs=[self.SAS_LOGICAL_JBOD_1.copy(), item_2_changed.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        item_2_merged = dict(numPhysicalDrives=2,
                             id=2, name="jbod-2", deviceSlot="Mezz 1", driveTechnology="SataHdd", status="Pending")
        expected_sas_logical_jbods = [self.SAS_LOGICAL_JBOD_1.copy(), item_2_merged.copy()]
        self.assertEqual(merged_data[Keys.LOCAL_STORAGE][Keys.SAS_LOGICAL_JBODS], expected_sas_logical_jbods)

    @mock.patch('hpOneView.extras.server_profile_utils.merge_list_by_key')
    def test_merge_should_ignore_logical_jbod_uri_when_null(self, mock_merge_list):
        data = dict(name="Profile101",
                    localStorage=dict(sasLogicalJBODs=[self.SAS_LOGICAL_JBOD_1.copy(), self.SAS_LOGICAL_JBOD_2.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        ServerProfileMerger().merge_data(resource, data)

        mock_merge_list.assert_called_once_with(mock.ANY, mock.ANY, key=mock.ANY,
                                                ignore_when_null=[Keys.SAS_LOGICAL_JBOD_URI])

    def test_merge_when_sas_logical_jbod_list_is_removed(self):
        data = dict(name="Profile101",
                    localStorage=dict(sasLogicalJBODs=[]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        self.assertFalse(merged_data[Keys.LOCAL_STORAGE][Keys.SAS_LOGICAL_JBODS])

    def test_merge_when_controllers_have_new_item(self):
        controller_added = dict(deviceSlot="Device Slot Name", mode="RAID", initialize=False, importConfiguration=True)
        data = dict(name="Profile101",
                    localStorage=dict(controllers=[self.CONTROLLER_MEZZ_1.copy(),
                                                   self.CONTROLLER_EMBEDDED.copy(),
                                                   controller_added.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_controllers = [self.CONTROLLER_MEZZ_1.copy(), self.CONTROLLER_EMBEDDED.copy(), controller_added]
        self.assertEqual(merged_data[Keys.LOCAL_STORAGE][Keys.CONTROLLERS], expected_controllers)

    def test_merge_when_controllers_have_removed_item(self):
        data = dict(name="Profile101",
                    localStorage=dict(controllers=[self.CONTROLLER_MEZZ_1.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_controllers = [self.CONTROLLER_MEZZ_1.copy()]
        self.assertEqual(merged_data[Keys.LOCAL_STORAGE][Keys.CONTROLLERS], expected_controllers)

    def test_merge_when_controllers_have_changed_item(self):
        controller_embedded_changed = dict(deviceSlot="Embedded", initialize=True)
        data = dict(name="Profile101",
                    localStorage=dict(controllers=[self.CONTROLLER_MEZZ_1.copy(),
                                                   controller_embedded_changed.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        item_2_merged = dict(initialize=True,  # initialize value changed from False to True
                             deviceSlot="Embedded", mode="RAID", importConfiguration=True,
                             logicalDrives=self.DRIVES_CONTROLLER_EMBEDDED)
        expected_controllers = [self.CONTROLLER_MEZZ_1.copy(), item_2_merged.copy()]
        self.assertEqual(merged_data[Keys.LOCAL_STORAGE][Keys.CONTROLLERS], expected_controllers)

    def test_merge_when_controller_list_is_removed(self):
        data = dict(name="Profile101",
                    localStorage=dict(controllers=[]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        self.assertFalse(merged_data[Keys.LOCAL_STORAGE][Keys.CONTROLLERS])

    def test_merge_when_drives_from_embedded_controller_have_new_item(self):
        new_drive = dict(name="drive-3", raidLevel="RAID1", bootable=False, sasLogicalJBODId=None)
        controller_embedded = deepcopy(self.CONTROLLER_EMBEDDED)
        controller_embedded[Keys.LOGICAL_DRIVES].append(new_drive.copy())

        data = dict(name="Profile101",
                    localStorage=dict(controllers=[self.CONTROLLER_MEZZ_1.copy(),
                                                   controller_embedded.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_drives = [self.CONTROLLER_EMBEDDED[Keys.LOGICAL_DRIVES][0],
                           self.CONTROLLER_EMBEDDED[Keys.LOGICAL_DRIVES][1],
                           new_drive]
        result = merged_data[Keys.LOCAL_STORAGE][Keys.CONTROLLERS][self.INDEX_EMBED][Keys.LOGICAL_DRIVES]

        self.assertEqual(result, expected_drives)

    def test_merge_when_drives_from_embedded_controller_have_removed_item(self):
        controller_embedded = deepcopy(self.CONTROLLER_EMBEDDED)
        controller_embedded[Keys.LOGICAL_DRIVES].pop()

        data = dict(name="Profile101",
                    localStorage=dict(controllers=[self.CONTROLLER_MEZZ_1.copy(),
                                                   controller_embedded.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_drives = [self.CONTROLLER_EMBEDDED[Keys.LOGICAL_DRIVES][0]]
        self.assertEqual(merged_data[Keys.LOCAL_STORAGE][Keys.CONTROLLERS][self.INDEX_EMBED][Keys.LOGICAL_DRIVES],
                         expected_drives)

    def test_merge_when_drives_from_embedded_controller_have_changed_item(self):
        """
        Test the drive merge, although it's not supported by OneView.
        """
        drive_changed = dict(name="drive-1", raidLevel="RAID0")
        controller_embedded = deepcopy(self.CONTROLLER_EMBEDDED)
        controller_embedded[Keys.LOGICAL_DRIVES][0] = drive_changed

        data = dict(name="Profile101",
                    localStorage=dict(controllers=[self.CONTROLLER_MEZZ_1.copy(),
                                                   controller_embedded.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        drive_1_merged = dict(driveNumber=1, name="drive-1", raidLevel="RAID0", bootable=False, sasLogicalJBODId=None)
        expected_drives = [drive_1_merged,
                           self.CONTROLLER_EMBEDDED[Keys.LOGICAL_DRIVES][1]]
        self.assertEqual(merged_data[Keys.LOCAL_STORAGE][Keys.CONTROLLERS][self.INDEX_EMBED][Keys.LOGICAL_DRIVES],
                         expected_drives)

    def test_merge_when_drives_from_mezz_controller_have_new_item(self):
        new_drive = dict(name=None, raidLevel="RAID1", bootable=False, sasLogicalJBODId=3)
        controller_mezz = deepcopy(self.CONTROLLER_MEZZ_1)
        controller_mezz[Keys.LOGICAL_DRIVES].append(new_drive)

        data = dict(name="Profile101",
                    localStorage=dict(controllers=[controller_mezz.copy(),
                                                   self.CONTROLLER_EMBEDDED.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_drives = [self.CONTROLLER_MEZZ_1[Keys.LOGICAL_DRIVES][0],
                           self.CONTROLLER_MEZZ_1[Keys.LOGICAL_DRIVES][1],
                           new_drive]
        self.assertEqual(merged_data[Keys.LOCAL_STORAGE][Keys.CONTROLLERS][self.INDEX_MEZZ][Keys.LOGICAL_DRIVES],
                         expected_drives)

    def test_merge_when_drives_from_mezz_controller_have_removed_item(self):
        controller_mezz = deepcopy(self.CONTROLLER_MEZZ_1)
        controller_mezz[Keys.LOGICAL_DRIVES].pop()

        data = dict(name="Profile101",
                    localStorage=dict(controllers=[controller_mezz.copy(),
                                                   self.CONTROLLER_EMBEDDED.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        expected_drives = [self.CONTROLLER_MEZZ_1[Keys.LOGICAL_DRIVES][0]]
        self.assertEqual(merged_data[Keys.LOCAL_STORAGE][Keys.CONTROLLERS][self.INDEX_MEZZ][Keys.LOGICAL_DRIVES],
                         expected_drives)

    def test_merge_when_drives_from_mezz_controller_have_changed_item(self):
        """
        Test the drive merge, although it's not supported by OneView.
        """
        drive_changed = dict(sasLogicalJBODId=1, raidLevel="RAID0")
        controller_mezz = deepcopy(self.CONTROLLER_MEZZ_1)
        controller_mezz[Keys.LOGICAL_DRIVES][0] = drive_changed

        data = dict(name="Profile101",
                    localStorage=dict(controllers=[controller_mezz.copy(),
                                                   self.CONTROLLER_EMBEDDED.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        drive_1_merged = dict(name=None, raidLevel="RAID0", bootable=False, sasLogicalJBODId=1)
        expected_drives = [drive_1_merged,
                           self.CONTROLLER_MEZZ_1[Keys.LOGICAL_DRIVES][1]]
        self.assertEqual(merged_data[Keys.LOCAL_STORAGE][Keys.CONTROLLERS][self.INDEX_MEZZ][Keys.LOGICAL_DRIVES],
                         expected_drives)

    def test_merge_when_controller_drives_are_removed(self):
        controller_mezz = deepcopy(self.CONTROLLER_MEZZ_1)
        controller_mezz[Keys.LOGICAL_DRIVES] = []

        data = dict(name="Profile101",
                    localStorage=dict(controllers=[controller_mezz.copy(),
                                                   self.CONTROLLER_EMBEDDED.copy()]))
        resource = deepcopy(self.profile_with_local_storage)

        merged_data = ServerProfileMerger().merge_data(resource, data)

        self.assertFalse(merged_data[Keys.LOCAL_STORAGE][Keys.CONTROLLERS][self.INDEX_MEZZ][Keys.LOGICAL_DRIVES])
