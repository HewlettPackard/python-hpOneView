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


def main():
    con = hpOneView.connection(applianceIP)
    srv = hpOneView.servers(con)

    if applianceProxy:
        con.set_proxy(applianceProxy.split(':')[0],
                        applianceProxy.split(':')[1])
    if applianceCerts:
        con.set_trusted_ssl_bundle(applianceCerts)
    # See if we need to accept the EULA before we try to log in
    con.get_eula_status()
    try:
        if con.get_eula_status() is True:
            print("EULA display needed")
            con.set_eula('no')
        else:
            print("EULA display NOT needed")
    except Exception as e:
        print('EXCEPTION:')
        print(e)
    credential = {'userName': applianceUser, 'password': appliancePassword}
    con.login(credential)

    encNum = 1
    for enclosure in srv.get_enclosures():
        print('Enclosure ' + str(encNum))
        print('\tName ' + enclosure['name'])
        print('\tType: ' + enclosure['enclosureType'])
        print('\tSerial Number: ' + enclosure['serialNumber'])
        for oa in enclosure['oa']:
            print('\tOA Bay ' + str(oa['bayNumber']))
            print('\t\tIP Address: ' + oa['ipAddress'])
            print('\t\tRole: ' + oa['role'])
            print('\t\tVersion: ' + oa['fwVersion'] + ' '
                                  + oa['fwBuildDate'])
        for blade in enclosure['deviceBays']:
            print('\tDevice Bay ' + str(blade['bayNumber']) + ' ' +
                            blade['devicePresence'])
            if blade['devicePresence'] != 'absent':
                hardware = con.get(blade['deviceUri'])
                print('\t\tSerial Number: ' + hardware['serialNumber'])
                print('\t\tName: ' + hardware['model'])
                if hardware['serverProfileUri'] is not None:
                    profile = con.get(hardware['serverProfileUri'])
                    print('\t\tProfile Name: ' + profile['name'])
                print('\t\tROM: ' + hardware['romVersion'])
                print('\t\tMezz Cards')
                for device in hardware['portMap']['deviceSlots']:
                    print('\t\t\t' + device['location'] +
                                ' ' + str(device['slotNumber']) + ': ' +
                                    device['deviceName'])
                print('\t\tiLO')
                print('\t\t\tIP Address: ' + hardware['mpIpAddress'])
                print('\t\t\tFirmware Version: ' +
                            hardware['mpFirmwareVersion'])
                print('\t\t\tDNS Name: ' + hardware['mpDnsName'])
        for interconnect in enclosure['interconnectBays']:
            print('\tInterconnect Bay ' + str(interconnect['bayNumber']))
            if interconnect['interconnectUri'] is not None:
                hardware = con.get(interconnect['interconnectUri'])
                print('\t\tProduct Name: ' + hardware['productName'])
                print('\t\tSerial Number: ' + hardware['serialNumber'])
                print('\t\tIP Address: ' + hardware['interconnectIP'])
                print('\t\tFirmware Version: ' + hardware['firmwareVersion'])
        encNum = encNum + 1

    con.logout()

if __name__ == '__main__':
    import sys
    sys.exit(main())
