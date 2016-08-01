# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
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

from pprint import pprint
from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException
from config_loader import try_load_from_file

config = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

options = {
    "hostname": config['server_hostname'],
    "username": config['server_username'],
    "password": config['server_password'],
    "licensingIntent": "OneView",
    "configurationState": "Managed"
}

# Set the server_hardware_id to run this example.
# server_hardware_id example: 37333036-3831-4753-4831-30315838524E
server_hardware_id = ""

oneview_client = OneViewClient(config)

# Get Statistics with defaults
print("Get server-hardware statistics")
try:
    server_utilization = oneview_client.server_hardware.get_utilization(
        server_hardware_id)
    pprint(server_utilization)
except HPOneViewException as e:
    print(e.msg['message'])

# Get Statistics specifying parameters
print("Get server-hardware statistics specifying parameters")
try:
    server_utilization = oneview_client.server_hardware.get_utilization(server_hardware_id,
                                                                        fields='AveragePower',
                                                                        filter='startDate=2016-05-30T03:29:42.000Z',
                                                                        view='day')
    pprint(server_utilization)
except HPOneViewException as e:
    print(e.msg['message'])

# Get list of all server hardware resources
print("Get list of all server hardware resources")
server_hardware_all = oneview_client.server_hardware.get_all()
for serv in server_hardware_all:
    print('  %s' % serv['name'])

# Create a rack-mount server
server = oneview_client.server_hardware.add(options)
print("Added rack mount server '%s'.\n  uri = '%s'" %
      (server['name'], server['uri']))

# Get recently added server hardware resource by uri
server_byId = oneview_client.server_hardware.get(server['uri'])
print("Found server '%s' by uri.\n  uri = '%s'" %
      (server_byId['name'], server_byId['uri']))

# Get recently added server hardware resource by name
server_byName = oneview_client.server_hardware.get_by(
    'name', server['name'])[0]
print("Found server at uri '%s'\n  by name = '%s'" %
      (server_byName['uri'], server_byName['name']))

# Get list of BIOS/UEFI Values
try:
    print("Get list of BIOS/UEFI Values")
    bios = oneview_client.server_hardware.get_bios(
        server_hardware_id)
    pprint(bios)
except HPOneViewException as e:
    print(e.msg['message'])

# Get the settings that describe the environmental configuration of server
print(
    "Get the settings that describe the environmental configuration of server")
server_envConf = oneview_client.server_hardware.get_environmental_configuration(server['uuid'])
pprint(server_envConf)

# Set the calibrated max power of an unmanaged or unsupported server
# hardware resource
print(
    "Set the calibrated max power of an unmanaged or unsupported server hardware resource")
try:
    configuration = {
        "calibratedMaxPower": 2500
    }
    server_updated_encConf = oneview_client.server_hardware.update_environmental_configuration(configuration,
                                                                                               server_hardware_id)
except HPOneViewException as e:
    print(e.msg['message'])

# Get URL to launch SSO session for iLO web interface
ilo_sso_url = oneview_client.server_hardware.get_ilo_sso_url(server['uri'])
print("URL to launch a Single Sign-On (SSO) session for the iLO web interface for server at uri:\n",
      "{}\n   '{}'".format(server['uri'], ilo_sso_url))

# Generates a Single Sign-On (SSO) session for the iLO Java Applet console
# and return URL to launch it
java_remote_console_url = oneview_client.server_hardware.get_java_remote_console_url(server['uri'])
print("URL to launch a Single Sign-On (SSO) session for the iiLO Java Applet console for server at uri:\n",
      "   {}\n   '{}'".format(
          server['uri'], java_remote_console_url))

# Update iLO firmware to minimum version required
oneview_client.server_hardware.update_mp_firware_version(server['uri'])
print("Successfully updated iLO firmware on server at\n  uri: '{}'".format(server['uri']))

# Request power operation to change the power state of the physical server.
try:
    configuration = {
        "powerState": "Off",
        "powerControl": "MomentaryPress"
    }
    server_power = oneview_client.server_hardware.update_power_state(configuration, server_hardware_id)
    print("Successfully changed the power state of server '{name}' to '{powerState}'".format(**server_power))
except HPOneViewException as e:
    print(e.msg['message'])

# Refresh server state
try:
    configuration = {
        "refreshState": "RefreshPending"
    }
    server_refresh = oneview_client.server_hardware.refresh_state(configuration, server_hardware_id)
    print("Successfully refreshed the state of the server at:\n   'uri': '{}'".format(
        server_refresh['uri']))
except HPOneViewException as e:
    print(e.msg['message'])

# Get URL to launch SSO session for iLO Integrated Remote Console
# Application (IRC)
remote_console_url = oneview_client.server_hardware.get_java_remote_console_url(server['uri'])
print("URL to launch a Single Sign-On (SSO) session for iLO Integrated Remote Console Application",
      " for server at uri:\n   {}\n   '{}'".format(server['uri'], remote_console_url))

# Remove rack server
oneview_client.enclosures.remove(server)
print("Server removed successfully")
