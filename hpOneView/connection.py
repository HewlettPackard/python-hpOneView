# -*- coding: utf-8 -*
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

"""
connection.py
~~~~~~~~~~~~~~

This module maintains communication with the appliance.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import open
from builtins import str
from future import standard_library

standard_library.install_aliases()

import http.client
import json
import logging
import shutil  # for shutil.copyfileobj()
import mmap  # so we can upload the iso without having to load it in memory
import os
import ssl
import time
import traceback

from hpOneView.exceptions import HPOneViewException

logger = logging.getLogger(__name__)


class connection(object):
    def __init__(self, applianceIp, api_version=300, sslBundle=False, timeout=None):
        self._session = None
        self._host = applianceIp
        self._cred = None
        self._apiVersion = int(api_version)
        self._headers = {
            'X-API-Version': self._apiVersion,
            'Accept': 'application/json',
            'Content-Type': 'application/json'}
        self._proxyHost = None
        self._proxyPort = None
        self._doProxy = False
        self._sslTrustAll = True
        self._sslBundle = sslBundle
        self._sslTrustedBundle = self.set_trusted_ssl_bundle(sslBundle)
        self._nextPage = None
        self._prevPage = None
        self._numTotalRecords = 0
        self._numDisplayedRecords = 0
        self._validateVersion = False
        self._timeout = timeout

    def validateVersion(self):
        version = self.get(uri['version'])
        if 'minimumVersion' in version:
            if self._apiVersion < version['minimumVersion']:
                raise HPOneViewException('Unsupported API Version')
        if 'currentVersion' in version:
            if self._apiVersion > version['currentVersion']:
                raise HPOneViewException('Unsupported API Version')
        self._validateVersion = True

    def set_proxy(self, proxyHost, proxyPort):
        self._proxyHost = proxyHost
        self._proxyPort = proxyPort
        self._doProxy = True

    def set_trusted_ssl_bundle(self, sslBundle):
        if sslBundle:
            self._sslTrustAll = False
        return sslBundle

    def get_session(self):
        return self._session

    def get_session_id(self):
        return self._headers.get('auth')

    def set_session_id(self, session_id):
        self._headers['auth'] = session_id
        self._session = True

    def get_host(self):
        return self._host

    def get_by_uri(self, xuri):
        return self.get(xuri)

    def make_url(self, path):
        return 'https://%s%s' % (self._host, path)

    def do_http(self, method, path, body, custom_headers=None):
        http_headers = self._headers.copy()
        if custom_headers:
            http_headers.update(custom_headers)

        bConnected = False
        conn = None
        while bConnected is False:
            try:
                conn = self.get_connection()
                conn.request(method, path, body, http_headers)
                resp = conn.getresponse()
                tempbytes = ''
                try:
                    tempbytes = resp.read()
                    tempbody = tempbytes.decode('utf-8')
                except UnicodeDecodeError:  # Might be binary data
                    tempbody = tempbytes
                    conn.close()
                    bConnected = True
                    return resp, tempbody
                if tempbody:
                    try:
                        body = json.loads(tempbody)
                    except ValueError:
                        body = tempbody
                conn.close()
                bConnected = True
            except http.client.BadStatusLine:
                logger.warning('Bad Status Line. Trying again...')
                if conn:
                    conn.close()
                time.sleep(1)
                continue
            except http.client.HTTPException:
                raise HPOneViewException('Failure during login attempt.\n %s' % traceback.format_exc())

        return resp, body

    def download_to_stream(self, stream_writer, url, body='', method='GET', custom_headers=None):
        http_headers = self._headers.copy()
        if custom_headers:
            http_headers.update(custom_headers)

        chunk_size = 4096
        conn = None

        successful_connected = False
        while not successful_connected:
            try:
                conn = self.get_connection()
                conn.request(method, url, body, http_headers)
                resp = conn.getresponse()

                if resp.status >= 400:
                    self.__handle_download_error(resp, conn)

                tempbytes = True
                while tempbytes:
                    tempbytes = resp.read(chunk_size)
                    if tempbytes:  # filter out keep-alive new chunks
                        stream_writer.write(tempbytes)

                conn.close()
                successful_connected = True
            except http.client.BadStatusLine:
                logger.warning('Bad Status Line. Trying again...')
                if conn:
                    conn.close()
                time.sleep(1)
                continue
            except http.client.HTTPException:
                raise HPOneViewException('Failure during login attempt.\n %s' % traceback.format_exc())

        return successful_connected

    def __handle_download_error(self, resp, conn):
        try:
            tempbytes = resp.read()
            tempbody = tempbytes.decode('utf-8')
            try:
                body = json.loads(tempbody)
            except ValueError:
                body = tempbody
        except UnicodeDecodeError:  # Might be binary data
            body = tempbytes
            conn.close()
        if not body:
            body = "Error " + str(resp.status)

        conn.close()
        raise HPOneViewException(body)

    def get_connection(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        if self._sslTrustAll is False:
            context.verify_mode = ssl.CERT_REQUIRED
            context.load_verify_locations(self._sslTrustedBundle)
            if self._doProxy is False:
                conn = http.client.HTTPSConnection(self._host,
                                                   context=context,
                                                   timeout=self._timeout)
            else:
                conn = http.client.HTTPSConnection(self._proxyHost,
                                                   self._proxyPort,
                                                   context=context,
                                                   timeout=self._timeout)
                conn.set_tunnel(self._host, 443)
        else:
            context.verify_mode = ssl.CERT_NONE
            if self._doProxy is False:
                conn = http.client.HTTPSConnection(self._host,
                                                   context=context,
                                                   timeout=self._timeout)
            else:
                conn = http.client.HTTPSConnection(self._proxyHost,
                                                   self._proxyPort,
                                                   context=context,
                                                   timeout=self._timeout)
                conn.set_tunnel(self._host, 443)

        return conn

    def _open(self, name, mode):
        return open(name, mode)

    def encode_multipart_formdata(self, fields, files, baseName, verbose=False):
        """
        Fields is a sequence of (name, value) elements for regular form fields.
        Files is a sequence of (name, filename, value) elements for data
        to be uploaded as files

        Returns: (content_type, body) ready for httplib.HTTP instance
        """
        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = '\r\n'
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        if verbose is True:
            print(('Encoding ' + baseName + ' for upload...'))
        fin = self._open(files, 'rb')
        fout = self._open(files + '.b64', 'wb')
        fout.write(bytearray('--' + BOUNDARY + CRLF, 'utf-8'))
        fout.write(bytearray('Content-Disposition: form-data'
                             '; name="file"; filename="' +
                             baseName + '"' + CRLF, "utf-8"))
        fout.write(bytearray('Content-Type: application/octet-stream' + CRLF,
                             'utf-8'))
        fout.write(bytearray(CRLF, 'utf-8'))
        shutil.copyfileobj(fin, fout)
        fout.write(bytearray(CRLF, 'utf-8'))
        fout.write(bytearray('--' + BOUNDARY + '--' + CRLF, 'utf-8'))
        fout.write(bytearray(CRLF, 'utf-8'))
        fout.close()
        fin.close()
        return content_type

    def post_multipart_with_response_handling(self, uri, file_path, baseName):
        resp, body = self.post_multipart(uri, None, file_path, baseName)

        if resp.status == 202:
            task = self.__get_task_from_response(resp, body)
            return task, body

        if self.__body_content_is_task(body):
            return body, body

        return None, body

    def post_multipart(self, uri, fields, files, baseName, verbose=False):
        content_type = self.encode_multipart_formdata(fields, files, baseName,
                                                      verbose)
        inputfile = self._open(files + '.b64', 'rb')
        mappedfile = mmap.mmap(inputfile.fileno(), 0, access=mmap.ACCESS_READ)
        if verbose is True:
            print(('Uploading ' + files + '...'))
        conn = self.get_connection()
        # conn.set_debuglevel(1)
        conn.connect()
        conn.putrequest('POST', uri)
        conn.putheader('uploadfilename', baseName)
        conn.putheader('auth', self._headers['auth'])
        conn.putheader('Content-Type', content_type)
        totalSize = os.path.getsize(files + '.b64')
        conn.putheader('Content-Length', totalSize)
        conn.putheader('X-API-Version', self._apiVersion)
        conn.endheaders()

        while mappedfile.tell() < mappedfile.size():
            # Send 1MB at a time
            # NOTE: Be careful raising this value as the read chunk
            # is stored in RAM
            readSize = 1048576
            conn.send(mappedfile.read(readSize))
            if verbose is True:
                print('%d bytes sent... \r' % mappedfile.tell())
        mappedfile.close()
        inputfile.close()
        os.remove(files + '.b64')
        response = conn.getresponse()
        body = response.read().decode('utf-8')

        if body:
            try:
                body = json.loads(body)
            except ValueError:
                body = response.read().decode('utf-8')

        conn.close()

        if response.status >= 400:
            raise HPOneViewException(body)

        return response, body

    ###########################################################################
    # Utility functions for making requests - the HTTP verbs
    ###########################################################################
    def get(self, uri):
        resp, body = self.do_http('GET', uri, '')
        if resp.status >= 400:
            raise HPOneViewException(body)
        if resp.status == 302:
            body = self.get(resp.getheader('Location'))
        if type(body) is dict:
            if 'nextPageUri' in body:
                self._nextPage = body['nextPageUri']
            if 'prevPageUri' in body:
                self._prevPage = body['prevPageUri']
            if 'total' in body:
                self._numTotalRecords = body['total']
            if 'count' in body:
                self._numDisplayedRecords = body['count']
        return body

    def getNextPage(self):
        body = self.get(self._nextPage)
        return get_members(body)

    def getPrevPage(self):
        body = self.get(self._prevPage)
        return get_members(body)

    def getLastPage(self):
        while self._nextPage is not None:
            members = self.getNextPage()
        return members

    def getFirstPage(self):
        while self._prevPage is not None:
            members = self.getPrevPage()
        return members

    def delete(self, uri, custom_headers=None):
        return self.__do_rest_call('DELETE', uri, {}, custom_headers=custom_headers)

    def put(self, uri, body, custom_headers=None):
        return self.__do_rest_call('PUT', uri, body, custom_headers=custom_headers)

    def post(self, uri, body, custom_headers=None):
        return self.__do_rest_call('POST', uri, body, custom_headers=custom_headers)

    def patch(self, uri, body, custom_headers=None):
        return self.__do_rest_call('PATCH', uri, body, custom_headers=custom_headers)

    def __body_content_is_task(self, body):
        return isinstance(body, dict) and 'category' in body and body['category'] == 'tasks'

    def __get_task_from_response(self, response, body):
        location = response.getheader('Location')
        if location:
            task = self.get(location)
        elif 'taskState' in body:
            # This check is needed to handle a status response 202 without the location header,
            # as is for PowerDevices. We are not sure if there are more resources with the same behavior.
            task = body
        else:
            # For the resource Label the status is 202 but the response not contains a task.
            task = None
        return task

    def __do_rest_call(self, http_method, uri, body, custom_headers):
        resp, body = self.do_http(method=http_method,
                                  path=uri,
                                  body=json.dumps(body),
                                  custom_headers=custom_headers)
        if resp.status >= 400:
            raise HPOneViewException(body)

        if resp.status == 304:
            if body and not isinstance(body, dict):
                try:
                    body = json.loads(body)
                except Exception:
                    pass
        elif resp.status == 202:
            task = self.__get_task_from_response(resp, body)
            return task, body

        if self.__body_content_is_task(body):
            return body, body

        return None, body

    ###########################################################################
    # EULA
    ###########################################################################
    def get_eula_status(self):
        return self.get(uri['eulaStatus'])

    def set_eula(self, supportAccess='yes'):
        eula = make_eula_dict(supportAccess)
        self.post(uri['eulaSave'], eula)
        return

    ###########################################################################
    # Initial Setup
    ###########################################################################
    def change_initial_password(self, newPassword):
        password = make_initial_password_change_dict('Administrator',
                                                     'admin', newPassword)
        # This will throw an exception if the password is already changed
        self.post(uri['changePassword'], password)

    ###########################################################################
    # Login/Logout to/from appliance
    ###########################################################################
    def login(self, cred, verbose=False):
        try:
            if self._validateVersion is False:
                self.validateVersion()
        except Exception:
            raise(HPOneViewException('Failure during login attempt.\n %s' % traceback.format_exc()))

        self._cred = cred
        try:
            if self._cred.get("sessionID"):
                self.set_session_id(self._cred["sessionID"])
                task, body = self.put(uri['loginSessions'], None)
            else:
                self._cred.pop("sessionID", None)
                task, body = self.post(uri['loginSessions'], self._cred)
        except HPOneViewException:
            logger.exception('Login failed')
            raise
        auth = body['sessionID']
        # Add the auth ID to the headers dictionary
        self._headers['auth'] = auth
        self._session = True
        if verbose is True:
            print(('Session Key: ' + auth))
        logger.info('Logged in successfully')

    def logout(self, verbose=False):
        # resp, body = self.do_http(method, uri['loginSessions'] \
        #                        , body, self._headers)
        try:
            self.delete(uri['loginSessions'])
        except HPOneViewException:
            logger.exception('Logout failed')
            raise
        if verbose is True:
            print('Logged Out')
        del self._headers['auth']
        self._session = False
        logger.info('Logged out successfully')
        return None

    def enable_etag_validation(self):
        """
        Enable the concurrency control for the PUT and DELETE requests, in which the requests are conditionally
        processed only if the provided entity tag in the body matches the latest entity tag stored for the resource.

        The eTag validation is enabled by default.
        """
        self._headers.pop('If-Match', None)

    def disable_etag_validation(self):
        """
        Disable the concurrency control for the PUT and DELETE requests. The requests will be forced without specifying
        an explicit ETag. This method sets an If-Match header of "*".
        """
        self._headers['If-Match'] = '*'


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


def make_eula_dict(supportAccess):
    return {'supportAccess': supportAccess}


def make_initial_password_change_dict(userName, oldPassword, newPassword):
    return {
        'userName': userName,
        'oldPassword': oldPassword,
        'newPassword': newPassword}
