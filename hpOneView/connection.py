# -*- coding: utf-8 -*

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
import json
import logging
import shutil  # for shutil.copyfileobj()
import mmap  # so we can upload the iso without having to load it in memory
import os
import ssl
import time

from hpOneView.common import uri, get_members, get_member, make_eula_dict, make_initial_password_change_dict
from hpOneView.exceptions import HPOneViewException

logger = logging.getLogger(__name__)


class connection(object):
    def __init__(self, applianceIp, api_version=300):
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
        self._sslTrustedBundle = None
        self._sslTrustAll = True
        self._nextPage = None
        self._prevPage = None
        self._numTotalRecords = 0
        self._numDisplayedRecords = 0
        self._validateVersion = False

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
        self._sslTrustAll = False
        self._sslTrustedBundle = sslBundle

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
                                                   context=context)
            else:
                conn = http.client.HTTPSConnection(self._proxyHost,
                                                   self._proxyPort,
                                                   context=context)
                conn.set_tunnel(self._host, 443)
        else:
            context.verify_mode = ssl.CERT_NONE
            if self._doProxy is False:
                conn = http.client.HTTPSConnection(self._host,
                                                   context=context)
            else:
                conn = http.client.HTTPSConnection(self._proxyHost,
                                                   self._proxyPort,
                                                   context=context)
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

    def get_entities_byrange(self, uri, field, xmin, xmax, count=-1):
        new_uri = uri + '?filter="\'' + field + '\'%20>%20\'' + xmin \
                      + '\'"&filter="\'' + field + '\'%20<%20\'' + xmax \
                      + '\'"&start=0&count=' + str(count)
        body = self.get(new_uri)
        return get_members(body)

    def get_entities_byfield(self, uri, field, value, count=-1):
        new_uri = uri + '?start=0&count=' + str(count) \
                      + '&filter=' + field + '=\'' + value + '\''
        try:
            body = self.get(new_uri)
        except:
            print(new_uri)
            raise
        return get_members(body)

    def get_entity_byfield(self, uri, field, value, count=-1):
        new_uri = uri + '?filter="\'' + field + '\'%20=%20\'' + value \
                      + '\'"&start=0&count=' + str(count)

        try:
            body = self.get(new_uri)
        except:
            print(new_uri)
            raise
        return get_member(body)

    def conditional_post(self, uri, body):
        try:
            task, entity = self.post(uri, body)
        except HPOneViewException as e:
            # this may have failed because the entity already exists,
            # unfortunately there is not a uniform way to report this,
            # so we just try to find an existing entity with the same name
            # and return it assuming all names are unique (which is a
            # reasonable assumption)
            if 'DUPLICATE' in e.errorCode and 'NAME' in e.errorCode:
                try:
                    entity = self.get_entity_byfield(uri, 'name', body['name'])
                except Exception:
                    # Didn't find the entity, raise exception
                    raise e
                if not entity:
                    raise e
            else:
                raise e
        return entity

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
        if self._validateVersion is False:
            self.validateVersion()

        self._cred = cred
        try:
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
