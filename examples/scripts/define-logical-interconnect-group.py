#!/usr/bin/env python
#
# (C) Copyright (2012-2015) Hewlett Packard Enterprise Development LP
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
#
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import range
from future import standard_library
standard_library.install_aliases()
import sys
import argparse
from collections import defaultdict
sys_ver = sys.version_info
if sys_ver == 2:
	if sys.version_info < (2, 9):
		raise Exception('Must use Python 2.9 or later')
elif sys_ver == 3:
	if sys.version_info < (3, 4):
		raise Exception('Must use Python 3.4 or later')

import hpOneView as hpov
from pprint import pprint


def acceptEULA(con):
    # See if we need to accept the EULA before we try to log in
    con.get_eula_status()
    try:
        if con.get_eula_status() is True:
            print('EULA display needed')
            con.set_eula('no')
    except Exception as e:
        print('EXCEPTION:')
        print(e)


def login(con, credential):
    # Login with givin credentials
    try:
        con.login(credential)
    except:
        print('Login failed')


def defethernet(igmp, timeout, mac_failover, mac_interval,
                pause_flood, network_loop):

    # Invert the boolean values to match the correct disable or enable intent
    mac_failover = not mac_failover
    pause_flood = not pause_flood
    network_loop = not network_loop

    ethernetSettings = hpov.common.make_ethernetsettings_dict(
        enableFastMacCacheFailover=mac_failover,
        enableIgmpSnooping=igmp,
        enableNetworkLoopProtection=network_loop,
        enablePauseFloodProtection=pause_flood,
        igmpIdleTimeoutInterval=timeout,
        macRefreshInterval=mac_interval)

    return ethernetSettings


def deflig(net, con, name, ics, ethernetSettings):

    lig = hpov.common.make_lig_dict(name, ethernetSettings)

    # Create a bays dictionary and initalize each interconnect bays value to be
    # None. Then walk the list of interconnects supplied and assign the
    # appropriate part number as the value.
    bays = {}
    for ii in range(1, 9):
        bays[int(ii)] = None
    for items in ics:
        bay, ic = items.split(':')
        if ic == 'FlexFabric':
            pn = '571956-B21'
        elif ic == 'Flex10':
            pn = '455880-B21'
        elif ic == 'Flex1010D':
            pn = '638526-B21'
        elif ic == 'Flex2040f8':
            pn = '691367-B21'
        elif ic == 'VCFC20':
            pn = '572018-B21'
        elif ic == 'VCFC24':
            pn = '466482-B21'
        elif ic == 'FEX':
            pn = '641146-B21'
        else:
            print('Error, invalid interconnect type: ', ic)
            sys.exit()
        bays[int(bay)] = pn

    # Ensure that adjacent modules are identical
    for ii in range(1, 8, 2):
        if bays[ii] is not None:
            if bays[ii] != bays[ii+1]:
                print('Error, adjacent bays must contain the same '
                      'interconnect modules')
                sys.exit()

    # Build a dict with the pn as the key and and a list of the bays as the
    # value
    sw = defaultdict(list)
    for ii in range(1, 9):
        sw[bays[ii]].append(ii)

    for item in sw:
        if item is not None:
            swtype = con.get_entity_byfield(hpov.common.uri['ictype'],
                                            'partNumber', item)
            hpov.common.set_iobay_occupancy(lig['interconnectMapTemplate'],
                                            sw[item], swtype['uri'])

    lig = net.create_lig(lig)
    print('\nCreating Logical Interconnect Group\n')
    if 'name' in lig:
        print('Name:          ', lig['name'])
        print('State:         ', lig['state'])
    else:
        pprint(lig)


def main():
    parser = argparse.ArgumentParser(add_help=True,
                        formatter_class=argparse.RawTextHelpFormatter,
                                     description='''
    Add new Logical Interconnect Group

    Usage: ''')
    parser.add_argument('-a', dest='host', required=True,
                        help='''
    HP OneView Appliance hostname or IP address''')
    parser.add_argument('-u', dest='user', required=False,
                        default='Administrator',
                        help='''
    HP OneView Username''')
    parser.add_argument('-p', dest='passwd', required=True,
                        help='''
    HP OneView Password''')
    parser.add_argument('-c', dest='cert', required=False,
                        help='''
    Trusted SSL Certificate Bundle in PEM (Base64 Encoded DER) Format''')
    parser.add_argument('-y', dest='proxy', required=False,
                        help='''
    Proxy (host:port format''')
    parser.add_argument('-n', dest='logical_interconnect_group_name',
                        required=True,
                        help='''
    Name of the logical interconnect group''')
    parser.add_argument('-i', dest='interconnects', required=True, nargs='+',
                        help='''
    List of interconnect modules specified as
    BAY:INTERCONNECT where INTERCONNECT must be one of
    the following [FlexFabric, Flex10, Flex1010D,
    Flex2040f8 VCFC20, VCFC24 and FEX] For example Virtual
    Connect Flex10 modules in bays and 2 with Virtual
    Connect 24 port Fibre Channel modules in bays 3 and 4
    would be specified as:

        -i 1:Flex10 2:Flex10 3:VCFC24 4:VCFC24''')
    parser.add_argument('-g', dest='igmp_snooping', action='store_true',
                        required=False,
                        help='''
    Enable IGMP Snooping

    The Group Membership Interval value, as specified by
    the IGMP v2 specification(RFC 2236).  For optimum
    network resource usage, set the timeout interval to
    match your network\'s multicast router settings.''')
    parser.add_argument('-t', dest='igmp_idle_timeout', required=False,
                        default=260, type=int,
                        help='''
    The Group Membership Interval value, as
    specified by the IGMP v2 specification(RFC 2236).
    For optimum network resource usage, set the timeout
    interval to match your network\'s multicast router
    settings.''')
    parser.add_argument('-m', dest='fast_mac_cache_failover',
                        action='store_true', required=False,
                        help='''
    Disable Fast MAC Cache Failover.

    When an uplink that was in standby mode becomes
    active, it can take several minutes for external
    Ethernet interconnects to recognize that the server
    blades can now be reached on this newly active
    connection.  Enabling Fast MAC Cache Failover causes
    Ethernet packets to be transmitted on the newly
    active connection, which enables the external
    Ethernet interconnects to identify the new
    connection(and update their MAC caches) The
    transmission sequence is repeated a few times at the
    MAC refresh interval and completes in about 1
    minute.''')
    parser.add_argument('-e', dest='mac_refresh_interval', required=False,
                        default=5, type=int,
                        help='''
    The time interval at which MAC caches are refreshed
    in seconds''')
    parser.add_argument('-o', dest='pause_flood_protection',
                        action='store_true', required=False,
                        help='''
    Disable pause flood protection:

    Ethernet switch interfaces use pause frame based flow
    control mechanisms to control data flow. When a pause
    frame is received on a flow control enabled interface,
    the transmit operation is stopped for the pause
    duration specified in the pause frame. All other
    frames destined for this interface are queued up.  If
    another pause frame is received before the previous
    pause timer expires, the pause timer is refreshed to
    the new pause duration value. If a steady stream of
    pause frames is received for extended periods of time,
    the transmit queue for that interface continues to
    grow until all queuing resources are exhausted.  This
    condition severely impacts the switch operation on
    other interfaces. In addition, all protocol operations
    on the switch are impacted because of the inability to
    transmit protocol frames. Both port pause and
    priority-based pause frames can cause the same
    resource exhaustion condition.

    VC interconnects provide the ability to monitor server
    downlink ports for pause flood conditions and take
    protective action by disabling the port. The default
    polling interval is 10 seconds and is not customer
    configurable. The SNMP agent supports trap generation
    when a pause flood condition is detected or cleared.

    This feature operates at the physical port level. When
    a pause flood condition is detected on a Flex-10
    physical port, all Flex-10 logical ports associated
    with physical ports are disabled. When the pause flood
    protection feature is enabled, this feature detects
    pause flood conditions on server downlink ports and
    disables the port. The port remains disabled until an
    administrative action is taken. The administrative
    action involves the following steps:

    1. Resolve the issue with the NIC on the server
    causing the continuous pause generation. This might
    include updating the NIC firmware and device drivers.

    Rebooting the server might not clear the pause flood
    condition if the cause of the pause flood condition is
    in the NIC firmware. In this case, the server must be
    completely disconnected from the power source to reset
    the NIC firmware.

    2. Re-enable the disabled ports on the VC interconnect
    modules.''')
    parser.add_argument('-l', dest='network_loop_protection',
                        action='store_true', required=False,
                        help='''
    Disable Network loop protection:

    The loop protection feature enables detection of loops
    on downlink ports, which can be Flex-10 logical ports
    or physical ports. The feature applies when Device
    Control Channel (DCC) protocol is running on the
    Flex-10 port. If DCC is not available, the feature
    applies to the physical downlink port.

    Network loop protection uses two methods to detect
    loops:

    1. It periodically injects a special probe frame into
    the VC domain and monitors downlink ports for the
    looped back probe frame. If this special probe frame
    is detected on downlink ports, the port is considered
    to cause the loop condition.

    2. It monitors and intercepts common loop detection
    frames used in other switches. In network environments
    where the upstream switches send loop detection
    frames, the VC interconnects must ensure that any
    downlink loops do not cause these frames to be sent
    back to the uplink ports. Even though the probe frames
    ensure loops are detected, there is a small time
    window depending on the probe frame transmission
    interval in which the loop detection frames from the
    external switch might loop through down link ports and
    reach uplink ports. By intercepting the external loop
    detection frames on downlinks, the possibility of
    triggering loop protection on the upstream switch is
    eliminated. When network loop protection is enabled,
    VC interconnects intercept loop detection frames from
    various switch vendors, such as Cisco and HP
    Networking.

    When the network loop protection feature is enabled,
    any probe frame or other supported loop detection
    frame received on a downlink port is considered to be
    causing the network loop, and the port is disabled
    immediately until an administrative action is taken.
    The administrative action involves resolving the loop
    condition and clearing the loop protection error
    condition. The loop detected status on a port can be
    cleared by un-assigning all networks from the profile
    connect corresponding to the port in the loop detected
    state.

    The SNMP agent supports trap generation when a loop
    condition is detected or cleared.''')

    args = parser.parse_args()
    credential = {'userName': args.user, 'password': args.passwd}

    con = hpov.connection(args.host)
    net = hpov.networking(con)

    if args.proxy:
        con.set_proxy(args.proxy.split(':')[0], args.proxy.split(':')[1])
    if args.cert:
        con.set_trusted_ssl_bundle(args.cert)

    login(con, credential)
    acceptEULA(con)

    ethernetSettings = defethernet(args.igmp_snooping,
                                   args.igmp_idle_timeout,
                                   args.fast_mac_cache_failover,
                                   args.mac_refresh_interval,
                                   args.pause_flood_protection,
                                   args.network_loop_protection)

    deflig(net, con,
           args.logical_interconnect_group_name,
           args.interconnects,
           ethernetSettings)


if __name__ == '__main__':
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
