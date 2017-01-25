# -*- coding: utf-8 -*-

"""
settings.py
~~~~~~~~~~~~

This module implements settings HPE OneView REST API.

It has been deprecated and will be removed soon. We strongly recommend to use the OneViewClient class instead.
See more details at: https://github.com/HewlettPackard/python-hpOneView/tree/master/hpOneView/README.md
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import open
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

from hpOneView.common import uri, get_members
from hpOneView.activity import activity
from hpOneView.exceptions import HPOneViewException
from warnings import warn


def deprecated(func):
    def wrapper(*args, **kwargs):
        warn("Module settings is deprecated, use OneViewClient class instead", DeprecationWarning)
        return func(*args, **kwargs)
    return wrapper


class settings(object):
    def __init__(self, con):
        self._con = con
        self._activity = activity(con)

    ###########################################################################
    # Appliance Firmware
    ###########################################################################
    @deprecated
    def upload_fw(self, path, name, verbose=False):
        response, body = self._con.post_multipart(uri['appliance-firmware'],
                                                  '', path, name, verbose)
        return body

    @deprecated
    def get_pending_fw(self):
        body = self._con.get(uri['fw-pending'])
        return body

    @deprecated
    def upgrade_appliance_fw(self, filename):
        task, body = self._con.put(uri['fw-pending'] + '?file=' + filename, '')
        return body

    @deprecated
    def delete_appliance_fw(self):
        task, body = self._con.delete(uri['fw-pending'])
        return body

    ###########################################################################
    # SPP Upload
    ###########################################################################
    @deprecated
    def upload_spp(self, sppPath, sppName, verbose=False, blocking=True):
        response, body = self._con.post_multipart(uri['fwUpload'], '',
                                                  sppPath, sppName, verbose)
        if response.status == 202 and verbose is True:
            print('Upload complete. Waiting for processing.')
        task, spp = self._activity.make_task_entity_tuple(body)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        if verbose is True:
            print('Processing complete.')
        return spp['resourceId']

    @deprecated
    def delete_spp(self, sppName):
        task, body = self._con.delete(uri['fwDrivers'] + '/' + sppName)
        return body

    @deprecated
    def get_spps(self):
        body = self._con.get(uri['fwDrivers'])
        return get_members(body)

    @deprecated
    def get_health_status(self):
        body = self._con.get(uri['healthStatus'])
        return get_members(body)

    @deprecated
    def get_version(self):
        body = self._con.get(uri['version'])
        return body

    @deprecated
    def generate_support_dump(self, encrypt=True, logicalInterconnect=None):
        request = {}
        if logicalInterconnect is None:
            request['encrypt'] = encrypt
            request['errorCode'] = 'CI'
            task, body = self._con.post(uri['supportDump'], request)
        else:
            request['errorCode'] = 'LI'
            task, body = self._con.post(
                logicalInterconnect['uri'] + '/support-dumps',
                request)
        return body

    @deprecated
    def download_support_dump(self, dumpInfo):
        body = self._con.get(dumpInfo['uri'])
        f = open(dumpInfo['uri'].split('/')[-1], 'wb')
        f.write(body)
        f.close()
        return

    @deprecated
    def generate_backup(self, blocking=True, verbose=False):
        resp, body = self._con.do_http('POST', uri['backups'], None)
        if resp.status >= 400:
            raise HPOneViewException(body)
        taskuri = resp.getheader('Location')
        task = self._con.get(taskuri)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        backupResource = self._activity.get_task_associated_resource(task)
        backup = self._con.get(backupResource['resourceUri'])
        return backup

    @deprecated
    def download_backup(self, backup):
        body = self._con.get(backup['downloadUri'])
        f = open(backup['downloadUri'].split('/')[-1] + '.bkp', 'wb')
        f.write(body)
        f.close()
        return

    @deprecated
    def upload_backup(self, path, name, verbose=False, blocking=True):
        response, body = self._con.post_multipart(uri['archive'], '',
                                                  path, name, verbose)
        if response.status == 202 and verbose is True:
            print('Upload complete. Waiting for processing.')
        task, backup = self._activity.make_task_entity_tuple(body)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
        if verbose is True:
            print('Processing complete.')
        return backup

    @deprecated
    def restore_backup(self, backupUri):
        request = {
            'type': 'RESTORE',
            'uriOfBackupToRestore': backupUri}
        task, body = self._con.post(uri['restores'], request)
        return body

    @deprecated
    def get_backups(self):
        body = self._con.get(uri['backups'])
        return body

    @deprecated
    def get_restores(self):
        body = self._con.get(uri['restores'])
        return body

    @deprecated
    def get_dev_read_comm_string(self):
        body = self._con.get(uri['dev-read-community-str'])
        return body['communityString']

    @deprecated
    def set_dev_read_comm_string(self, communityString):
        request = {'communityString': communityString}
        task, body = self._con.put(uri['dev-read-community-str'], request)
        return body

    @deprecated
    def get_licenses(self):
        body = self._con.get(uri['licenses'])
        return get_members(body)

    @deprecated
    def add_license(self, licenseKey):
        request = {
            'key': licenseKey,
            'type': 'License'}
        task, body = self._con.post(uri['licenses'], request)
        return body

    @deprecated
    def factory_reset(self, mode='PRESERVE_NETWORK'):
        response = self._con.delete('/rest/appliance?mode=' + mode)
        return response

    @deprecated
    def get_node_status(self):
        body = self._con.get(uri['nodestatus'])
        return body

    @deprecated
    def get_node_version(self):
        body = self._con.get(uri['nodeversion'])
        return body

    @deprecated
    def shutdown(self, mode='HALT'):
        task, body = self._con.post('/rest/appliance/shutdown?type=' + mode,
                                    None)
        return body

    @deprecated
    def get_trap_destinations(self):
        body = self._con.get(uri['trap'])
        return body

    @deprecated
    def get_serviceaccess(self):
        body = self._con.get(uri['service'])
        return body

    @deprecated
    def set_service_access(self, serviceAccess):
        task, body = self._con.put(uri['serviceAccess'], serviceAccess)
        return body

    @deprecated
    def get_domains(self):
        body = self._con.get(uri['domains'])
        return body

    @deprecated
    def get_schema(self):
        body = self._con.get(uri['schema'])
        return body

    @deprecated
    def get_global_settings(self):
        body = self._con.get(uri['globalSettings'])
        return body

    @deprecated
    def get_storage_vol_template_policy(self):
        body = self._con.get(uri['vol-tmplate-policy'])
        return body

    @deprecated
    def get_startup_progress(self):
        body = self._con.get(uri['progress'])
        return body

    ###########################################################################
    # Appliance Network Interfaces
    ###########################################################################
    @deprecated
    def get_appliance_network_interfaces(self):
        return self._con.get(uri['applianceNetworkInterfaces'])

    @deprecated
    def set_appliance_network_interface(self, interfaceConfig):
        self._con.post(uri['applianceNetworkInterfaces'], interfaceConfig)
        return

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
