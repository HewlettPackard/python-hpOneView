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

from pprint import pprint
from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException
from config_loader import try_load_from_file

config = {
    "ip": "",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# To run this example you must define a logical interconnect id
interconnect_id = ""

port_d1 = {
    "type": "port",
    "portName": "d1",
    "bayNumber": 1,
    "enabled": False,
    "portId": "{0}:d1".format(interconnect_id)
}

port_d2 = {
    "portName": "d2",
    "enabled": False,
    "portId": "{0}:d2".format(interconnect_id)
}

ports_for_update = [port_d1, port_d2]

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Get the first two Interconnects
print("Get the first two interconnects")
try:
    interconnects = oneview_client.interconnects.get_all(0, 2)
    pprint(interconnects)
except HPOneViewException as e:
    print(e.msg)

# Get Interconnects Statistics
print("Get an interconnect statistics")
try:
    interconnect_statistics = oneview_client.interconnects.get_statistics(interconnect_id)
    if interconnect_statistics:
        pprint(interconnect_statistics['moduleStatistics'])
    else:
        pprint("There are no statistics for the interconnect {0}".format(interconnect_id))
except HPOneViewException as e:
    print(e.msg)

# Get the Statistics from a port of an Interconnects
print("Get the port statistics for downlink port 1 on the interconnect "
      "that matches the specified ID")
try:
    statistics = oneview_client.interconnects.get_statistics(interconnect_id, port_d1["portName"])
    pprint(statistics)
except HPOneViewException as e:
    print(e.msg)

# Get the subport Statistics from a port of an Interconnects
print("Get the subport statistics for subport 1 on downlink port 2 on the interconnect "
      "that matches the specified ID")
try:
    statistics = oneview_client.interconnects.get_subport_statistics(interconnect_id,
                                                                     port_d1["portName"],
                                                                     port_d1["bayNumber"])
    pprint(statistics)
except HPOneViewException as e:
    print(e.msg)

# Get by ID
print("Get Interconnect that matches the specified ID")
try:
    interconnect = oneview_client.interconnects.get(interconnect_id)
    pprint(interconnect)
except HPOneViewException as e:
    print(e.msg)

# Get by hostName
print("Get an interconnect by hostName")
try:
    interconnect = oneview_client.interconnects.get_by('hostName', interconnect["hostName"])[0]
    pprint(interconnect)
except HPOneViewException as e:
    print(e.msg)

# Get by name
print("Get an interconnect by name")
try:
    interconnect = oneview_client.interconnects.get_by_name(interconnect["name"])
    pprint(interconnect)
except HPOneViewException as e:
    print(e.msg)

# Turn the power off
print("Turn the power off and the UID light to 'Off' for interconnect " +
      "that matches the specified ID")
try:
    interconnect = oneview_client.interconnects.patch(
        id_or_uri=interconnect_id,
        operation='replace',
        path='/powerState',
        value='Off'
    )
    pprint(interconnect)
except HPOneViewException as e:
    print(e.msg)

# Updates an interconnect port.
print("Update the interconnect port")
try:
    port_for_update = port_d1.copy()
    port_for_update["enabled"] = False

    updated = oneview_client.interconnects.update_port(port_for_update, interconnect_id)
    pprint(updated)
except HPOneViewException as e:
    print(e.msg)

# Reset of port protection.
print("Trigger a reset of port protection of the interconnect that matches the specified ID")
try:
    result = oneview_client.interconnects.reset_port_protection(interconnect_id)
    pprint(result)
except HPOneViewException as e:
    print(e.msg)

# Get name servers
print("Get the named servers for the interconnect that matches the specified ID")

try:
    interconnect_ns = oneview_client.interconnects.get_name_servers(interconnect_id)
    pprint(interconnect_ns)
except HPOneViewException as e:
    print(e.msg)

# Updates the interconnect ports.
print("Update the interconnect ports")

try:
    updated = oneview_client.interconnects.update_ports(ports_for_update, interconnect_id)

    # filtering only updated ports
    names = [port_d1["portName"], port_d2["portName"]]
    updated_ports = [port for port in updated["ports"] if port["portName"] in names]

    pprint(updated_ports)
except HPOneViewException as e:
    print(e.msg)
