# -*- coding: utf-8 -*-

"""
common.py
~~~~~~~~~~~~

This module implements the common and helper functions for the OneView REST API.

It has been deprecated and will be removed soon. We strongly recommend to use the OneViewClient class instead.
See more details at: https://github.com/HewlettPackard/python-hpOneView/tree/master/hpOneView/README.md
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import range
from future import standard_library

standard_library.install_aliases()

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
from warnings import warn
import logging

logger = logging.getLogger(__name__)


def deprecated(func):
    def wrapper(*args, **kwargs):
        warn("Module common is deprecated, use OneViewClient class instead", DeprecationWarning)
        return func(*args, **kwargs)

    return wrapper


# Looking for a switch type, using filters:
# https://<appliance>/rest/switch-types?filter="partNumber = '455880-B21'"
uri = {
    # ------------------------------------
    # Settings
    # ------------------------------------
    'globalSettings': '/rest/global-settings',
    'vol-tmplate-policy': '/rest/global-settings/StorageVolumeTemplateRequired',
    'eulaStatus': '/rest/appliance/eula/status',
    'eulaSave': '/rest/appliance/eula/save',
    'serviceAccess': '/rest/appliance/settings/enableServiceAccess',
    'service': '/rest/appliance/settings/serviceaccess',
    'applianceNetworkInterfaces': '/rest/appliance/network-interfaces',
    'healthStatus': '/rest/appliance/health-status',
    'version': '/rest/version',
    'supportDump': '/rest/appliance/support-dumps',
    'backups': '/rest/backups',
    'archive': '/rest/backups/archive',
    'dev-read-community-str': '/rest/appliance/device-read-community-string',
    'licenses': '/rest/licenses',
    'nodestatus': '/rest/appliance/nodeinfo/status',
    'nodeversion': '/rest/appliance/nodeinfo/version',
    'shutdown': '/rest/appliance/shutdown',
    'trap': '/rest/appliance/trap-destinations',
    'restores': '/rest/restores',
    'domains': '/rest/domains',
    'schema': '/rest/domains/schema',
    'progress': '/rest/appliance/progress',
    'appliance-firmware': '/rest/appliance/firmware/image',
    'fw-pending': '/rest/appliance/firmware/pending',
    # ------------------------------------
    # Security
    # ------------------------------------
    'activeSessions': '/rest/active-user-sessions',
    'loginSessions': '/rest/login-sessions',
    'users': '/rest/users',
    'userRole': '/rest/users/role',
    'changePassword': '/rest/users/changePassword',
    'roles': '/rest/roles',
    'category-actions': '/rest/authz/category-actions',
    'role-category-actions': '/rest/authz/role-category-actions',
    'validator': '/rest/authz/validator',
    # ------------------------------------
    # Facilities
    # ------------------------------------
    'datacenters': '/rest/datacenters',
    'powerDevices': '/rest/power-devices',
    'powerDevicesDiscover': '/rest/power-devices/discover',
    'racks': '/rest/racks',
    # ------------------------------------
    # Systems
    # ------------------------------------
    'servers': '/rest/server-hardware',
    'server-hardware-types': '/rest/server-hardware-types',
    'enclosures': '/rest/enclosures',
    'enclosureGroups': '/rest/enclosure-groups',
    'enclosurePreview': '/rest/enclosure-preview',
    'fwUpload': '/rest/firmware-bundles',
    'fwDrivers': '/rest/firmware-drivers',
    # ------------------------------------
    # Connectivity
    # ------------------------------------
    'conn': '/rest/connections',
    'ct': '/rest/connection-templates',
    'enet': '/rest/ethernet-networks',
    'fcnet': '/rest/fc-networks',
    'nset': '/rest/network-sets',
    'li': '/rest/logical-interconnects',
    'lig': '/rest/logical-interconnect-groups',
    'ic': '/rest/interconnects',
    'ictype': '/rest/interconnect-types',
    'uplink-sets': '/rest/uplink-sets',
    'ld': '/rest/logical-downlinks',
    'idpool': '/rest/id-pools',
    'vmac-pool': '/rest/id-pools/vmac',
    'vwwn-pool': '/rest/id-pools/vwwn',
    'vsn-pool': '/rest/id-pools/vsn',
    # ------------------------------------
    #  Server Profiles
    # ------------------------------------
    'profiles': '/rest/server-profiles',
    'profile-templates': '/rest/server-profile-templates',
    'profile-networks': '/rest/server-profiles/available-networks',
    'profile-networks-schema': '/rest/server-profiles/available-networks/schema',
    'profile-available-servers': '/rest/server-profiles/available-servers',
    'profile-available-servers-schema': '/rest/server-profiles/available-servers/schema',
    'profile-available-storage-system': '/rest/server-profiles/available-storage-system',
    'profile-available-storage-systems': '/rest/server-profiles/available-storage-systems',
    'profile-available-targets': '/rest/server-profiles/available-targets',
    'profile-messages-schema': '/rest/server-profiles/messages/schema',
    'profile-ports': '/rest/server-profiles/profile-ports',
    'profile-ports-schema': '/rest/server-profiles/profile-ports/schema',
    'profile-schema': '/rest/server-profiles/schema',
    # ------------------------------------
    #  Health
    # ------------------------------------
    'alerts': '/rest/alerts',
    'events': '/rest/events',
    'audit-logs': '/rest/audit-logs',
    'audit-logs-download': '/rest/audit-logs/download',
    # ------------------------------------
    #  Certificates
    # ------------------------------------
    'certificates': '/rest/certificates',
    'ca': '/rest/certificates/ca',
    'crl': '/rest/certificates/ca/crl',
    'rabbitmq-kp': '/rest/certificates/client/rabbitmq/keypair',
    'rabbitmq': '/rest/certificates/client/rabbitmq',
    'cert-https': '/rest/certificates/https',
    # ------------------------------------
    #  Searching and Indexing
    # ------------------------------------
    'resource': '/rest/index/resources',
    'association': '/rest/index/associations',
    'tree': '/rest/index/trees',
    'search-suggestion': '/rest/index/search-suggestions',
    # 'GetAllNetworks': ('/index/rest/index/resources'
    #                   '?sort=name:asc&category=fc-networks'
    #                   '&category=networks&start=0&count=-1'),
    # 'GetEthNetworks': ('/index/rest/index/resources'
    #                   '?sort=name:asc&category=networks&start=0&count=-1'),
    # 'GetFcNetworks': ('/index/rest/index/resources'
    #                  '?sort=name:asc&category=fc-networks&start=0&count=-1'),
    # ------------------------------------
    #  Logging and Tracking
    # ------------------------------------
    'task': '/rest/tasks',
    # ------------------------------------
    # Storage
    # ------------------------------------
    'storage-pools': '/rest/storage-pools',
    'storage-systems': '/rest/storage-systems',
    'storage-volumes': '/rest/storage-volumes',
    'vol-templates': '/rest/storage-volume-templates',
    'connectable-vol': '/rest/storage-volume-templates/connectable-volume-templates',
    'attachable-volumes': '/rest/storage-volumes/attachable-volumes',
    # ------------------------------------
    # FC-SANS
    # ------------------------------------
    'device-managers': '/rest/fc-sans/device-managers',
    'managed-sans': '/rest/fc-sans/managed-sans',
    'providers': '/rest/fc-sans/providers',
    # ------------------------------------
    # Metrcs
    # ------------------------------------
    'metricsCapabilities': '/rest/metrics/capability',
    'metricsConfiguration': '/rest/metrics/configuration',
    # ------------------------------------
    # Uncategorized
    # ------------------------------------
    'unmanaged-devices': '/rest/unmanaged-devices'
}


############################################################################
# Utility to print resource to standard output
############################################################################
@deprecated
def print_entity(entity):
    if not entity:
        return
    if 'name' in entity:
        print(('name: ', entity['name']))
    if isinstance(entity, dict):
        for key, value in list(entity.items()):
            print(('\t', key, ' = ', value))
    elif hasattr(entity, '__iter__'):
        for item in entity:
            print(('\t', item))
    else:
        print(('\t', entity))


@deprecated
def print_task_tuple(entities):
    print('Task/Entity Tuples:')
    for indx, (task, entity) in enumerate(entities):
        print((indx, ') Entry'))
        try:
            print(('\tTask: ', task['name'], task['taskState'],
                   task['taskStatus'], task['uri']))
        except KeyError:
            print('\tTask: n/a')
        try:
            print(('\tResource: ', entity['name'], entity['uri']))
        except KeyError:
            print('\tResource: n/a')


@deprecated
def get_members(mlist):
    if not mlist:
        return []
    if not mlist['members']:
        return []
    return mlist['members']


@deprecated
def get_member(mlist):
    if not mlist:
        return None
    if not mlist['members']:
        return None
    return mlist['members'][0]


############################################################################
# Create default Resource Instances
############################################################################
@deprecated
def make_user_dict(name, password, enabled, fullName, emailAddress,
                   officePhone, mobilePhone, roles=[]):
    return {
        'userName': name,
        'password': password,
        'fullName': fullName,
        'emailAddress': emailAddress,
        'officePhone': officePhone,
        'mobilePhone': mobilePhone,
        'enabled': enabled,
        'type': 'UserAndRoles',
        'roles': roles}


@deprecated
def make_Bandwidth(typicalBandwidth=2500, maximumBandwidth=10000):
    """ Create an Bandwidth dictionary

    Args:
        typicalBandwidth:
            The transmit throughput (mbps) that should be allocated to this
            connection.  For FlexFabric connections,this value must not exceed
            the maximum bandwidth of the selected network
        maximumBandwidth:
            Maximum transmit throughput (mbps) allowed on this connection. The
            value is limited by the maximum throughput of the network link and
            maximumBandwidth of the selected network.

    Returns: dict
    """

    return {'maximumBandwidth': maximumBandwidth,
            'typicalBandwidth': typicalBandwidth
            }


@deprecated
def make_network_set(name, networkUris=[]):
    """ Create an network-set dictionary

    Args:
        name:
            Name of the Network Set
        networkUris:
            A set of Ethernet network URIs that will be members of this network
            set. NOTE: all Ethernet networks in a network set must have unique
            VLAN IDs.

    Returns: dict
    """

    return {
        'name': name,
        'type': 'network-set',
        'nativeNetworkUri': None,
        'networkUris': networkUris[:],
        'connectionTemplateUri': None}


@deprecated
def make_ethernet_networkV3(name, description=None, ethernetNetworkType=None,
                            purpose='General', privateNetwork=False,
                            smartLink=True, vlanId=0):
    """ Create an ethernet-networkV3 dictionary

    Args:
        name:
            Name of the Ethernet Network
        description:
            Breif description of the Ethernet Network
        vlanId:
            The Virtual LAN (VLAN) identification number assigned to the
            network. The VLAN ID is optional when ethernetNetworkType is
            Untagged or Tunnel. Multiple Ethernet networks can be defined
            with the same VLAN ID, but all Ethernet networks in an uplink set
            or network set must have unique VLAN IDs. The VLAN ID cannot be
            changed once the network has been created.
        purpose:
            A description of the network's role within the logical
            interconnect. Values: 'FaultTolerance', 'General', 'Management',
            or 'VMMigration'
        smartLink:
            When enabled, the network is configured so that, within a logical
            interconnect, all uplinks that carry the network are monitored.
            If all uplinks lose their link to external interconnects, all
            corresponding dowlink (server) ports which connect to the network
            are forced into an unlinked state. This allows a server side NIC
            teaming driver to automatically failover to an alternate path.
        privateNetwork:
             When enabled, the network is configured so that all downlink
             (server) ports connected to the network are prevented from
             communicating with each other within the logical interconnect.
             Servers on the network only communicate with each other through an
             external L3 router that redirects the traffic back to the logical
             interconnect.
        ethernetNetworkType:
            The type of Ethernet network. It is optional. If this field is
            missing or its value is Tagged, you must supply a valid vlanId;
            if this value is Untagged or Tunnel, please either ignore vlanId
            or specify vlanId equals 0. Values: 'NotApplicable', 'Tagged',
            'Tunnel', 'Unknown', or 'Untagged'.

    Returns: dict
    """
    return {
        'name': name,
        'type': 'ethernet-networkV3',
        'purpose': purpose,
        'connectionTemplateUri': None,
        'vlanId': vlanId,
        'smartLink': smartLink,
        'ethernetNetworkType': ethernetNetworkType,
        'privateNetwork': privateNetwork}


@deprecated
def make_fc_networkV2(name, autoLoginRedistribution=True, description=None,
                      fabricType='FabricAttach', linkStabilityTime=30,
                      managedSanUri=None):
    """ Create an ethernet-networkV3 dictionary

    Args:
        name:
            Name of the Fibre Channel Network
        autoLoginRedistribution:
             Used for load balancing when logins are not evenly distributed
             over the Fibre Channel links, such as when an uplink that was
             previously down becomes available.
        description:
            Breif description of the Fibre Channel Network
        fabricType:
            The supported Fibre Channel access method. Values: 'FabricAttach',
            or 'DirectAttach'.
        linkStabilityTime:
            The time interval, expressed in seconds, to wait after a link that
            was previously offline becomes stable, before automatic
            redistribution occurs within the fabric. This value is not
            effective if autoLoginRedistribution is false.
        managedSanUri:
            The managed SAN URI that is associated with this Fibre Channel
            network. This value should be null for Direct Attach Fibre Channel
            networks and may be null for Fabric Attach Fibre Channel networks.

    Returns: dict
    """
    return {
        'name': name,
        'type': 'fc-networkV2',
        'connectionTemplateUri': None,
        'fabricType': fabricType,
        'autoLoginRedistribution': autoLoginRedistribution,
        'linkStabilityTime': linkStabilityTime,
        'managedSanUri': managedSanUri}


@deprecated
def make_interconnect_map_template():
    return {
        'interconnectMapEntryTemplates':
            [{'logicalLocation':
                {
                    'locationEntries':
                        [{'type': 'Bay', 'relativeValue': N},
                         {'type': 'Enclosure', 'relativeValue': 1}]
                }, 'permittedInterconnectTypeUri': None, 'logicalDownlinkUri': None} for N in range(1, 9)],
    }


@deprecated
def make_enet_settings(name,
                       enableIgmpSnooping=False,
                       igmpIdleTimeoutInterval=260,
                       enableFastMacCacheFailover=True,
                       macRefreshInterval=5,
                       enableNetworkLoopProtection=True):
    return {
        'type': 'EthernetInterconnectSettings',
        'name': name,
        'enableIgmpSnooping': enableIgmpSnooping,
        'igmpIdleTimeoutInterval': igmpIdleTimeoutInterval,
        'enableFastMacCacheFailover': enableFastMacCacheFailover,
        'macRefreshInterval': macRefreshInterval,
        'enableNetworkLoopProtection': enableNetworkLoopProtection,
        'interconnectType': 'Ethernet'
        # 'description': null,
    }


@deprecated
def make_storage_vol_templateV3(name,
                                capacity,
                                shareable,
                                storagePoolUri,
                                state='Normal',
                                description='',
                                storageSystemUri=None,
                                snapshotPoolUri=None,
                                provisionType='Thin'):
    return {
        'provisioning': {
            'shareable': shareable,
            'provisionType': provisionType,
            'capacity': capacity,
            'storagePoolUri': storagePoolUri},
        'name': name,
        'state': state,
        'description': description,
        'storageSystemUri': storageSystemUri,
        'snapshotPoolUri': snapshotPoolUri,
        'type': 'StorageVolumeTemplateV3'
    }


@deprecated
def make_storage_volume(name,
                        capacity,
                        shareable,
                        storagePoolUri,
                        description='',
                        provisionType='Thin'):
    return {
        'name': name,
        'description': description,
        'provisioningParameters': {
            'shareable': shareable,
            'provisionType': provisionType,
            'requestedCapacity': capacity,
            'storagePoolUri': storagePoolUri},
        'type': 'StorageVolumeTemplate'
    }


@deprecated
def make_connectionInfo_dict(hostname, port, user, passwd, ssl=True):
    return {'connectionInfo': [
        {'name': 'Host',
         'value': hostname},
        {'name': 'Port',
         'value': port},
        {'name': 'Username',
         'value': user},
        {'name': 'Password',
         'value': passwd},
        {'name': 'UseSsl',
         'value': ssl}]
    }


@deprecated
def make_LogicalInterconnectGroupV2(name, ethernetSettings=[]):
    return {
        'name': name,
        'type': 'logical-interconnect-groupV2',
        'interconnectMapTemplate': make_interconnect_map_template(),
        'uplinkSets': [],  # call make_uplink_template
        'stackingMode': 'Enclosure',
        'ethernetSettings': ethernetSettings,
        # 'telemetryConfiguration': None,
        # 'snmpConfiguration' : None,
        # 'description': None
    }


@deprecated
def make_LogicalInterconnectGroupV3(name, ethernetSettings=[],
                                    enclosureType='C7000'):
    return {
        'name': name,
        'type': 'logical-interconnect-groupV3',
        'interconnectMapTemplate': make_interconnect_map_template(),
        'uplinkSets': [],  # call make_uplink_template
        'stackingMode': 'Enclosure',
        'ethernetSettings': ethernetSettings,
        # 'telemetryConfiguration': None,
        # 'snmpConfiguration' : None,
        # 'description': None
    }


@deprecated
def make_EthernetSettingsV2(enableFastMacCacheFailover=True,
                            enableIgmpSnooping=False,
                            enableNetworkLoopProtection=True,
                            enablePauseFloodProtection=True,
                            igmpIdleTimeoutInterval=260,
                            macRefreshInterval=5):
    return {
        'enableFastMacCacheFailover': enableFastMacCacheFailover,
        'enableIgmpSnooping': enableIgmpSnooping,
        'enableNetworkLoopProtection': enableNetworkLoopProtection,
        'enablePauseFloodProtection': enablePauseFloodProtection,
        'igmpIdleTimeoutInterval': igmpIdleTimeoutInterval,
        'macRefreshInterval': macRefreshInterval,
        'type': 'EthernetInterconnectSettingsV2'
    }


@deprecated
def make_EthernetSettingsV3(enableFastMacCacheFailover=True,
                            enableIgmpSnooping=False,
                            enableNetworkLoopProtection=True,
                            enablePauseFloodProtection=True,
                            enableRichTLV=False,
                            igmpIdleTimeoutInterval=260,
                            macRefreshInterval=5):
    return {
        'enableFastMacCacheFailover': enableFastMacCacheFailover,
        'enableIgmpSnooping': enableIgmpSnooping,
        'enableNetworkLoopProtection': enableNetworkLoopProtection,
        'enablePauseFloodProtection': enablePauseFloodProtection,
        'igmpIdleTimeoutInterval': igmpIdleTimeoutInterval,
        'macRefreshInterval': macRefreshInterval,
        'type': 'EthernetInterconnectSettingsV3'
    }


@deprecated
def make_trapdestinations_dict(trapDestination,
                               communityString='public',
                               enetTrapCategories=['Other',
                                                   'PortStatus',
                                                   'PortThresholds'],
                               fcTrapCategories=['Other', 'PortStatus'],
                               trapFormat='SNMPv1',
                               trapSeverities=['Critical',
                                               'Info',
                                               'Major',
                                               'Minor',
                                               'Normal',
                                               'Unknown',
                                               'Warning'],
                               vcmTrapCategories=['Legacy']):
    return {
        'trapDestination': trapDestination,
        'communityString': communityString,
        'enetTrapCategories': enetTrapCategories,
        'fcTrapCategories': fcTrapCategories,
        'trapFormat': trapFormat,
        'trapSeverities': trapSeverities,
        'vcmTrapCategories': vcmTrapCategories
    }


@deprecated
def make_snmpconfiguration_dict(enabled=False,
                                readCommunity='public',
                                snmpAccess=[],
                                systemContact=None,
                                trapDestinations=[]):
    return {
        'enabled': enabled,
        'readCommunity': readCommunity,
        'snmpAccess': snmpAccess,
        'systemContact': systemContact,
        'trapDestinations': trapDestinations,
    }


@deprecated
def set_iobay_occupancy(switchMap, bays, stype):
    for location in switchMap['interconnectMapEntryTemplates']:
        entries = location['logicalLocation']['locationEntries']
        if [x for x in entries if x['type'] == 'Bay' and x['relativeValue'] in bays]:
            location['permittedInterconnectTypeUri'] = stype


@deprecated
def get_iobay_entry(interconnectMap, bay):
    if not interconnectMap:
        return
    for iobay_entry in interconnectMap['interconnectMapEntryTemplates']:
        entries = iobay_entry['logicalLocation']['locationEntries']
        for entry in entries:
            if entry['type'] == 'Bay':
                if bay == entry['relativeValue']:
                    return iobay_entry


@deprecated
def make_UplinkSetGroupV2(name,
                          ethernetNetworkType='Tagged',
                          lacpTimer='Long',
                          logicalPortConfigInfos=[],
                          mode='Auto',
                          nativeNetworkUri=None,
                          networkType='Ethernet',
                          networkUris=[]):
    if networkType == 'Ethernet':
        return {'name': name,
                'ethernetNetworkType': ethernetNetworkType,
                'lacpTimer': lacpTimer,
                'networkUris': networkUris,
                'networkType': networkType,
                'mode': mode,
                'primaryPort': None,
                'logicalPortConfigInfos': logicalPortConfigInfos,
                'nativeNetworkUri': nativeNetworkUri,
                }
    if networkType == 'FibreChannel':
        return {'name': name,
                'ethernetNetworkType': 'NotApplicable',
                'networkUris': networkUris,
                'logicalPortConfigInfos': logicalPortConfigInfos,
                'networkType': 'FibreChannel',  # Ethernet or FibreChannel
                'mode': mode,
                }
    raise Exception('networkType must be Ethernet or FibreChannel.')


@deprecated
def make_port_config_info(enclosure, bay, port, speed='Auto'):
    return {'logicalLocation': {
        'locationEntries':
            [{'type': 'Enclosure', 'relativeValue': enclosure},
             {'type': 'Bay', 'relativeValue': bay},
             {'type': 'Port', 'relativeValue': port}]
    },
        'desiredSpeed': speed
    }


@deprecated
def make_EnclosureGroupV200(associatedLIGs, name,
                            powerMode='RedundantPowerSupply'):
    """ Create an EnclosureGroupV200 dictionary

    Args:
        associatedLIGs:
            A sorted list of logical interconnect group URIs associated with
            the enclosure group.
        name:
            The name of the enclosure group.
        stackingMode:
            Stacking mode of the enclosure group. Currently only the Enclosure
            mode is supported. Values are 'Enclosure', 'MultiEnclosure',
            'None', or 'SwitchParis'.
        powerMode:
             Power mode of the enclosure group. Values are 'RedundantPowerFeed'
             or 'RedundantPowerSupply'.

    Returns: dict
    """
    ligUri = associatedLIGs['uri']
    icms = associatedLIGs['interconnectMapTemplate']['interconnectMapEntryTemplates']
    ligs = []
    # With the 200 API, the LIG uri can only be assigned if the LIG contains a
    # definition of the interconnect bay. I.E. if the LIG only has ICM 1 and 2
    # defined then 3 - 8 must be set to None. I.E:
    #    'interconnectBayMappings': [{'interconnectBay': 1,
    #                                 'logicalInterconnectGroupUri':
    #                                    '/rest/logical-interconnect-groups/f8371e33-6d07-4477-9b63-cf8400242059'},
    #                                {'interconnectBay': 2,
    #                                 'logicalInterconnectGroupUri':
    #                                    '/rest/logical-interconnect-groups/f8371e33-6d07-4477-9b63-cf8400242059'}]}
    #                                {'interconnectBay': 3,
    #                                 'logicalInterconnectGroupUri': None},
    #                                {'interconnectBay': 4,
    #                                 'logicalInterconnectGroupUri': None},
    #                                 ...
    for N in range(1, 9):
        if N > len(icms):
            ligs.append({'interconnectBay': N,
                         'logicalInterconnectGroupUri': None})
        else:
            ligs.append({'interconnectBay': N,
                         'logicalInterconnectGroupUri': ligUri})
    return {
        'name': name,
        'type': 'EnclosureGroupV200',
        'stackingMode': 'Enclosure',
        'powerMode': powerMode,
        'enclosureCount': 1,
        'enclosureTypeUri': "/rest/enclosure-types/c7000",
        'interconnectBayMappingCount': 8,
        'interconnectBayMappings': ligs
    }


@deprecated
def make_enclosure_dict(host, user, passwd, egroup, state="",
                        licenseIntent='OneView',
                        firmwareBaseLineUri=None, force=False, forcefw=False):
    return {
        'hostname': host,
        'username': user,
        'password': passwd,
        'force': force,
        'enclosureGroupUri': egroup,
        'firmwareBaselineUri': firmwareBaseLineUri,
        'updateFirmwareOn': 'EnclosureOnly',
        'forceInstallFirmware': forcefw,
        'state': state,
        'licensingIntent': licenseIntent}


@deprecated
def make_monitored_enclosure_dict(host, user, passwd, state='Monitored',
                                  licenseIntent='OneViewStandard', force=False):
    return {
        'hostname': host,
        'username': user,
        'password': passwd,
        'force': force,
        'state': state,
        'licensingIntent': licenseIntent}


@deprecated
def make_storage_system_dict(mdom, udom, mports, uports):
    return {
        'type': 'StorageSystem',
        'managedDomain': mdom,
        'unmanagedDomains': udom[:],
        'managedPorts': mports[:],
        'unmanagedPorts': uports[:],
    }


@deprecated
def make_ProfileConnectionV4(cid, name, networkUri, profileTemplateConnection,
                             connectionBoot=None, functionType='Ethernet',
                             mac=None, macType='Virtual', portId='Auto',
                             requestedMbps=None, wwnn=None, wwpn=None,
                             wwpnType='Virtual'):
    """ Create a ProfileConnectionV4 dictionary

    Args:
        connectionBoot:
            ConnectionBoot dictionary that descirbes server boot management.
        functionType:
            The function of the connection, either 'Ethernet' or 'FibreChannel'
        cid:
            A unique identifier for this connection. When creating or editing a
            profile, an id is automatically assigned if the attribute is
            omitted or 0 is specified. When editing a profile, a connection is
            created if the id does not identify an existing connection.
        mac:
            The MAC address that is currently programmed on the FlexNic. The
            value can be a virtual MAC, user defined MAC or physical MAC read
            from the device. It cannot be modified after the connection is
            created.
        macType:
            Specifies the type of MAC address to be programmed into the IO
            Devices. The value can be 'Virtual', 'Physical' or 'UserDefined'.
            It cannot be modified after the connection is created.
        name:
            A string used to identify the respective connection. The connection
            name is case insensitive, limited to 63 characters and must be
            unique within the profile.
        networkUri:
            Identifies the network or network set to be connected. Use GET
            /rest/server-profiles/available-networks to retrieve the list of
            available Ethernet networks, Fibre Channel networks and network
            sets that are available along with their respective ports.
        profileTemplateConnection:
            Specifies if the connection list is to be used in defining a server
            profile template.
        portId:
            Identifies the port (FlexNIC) used for this connection, for
            example 'Flb 1:1-a'. The port can be automatically selected by
            specifying 'Auto', 'None', or a physical port when creating or
            editing the connection. If 'Auto' is specified, a port that
            provides access to the selected network(networkUri) will be
            selected. A physical port(e.g. 'Flb 1:2') can be specified if the
            choice of a specific FlexNIC on the physical port is not important.
            If 'None' is specified, the connection will not be configured on
            the server hardware. When omitted, portId defaults to 'Auto'. Use
            / rest / server - profiles / profile - ports to retrieve the list
            of available ports.
        requestedMbps:
            The transmit throughput (mbps) that should be allocated to this
            connection. For FlexFabric connections, this value must not exceed
            the maximum bandwidth of the selected network (networkUri). If
            omitted, this value defaults to the typical bandwidth value of the
            selected network. The sum of the requestedBW values for the
            connections (FlexNICs) on an adapter port cannot exceed the
            capacity of the network link. For Virtual Connect Fibre Channel
            connections, the available discrete values are based on the adapter
            and the Fibre Channel interconnect module.
        wwnn:
            The node WWN address that is currently programmed on the FlexNic.
            The value can be a virtual WWNN, user defined WWNN or physical WWNN
            read from the device. It cannot be modified after the connection
            is created.
        wwpn:
            The port WWN address that is currently programmed on the FlexNIC.
            The value can be a virtual WWPN, user defined WWPN or the physical
            WWPN read from the device. It cannot be modified after the
            connection is created.
        wwpnType:
            Specifies the type of WWN address to be porgrammed on the FlexNIC.
            The value can be 'Virtual', 'Physical' or 'UserDefined'. It cannot
            be modified after the connection is created. If the WWPN, WWNN,
            MAC, connection's macType and connection's wwpnType are omitted in
            the FC connection, then the connection's macType and connection's
            wwpnType are set to the profile's default macType and profile's
            default wwnnType.

    Returns: dict
    """
    if profileTemplateConnection:
        return {
            'boot': connectionBoot,
            'functionType': functionType,
            'id': cid,
            'name': name,
            'networkUri': networkUri,
            'portId': portId,
            'requestedMbps': requestedMbps,
        }
    else:
        return {
            'boot': connectionBoot,
            'functionType': functionType,
            'id': cid,
            'mac': mac,
            'macType': macType,
            'name': name,
            'networkUri': networkUri,
            'portId': portId,
            'requestedMbps': requestedMbps,
            'wwnn': wwnn,
            'wwpn': wwpn,
            'wwpnType': wwpnType,
        }


@deprecated
def make_ConnectionBoot(priority='Primary',
                        arrayWwpn=None,
                        lun=None):
    """ Create a ConnectionBoot dictionary

    Args:
        priority:
            Indicates the boot priority for this device. PXE and Fibre Channel
            connections are treated separately; an Ethernet connection and a
            Fibre Channel connection can both be marked as Primary. The 'order'
            attribute controls ordering among the different device types.
            Choices are 'NotBootable', 'Primary', or 'Secondary'
        arrayWwpn:
            The wwpn of the target device that provides access to the Boot
            Volume, 16 HEX digits as a string.
        lun:
            The LUN of the boot volume presented by the target device. The
            value can be either 1 to 3 decimal digits in the range 0 to 255 or
            13 to 16 HEX digits as a string.

    Returns: dict
    """
    if arrayWwpn is None and lun is None:
        return {
            'priority': priority}
    else:
        return {
            'priority': priority,
            'targets': make_BootTarget(arrayWwpn, lun)}


@deprecated
def make_BootTarget(arrayWwpn=None, lun=None):
    """ Create a BootTarget dictionary

    Args:
        arrayWwpn:
            The wwpn of the target device that provides access to the Boot
            Volume, 16 HEX digits as a string.
        lun:
            The LUN of the boot volume presented by the target device. The
            value can be either 1 to 3 decimal digits in the range 0 to 255 or
            13 to 16 HEX digits as a string.

    Returns: dict
    """
    return [{'arrayWwpn': arrayWwpn,
             'lun': lun}]


@deprecated
def make_ServerProfileTemplateV1(name=None,
                                 description=None,
                                 serverProfileDescription=None,
                                 serverHardwareTypeUri=None,
                                 enclosureGroupUri=None,
                                 affinity=None,
                                 hideUnusedFlexNics=None,
                                 profileConnectionV4=None,
                                 firmwareSettingsV3=None,
                                 bootSettings=None,
                                 bootModeSetting=None,
                                 sanStorageV3=None):
    """
    Create a ServerProfileTemplateV1 dictionary for use with the V200 API
    Args:
        name:
            Unique name of the Server Profile Template
        description:
            Description of the Server Profile Template
        serverProfileDescription:
            The description of the server profiles created from this template.
        serverHardwareTypeUri:
            Identifies the server hardware type for which the Server Profile
            was designed. The serverHardwareTypeUri is determined when the
            profile is created.
        enclosureGroupUri:
             Identifies the enclosure group for which the Server Profile Template
             was designed. The enclosureGroupUri is determined when the profile
             template is created and cannot be modified.
        affinity:
            This identifies the behavior of the server profile when the server
            hardware is removed or replaced. This can be set to 'Bay' or
            'BayAndServer'.
        hideUnusedFlexNics:
            This setting controls the enumeration of physical functions that do
            not correspond to connections in a profile.
        profileConnectionV4:
            An array of profileConnectionV4
        firmwareSettingsV3:
            FirmwareSettingsV3 dictionary that defines the firmware baseline
            and management
        bootSettings:
            Dictionary that indicates that the server will attempt to boot from
            this connection. This object can only be specified if
            "boot.manageBoot" is set to 'true'
        bootModeSetting:
            Dictionary that describes the boot mode settings to be configured on
            Gen9 and newer servers.
        sanStorageV3:
            Dictionary that describes the SAN storage settings.

    Returns: dict
    """
    return {
        'type': 'ServerProfileTemplateV1',
        'name': name,
        'description': description,
        'serverProfileDescription': serverProfileDescription,
        'serverHardwareTypeUri': serverHardwareTypeUri,
        'enclosureGroupUri': enclosureGroupUri,
        'affinity': affinity,
        'hideUnusedFlexNics': hideUnusedFlexNics,
        'connections': profileConnectionV4,
        'firmware': firmwareSettingsV3,
        'boot': bootSettings,
        'bootMode': bootModeSetting,
        'sanStorage': sanStorageV3
    }


@deprecated
def make_ServerProfileV5(affinity='Bay',
                         biosSettings=None,
                         bootSettings=None,
                         bootModeSetting=None,
                         profileConnectionV4=None,
                         description=None,
                         firmwareSettingsV3=None,
                         hideUnusedFlexNics=True,
                         localStorageSettingsV3=None,
                         macType='Virtual',
                         name=None,
                         sanStorageV3=None,
                         serialNumber=None,
                         serialNumberType='Physical',
                         serverHardwareTypeUri=None,
                         serverHardwareUri=None,
                         serverProfileTemplateUri=None,
                         uuid=None,
                         wwnType='Virtual'):
    """ Create a ServerProfileV5 dictionary for use with the V200 API

    Args:
        affinity:
            This identifies the behavior of the server profile when the server
            hardware is removed or replaced. This can be set to 'Bay' or
            'BayAndServer'.
        biosSettings:
            Dictionary that describes Server BIOS settings
        bootSettings:
            Dictionary that indicates that the server will attempt to boot from
            this connection. This object can only be specified if
            "boot.manageBoot" is set to 'true'
        bootModeSetting:
            Dictionary that describes the boot mode settings to be configured on
            Gen9 and newer servers.
        profileConnectionV4:
            Array of ProfileConnectionV3
        description:
            Description of the Server Profile
        firmwareSettingsV3:
            FirmwareSettingsV3 dictionary that defines the firmware baseline
            and management
        hideUnusedFlexNics:
            This setting controls the enumeration of physical functions that do
            not correspond to connections in a profile.
        localStorageSettingsV3:
            Dictionary that describes the local storage settings.
        macType:
            Specifies the type of MAC address to be programmed into the IO
            devices. The value can be 'Virtual', 'Physical' or 'UserDefined'.
        name:
            Unique name of the Server Profile
        sanStorageV3:
            Dictionary that describes the SAN storage settings.
        serialNumber:
            A 10-byte value that is exposed to the Operating System as the
            server hardware's Serial Number. The value can be a virtual serial
            number, user defined serial number or physical serial number read
            from the server's ROM. It cannot be modified after the profile is
            created.
        serialNumberType:
             Specifies the type of Serial Number and UUID to be programmed into
             the server ROM. The value can be 'Virtual', 'UserDefined', or
             'Physical'. The serialNumberType defaults to 'Virtual' when
             serialNumber or uuid are not specified. It cannot be modified
             after the profile is created.
        serverHardwareTypeUri:
            Identifies the server hardware type for which the Server Profile
            was designed. The serverHardwareTypeUri is determined when the
            profile is created.
        serverHardwareUri:
             Identifies the server hardware to which the server profile is
             currently assigned, if applicable
        serverProfileTemplateUri:
            Identifies the Server profile template the Server Profile is based
            on.
        uuid:
            A 36-byte value that is exposed to the Operating System as the
            server hardware's UUID. The value can be a virtual uuid, user
            defined uuid or physical uuid read from the server's ROM. It
            cannot be modified after the profile is created.
        wwnType:
             Specifies the type of WWN address to be programmed into the IO
             devices. The value can be 'Virtual', 'Physical' or 'UserDefined'.
             It cannot be modified after the profile is created.

    Returns: dict
    """

    return {
        'affinity': affinity,
        'bios': biosSettings,
        'boot': bootSettings,
        'bootMode': bootModeSetting,
        'connections': profileConnectionV4,
        'description': description,
        'firmware': firmwareSettingsV3,
        'hideUnusedFlexNics': hideUnusedFlexNics,
        'localStorage': localStorageSettingsV3,
        'macType': macType,
        'name': name,
        'sanStorage': sanStorageV3,
        'serialNumber': serialNumber,
        'serialNumberType': serialNumberType,
        'serverHardwareTypeUri': serverHardwareTypeUri,
        'serverHardwareUri': serverHardwareUri,
        'serverProfileTemplateUri': serverProfileTemplateUri,
        'type': 'ServerProfileV5',
        'uuid': uuid,
        'wwnType': wwnType
    }


def make_FirmwareSettingsV3(firmwareUri,
                            firmwareInstallType,
                            manageFirmware=True,
                            forceInstallFirmware=False):
    """ Create a FirmwareSettingsV3 dictionary for use with the V200 API

    Args:
        firmwareUri:
            Identifies the firmware baseline to be applied to the server
            hardware.
        firmwareInstallType:
            FirmwareAndOSDrivers:
                Updates the firmware and OS drivers without powering down the
                server hardware using HPE Smart Update Tools.
            FirmwareOnly:
                 Updates the firmware without powering down the server hardware
                 using using HPE Smart Update Tools.
            FirmwareOnlyOfflineMode:
                Manages the firmware through HPE OneView. Selecting this option
                requires the server hardware to be powered down.
        manageFirmware:
            Indicates that the server firmware is configured using the server
            profile
        forceInstallFirmware:
            Force installation of firmware even if same or newer version is
            installed.

    Returns: dict
    """

    return {'firmwareBaselineUri': firmwareUri,
            'manageFirmware': manageFirmware,
            'forceInstallFirmware': forceInstallFirmware
            }


@deprecated
def make_BiosSettings(manageBios=True, overriddenSettings=[]):
    return {'manageBios': manageBios,
            'overriddenSettings': overriddenSettings
            }


def make_BootSettings(order, manageBoot=False):
    """ Create a BootSettings dictionary for use with ServerProfileV5

    Args:
        manageBoot:
            Indicates whether the boot order is configured using the server
            profile.
        order:
            Defines the order in which boot will be attempted on the available
            devices as an array of strings: 'CD', 'USB', 'HardDisk', 'PXE'

    Returns: dict
    """
    return {'manageBoot': manageBoot,
            'order': order
            }


def make_BootModeSetting(manageMode, mode, pxeBootPolicy):
    """ Create a BootModeSetting dictionary (only with Gen9 and newer)

    Args:
        manageMode:
           Boolean value indicates whether the boot mode is configured using
           the server profile.
        mode:
            The environment used for server boot operations. Supported values
            are: 'UEFI', 'UEFIOptimized', or 'BIOS'.
        pxeBootPolicy:
            Defines the filtering or priority of the PXE boot options for each
            enabled NIC port. This field is required only when the "mode" is
            set to "UEFI" or "UEFIOptimized". Possible values are:

                'Auto': No change from current server setting
                'IPv4': Only IPv4 entries will be allowed in the boot order.
                'IPv6': Only IPv6 entries will be allowed in the boot order.
                'IPv4ThenIPv6': both IPv4 and IPv6 entries will be present in
                                the boot order with IPV4 entries coming first.
                'IPv6ThenIPv4': both IPv4 and IPv6 entries will be present in
                                the boot order with IPv6 entries coming first.

    Returns: dict
    """
    return {'manageMode': manageMode,
            'mode': mode,
            'pxeBootPolicy': pxeBootPolicy
            }


def make_LocalStorageSettingsV3(controllers):
    """ Create a LocalStorageSettingsV3 dictionary

    Args:
        controllers:
            Array of LocalStorageEmbeddedController

    Returns: dict
    """
    return {'controllers': controllers}


def make_LocalStorageEmbeddedController(importConfiguration, initialize,
                                        LogicalDrives, managed, mode,
                                        slotNumber='0'):
    """ Create a LocalStorageEmbeddedController dictionary

    Args:
        importConfiguration:
            Boolean, should the logical drives in the current configuration be
            imported.
        initialize:
            Boolearn, should the controller be initalized before configuration.
        LogicalDrives:
            Array of LogicalDrivesV3
        managed:
            Boolean value determines if the controler is managed by OneView
        mode:
            Determines the mode of operation of the controller. The controller
            mode can be RAID or HBA.
        slotNumber:
            The PCI slot number used by the controller. This value will always
            be set to '0;, as only the embedded controller is supported in the
            current version.

    Returns: dict
    """
    return {'slotNumber': slotNumber,
            'managed': managed,
            'mode': mode,
            'initialize': initialize,
            'importConfiguration': importConfiguration,
            'logicalDrives': LogicalDrives
            }


def make_LogicalDriveV3(bootable, driveName, driveTechnology,
                        numPhysicalDrives, raidLevel):
    """ Create a LocalDriveV3 dictionary

    Args:
        bootable:
            Indicates if the logical drive is bootable or not.
        driveName:
            The name of the logical drive.
        driveTechnology:
            Defines the interface type for drives that will be used to build
            the logical drive. Supported values depend on the local storage
            capabilities of the selected server hardware type.
        numPhysicalDrives:
            The number of physical drives to be used to build the logical
            drive. The provided values must be consistent with the selected
            RAID level and cannot exceed the maximum supported number of
            drives for the selected server hardware type.
        raidLevel:
            The RAID level of the logical drive.

    Returns: dict
    """
    return {'bootable': bootable,
            'driveName': driveName,
            'driveTechnology': driveTechnology,
            'numPhysicalDrives': numPhysicalDrives,
            'raidLevel': raidLevel
            }


@deprecated
def make_SanStorageV3(hostOSType, manageSanStorage, volumeAttachments):
    """ Create a SanStorageV3 dictionary

    Args:
        hostOSType:
            The operating system type of the host. To retrieve the list of
            supported host OS types, issue a REST Get request using the
            /rest/storage-systems/host-types API.
        manageSanStorage:
            Boolean, identifies if SAN is managed in the server profile.
        volumeAttachments:
            Array of VolumeAttachmentV2

    Returns: dict
    """
    return {'hostOSType': hostOSType,
            'manageSanStorage': manageSanStorage,
            'volumeAttachments': [volumeAttachments],
            }


@deprecated
def make_VolumeAttachmentV2(lun=None,
                            lunType='Auto',
                            permanent=False,
                            storagePaths=[],
                            volumeName=None,
                            volumeProvisionType='Thin',
                            volumeProvisionedCapacityBytes=None,
                            volumeShareable=False,
                            volumeStoragePoolUri=None,
                            volumeStorageSystemUri=None,
                            volumeUri=None):
    """ Create a VolumeAttachmentV2 dictionary

    Args:
        lun:
            The logical unit number.
        lunType:
            The logical unit number type: 'Auto' or 'Manual'.
        permanent:
            If true, indicates that the volume will persist when the profile is
            deleted. If false, then the volume will be deleted when the profile
            is deleted.
        storagePaths:
            Array of StoragePathV2
        volumeName:
            The name of the volume. Required when creating a volume.
        volumeProvisionType:
            The provisioning type of the new volume: 'Thin' or 'Thick'. This
            attribute is required when creating a volume.
        volumeProvisionedCapacityBytes:
            The requested provisioned capacity of the storage volume in bytes.
            This attribute is required when creating a volume.
        volumeShareable:
            Identifies whether the storage volume is shared or private. If
            false, then the volume will be private. If true, then the volume
            will be shared. This attribute is required when creating a volume.
        volumeStoragePoolUri:
            The URI of the storage pool associated with this volume
            attachment's volume.
        volumeStorageSystemUri:
            The URI of the storage system associated with this volume
            attachment.
        volumeUri:
            The URI of the storage volume associated with this volume
            attachment.

    Returns: dict
    """
    if volumeProvisionedCapacityBytes:
        volAttach = {'id': None,
                     'lunType': lunType,
                     'permanent': permanent,
                     'volumeName': volumeName,
                     'volumeUri': None,
                     'volumeProvisionType': volumeProvisionType,
                     'volumeProvisionedCapacityBytes': volumeProvisionedCapacityBytes,
                     'volumeShareable': volumeShareable,
                     'volumeStoragePoolUri': volumeStoragePoolUri,
                     'volumeStorageSystemUri': None,
                     'storagePaths': storagePaths,
                     }
    else:
        volAttach = {'id': None,
                     'lunType': lunType,
                     'volumeUri': volumeUri,
                     'volumeStoragePoolUri': volumeStoragePoolUri,
                     'volumeStorageSystemUri': volumeStorageSystemUri,
                     'storagePaths': storagePaths,
                     }

    if lunType == 'Manual':
        volAttach['lun'] = lun

    return volAttach


@deprecated
def make_ephemeral_volume_dict(lun, lunType, volumeUri, volumeStoragePoolUri,
                               volumeStorageSystemUri, storagePaths,
                               permanent=True, volumeId=None):
    return {'id': volumeId,
            'lun': lun,
            'lunType': lunType,
            'volumeUri': volumeUri,
            'volumeStoragePoolUri': volumeStoragePoolUri,
            'volumeStorageSystemUri': volumeStorageSystemUri,
            'storagePaths': storagePaths,
            }


@deprecated
def make_StoragePathV2(connectionId=None, isEnabled=True,
                       storageTargetType='Auto', storageTargets=[]):
    """ Create a StoragePathV2 dictionary

    Args:
        connectionId:
            The ID of the connection associated with this storage path. Use
            GET /rest/server-profiles/available-networks to retrieve the list
            of available networks
        isEnabled:
            Identifies if the storage path is enabled.
        storageTargetType:
            If set to 'Auto', the storage system will automatically identify
            the storage targets. In this case, set the storageTargets field to
            an empty array.  If set to 'TargetPorts', the storage targets can
            be manually specified in the storageTargets field using
            comma-separated strings.
        storageTargets:
            Array of WWPNs of the targets on the storage system. If
            storageTargetType is set to Auto, the storage system will
            automatically select the target ports, in which case the
            storageTargets field is not needed and should be set to an empty
            array.  If storageTargetType is set to TargetPorts, then the the
            storageTargets field should be an array of comma-separated strings
            representing the WWPNs intended to be used to connect with the
            storage system.

    Returns: dict
    """
    return {'connectionId': connectionId,
            'isEnabled': isEnabled,
            'storageTargetType': storageTargetType,
            'storageTargets': storageTargets
            }


@deprecated
def make_powerstate_dict(state, control):
    return {'powerState': state,
            'powerControl': control}


@deprecated
def make_server_type_dict(name, description):
    return {'name': name,
            'description': description}


@deprecated
def make_ls_firmware_dict(action, sppUri, force='true'):
    return {'command': action, 'sppUri': sppUri, 'force': force}


# def get_entities(uri):
#    return self._get_members(self.get(uri))


@deprecated
def make_eula_dict(supportAccess):
    return {'supportAccess': supportAccess}


@deprecated
def make_initial_password_change_dict(userName, oldPassword, newPassword):
    return {
        'userName': userName,
        'oldPassword': oldPassword,
        'newPassword': newPassword}


@deprecated
def make_appliance_network_config_dict(hostName,
                                       macAddress,
                                       newApp1Ipv4Addr=None,
                                       newIpv4Subnet=None,
                                       newIpv4Gateway=None,
                                       newSearchDomain1=None,
                                       newSearchDomain2=None,
                                       ipv4Type='DHCP',
                                       ipv6Type='DHCP'):
    # Only DHCP enable for now. Need more attributes for static
    if ipv4Type == 'DHCP':
        return {'applianceNetworks': [{
            'confOneNode': True,
            'hostname': hostName,
            'macAddress': macAddress,
            'ipv4Type': ipv4Type,
            'ipv6Type': ipv6Type}]
        }
    if ipv4Type == 'STATIC':
        return {
            'applianceNetworks': [{
                'confOneNode': True,
                'hostname': hostName,
                'macAddress': macAddress,
                'ipv4Type': ipv4Type,
                'ipv6Type': ipv6Type,
                'app1Ipv4Addr': newApp1Ipv4Addr,
                'ipv4Subnet': newIpv4Subnet,
                'ipv4Gateway': newIpv4Gateway,
                # 'searchDomains': [newSearchDomain1, newSearchDomain2]
                'searchDomains': []
            }]
        }
    raise Exception('ipv4Type must be STATIC or DHCP.')


@deprecated
def make_audit_log_dict(dateTimeStamp='',
                        componentId='',
                        organizationId='',
                        userId='',
                        domain='',
                        sourceIp='',
                        result='SUCCESS',
                        action='DONE',
                        objectType='',
                        objectTypeDescriptor='',
                        severity='INFO',
                        taskId='',
                        msg=''):
    return {
        'componentId': componentId,
        'organizationId': organizationId,
        'userId': userId,
        'domain': domain,
        'sourceIp': sourceIp,
        'result': result,
        'action': action,
        'objectType': objectType,
        'objectTypeDescriptor': objectTypeDescriptor,
        'severity': severity,
        'taskId': taskId,
        'msg': msg}


@deprecated
def make_event_dict(severity='Unknown',
                    description='',
                    eventTypeID='',
                    eventDetails=None,
                    healthCategory='None',
                    urgency='None'):
    return {
        'severity': severity,
        'description': description,
        'eventTypeID': eventTypeID,
        'eventDetails': eventDetails,
        'healthCategory': healthCategory,
        'type': 'EventResourceV2',
        'urgency': urgency}


@deprecated
def make_event_detail_dict(eventItemName='',
                           eventItemValue=''):
    return {
        'eventItemName': eventItemName,
        'eventItemValue': eventItemValue}


@deprecated
def make_user_modify_dict(userName,
                          password=None,
                          currentPassword=None,
                          replaceRoles=None,
                          roles=None,
                          emailAddress=None,
                          officePhone=None,
                          mobilePhone=None,
                          enabled=None,
                          fullName=None):
    userDict = {'userName': userName}
    if password is not None and currentPassword is not None:
        userDict['password'] = password
        userDict['currentPassword'] = currentPassword
    if replaceRoles is not None:
        userDict['replaceRoles'] = replaceRoles
    if roles is not None:
        userDict['roles'] = roles
    if emailAddress is not None:
        userDict['emailAddress'] = emailAddress
    if officePhone is not None:
        userDict['officePhone'] = officePhone
    if mobilePhone is not None:
        userDict['mobilePhone'] = mobilePhone
    if enabled is not None:
        userDict['enabled'] = enabled
    if fullName is not None:
        userDict['fullName'] = fullName
    return userDict


@deprecated
def make_update_alert_dict(alertState=None,
                           assignedToUser=None,
                           eTag=None):
    alertDict = {}
    if alertState is not None:
        alertDict['alertState'] = alertState
    if assignedToUser is not None:
        alertDict['assignedToUser'] = assignedToUser
    if eTag is not None:
        alertDict['eTag'] = eTag
    return alertDict


@deprecated
def make_server_dict(hostname,
                     username,
                     password,
                     force=False,
                     licensingIntent='OneView',
                     configurationState='Managed'):
    return {
        'hostname': hostname,
        'username': username,
        'password': password,
        'force': force,
        'licensingIntent': licensingIntent,
        'configurationState': configurationState}


@deprecated
def make_rack_dict(name, sn, thermal, height, depth, width, uheight):
    return {
        'name': name,
        'serialNumber': sn,
        'thermalLimit': thermal,
        'height': height,
        'depth': depth,
        'width': width,
        'uHeight': uheight}


@deprecated
def make_datacenter_dict(name, coolingCapacity, coolingMultiplier, currency,
                         costPerKilowattHour, defaultPowerLineVoltage,
                         width, depth, deratingType, deratingPercentage):
    return {
        'name': name,
        'coolingCapacity': coolingCapacity,
        'coolingMultiplier': coolingMultiplier,
        'currency': currency,
        'costPerKilowattHour': costPerKilowattHour,
        'defaultPowerLineVoltage': defaultPowerLineVoltage,
        'depth': depth,
        'width': width,
        'deratingType': deratingType,
        'deratingPercentage': deratingPercentage,
        'contents': []}


@deprecated
def make_powerdevice_dict(name, deviceType, feedIdentifier, lineVoltage,
                          model, partNumber, phaseType, ratedCapacity,
                          serialNumber):
    return {
        'name': name,
        'deviceType': deviceType,
        'feedIdentifier': feedIdentifier,
        'lineVoltage': lineVoltage,
        'model': model,
        'partNumber': partNumber,
        'phaseType': phaseType,
        'ratedCapacity': ratedCapacity,
        'serialNumber': serialNumber}


@deprecated
def make_alertMap_dict(notes, etag, state='Active', user='None',
                       urgency='None'):
    return {
        'alertState': state,
        'assignedToUser': user,
        'alertUrgency': urgency,
        'notes': notes,
        'eTag': etag
    }


class pages(object):
    def __init__(self, page, connection):
        self._con = connection
        self.currentPage = page

    def __iter__(self):
        return self

    def __next__(self):
        if self._con._nextPage is not None:
            self.currentPage = self._con.getNextPage()
            return self.currentPage
        else:
            raise StopIteration


def transform_list_to_dict(list):
    """
        Transforms a list into a dictionary, putting values as keys
    Args:
        id:
    Returns:
        dict: dictionary built
    """

    ret = {}

    for value in list:
        if isinstance(value, dict):
            ret.update(value)
        else:
            ret[str(value)] = True

    return ret


def extract_id_from_uri(id_or_uri):
    """
    Extract ID from the end of the URI

    Args:
        id_or_uri: ID or URI of the OneView resources.

    Returns:
        str: The string founded after the last "/"
    """
    if '/' in id_or_uri:
        return id_or_uri[id_or_uri.rindex('/') + 1:]
    else:
        return id_or_uri
