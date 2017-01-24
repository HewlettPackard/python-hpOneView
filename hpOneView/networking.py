# -*- coding: utf-8 -*-

"""
networking.py
~~~~~~~~~~~~

This module implements Settings HPE OneView REST API.

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
import http.client

from hpOneView.common import uri, get_members, make_enet_settings, \
    make_network_set, make_Bandwidth, make_ethernet_networkV3, make_fc_networkV2
from hpOneView.activity import activity
from hpOneView.exceptions import HPOneViewException, HPOneViewInvalidResource
from warnings import warn


def deprecated(func):
    def wrapper(*args, **kwargs):
        warn("Module networking is deprecated, use OneViewClient class instead", DeprecationWarning)
        return func(*args, **kwargs)
    return wrapper


class networking(object):
    def __init__(self, con):
        self._con = con
        self._activity = activity(con)

    ###########################################################################
    # Logical Interconnect Group
    ###########################################################################
    @deprecated
    def get_lig_default_settings(self):
        """ Gets default settings for a logical interconnect group."""
        return self._con.get(uri['lig'] + '/defaultSettings')

    @deprecated
    def get_lig_settings(self, id):
        """ Gets the interconnect settings for a logical interconnect group."""
        lig_settings_uri = uri['lig'] + '/{id}/settings'
        return self._con.get(lig_settings_uri.format(id=id))

    @deprecated
    def update_settings_from_default(self, settings={}):
        if not settings:
            settings = make_enet_settings('__NoName__')
        default = self._con.get('%s/defaultSettings')
        return default

        for key in list(settings.keys()):
            if key != 'name':
                settings[key] = default[key]
        return settings

    @deprecated
    def create_lig(self, lig, blocking=True, verbose=False):
        task, body = self._con.post(uri['lig'], lig)
        task, entity = self._activity.make_task_entity_tuple(task)
        if blocking is True:
            task = self._activity.wait4task(task, verbose=verbose)
        return entity

    @deprecated
    def update_lig(self, lig, blocking=True, verbose=False):
        task, body = self._con.put(lig['uri'], lig)
        if blocking is True:
            task = self._activity.wait4task(task, verbose=verbose)
        return task

    @deprecated
    def delete_lig(self, lig, blocking=True, verbose=False):
        task, body = self._con.delete(lig['uri'])
        if blocking is True:
            task = self._activity.wait4task(task, verbose=verbose)
        return task

    @deprecated
    def get_ligs(self):
        return get_members(self._con.get(uri['lig']))

    @deprecated
    def get_lig_by_name(self, ligname):
        return self._con.get_entity_byfield(uri['lig'], 'name', ligname)

    @deprecated
    def get_lig_by_id(self, id):
        """ Gets a logical interconnect group."""
        return self._con.get(uri['lig'] + '/' + id)

    @deprecated
    def get_lig_schema(self):
        """ Gets the JSON schema for the logical interconnect group."""
        return self._con.get(uri['lig'] + '/schema')

    @deprecated
    def get_interconnect_types(self):
        # get all the supported interconnect types
        resp = get_members(self._con.get(uri['ictype']))
        return resp

    ###########################################################################
    # Logical Interconnects
    ###########################################################################
    @deprecated
    def get_lis(self, filter=''):
        """
        This function is deprecated, use
            OneViewClient(config).logical_interconnects.get_all() instead.

        Gets a collection of logical interconnects.

        Args:
            filter:
                A general filter/query string that narrows the list of
                resources returned by a multi-resource GET (read) request and
                DELETE (delete) request. The default is no filter
                (all resources are returned). The filter parameter specifies
                a general filter/query string. This query string narrows the
                selection of resources returned from a GET request that
                returns a list of resources. The following example shows how to
                retrieve only the first 10 logical interconnects:

                self.get_lis(filter='?start=0&count=10')

                For more options, see the Common Parameters session from
                the HPE OneView API reference.
        Returns: dict
        """
        return get_members(self._con.get(uri['li'] + filter))

    @deprecated
    def correct_lis(self, uris, blocking=True, verbose=False):
        """ Returns logical interconnects to a consistent state.

        The current logical interconnect state is compared to the associated
        logical interconnect group. Any differences identified are corrected,
        bringing the logical interconnect back to a consistent state. Changes
        are asynchronously applied to all managed interconnects. Note that if
        the changes detected involve differences in the interconnect map
        between the logical interconnect group and the logical interconnect,
        the process of bringing the logical interconnect back to a consistent
        state may involve automatically removing existing interconnects from
        management and/or adding new interconnects for management.
        """
        request = {"uris": uris}
        task, body = self._con.put(uri['li'] + '/compliance', request)
        if blocking is True:
            task = self._activity.wait4task(task, verbose=verbose)
        return task

    @deprecated
    def create_li(self, location_entries, blocking=True, verbose=False):
        """"
        This function is deprecated, use
            OneViewClient(config).logical_interconnects.create_interconnect() instead.

        Creates an interconnect at the given location.

        Args:
            location_entries:
                A list of location entries. For example:
                [
                    {"type": "Enclosure", "value": "1"},
                    {"type": "Bay", "value": "1"}
                ]
        """
        request = {"locationEntries": location_entries}
        task, body = self._con.post(
            uri['li'] + '/locations/interconnects', request)
        if blocking is True:
            task = self._activity.wait4task(task, verbose=verbose)
        return task

    @deprecated
    def delete_li(self, location, blocking=True, verbose=False):
        """
        This function is deprecated, use
            OneViewClient(config).logical_interconnects.delete_interconnect() instead.

        Deletes an interconnect from a location.

        Args:
            location:
                where the logical interconnect is located. For example:

                self.delete_li('Enclosure:/rest/enclosures/09XXX,Bay:1')
        """
        task, body = self._con.delete(
            uri['li'] + '/locations/interconnects?location=' + location)
        if blocking is True:
            task = self._activity.wait4task(task, verbose=verbose)
        return task

    @deprecated
    def get_li_schema(self):
        """ Gets the JSON schema for the logical interconnect."""
        return self._con.get(uri['li'] + '/schema')

    @deprecated
    def get_li_by_id(self, id):
        """
        This function is deprecated, use
            OneViewClient(config).logical_interconnects.get() instead.

        Gets a logical interconnect."""
        return self._con.get(uri['li'] + '/' + id)

    @deprecated
    def correct_li_by_id(self, id, blocking=True, verbose=False):
        """
        This function is deprecated, use
            OneViewClient(config).logical_interconnects.update_compliance() instead.

        Returns a logical interconnect to a consistent state.

        The current logical interconnect state is compared to the associated
        logical interconnect group. Any differences identified are corrected,
        bringing the logical interconnect back to a consistent state. Changes
        are asynchronously applied to all managed interconnects. Note that if
        the changes detected involve differences in the interconnect map
        between the logical interconnect group and the logical interconnect,
        the process of bringing the logical interconnect back to a consistent
        state may involve automatically removing existing interconnects from
        management and/or adding new interconnects for management.
        """
        li_uri = uri['li'] + '/{id}/compliance'
        task, body = self._con.put(li_uri.format(id=id), {})
        if blocking is True:
            task = self._activity.wait4task(task, verbose=verbose)
        return task

    @deprecated
    def update_ethernet_interconnected_settings(self, id, settings,
                                                blocking=True, verbose=False):
        """
        This function is deprecated, use
            OneViewClient(config).logical_interconnects.update_ethernet_settings() instead.

        Updates the Ethernet settings for the logical interconnect.

        Args:
            id:
                the id of the logical interconnect that will be updated.
            settings:
                a dict with settings properties that must be updated. Example
                of a settings dict:

                {
                "interconnectType": "Ethernet",
                "igmpIdleTimeoutInterval": 200,
                "macRefreshInterval": 10,
                "name": "ES-882901476",
                "created": "2015-08-21T21:48:01.096Z",
                "enableRichTLV": false,
                "uri": "/rest/logical-interconnects/ID/ethernetSettings",
                "enableNetworkLoopProtection": true,
                "enableFastMacCacheFailover": true,
                "modified": "2015-08-21T21:48:01.099Z",
                "enableIgmpSnooping": true,
                "enablePauseFloodProtection": true,
                "dependentResourceUri": "/rest/logical-interconnects/ID",
                "type": "EthernetInterconnectSettingsV3",
                "id": "9b1380ee-a0bb-4388-af35-2c5a05e84c47"
                }
        """
        settings_uri = uri['li'] + '/{id}/ethernetSettings'
        task, body = self._con.put(settings_uri.format(id=id), settings)
        if blocking is True:
            task = self._activity.wait4task(task, verbose=verbose)
        return task

    @deprecated
    def get_li_firmware(self, id):
        """
        This function is deprecated, use
            OneViewClient(config).logical_interconnects.get_firmware() instead.

        Gets the installed firmware for a logical interconnect."""
        firmware_uri = uri['li'] + '/{id}/firmware'
        return self._con.get(firmware_uri.format(id=id))

    ###########################################################################
    # Connection Templates
    ###########################################################################
    @deprecated
    def get_connection_templates(self):
        return get_members(self._con.get(uri['ct']))

    @deprecated
    def update_net_ctvalues(self, xnet, bw={}):
        if not bw:
            return
        if not xnet:
            raise HPOneViewInvalidResource('Missing Network')
        defaultCT = self._con.get(xnet['connectionTemplateUri'])
        defaultCT['bandwidth']['maximumBandwidth'] = bw['maximumBandwidth']
        defaultCT['bandwidth']['typicalBandwidth'] = bw['typicalBandwidth']
        task, body = self._con.put(defaultCT['uri'], defaultCT)
        return self._activity.make_task_entity_tuple(task)

    ###########################################################################
    # NetworkSets
    ###########################################################################
    @deprecated
    def create_networkset(self, name, networkUris=[], typicalBandwidth=2500,
                          maximumBandwidth=10000, blocking=True,
                          verbose=False):
        """ Create an network-set

        Args:
            name:
                Name of the Network Set
            networkUris:
                A set of Ethernet network URIs that will be members of this
                network set. NOTE: all Ethernet networks in a network set must
                have unique VLAN IDs.
             typicalBandwidth:
                The transmit throughput (mbps) that should be allocated to
                this connection. For FlexFabric connections this value must not
                exceed the maximum bandwidth of the selected network
             maximumBandwidth:
                 Maximum transmit throughput (mbps) allowed on this
                 connection. The value is limited by the maximum throughput
                 of the network link and maximumBandwidth of the selected
                 network.


        Returns: dict
        """
        bw = make_Bandwidth(typicalBandwidth, maximumBandwidth)
        nset = make_network_set(name, networkUris)
        body = self._con.conditional_post(uri['nset'], nset)
        task, entity = self._activity.make_task_entity_tuple(body)
        if not task and not entity:
            # contitional_post returned an already existing resource
            return body
        else:
            # assume we can update CT even if network create task is not cmpelt
            self.update_net_ctvalues(entity, bw)
            if blocking is True:
                task = self._activity.wait4task(task, tout=60, verbose=verbose)
            return entity

    @deprecated
    def delete_networkset(self, networkset, blocking=True, verbose=False):
        task, body = self._con.delete(networkset['uri'])
        if blocking is True:
            task = self._activity.wait4task(task, verbose=verbose)
        return task

    @deprecated
    def get_networksets(self):
        return get_members(self._con.get(uri['nset']))

    ###########################################################################
    # Networks
    ###########################################################################
    @deprecated
    def create_enet_networks(self, prefix, vid_start, vid_count, bw={}):
        enet_list = []
        try:
            for vid in range(vid_start, vid_start + vid_count):
                enet_name = '%s%s' % (prefix, vid)
                enet_list.append(self.create_enet_network(enet_name,
                                                          vid,
                                                          bw=bw
                                                          ))
        except http.client.HTTPException:
            # All or nothing
            for enet in enet_list:
                try:
                    self._con.delete(enet['uri'])
                except http.client.HTTPException:
                    pass
            raise HPOneViewException('Could not create one or more networks')
        return enet_list

    @deprecated
    def create_enet_network(self, name, description=None,
                            ethernetNetworkType=None, purpose='General',
                            privateNetwork=False, smartLink=True, vlanId=0,
                            typicalBandwidth=2500, maximumBandwidth=10000,
                            blocking=True, verbose=False):
        """ Create an Ethernet Network

        Args:
            name:
                Name of the Ethernet Network
            description:
                Breif description of the Ethernet Network
            vlanId:
                The Virtual LAN (VLAN) identification number assigned to the
                network. The VLAN ID is optional when ethernetNetworkType is
                Untagged or Tunnel. Multiple Ethernet networks can be defined
                with the same VLAN ID, but all Ethernet networks in an uplink
                set or network set must have unique VLAN IDs. The VLAN ID
                cannot be changed once the network has been created.
            purpose:
                A description of the network's role within the logical
                interconnect. Values: 'FaultTolerance', 'General',
                'Management', or 'VMMigration'
            smartLink:
                When enabled, the network is configured so that, within a
                logical interconnect, all uplinks that carry the network are
                monitored.  If all uplinks lose their link to external
                interconnects, all corresponding dowlink (server) ports which
                connect to the network are forced into an unlinked state. This
                allows a server side NIC teaming driver to automatically
                failover to an alternate path.
            privateNetwork:
                 When enabled, the network is configured so that all downlink
                 (server) ports connected to the network are prevented from
                 communicating with each other within the logical interconnect.
                 Servers on the network only communicate with each other
                 through an external L3 router that redirects the traffic back
                 to the logical interconnect.
            ethernetNetworkType:
                The type of Ethernet network. It is optional. If this field is
                missing or its value is Tagged, you must supply a valid vlanId;
                if this value is Untagged or Tunnel, please either ignore vlanId
                or specify vlanId equals 0. Values: 'NotApplicable', 'Tagged',
                'Tunnel', 'Unknown', or 'Untagged'.
             typicalBandwidth:
                The transmit throughput (mbps) that should be allocated to
                this connection. For FlexFabric connections this value must not
                exceed the maximum bandwidth of the selected network
             maximumBandwidth:
                 Maximum transmit throughput (mbps) allowed on this
                 connection. The value is limited by the maximum throughput
                 of the network link and maximumBandwidth of the selected
                 network.

        Returns: dict
        """
        bw = make_Bandwidth(typicalBandwidth, maximumBandwidth)
        xnet = make_ethernet_networkV3(name=name,
                                       ethernetNetworkType=ethernetNetworkType,
                                       purpose=purpose,
                                       privateNetwork=privateNetwork,
                                       smartLink=smartLink,
                                       vlanId=vlanId)
        task, entity = self.create_network(uri['enet'], xnet, bw, verbose)
        if blocking is True:
            task = self._activity.wait4task(task, tout=60, verbose=verbose)
        return entity

    @deprecated
    def create_fc_network(self, name, autoLoginRedistribution=True,
                          description=None, fabricType='FabricAttach',
                          linkStabilityTime=30, managedSanUri=None,
                          typicalBandwidth=2500, maximumBandwidth=10000,
                          blocking=True, verbose=False):
        """
        Deprecated function, use: OneViewClient(config).fc_networks.create()

        Create a Fibre Channel Network

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
                The supported Fibre Channel access method. Values
                'FabricAttach' or 'DirectAttach'.
            linkStabilityTime:
                The time interval, expressed in seconds, to wait after a link
                that was previously offline becomes stable, before automatic
                redistribution occurs within the fabric. This value is not
                effective if autoLoginRedistribution is false.
            managedSanUri:
                The managed SAN URI that is associated with this Fibre Channel
                network. This value should be null for Direct Attach Fibre
                Channel networks and may be null for Fabric Attach Fibre
                Channel networks.
             typicalBandwidth:
                The transmit throughput (mbps) that should be allocated to
                this connection. For FlexFabric connections this value must not
                exceed the maximum bandwidth of the selected network
             maximumBandwidth:
                 Maximum transmit throughput (mbps) allowed on this
                 connection. The value is limited by the maximum throughput
                 of the network link and maximumBandwidth of the selected
                 network.

        Returns: dict
        """
        bw = make_Bandwidth(typicalBandwidth, maximumBandwidth)
        xnet = make_fc_networkV2(name,
                                 autoLoginRedistribution=autoLoginRedistribution,
                                 description=description,
                                 fabricType=fabricType,
                                 linkStabilityTime=linkStabilityTime,
                                 managedSanUri=managedSanUri)
        task, entity = self.create_network(uri['fcnet'], xnet, bw, verbose)
        if blocking is True:
            task = self._activity.wait4task(task, tout=60, verbose=verbose)
        return entity

    @deprecated
    def create_network(self, uri, xnet, bw={}, verbose=False):
        # throws an exception if there is an error
        body = self._con.conditional_post(uri, xnet)
        task, entity = self._activity.make_task_entity_tuple(body)
        if not task and not entity:
            # contitional_post returned an already existing resource
            return None, body
        else:
            # assume we can update CT even if network create task is not cmpelt
            self.update_net_ctvalues(entity, bw)
            return task, entity

    @deprecated
    def update_network(self, xnet):
        task, body = self._con.put(xnet['uri'], xnet)
        return self._activity.make_task_entity_tuple(task)

    @deprecated
    def delete_network(self, xnet, blocking=True, verbose=False):
        """
        Deprecated function, use: OneViewClient(config).fc_networks.delete()
        Returns: dict

        """
        task, body = self._con.delete(xnet['uri'])
        if blocking is True:
            task = self._activity.wait4task(task, verbose=verbose)
        return task

    @deprecated
    def get_enet_networks(self):
        # TODO remove the evil use/hack of the large count default. The OneView
        # API documents that count=-1 should return everything but it is not
        # universally honored, where the extremely large count number is.
        return get_members(self._con.get(uri['enet'] +
                                         '?start=0&count=9999999'))

    @deprecated
    def get_fc_networks(self):
        """
        Deprecated function, use: OneViewClient(config).fc_networks.get_all()
        Returns: dict

        """
        return get_members(self._con.get(uri['fcnet'] +
                                         '?start=0&count=9999999'))

    ###########################################################################
    # Uplink Sets
    ###########################################################################
    @deprecated
    def get_uplink_sets(self):
        return get_members(self._con.get(uri['uplink-sets']))

    @deprecated
    def delete_uplink_set(self, uplink_set, blocking=True, verbose=False):
        task, body = self._con.delete(uplink_set['uri'])
        if blocking is True:
            task = self._activity.wait4task(task, verbose=verbose)
        return task

    ###########################################################################
    # Logical Downlinks
    ###########################################################################
    @deprecated
    def get_logical_downlinks(self, filter=''):
        """ Gets a list of logical downlinks.

        Args:
            filter:
                A general filter/query string that narrows the list of
                resources returned by a multi-resource GET (read) request and
                DELETE (delete) request. The default is no filter
                (all resources are returned). The filter parameter specifies
                a general filter/query string. This query string narrows the
                selection of resources returned from a GET request that
                returns a list of resources. The following example shows how to
                retrieve only the first 10 logical downlinks:

                self.get_logical_downlinks(filter='?start=0&count=10')

                For more options, see the Common Parameters session from
                the HPE OneView API reference.
        Returns: dict
        """
        downlinks_uri = uri['ld'] + filter
        return self._con.get(downlinks_uri)

    @deprecated
    def get_logical_downlinks_schema(self):
        """ Gets the JSON schema for the logical downlink.

        Returns: JSON
        """
        return self._con.get(uri['ld'] + '/schema')

    @deprecated
    def get_logical_downlinks_without_ethernet(self, filter=''):
        """ Gets a list of logical downlinks, except existing Ethernet networks.

        Args:
            filter:
                A general filter/query string that narrows the list of
                resources returned by a multi-resource GET (read) request and
                DELETE (delete) request. The default is no filter
                (all resources are returned). The filter parameter specifies
                a general filter/query string. This query string narrows the
                selection of resources returned from a GET request that
                returns a list of resources. The following example shows how to
                retrieve only the first 10 logical downlinks without ethernet:

                self.get_logical_downlinks_without_ethernet(filter=
                                                            '?start=0&count=10')

                For more options, see the Common Parameters session from
                the HPE OneView API reference.
        Returns: dict
        """
        downlinks_uri = uri['ld'] + '/withoutEthernet' + filter
        return self._con.get(downlinks_uri)

    @deprecated
    def get_logical_downlink(self, id):
        """ Gets a logical downlink

        Args:
            id:
                the logical downlink id
        Returns: dict
        """
        return self._con.get(uri['ld'] + '/' + id)

    @deprecated
    def get_logical_downlink_without_ethernet(self, id):
        """ Gets a logical downlink excluding any existing Ethernet networks.

        Args:
            id:
                the logical downlink id
        Returns: dict
        """
        ld_uri = uri['ld'] + '/{id}/withoutEthernet'
        return self._con.get(ld_uri.format(id=id))

    ###########################################################################
    # Interconnects
    ###########################################################################
    @deprecated
    def get_interconnects(self):
        return get_members(self._con.get(uri['ic']))

    @deprecated
    def get_enet_network_by_name(self, nwname):
        return self._con.get_entity_byfield(uri['enet'], 'name', nwname)

    @deprecated
    def get_fc_network_by_name(self, nwname):
        return self._con.get_entity_byfield(uri['fcnet'], 'name', nwname)

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
