# -*- coding: utf-8 -*-

"""
common.py
~~~~~~~~~~~~

This module implements the common and helper functions for the OneView REST API
"""

__title__ = 'common'
__version__ = "0.0.1"
__copyright__ = "(C) Copyright 2012-2013 Hewlett-Packard Development " \
                " Company, L.P."
__license__ = "MIT"
__status__ = "Development"

###
# (C) Copyright 2013 Hewlett-Packard Development Company, L.P.
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


# Looking for a switch type, using filters:
# https://<appliance>/rest/switch-types?filter="partNumber = '455880-B21'"
uri = {
    #------------------------------------
    # CI Controller
    #------------------------------------
    'applNetConfig': "/rest/appliance/network-interfaces",
    'applGlobalSettings': "/rest/global-settings",
    'eulaStatus': "/rest/appliance/eula/status",
    'eulaSave': "/rest/appliance/eula/save",
    'serviceAccess': "/rest/appliance/settings/enableServiceAccess",
    'applianceNetworkInterfaces': "/rest/appliance/network-interfaces",
    'healthStatus': "/rest/appliance/health-status",
    'version': "/rest/version",
    'supportDump': "/rest/appliance/support-dumps",
    'backups': "/rest/backups",
    #------------------------------------
    # Security
    #------------------------------------
    'loginSessions': "/rest/login-sessions",
    'users': "/rest/users",
    'userRole': "/rest/users/role",
    'changePassword': "/rest/users/changePassword",
    'roles': "/rest/roles",
    #------------------------------------
    # Environment
    #------------------------------------
    #------------------------------------
    # Systems
    #------------------------------------
    'servers': '/rest/server-hardware',
    'enclosures': '/rest/enclosures',
    'enclosureGroups': '/rest/enclosure-groups',
    'enclosurePreview': '/rest/enclosure-preview',
    'fwUpload': '/rest/firmware-bundles',
    'fwDrivers': '/rest/firmware-drivers',
    #------------------------------------
    # Connectivity
    #------------------------------------
    'conn': '/rest/connections',
    'ct': '/rest/connection-templates',
    'enet': '/rest/ethernet-networks',
    'fcnet': '/rest/fc-networks',
    'nset': '/rest/network-sets',
    'li': '/rest/logical-interconnects',
    'lig': '/rest/logical-interconnect-groups',
    'ic': '/rest/interconnects',
    'ictype': '/rest/interconnect-types',
    'us': '/rest/uplink-sets',
    'ld': '/rest/logical-downlinks',
    'idpool': '/rest/id-pools',
    'vmac-pool': '/rest/id-pools/vmac',
    'vwwn-pool': '/rest/id-pools/vwwn',
    'vsn-pool': '/rest/id-pools/vsn',
    #------------------------------------
    #  Server Profiles
    #------------------------------------
    'profiles': '/rest/server-profiles',
    #------------------------------------
    #  Health
    #------------------------------------
    'alerts': '/rest/alerts',
    'events': '/rest/events',
    'audit-logs': '/rest/audit-logs',
    #------------------------------------
    #  Searching and Indexing
    #------------------------------------
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
    #------------------------------------
    #  Logging and Tracking
    #------------------------------------
    'task': '/rest/tasks',
}


############################################################################
# Utility to print resource to standard output
############################################################################
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


def print_task_tuple(entities):
    print('Task/Entity Tuples:')
    for indx, (task, entity) in enumerate(entities):
        print((indx, ') Entry'))
        try:
            print (('\tTask: ', task['name'], task['taskState'],
                    task['taskStatus'], task['uri']))
        except KeyError:
            print('\tTask: n/a')
        try:
            print(('\tResource: ', entity['name'], entity['uri']))
        except KeyError:
            print('\tResource: n/a')


def get_members(mlist):
    if not mlist:
        return []
    if not mlist['members']:
        return []
    return mlist['members']


def get_member(mlist):
    if not mlist:
        return None
    if not mlist['members']:
        return None
    return mlist['members'][0]


############################################################################
# Create default Resource Instances
############################################################################
def make_user_dict(name, password,
                    enabled=True,
                    fullName="",
                    emailAddress="",
                    officePhone="",
                    mobilePhone="",
                    roles=[]):
    return {"userName": name,
            "fullName": fullName,
            "password": password,
            "emailAddress": emailAddress,
            "officePhone": officePhone,
            "mobilePhone": mobilePhone,
            "enabled": enabled,
            "roles": roles
            }


def make_bw_dict(maxbw=10000, minbw=1000):
    return {'maximumBandwidth': maxbw,
            'typicalBandwidth': minbw
            }


def make_netset_dict(name, networks=[]):
    return {'name': name,
            'type': 'network-set',
            'nativeNetworkUri': None,
            'networkUris': networks[:],
            'connectionTemplateUri': None
            }


def make_enet_dict(name, vlanid=0,
                   smartLink=True, privateNetwork=False):
    return {'name': name,
            'type': 'ethernet-network',
            'purpose': 'General',
            'connectionTemplateUri': None,
            'vlanId': vlanid,
            'smartLink': smartLink,
            'privateNetwork': privateNetwork
            }


def make_fc_dict(name, fabricType='FabricAttach',
                    uplinkBandwidth='Auto',
                    autoLoginRedistribution=True,
                    linkStabilityTime=30):
    return {'name': name,
            'type': 'fc-network',
            'connectionTemplateUri': None,
            'fabricType': fabricType,
            'uplinkBandwidth': uplinkBandwidth,
            'autoLoginRedistribution': autoLoginRedistribution,
            'linkStabilityTime': linkStabilityTime
            }


def make_interconnect_map_template():
    return {'interconnectMapEntryTemplates':
                    [{'logicalLocation': {
                        'locationEntries':
                            [{'type': 'Bay', 'relativeValue': N},
                             {'type': 'Enclosure', 'relativeValue': 1}]},
                      'permittedInterconnectTypeUri': None,
                      'logicalDownlinkUri': None
                     } for N in range(1, 9)],
                 }


def make_enet_settings(name,
                        enableIgmpSnooping=False,
                        igmpIdleTimeoutInterval=260,
                        enableFastMacCacheFailover=True,
                        macRefreshInterval=5,
                        enableNetworkLoopProtection=True):
    return {'type': 'EthernetInterconnectSettings',
            'name': name,
            'enableIgmpSnooping': enableIgmpSnooping,
            'igmpIdleTimeoutInterval': igmpIdleTimeoutInterval,
            'enableFastMacCacheFailover': enableFastMacCacheFailover,
            'macRefreshInterval': macRefreshInterval,
            'enableNetworkLoopProtection': enableNetworkLoopProtection,
            'interconnectType': 'Ethernet'
            # 'description': null,
            }


def make_lig_dict(name):
    return {'name': name,
            'type': 'logical-interconnect-group',
            'interconnectMapTemplate': make_interconnect_map_template(),
            'uplinkSets': [],  # call make_uplink_template
            'stackingMode': 'Enclosure',
            # 'ethernetSettings': None,
            'state': 'Active',
            # 'telemetryConfiguration': None,
            # 'snmpConfiguration' : None,
            # 'description': None
        }


def set_iobay_occupancy(switchMap, bays, stype):
    for location in switchMap['interconnectMapEntryTemplates']:
        entries = location['logicalLocation']['locationEntries']
        if [x for x in entries if x['type'] == 'Bay' and x['relativeValue']
             in bays]:
            location['permittedInterconnectTypeUri'] = stype


def make_uplink_set_dict(name, networks=[], ntype='Ethernet'):
    return {'name': name,
            'mode': 'Auto',  # Auto or Failover
            'networkUris': networks[:],
            'networkType': ntype,  # Ethernet or FibreChannel
            'primaryPort': None,
            'logicalPortConfigInfos': [],  # Array of logicalLocations
            'nativeNetworkUri': None
            }


def make_port_config_info(enclosure, bay, port, speed='Auto'):
    return {'logicalLocation': {
                'locationEntries':
                    [{'type': 'Enclosure', 'relativeValue': enclosure},
                     {'type': 'Bay', 'relativeValue': bay},
                     {'type': 'Port', 'relativeValue': port}]
                },
            'desiredSpeed': speed
            }


def make_egroup_dict(name, lig):
    return {
              'name': name,
              'type': 'EnclosureGroup',
              'stackingMode': 'Enclosure',
              'interconnectBayMappings': [{
                                        'interconnectBay': N,
                                        'logicalInterconnectGroupUri': lig
                                         } for N in range(1, 9)],
              }


def make_add_enclosure_dict(host, user, passwd, egroup,
                            firmwareBaseLineUri=None, force=False):
    return {
            'hostname': host,
            'username': user,
            'password': passwd,
            'force': force,
            'enclosureGroupUri': egroup,
            'firmwareBaselineUri': firmwareBaseLineUri,
            'updateFirmwareOn': 'EnclosureOnly',
            'licensingIntent': 'OneView'
        }


def make_profile_connection_dict(network,
                                    portId='Auto',
                                    functionType='Ethernet',
                                    boot=None):
    return {
            'networkUri': network['uri'],
            'portId': portId,
            'functionType': functionType,
            'boot': boot
            }


def make_profile_connection_boot_dict(priority='Primary',
                                    arrayWwpn=None,
                                    lun=None):
    if arrayWwpn is None and lun is None:
        return {
            'priority': priority
            }
    else:
        return {
            'priority': priority,
            'targets': make_profile_connection_boot_target_dict(
                            arrayWwpn,
                            lun)}


def make_profile_connection_boot_target_dict(arrayWwpn=None, lun=None):
    return [{
        'arrayWwpn': arrayWwpn,
        'lun': lun
        }]


def make_add_profile_dict(profileName, server, firmwareBaseline=None,
                            connections=[]):
    return {
            'type': 'ServerProfileV1',
            'name': profileName,
            'wwnType': 'Virtual',
            'serialNumberType': 'Virtual',
            'macType': 'Virtual',
            'serverHardwareUri': server['uri'],
            'serverHardwareTypeUri': server['serverHardwareTypeUri'],
            'firmware': firmwareBaseline,
            'connections': connections
            }


def make_profile_firmware_baseline(firmwareUri, manageFirmware=True):
    return {
            'firmwareBaselineUri': firmwareUri,
            'manageFirmware': manageFirmware
            }


def make_powerstate_dict(state, control):
    return {'powerState': state,
            'powerControl': control}


def make_ls_firmware_dict(action, sppUri, force='true'):
    return {'command': action, 'sppUri': sppUri, 'force': force}


#def get_entities(uri):
#    return self._get_members(self.get(uri))


def make_eula_dict(supportAccess):
    return {'supportAccess': supportAccess}


def make_initial_password_change_dict(userName, oldPassword, newPassword):
    return {
        'userName': userName,
        'oldPassword': oldPassword,
        'newPassword': newPassword}


def make_appliance_network_config_dict(hostName,
                                        macAddress,
                                        ipv4Type='DHCP',
                                        ipv6Type='DHCP'):
    # Only DHCP enable for now. Need more attributes for static
    return {
        "applianceNetworks": [{
            "confOneNode": True,
            "hostname": hostName,
            "macAddress": macAddress,
            "ipv4Type": ipv4Type,
            "ipv6Type": ipv6Type
            }]
        }


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


def make_event_detail_dict(eventItemName='',
                        eventItemValue=''):
    return {
        'eventItemName': eventItemName,
        'eventItemValue': eventItemValue}


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


def make_add_server_dict(
                    hostname,
                    username,
                    password,
                    force=False,
                    licensingIntent='OneView'):
    return {
        'hostname': hostname,
        'username': username,
        'password': password,
        'force': force,
        'licensingIntent': licensingIntent}


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
