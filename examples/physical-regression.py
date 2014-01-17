# -*- coding: utf-8 -*-
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

import hpOneView
import string
import random
import time
import configparser
import argparse

parser = argparse.ArgumentParser(description='Process config file')
parser.add_argument('--file',
                    dest='configFile',
                    type=str,
                    help='Config File',
                    default='config.cfg')
args = parser.parse_args()
config = configparser.RawConfigParser()
config.read(args.configFile)

applianceIP = config.get('Main', 'applianceIP')
applianceUser = config.get('Main', 'applianceUser')
appliancePassword = config.get('Main', 'appliancePassword')
enclosureIP = config.get('Main', 'enclosureIP')
enclosureUser = config.get('Main', 'enclosureUser')
enclosurePassword = config.get('Main', 'enclosurePassword')
applianceProxy = config.get('Main', 'applianceProxy', fallback=None)
applianceCerts = config.get('Main', 'applianceCerts', fallback=None)
doRackConfiguration = config.getboolean('Main',
                                        'doRackConfiguration',
                                        fallback=False)
rackiLOIp = config.get('Main', 'rackiLOIp', fallback='')
rackiLOUser = config.get('Main', 'rackiLOUser', fallback='')
rackiLOPassword = config.get('Main', 'rackiLOPassword', fallback='')
licenseKey = config.get('Main', 'licenseKey', fallback='')

# SPP Tests add an additional 10 or so minutes. Provide a way to skip them
doSppTests = config.getboolean('Main', 'doSppTests', fallback=False)
firmwareBundlePath = config.get('Main', 'firmwareBundlePath', fallback='')
aFirmwarePath = firmwareBundlePath.split(sep='\\')
firmwareBundleFileName = aFirmwarePath[len(aFirmwarePath) - 1]

newApp1Ipv4Addr = config.get('NewApplianceIP', 'newApp1Ipv4Addr')
newDomainName = config.get('NewApplianceIP', 'newDomainName')
newIpv4Subnet = config.get('NewApplianceIP', 'newIpv4Subnet')
newIpv4Gateway = config.get('NewApplianceIP', 'newIpv4Gateway')
newSearchDomain1 = config.get('NewApplianceIP', 'newSearchDomain1')
newSearchDomain2 = config.get('NewApplianceIP', 'newSearchDomain2')

def insecure_random_string_generator(size=8, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for x in range(size))

def try_connect(ip):
    con = hpOneView.connection(ip)
    if applianceProxy:
        con.set_proxy(applianceProxy.split(':')[0],
                        applianceProxy.split(':')[1])
    if applianceCerts:
        con.set_trusted_ssl_bundle(applianceCerts)
    # See if we need to accept the EULA before we try to log in
    try:
        con.get_eula_status()
    except OSError as ex:
        print ('ex:')
        print (ex)
        if ( "503" in ex ):
            switchToDHCP()
    try:
        if con.get_eula_status() is True:
            print("EULA display needed")
            con.set_eula('no')
        else:
            print("EULA display NOT needed")
    except Exception as e:
        print('EXCEPTION:')
        print(e)
    # First try to log in with the initial credentials
    try:
        credential = {'userName': applianceUser, 'password': 'admin'}
        con.login(credential)
    except hpOneView.exceptions.HPOneViewException as ex:
        if ex.errorCode == 'PASSWORD_CHANGE_REQUIRED':
            con.change_initial_password('password')
        elif ex.errorCode == 'AUTHN_AUTH_FAUL':
            print('Initial login failed so assume password already changed')
    credential = {'userName': applianceUser, 'password': appliancePassword}
    con.login(credential)
    return con


def connect(ip_address):
    working = 1
    while working:
        try:
            con = try_connect(ip_address)
            working = 0
        except Exception as e:
            working = 1
            print('Connection failed for ip: ' + ip_address)
            print('IP may have changed.  Will retry connection in 30 seconds')
            time.sleep(30)
    return con

def main():
#    con = connect(newApp1Ipv4Addr)    # just here for debugging...
    con = connect(applianceIP)

    # Get the appliance MAC address
    data = con.get_appliance_network_interfaces()
    macAddress = data['applianceNetworks'][0]['macAddress']
    hostName = data['applianceNetworks'][0]['hostname']

    # Try changing appliance to static ip...
    if newApp1Ipv4Addr:
        print("Setting ipv4...")
        interfaceConfig = hpOneView.common.make_appliance_network_config_dict(
                                            newDomainName,
                                            macAddress,
                                            newApp1Ipv4Addr,
                                            newIpv4Subnet,
                                            newIpv4Gateway,
                                            newSearchDomain1,
                                            newSearchDomain2,
                                            ipv4Type='STATIC',
                                            ipv6Type='UNCONFIGURE',
                                            )
        con.set_appliance_network_interface(interfaceConfig)
        print("Network set to static ip: " + newApp1Ipv4Addr)

        # Connect via the new IP...
        con = connect(newApp1Ipv4Addr)

        print('Sleep for 60 seconds before reverting back to DHCP...')
        time.sleep(60)


    # Change appliance to DHCP...
    interfaceConfig = hpOneView.common.make_appliance_network_config_dict(
                                        hostName,
                                        macAddress,
                                        ipv4Type='DHCP',
                                        ipv6Type='DHCP')
    con.set_appliance_network_interface(interfaceConfig)
    print("Network set to DHCP: "+ applianceIP)

    con = connect(applianceIP)

    # IP should not change anymore--set variables from con:
    srv = hpOneView.servers(con)
    net = hpOneView.networking(con)
    sec = hpOneView.security(con)
    settings = hpOneView.settings(con)
    act = hpOneView.activity(con)
    sear = hpOneView.search(con)

    try:
        settings.add_license(licenseKey)
    except hpOneView.exceptions.HPOneViewException as ex:
        print('WARNING: License failed to add. Check message.')
        print('Message: ' + ex.message)
    licenses = settings.get_licenses()
    print(str(len(licenses)) + ' licenses installed')


    if doRackConfiguration is True:
        # Rack based support
        serverdict = hpOneView.common.make_add_server_dict(
                                        hostname=rackiLOIp,
                                        username=rackiLOUser,
                                        password=rackiLOPassword,
                                        force=False,
                                        licensingIntent='OneView')
        print('Adding rack server...')
        server = srv.add_server(serverdict)
        print('Removing rack server...')
        srv.delete_server(server)

    readCommunityString = insecure_random_string_generator()
    response = settings.set_dev_read_comm_string(readCommunityString)
    if response != readCommunityString:
        raise Exception("Community string not set")
    newCommString = settings.get_dev_read_comm_string()
    if newCommString != readCommunityString:
        raise Exception("Community strings differ")

    print('Generating Appliance Dump')
    dumpInfo = settings.generate_support_dump()
    print('Downloading Appliance Dump')
    settings.download_support_dump(dumpInfo)

    version = settings.get_version()
    print('Minimum API Version: ' + str(version['minimumVersion']))
    print('Current API Version: ' + str(version['currentVersion']))

    status = settings.get_health_status()
    for member in status:
        print(member['available'] + ' available ' + member['resourceType'])

    # Clean up everything before we start in case of aborted previous run
    servers = srv.get_servers()
    for server in servers:
        if server['powerState'] == 'On':
            srv.set_server_powerstate(server, 'Off', force=True)
    profiles = srv.get_server_profiles()
    for profile in profiles:
        print(("Removing Profile %s" % profile['name']))
        srv.remove_server_profile(profile)
    enclosures = srv.get_enclosures()
    for enclosure in enclosures:
        print(("Removing Enclosure %s" % enclosure['serialNumber']))
        srv.remove_enclosure(enclosure)
    egroups = srv.get_enclosure_groups()
    for egroup in egroups:
        srv.delete_enclosure_group(egroup)
    ligs = net.get_ligs()
    for lig in ligs:
        net.delete_lig(lig)
    networksets = net.get_networksets()
    for networkset in networksets:
        net.delete_networkset(networkset)
    fcnets = net.get_fc_networks()
    for fcnet in fcnets:
        net.delete_network(fcnet)
    enets = net.get_enet_networks()
    for enet in enets:
        net.delete_network(enet)

    # Check how many non-cleared alerts we have
    alerts = act.get_alerts('Active')
    startNumAlerts = len(alerts)
    print(("%d active alerts" % startNumAlerts))
    # Clear (or Delete) active alerts so we start clean
    if startNumAlerts > 0:
        for alert in alerts:
            alertMap = hpOneView.common.make_update_alert_dict(
                                            alertState='Cleared',
                                            assignedToUser='Administrator')
            act.update_alert(alert, alertMap)
            # or Delete it - act.delete_alert(alert)
    alerts = act.get_alerts('Active')
    startNumAlerts = len(alerts)
    print(("%d active alerts" % startNumAlerts))
    # Delete active alerts so we start clean
    if startNumAlerts > 0:
        raise Exception("Still have active alerts")

    if doSppTests is True:
        print("Getting current SPPs")
        spps = settings.get_spps()
        startNumSpps = len(spps)
        print("Uploading SPP")
        spp = settings.upload_spp(firmwareBundlePath, firmwareBundleFileName)
        spps = settings.get_spps()
        if len(spps) == startNumSpps:
            raise Exception('Same number of SPPs found %d' % (len(spps)))
        print("Deleting SPP")
        settings.delete_spp(spp)
    con.set_service_access('false')

    roles = sec.get_roles()
    print(str(len(roles)) + " user roles")
    users = sec.get_users()
    numUsers = len(users)
    print(('Current Users (' + str(numUsers) + '):'))
    for user in users:
        print((' ' + (user['userName'])))
    testUser = insecure_random_string_generator()
    testPassword = insecure_random_string_generator()
    print(('Adding User ' + testUser))
    user = hpOneView.common.make_user_dict(testUser,
                            testPassword,
                            enabled=True,
                            fullName='Test User',
                            emailAddress='test@abc.com',
                            roles=['Infrastructure administrator'])
    sec.create_user(user)
    users = sec.get_users()
    if len(users) != numUsers + 1:
        raise Exception('User not added')
    con.logout()
    print(('Testing user ' + testUser))
    testCredential = {'userName': testUser, 'password': testPassword}
    con.login(testCredential)
    con.logout()
    con.login(credential)
    print('Modifying User')
    updateUser = hpOneView.common.make_user_modify_dict(
                        userName=testUser,
                        fullName='Renamed Test User')
    updatedUser = sec.update_user(updateUser)
    updatedUser = sec.get_user(testUser)
    if updatedUser['fullName'] != 'Renamed Test User':
        raise Exception('User not renamed')
    print(('Deleting User ' + testUser))
    sec.delete_user(testUser)
    users = sec.get_users()
    if len(users) != numUsers:
        raise Exception('User not deleted')
    pool = srv.get_vsn_pool()
    print(('Current SN Pool Type: ' + (pool['poolType'])))
    pool = srv.get_vwwn_pool()
    print(('Current WWN Pool Type: ' + (pool['poolType'])))
    pool = srv.get_vmac_pool()
    print(('Current MAC Pool Type: ' + (pool['poolType'])))
    roles = sec.get_user_roles('administrator')
    print('Roles:')
    for role in roles:
        print((' ' + (role['roleName'])))
    user = sec.get_user('administrator')
    print('User Properties:')
    pprint(user, indent=4)
    # Create Network
    bandDict = hpOneView.common.make_bw_dict(maxbw=10000, minbw=1000)
    print('Creating Ethernet Network')
    enet = net.create_enet_network('RDP',
                                    1,
                                    smartLink=True,
                                    privateNetwork=False,
                                    bw=bandDict)
    print('Creating FC Networks')
    fcneta = net.create_fc_network('SAN-A',
                                    bw=bandDict)
    fcnetb = net.create_fc_network('SAN-B',
                                    bw=bandDict)
    print('Creating Network Set')
    nset = net.create_networkset('RDP Network Set',
                                    nets=[enet['uri']],
                                    bw=bandDict)
    print('Creating Logical Interconnect Group')
    lig = hpOneView.common.make_lig_dict('Test LIG')
    swtype = con.get_entity_byfield(hpOneView.common.uri['ictype'],
                                    'partNumber',
                                    '571956-B21')
    hpOneView.common.set_iobay_occupancy(lig['interconnectMapTemplate'],
                            [1, 2], swtype['uri'])
    net_uris = [enet['uri']]
    uplinkSet = hpOneView.common.make_uplink_set_dict(
                                    "RDPUplinkSet",
                                    net_uris)
    # Get Port Number
    pnum = -1
    for port in swtype['portInfos']:
        if port['portName'] == 'X5':
            pnum = port['portNumber']
            break
    uplinkSet['logicalPortConfigInfos'].append(
                                    hpOneView.common.make_port_config_info(
                                                    1, 1, pnum))
    lig['uplinkSets'].append(uplinkSet)

    net_uris = [fcneta['uri']]
    uplinkSet = hpOneView.common.make_uplink_set_dict(
                                            "SanAUplinkSet",
                                            net_uris,
                                            'FibreChannel')
    # Get Port Number
    pnum = -1
    for port in swtype['portInfos']:
        if port['portName'] == 'X1':
            pnum = port['portNumber']
            break
    uplinkSet['logicalPortConfigInfos'].append(
                                    hpOneView.common.make_port_config_info(
                                                    1, 1, pnum))
    lig['uplinkSets'].append(uplinkSet)

    net_uris = [fcnetb['uri']]
    uplinkSet = hpOneView.common.make_uplink_set_dict(
                                            "SanBUplinkSet",
                                            net_uris,
                                            'FibreChannel')
    # Use same port number
    uplinkSet['logicalPortConfigInfos'].append(
                                    hpOneView.common.make_port_config_info(
                                                    1, 2, pnum))
    lig['uplinkSets'].append(uplinkSet)

    lig = net.create_lig(lig)
    print('Creating Enclosure Group')
    egroup = hpOneView.common.make_egroup_dict("Enclosure Group", lig['uri'])
    egroup = srv.create_enclosure_group(egroup)
    print('Renaming Enclosure Group')
    egroup['name'] = 'Renamed Enclosure Group'
    egroup = srv.update_enclosure_group(egroup)
    print('Adding Enclosure')
    # Find the first Firmware Baseline
    spp = settings.get_spps()[0]
    add_enclosure = hpOneView.common.make_add_enclosure_dict(
                                    enclosureIP,
                                    enclosureUser,
                                    enclosurePassword,
                                    egroup['uri'],
                                    firmwareBaseLineUri=spp['uri'])
    enclosure = srv.add_enclosure(add_enclosure)
    print('Creating Profiles')
    # See if we need to turn any servers off
    servers = srv.get_servers()
    for server in servers:
        if server['powerState'] == 'On':
            srv.set_server_powerstate(server, 'Off', force=True)
    g7server = srv.get_server_by_bay(7)
    gen8server = srv.get_server_by_bay(13)
    connection1 = hpOneView.common.make_profile_connection_dict(enet,
                    boot=hpOneView.common.make_profile_connection_boot_dict(
                        priority='Primary'))
    connection2 = hpOneView.common.make_profile_connection_dict(fcneta,
                    functionType='FibreChannel',
                    boot=hpOneView.common.make_profile_connection_boot_dict(
                        priority='Primary',
                        arrayWwpn='5001438004C8E7F8',
                        lun='1'))
    connection3 = hpOneView.common.make_profile_connection_dict(fcnetb,
                    functionType='FibreChannel',
                    boot=hpOneView.common.make_profile_connection_boot_dict(
                        priority='Secondary',
                        arrayWwpn='5001438004C8E7FC',
                        lun='1'))
    connections = [connection1, connection2, connection3]
    firmwareBaseline = hpOneView.common.make_profile_firmware_baseline(
                                                spp['uri'])
    print('Creating G7 Profile')
    g7profile = hpOneView.common.make_add_profile_dict('G7 Profile',
                                                g7server,
                                                connections=connections)
    print('Creating Gen8 Profile')
    gen8profile = hpOneView.common.make_add_profile_dict('Gen8 Profile',
                                            gen8server,
                                            connections=connections,
                                            firmwareBaseline=firmwareBaseline)
    g7profile = srv.create_server_profile(g7profile)
    gen8profile = srv.create_server_profile(gen8profile)
    g7profile['name'] = 'Renamed G7 Profile'
    g7profile = srv.update_server_profile(g7profile)
    gen8profile['name'] = 'Renamed Gen8 Profile'
    gen8profile = srv.update_server_profile(gen8profile)

    # Try searching now that we have resources
    resources = sear.get_resources('category=interconnect-types')
    print(('%s Interconnect Types' % len(resources)))
    resources = sear.get_resources({'category': 'interconnect-types'})
    print(('%s Interconnect Types' % len(resources)))
    assoc = sear.get_associations('category=interconnect-types')
    print(('%s Associations' % len(assoc)))
    trees = sear.get_trees('category=interconnect-types')
    print(('%s Trees' % len(trees)))
    sugg = sear.get_search_suggestions('Flex')
    print(('%s Suggestions' % len(sugg['suggestions'])))

    #print('Generating LI Dump')
    #li = net.get_interconnects()
    #dumpInfo = settings.generate_support_dump(logicalInterconnect=li[0])
    #print('Downloading LI Dump')
    #settings.download_support_dump(dumpInfo)

    print('Generating appliance backup')
    backup = settings.generate_backup()
    print('Downloading appliance backup')
    settings.download_backup(backup)

    # Check and see if we have any new alerts
    alerts = act.get_alerts('Active')
    if len(alerts) > 0:
        print(('WARNING: You have %d active alerts' % (len(alerts))))
        for alert in alerts:
            print(('- ' + alert['description']))

    # Events
    events = act.get_events('filter="eventTypeID=\'Demo.Event\'"')
    numEvents = len(events)
    eventDetail = hpOneView.common.make_event_detail_dict('ipv4Address',
                                                            enclosureIP)
    eventRecord = hpOneView.common.make_event_dict(description='Test',
                                        eventTypeID='Demo.Event',
                                        eventDetails=[eventDetail])
    act.create_event(eventRecord)
    events = act.get_events('filter="eventTypeID=\'Demo.Event\'"')
    if len(events) is numEvents:
        print('WARNING: Event record not created')

    # Audit Logs
    logs = act.get_audit_logs('filter="componentId=\'Test\'"')
    numLogs = len(logs)
    auditRecord = hpOneView.common.make_audit_log_dict(componentId='Test',
                                                        userId='Administrator',
                                                        domain='Local',
                                                        objectType='SERVER',
                                                        msg='Test Log')
    act.create_audit_log(auditRecord)
    logs = act.get_audit_logs('filter="componentId=\'Test\'"')
    if len(logs) is numLogs:
        print('WARNING: Audit log not created')

    # Paging example
    #pages = hpOneView.common.pages(act.get_alerts(), act._con)
    #firstPage = pages.currentPage
    #firstRecord = firstPage[0]
    #for page in pages:
    #    for record in page:
    #        pass  # OR print(record)
    #lastPage = pages.currentPage
    #lastRecord = lastPage[len(lastPage) - 1]

    print()
    print('We have now created everything. Check the UI and if all is good.'
            ' Press Enter to clean up.')
    input()

    # Clean Up
    print('Removing Profiles')
    srv.remove_server_profile(g7profile)
    srv.remove_server_profile(gen8profile)
    print('Removing Enclosure')
    srv.remove_enclosure(enclosure)
    print('Deleting Enclosure Group')
    srv.delete_enclosure_group(egroup)
    print('Deleting Logical Interconnect Group')
    net.delete_lig(lig)
    print('Deleting Network Set')
    net.delete_networkset(nset)
    print('Deleting FC Network')
    net.delete_network(fcneta)
    net.delete_network(fcnetb)
    print('Deleting Ethernet Network')
    net.delete_network(enet)
    # Check and see if we have any new alerts
    alerts = act.get_alerts('Active')
    if len(alerts) > 0:
        print(('WARNING: You have %d active alerts' % (len(alerts))))
        for alert in alerts:
            print((alert['description']))
    con.logout()

if __name__ == '__main__':
    import sys
    from pprint import pprint
    sys.exit(main())
