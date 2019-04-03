# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2019 Hewlett Packard Enterprise Development LP
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
from config_loader import try_load_from_file

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
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
server_name = "RenamedEnclosure, bay 1"

oneview_client = OneViewClient(config)
server_hardwares = oneview_client.server_hardware

# Get list of all server hardware resources
print("Get list of all server hardware resources")
server_hardware_all = server_hardwares.get_all()
for serv in server_hardware_all:
    print('  %s' % serv['name'])

server = server_hardwares.get_by_name(server_name)
if not server:
    # Create a rack-mount server
    # This is only supported on appliance which support rack mounted servers
    server = server_hardwares.add(options)
    print("Added rack mount server '%s'.\n  uri = '%s'" % (server['name'], server['uri']))

# Create Multiple rack-mount servers
# This is only supported on appliance which support rack mounted servers
if oneview_client.api_version >= 600:
    options_to_add_multiple_server = {
        "mpHostsAndRanges": config['server_mpHostsAndRanges'],
        "username": config['server_username'],
        "password": config['server_password'],
        "licensingIntent": "OneView",
        "configurationState": "Managed",
    }
    multiple_server = server_hardwares.add_multiple_servers(options_to_add_multiple_server)
else:
    print("\nCANNOT CREATE MULTIPLE SERVERS! Endpoint supported for REST API Versions 600 and above only.\n")

# Get recently added server hardware resource by uri
server_byId = server_hardwares.get_by_uri(server.data['uri'])
print("Found server '%s' by uri.\n  uri = '%s'" %
      (server_byId.data['name'], server_byId.data['uri']))

# Get Statistics with defaults
print("Get server-hardware statistics")
server_utilization = server.get_utilization()
pprint(server_utilization)

# Get Statistics specifying parameters
print("Get server-hardware statistics specifying parameters")
server_utilization = server.get_utilization(fields='AveragePower',
                                            filter='startDate=2016-05-30T03:29:42.000Z',
                                            view='day')
pprint(server_utilization)

# Get list of BIOS/UEFI Values
print("Get list of BIOS/UEFI Values")
bios = server.get_bios()
pprint(bios)

# Get the settings that describe the environmental configuration of server
print(
    "Get the settings that describe the environmental configuration of server")
server_envConf = server.get_environmental_configuration()
pprint(server_envConf)

# Set the calibrated max power of an unmanaged or unsupported server
# hardware resource
print("Set the calibrated max power of an unmanaged or unsupported server hardware resource")
configuration = {
    "calibratedMaxPower": 2500
}
server_updated_encConf = server.update_environmental_configuration(configuration)

# Get URL to launch SSO session for iLO web interface
ilo_sso_url = server.get_ilo_sso_url()
print("URL to launch a Single Sign-On (SSO) session for the iLO web interface for server at uri:\n",
      "{}\n   '{}'".format(server.data['uri'], ilo_sso_url))

# Generates a Single Sign-On (SSO) session for the iLO Java Applet console
# and return URL to launch it
java_remote_console_url = server.get_java_remote_console_url()
print("URL to launch a Single Sign-On (SSO) session for the iiLO Java Applet console for server at uri:\n",
      "   {}\n   '{}'".format(
          server.data['uri'], java_remote_console_url))

# Update iLO firmware to minimum version required
server.update_mp_firware_version()
print("Successfully updated iLO firmware on server at\n  uri: '{}'".format(server.data['uri']))

# Request power operation to change the power state of the physical server.
configuration = {
    "powerState": "Off",
    "powerControl": "MomentaryPress"
}
server_power = server.update_power_state(configuration)
print("Successfully changed the power state of server '{name}' to '{powerState}'".format(**server_power))

# Refresh server state
configuration = {
    "refreshState": "RefreshPending"
}
server_refresh = server.refresh_state(configuration)
print("Successfully refreshed the state of the server at:\n   'uri': '{}'".format(
      server_refresh['uri']))

# Get URL to launch SSO session for iLO Integrated Remote Console
# Application (IRC)
remote_console_url = server.get_java_remote_console_url()
print("URL to launch a Single Sign-On (SSO) session for iLO Integrated Remote Console Application",
      " for server at uri:\n   {}\n   '{}'".format(server.data['uri'], remote_console_url))

if oneview_client.api_version >= 300:
    # These functions are only available for the API version 300 or higher

    # Turn the Server Hardware led light On
    server.patch('replace', '/uidState', 'On')
    print("Server Hardware led light turned on")

    # Get a Firmware by Server Hardware ID
    print("Get a Firmware by Server Hardware ID")
    p = server.get_firmware()
    pprint(p)

    # Get all server hardware firmwares
    print("Get all Server Hardware firmwares")
    p = server_hardwares.get_all_firmwares()
    pprint(p)

    # Get server hardware firmwares filtering by server name
    print("Get Server Hardware firmwares filtering by server name")
    p = server_hardwares.get_all_firmwares(filter="serverName='{}'".format(server_name))
    pprint(p)

if oneview_client.api_version >= 500:
    # Get information describing an 'SDX' partition including a list of physical server blades represented by a
    # server hardware. Only supported by SDX enclosures.
    print("Get SDX physical server hardware")
    sdx_server = server.get_physical_server_hardware()
    pprint(sdx_server)

# Remove rack server
server.remove()
print("Server removed successfully")
