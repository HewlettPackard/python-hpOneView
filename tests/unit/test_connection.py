# -*- coding: utf-8 -*-
###
# (C) Copyright (2016-2017) Hewlett Packard Enterprise Development LP
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
import json
import ssl
import unittest
import mmap
import os
import shutil
import os.path

from mock import patch, call, Mock, ANY
from http.client import HTTPSConnection, BadStatusLine, HTTPException
from hpOneView.connection import connection
from hpOneView.exceptions import HPOneViewException


class ConnectionTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self.accept_language_header = {
            'Accept-Language': 'en_US'
        }
        self.default_headers = {
            'X-API-Version': 300,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.default_headers_with_etag_validation_off = {
            'X-API-Version': 300,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'If-Match': '*'
        }
        self.merged_headers = {
            'X-API-Version': 300,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Accept-Language': 'en_US'
        }
        self.request_body = {"request body": "content"}
        self.response_body = {"response body": "content",
                              "message": "An error occurred."}
        self.dumped_request_body = json.dumps(self.request_body.copy())
        self.expected_response_body = self.response_body.copy()

    def __make_http_response(self, status):
        mock_response = Mock(status=status)
        mock_response.read.return_value = json.dumps(self.response_body).encode('utf-8')
        if status == 200 or status == 202:
            mock_response.getheader.return_value = '/task/uri'
        return mock_response

    def __create_fake_mapped_file(self):
        mock_mapped_file = Mock()
        mock_mapped_file.tell.side_effect = [0, 1048576, 2097152, 2621440]  # 0, 1MB, 2MB 2.5MB
        mock_mapped_file.size.return_value = 2621440  # 2.5MB
        mock_mapped_file.read.side_effect = ['data chunck 1', 'data chunck 2', 'data chunck 3']
        return mock_mapped_file

    def __prepare_connection_to_post_multipart(self, response_status=200):
        fake_connection = Mock()
        fake_connection.getresponse.return_value.read.return_value = json.dumps(self.response_body).encode('utf-8')
        fake_connection.getresponse.return_value.status = response_status

        self.connection.get_connection = Mock()
        self.connection.get_connection.return_value = fake_connection

        self.connection._open = Mock()

        self.connection._headers['auth'] = 'LTIxNjUzMjc0OTUzzHoF7eEkZLEUWVA-fuOZP4VGA3U8e67E'

        encode_multipart = "multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY_$"
        self.connection.encode_multipart_formdata = Mock()
        self.connection.encode_multipart_formdata.return_value = encode_multipart

    def test_default_headers(self):
        self.assertEqual(self.default_headers, self.connection._headers)

    def test_default_headers_when_etag_validation_is_disabled(self):
        self.connection.disable_etag_validation()
        self.assertEqual(self.default_headers_with_etag_validation_off, self.connection._headers)

    def test_default_headers_when_etag_validation_is_enabled(self):
        self.connection.enable_etag_validation()
        self.assertEqual(self.default_headers, self.connection._headers)

    def test_default_headers_when_etag_validation_is_disabled_and_enabled(self):
        self.connection.disable_etag_validation()
        self.connection.enable_etag_validation()
        self.assertEqual(self.default_headers, self.connection._headers)

    def test_default_headers_when_etag_validation_is_enabled_and_disabled(self):
        self.connection.enable_etag_validation()
        self.connection.disable_etag_validation()
        self.assertEqual(self.default_headers_with_etag_validation_off, self.connection._headers)

    def test_headers_with_api_version_300(self):
        self.connection = connection(self.host, 300)

        expected_headers = self.default_headers.copy()
        expected_headers['X-API-Version'] = 300
        self.assertEqual(expected_headers, self.connection._headers)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_post_when_status_is_202_and_task_contains_taskState(self, mock_response, mock_request):
        mock_request.return_value = {}

        fake_task = {"taskState": "Completed"}

        response = Mock(status=202)
        response.read.return_value = json.dumps(fake_task).encode('utf-8')
        response.getheader.return_value = ''
        mock_response.return_value = response

        task, body = self.connection.post('/path', self.request_body)

        self.assertEqual(task, fake_task)
        self.assertEqual(body, fake_task)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_post_when_status_is_202_and_response_is_not_a_task(self, mock_response, mock_request):
        mock_request.return_value = {}

        response = Mock(status=202)
        response.read.return_value = json.dumps(self.response_body).encode('utf-8')
        response.getheader.return_value = ''
        mock_response.return_value = response

        task, body = self.connection.post('/path', self.request_body)

        self.assertEqual(task, None)
        self.assertEqual(body, self.response_body)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_post_should_do_rest_call_when_status_ok(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=200)

        self.connection.post('/path', self.request_body)

        mock_request.assert_called_once_with('POST', '/path', self.dumped_request_body, self.default_headers)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_post_should_do_rest_calls_when_status_accepted(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=202)

        self.connection.post('/path', self.request_body)

        expected_calls = [call('POST', '/path', self.dumped_request_body, self.default_headers),
                          call('GET', '/task/uri', '', self.default_headers)]
        self.assertEqual(expected_calls, mock_request.call_args_list)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_post_should_send_merged_headers_when_headers_provided(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=202)

        self.connection.post('/path', self.request_body, custom_headers=self.accept_language_header)

        expected_calls = [call('POST', ANY, ANY, self.merged_headers), ANY]
        self.assertEqual(expected_calls, mock_request.call_args_list)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_post_should_return_body_when_status_ok(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=200)

        result = self.connection.post('/path', self.response_body, custom_headers=self.accept_language_header)

        expected_result = (None, self.expected_response_body)
        self.assertEqual(expected_result, result)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_post_should_return_tuple_when_status_accepted(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=202)

        result = self.connection.post('/path', self.response_body, custom_headers=self.accept_language_header)

        expected_result = (self.expected_response_body, self.expected_response_body)
        self.assertEqual(result, expected_result)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_post_should_raise_exception_when_status_internal_error(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=400)

        try:
            self.connection.post('/path', self.request_body)
        except HPOneViewException as e:
            self.assertEqual(e.oneview_response, self.expected_response_body)
        else:
            self.fail()

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_post_should_raise_exception_when_status_not_found(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=404)

        try:
            self.connection.post('/path', self.request_body)
        except HPOneViewException as e:
            self.assertEqual(e.oneview_response, self.expected_response_body)
        else:
            self.fail()

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_put_should_do_rest_call_when_status_ok(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=200)

        self.connection.put('/path', self.request_body)

        mock_request.assert_called_once_with('PUT', '/path', self.dumped_request_body, self.default_headers)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_put_should_do_rest_calls_when_status_accepted(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=202)

        self.connection.put('/path', self.request_body)

        expected_calls = [call('PUT', '/path', self.dumped_request_body, self.default_headers),
                          call('GET', '/task/uri', '', self.default_headers)]
        self.assertEqual(expected_calls, mock_request.call_args_list)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_put_should_send_merged_headers_when_headers_provided(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=202)

        self.connection.put('/path', self.request_body, custom_headers=self.accept_language_header)

        expected_calls = [call('PUT', ANY, ANY, self.merged_headers), ANY]
        self.assertEqual(expected_calls, mock_request.call_args_list)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_put_should_return_body_when_status_ok(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=200)

        result = self.connection.put('/path', self.response_body, custom_headers=self.accept_language_header)

        expected_result = (None, self.expected_response_body)
        self.assertEqual(result, expected_result)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_put_should_return_tuple_when_status_accepted(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=202)

        result = self.connection.put('/path', self.response_body, custom_headers=self.accept_language_header)

        expected_result = (self.expected_response_body, self.expected_response_body)
        self.assertEqual(result, expected_result)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_put_should_raise_exception_when_status_internal_error(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=400)

        try:
            self.connection.put('/path', self.request_body)
        except HPOneViewException as e:
            self.assertEqual(e.oneview_response, self.expected_response_body)
        else:
            self.fail()

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_put_should_raise_exception_when_status_not_found(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=404)

        try:
            self.connection.put('/path', self.request_body)
        except HPOneViewException as e:
            self.assertEqual(e.oneview_response, self.expected_response_body)
        else:
            self.fail()

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_patch_should_do_rest_call_when_status_ok(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=200)

        self.connection.patch('/path', self.request_body)

        mock_request.assert_called_once_with('PATCH', '/path', self.dumped_request_body, self.default_headers)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_patch_should_do_rest_calls_when_status_accepted(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=202)

        self.connection.patch('/path', self.request_body)

        expected_calls = [call('PATCH', '/path', self.dumped_request_body, self.default_headers),
                          call('GET', '/task/uri', '', self.default_headers)]
        self.assertEqual(expected_calls, mock_request.call_args_list)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_patch_should_send_merged_headers_when_headers_provided(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=202)

        self.connection.patch('/path', self.request_body, custom_headers=self.accept_language_header)

        expected_calls = [call('PATCH', ANY, ANY, self.merged_headers), ANY]
        self.assertEqual(expected_calls, mock_request.call_args_list)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_patch_should_return_body_when_status_ok(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=200)

        result = self.connection.patch('/path', self.response_body, custom_headers=self.accept_language_header)

        expected_result = (None, self.expected_response_body)
        self.assertEqual(result, expected_result)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_patch_should_return_tuple_when_status_accepted(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=202)

        result = self.connection.patch('/path', self.response_body, custom_headers=self.accept_language_header)

        expected_result = (self.expected_response_body, self.expected_response_body)
        self.assertEqual(result, expected_result)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_patch_should_raise_exception_when_status_internal_error(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=400)

        try:
            self.connection.patch('/path', self.request_body)
        except HPOneViewException as e:
            self.assertEqual(e.oneview_response, self.expected_response_body)
        else:
            self.fail()

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_patch_should_raise_exception_when_status_not_found(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=404)

        try:
            self.connection.patch('/path', self.request_body)
        except HPOneViewException as e:
            self.assertEqual(e.oneview_response, self.expected_response_body)
        else:
            self.fail()

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_delete_should_do_rest_calls_when_status_ok(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=200)

        self.connection.delete('/path')

        mock_request.assert_called_once_with('DELETE', '/path', json.dumps({}), self.default_headers)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_delete_should_do_rest_calls_when_status_accepted(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=202)

        self.connection.delete('/path')

        expected_calls = [call('DELETE', '/path', json.dumps({}), self.default_headers),
                          call('GET', '/task/uri', '', self.default_headers)]
        self.assertEqual(expected_calls, mock_request.call_args_list)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_delete_should_send_merged_headers_when_headers_provided(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=202)

        self.connection.delete('/path', custom_headers=self.accept_language_header)

        expected_calls = [call('DELETE', ANY, ANY, self.merged_headers), ANY]
        self.assertEqual(expected_calls, mock_request.call_args_list)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_delete_should_return_body_when_status_ok(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=200)

        result = self.connection.delete('/path', custom_headers=self.accept_language_header)

        expected_result = (None, self.expected_response_body)
        self.assertEqual(result, expected_result)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_delete_should_return_tuple_when_status_accepted(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=202)

        result = self.connection.delete('/path', custom_headers=self.accept_language_header)

        expected_result = (self.expected_response_body, self.expected_response_body)
        self.assertEqual(result, expected_result)

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_delete_should_raise_exception_when_status_internal_error(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=400)

        try:
            self.connection.delete('/path')
        except HPOneViewException as e:
            self.assertEqual(e.oneview_response, self.expected_response_body)
        else:
            self.fail()

    @patch.object(HTTPSConnection, 'request')
    @patch.object(HTTPSConnection, 'getresponse')
    def test_delete_should_raise_exception_when_status_not_found(self, mock_response, mock_request):
        mock_request.return_value = {}
        mock_response.return_value = self.__make_http_response(status=404)

        try:
            self.connection.delete('/path', self.request_body)
        except HPOneViewException as e:
            self.assertEqual(e.oneview_response, self.expected_response_body)
        else:
            self.fail()

    @patch.object(connection, 'do_http')
    def test_task_in_response_body_without_202_status(self, mock_do_http):

        # create the return values
        mockedResponse = type('mockResponse', (), {'status': 200})()
        mockedTaskBody = {'category': 'tasks'}

        # set-up the mock
        mock_do_http.return_value = (mockedResponse, mockedTaskBody)

        # call the method we are testing
        (testTask, testBody) = self.connection._connection__do_rest_call('PUT', '/rest/test', '{ "body": "test" }',
                                                                         None)

        # verify the result
        self.assertEqual(mockedTaskBody, testTask)
        self.assertEqual(mockedTaskBody, testBody)

    @patch.object(connection, 'do_http')
    def test_do_rest_call_with_304_status(self, mock_do_http):

        mockedResponse = type('mockResponse', (), {'status': 304})()

        mock_do_http.return_value = (mockedResponse, '{ "body": "test" }')

        (testTask, testBody) = self.connection._connection__do_rest_call('PUT',
                                                                         '/rest/test',
                                                                         '{ "body": "test" }',
                                                                         None)

        self.assertIsNone(testTask)
        self.assertEqual(testBody, {"body": "test"})

    @patch.object(connection, 'do_http')
    def test_do_rest_call_with_304_status_and_invalid_json(self, mock_do_http):

        mockedResponse = type('mockResponse', (), {'status': 304})()

        mock_do_http.return_value = (mockedResponse, 111)

        (testTask, testBody) = self.connection._connection__do_rest_call('PUT',
                                                                         '/rest/test',
                                                                         111,
                                                                         None)

        self.assertIsNone(testTask)
        self.assertEqual(testBody, 111)

    @patch('time.sleep')
    @patch.object(connection, 'get_connection')
    def test_download_to_stream_when_status_ok(self, mock_get_conn, mock_sleep):

        mock_conn = Mock()
        # First attempt: Error, second attempt: successful connection
        mock_get_conn.side_effect = [BadStatusLine(0), mock_conn]

        mock_response = mock_conn.getresponse.return_value
        # Stops at the fourth read call
        mock_response.read.side_effect = ['111', '222', '333', None]
        mock_response.status = 200

        mock_stream = Mock()

        result = self.connection.download_to_stream(mock_stream, '/rest/download.zip')

        self.assertTrue(result)
        mock_stream.write.assert_has_calls([call('111'), call('222'), call('333')])

    @patch('time.sleep')
    @patch.object(connection, 'get_connection')
    def test_download_to_stream_when_error_status_with_response_body(self, mock_get_conn, mock_sleep):
        mock_conn = Mock()
        mock_get_conn.return_value = mock_conn

        mock_response = mock_conn.getresponse.return_value
        mock_response.read.return_value = json.dumps('error message').encode('utf-8')
        mock_response.status = 500

        mock_stream = Mock()

        try:
            self.connection.download_to_stream(mock_stream, '/rest/download.zip')
        except HPOneViewException as e:
            self.assertEqual(e.msg, 'error message')
        else:
            self.fail()

    @patch('time.sleep')
    @patch.object(connection, 'get_connection')
    def test_download_to_stream_when_error_status_with_decode_error(self, mock_get_conn, mock_sleep):
        mock_conn = Mock()
        mock_get_conn.return_value = mock_conn

        mock_response = mock_conn.getresponse.return_value
        mock_response.read.return_value = json.dumps('error message').encode('utf-8')
        mock_response.read.decode.side_effect = UnicodeDecodeError('sn33af', b"", 42, 43, 'ths239sn')
        mock_response.status = 500

        mock_stream = Mock()

        try:
            self.connection.download_to_stream(mock_stream, '/rest/download.zip')
        except HPOneViewException as e:
            self.assertEqual(e.msg, 'error message')
        else:
            self.fail()

    @patch('time.sleep')
    @patch.object(connection, 'get_connection')
    def test_download_to_stream_when_error_status_with_empty_body(self, mock_get_conn, mock_sleep):
        mock_conn = Mock()
        mock_get_conn.return_value = mock_conn

        mock_response = mock_conn.getresponse.return_value
        mock_response.read.return_value = json.dumps('').encode('utf-8')
        mock_response.status = 500

        mock_stream = Mock()

        try:
            self.connection.download_to_stream(mock_stream, '/rest/download.zip')
        except HPOneViewException as e:
            self.assertEqual(e.msg, 'Error 500')
        else:
            self.fail()

    @patch.object(connection, 'get_connection')
    def test_download_to_stream_with_timeout_error(self, mock_get_connection):

        mock_conn = mock_get_connection.return_value = Mock()
        mock_response = Mock()
        mock_conn.getresponse.side_effect = [HTTPException('timed out'), mock_response]

        mock_stream = Mock()

        with self.assertRaises(HPOneViewException) as context:
            resp, body = self.connection.download_to_stream(mock_stream, '/rest/download.zip')

        self.assertTrue('timed out' in context.exception.msg)

    @patch.object(mmap, 'mmap')
    @patch.object(shutil, 'copyfileobj')
    @patch.object(os.path, 'getsize')
    @patch.object(os, 'remove')
    def test_post_multipart_should_put_request(self, mock_rm, mock_path_size, mock_copy, mock_mmap):
        self.__prepare_connection_to_post_multipart()
        mock_mmap.return_value = self.__create_fake_mapped_file()

        self.connection.post_multipart(uri='/rest/resources/',
                                       fields=None,
                                       files="/a/path/filename.zip",
                                       baseName="archive.zip")

        internal_conn = self.connection.get_connection.return_value
        internal_conn.putrequest.assert_called_once_with('POST', '/rest/resources/')

    @patch.object(mmap, 'mmap')
    @patch.object(shutil, 'copyfileobj')
    @patch.object(os.path, 'getsize')
    @patch.object(os, 'remove')
    def test_post_multipart_should_put_headers(self, mock_rm, mock_path_size, mock_copy, mock_mmap):
        self.__prepare_connection_to_post_multipart()
        mock_mmap.return_value = self.__create_fake_mapped_file()
        mock_path_size.return_value = 2621440  # 2.5 MB

        self.connection.post_multipart(uri='/rest/resources/',
                                       fields=None,
                                       files="/a/path/filename.zip",
                                       baseName="archive.zip")

        expected_putheader_calls = [
            call('uploadfilename', 'archive.zip'),
            call('auth', 'LTIxNjUzMjc0OTUzzHoF7eEkZLEUWVA-fuOZP4VGA3U8e67E'),
            call('Content-Type', 'multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY_$'),
            call('Content-Length', 2621440),
            call('X-API-Version', 300)]

        internal_conn = self.connection.get_connection.return_value
        internal_conn.putheader.assert_has_calls(expected_putheader_calls)

    @patch.object(mmap, 'mmap')
    @patch.object(shutil, 'copyfileobj')
    @patch.object(os.path, 'getsize')
    @patch.object(os, 'remove')
    def test_post_multipart_should_read_file_in_chunks_of_1mb(self, mock_rm, mock_path_size, mock_copy, mock_mmap):
        self.__prepare_connection_to_post_multipart()
        mock_mmap.return_value = self.__create_fake_mapped_file()

        self.connection.post_multipart(uri='/rest/resources/',
                                       fields=None,
                                       files="/a/path/filename.zip",
                                       baseName="archive.zip")

        expected_mmap_read_calls = [
            call(1048576),
            call(1048576),
            call(1048576)]

        mock_mmap.return_value.read.assert_has_calls(expected_mmap_read_calls)

    @patch.object(mmap, 'mmap')
    @patch.object(shutil, 'copyfileobj')
    @patch.object(os.path, 'getsize')
    @patch.object(os, 'remove')
    def test_post_multipart_should_send_file_in_chuncks_of_1mb(self, mock_rm, mock_path_size, mock_copy, mock_mmap):
        self.__prepare_connection_to_post_multipart()
        mock_mmap.return_value = self.__create_fake_mapped_file()

        self.connection.post_multipart(uri='/rest/resources/',
                                       fields=None,
                                       files="/a/path/filename.zip",
                                       baseName="archive.zip")

        expected_conn_send_calls = [
            call('data chunck 1'),
            call('data chunck 2'),
            call('data chunck 3')]

        internal_conn = self.connection.get_connection.return_value
        internal_conn.send.assert_has_calls(expected_conn_send_calls)

    @patch.object(mmap, 'mmap')
    @patch.object(shutil, 'copyfileobj')
    @patch.object(os.path, 'getsize')
    @patch.object(os, 'remove')
    def test_post_multipart_should_remove_temp_encoded_file(self, mock_rm, mock_path_size, mock_copy, mock_mmap):
        self.__prepare_connection_to_post_multipart()
        mock_mmap.return_value = self.__create_fake_mapped_file()

        self.connection.post_multipart(uri='/rest/resources/',
                                       fields=None,
                                       files="/a/path/filename.zip",
                                       baseName="archive.zip")

        mock_rm.assert_called_once_with('/a/path/filename.zip.b64')

    @patch.object(mmap, 'mmap')
    @patch.object(shutil, 'copyfileobj')
    @patch.object(os.path, 'getsize')
    @patch.object(os, 'remove')
    def test_post_multipart_should_raise_exception_when_response_status_400(self, mock_rm, mock_path_size, mock_copy,
                                                                            mock_mmap):
        self.__prepare_connection_to_post_multipart(response_status=400)
        mock_mmap.return_value = self.__create_fake_mapped_file()

        try:
            self.connection.post_multipart(uri='/rest/resources/',
                                           fields=None,
                                           files="/a/path/filename.zip",
                                           baseName="archive.zip")
        except HPOneViewException as e:
            self.assertEqual(e.msg, "An error occurred.")
        else:
            self.fail()

    @patch.object(mmap, 'mmap')
    @patch.object(shutil, 'copyfileobj')
    @patch.object(os.path, 'getsize')
    @patch.object(os, 'remove')
    def test_post_multipart_should_return_response_and_body_when_response_status_200(self, mock_rm, mock_path_size,
                                                                                     mock_copy, mock_mmap):
        self.__prepare_connection_to_post_multipart()
        mock_mmap.return_value = self.__create_fake_mapped_file()

        response, body = self.connection.post_multipart(uri='/rest/resources/',
                                                        fields=None,
                                                        files="/a/path/filename.zip",
                                                        baseName="archive.zip")

        self.assertEqual(body, self.expected_response_body)
        self.assertEqual(response.status, 200)

    @patch.object(mmap, 'mmap')
    @patch.object(shutil, 'copyfileobj')
    @patch.object(os.path, 'getsize')
    @patch.object(os, 'remove')
    @patch.object(json, 'loads')
    def test_post_multipart_should_handle_json_load_exception(self, mock_json_loads, mock_rm, mock_path_size, mock_copy,
                                                              mock_mmap):
        self.__prepare_connection_to_post_multipart()
        mock_mmap.return_value = self.__create_fake_mapped_file()
        mock_json_loads.side_effect = ValueError("Invalid JSON")

        response, body = self.connection.post_multipart(uri='/rest/resources/',
                                                        fields=None,
                                                        files="/a/path/filename.zip",
                                                        baseName="archive.zip")

        self.assertTrue(body)
        self.assertEqual(response.status, 200)

    @patch.object(connection, 'post_multipart')
    def test_post_multipart_with_response_handling_when_status_202_without_task(self, mock_post_multipart):
        mock_response = Mock(status=202)
        mock_response.getheader.return_value = None
        mock_post_multipart.return_value = mock_response, "content"

        task, body = self.connection.post_multipart_with_response_handling("uri", "filepath", "basename")

        self.assertFalse(task)
        self.assertEqual(body, "content")

    @patch.object(connection, 'post_multipart')
    @patch.object(connection, 'get')
    def test_post_multipart_with_response_handling_when_status_202_with_task(self, mock_get, mock_post_multipart):
        fake_task = {"category": "tasks"}
        mock_response = Mock(status=202)
        mock_response.getheader.return_value = "/rest/tasks/taskid"
        mock_post_multipart.return_value = mock_response, "content"
        mock_get.return_value = fake_task

        task, body = self.connection.post_multipart_with_response_handling("uri", "filepath", "basename")

        self.assertEqual(task, fake_task)
        self.assertEqual(body, "content")

    @patch.object(connection, 'post_multipart')
    def test_post_multipart_with_response_handling_when_status_200_and_body_is_task(self, mock_post_multipart):
        fake_task = {"category": "tasks"}
        mock_post_multipart.return_value = Mock(status=200), fake_task

        task, body = self.connection.post_multipart_with_response_handling("uri", "filepath", "basename")

        self.assertEqual(task, fake_task)
        self.assertEqual(body, fake_task)

    @patch.object(connection, 'post_multipart')
    def test_post_multipart_with_response_handling_when_status_200_and_body_is_not_task(self, mock_post_multipart):
        mock_post_multipart.return_value = Mock(status=200), "content"

        task, body = self.connection.post_multipart_with_response_handling("uri", "filepath", "basename")

        self.assertFalse(task)
        self.assertEqual(body, "content")

    @patch.object(connection, 'get_connection')
    def test_do_http_with_invalid_unicode(self, mock_get_connection):

        mock_conn = mock_get_connection.return_value = Mock()
        mock_conn.getresponse.return_value = Mock()
        mock_conn.getresponse.return_value.read.side_effect = UnicodeDecodeError("utf8", b"response", 0, 4, "reason")

        _, body = self.connection.do_http('POST', '/rest/test', 'body')

        self.assertEqual(body, '')

        mock_conn.request.assert_called_once_with('POST', '/rest/test', 'body',
                                                  {'Content-Type': 'application/json',
                                                   'X-API-Version': 300, 'Accept': 'application/json'})

        mock_conn.close.assert_called_once()

    @patch.object(connection, 'get_connection')
    def test_do_http_with_invalid_json_return(self, mock_get_connection):

        mock_conn = mock_get_connection.return_value = Mock()
        mock_conn.getresponse.return_value = Mock()
        mock_conn.getresponse.return_value.read.return_value = b"response data"

        resp, body = self.connection.do_http('POST', '/rest/test', 'body')

        self.assertEqual(body, 'response data')

        mock_conn.request.assert_called_once_with('POST', '/rest/test', 'body',
                                                  {'Content-Type': 'application/json',
                                                   'X-API-Version': 300, 'Accept': 'application/json'})

        mock_conn.close.assert_called_once()

    @patch.object(connection, 'get_connection')
    def test_do_http_with_bad_status_line(self, mock_get_connection):

        mock_conn = mock_get_connection.return_value = Mock()

        # First attempt: Error, second attempt: successful response
        mock_response = Mock()
        mock_conn.getresponse.side_effect = [BadStatusLine(0), mock_response]

        # Stops at the fourth read call
        mock_response.read.return_value = b"response data"
        mock_response.status = 200

        with patch('time.sleep'):
            resp, body = self.connection.do_http('POST', '/rest/test', 'body')

        self.assertEqual(body, 'response data')

        mock_conn.request.assert_called_with('POST', '/rest/test', 'body',
                                             {'Content-Type': 'application/json',
                                              'X-API-Version': 300,
                                              'Accept': 'application/json'})

        mock_conn.close.assert_has_calls([call(), call()])

    @patch.object(connection, 'get_connection')
    def test_do_http_with_timeout_error(self, mock_get_connection):

        mock_conn = mock_get_connection.return_value = Mock()
        mock_response = Mock()
        mock_conn.getresponse.side_effect = [HTTPException('timed out'), mock_response]

        with self.assertRaises(HPOneViewException) as context:
            resp, body = self.connection.do_http('POST', '/rest/test', 'body')

        self.assertTrue('timed out' in context.exception.msg)

    @patch.object(connection, 'get')
    @patch.object(connection, 'post')
    def test_login(self, mock_post, mock_get):
        mock_get.side_effect = [{'minimumVersion': 300, 'currentVersion': 400}]
        mock_post.return_value = {'cat': 'task'}, {'sessionID': '123'}

        self.connection.login({})

        self.assertEqual(self.connection.get_session_id(), '123')
        self.assertEqual(self.connection.get_session(), True)

    @patch.object(connection, 'get')
    def test_login_catches_exceptions_as_hpOneView(self, mock_get):
        mock_get.side_effect = [Exception('test')]

        with self.assertRaises(HPOneViewException):
            self.connection.login({})

    @patch.object(connection, 'get')
    @patch.object(connection, 'post')
    def test_login_with_exception_in_post(self, mock_post, mock_get):
        mock_get.side_effect = [{'minimumVersion': 300, 'currentVersion': 400}]
        mock_post.side_effect = HPOneViewException("Failed")

        self.assertRaises(HPOneViewException, self.connection.login, {})

    @patch.object(connection, 'get')
    @patch.object(connection, 'put')
    def test_login_sessionID(self, mock_put, mock_get):
        mock_get.side_effect = [{'minimumVersion': 300, 'currentVersion': 400}]
        mock_put.return_value = {'cat': 'task'}, {'sessionID': '123'}

        self.connection.login({"sessionID": "123"})

        self.assertEqual(self.connection.get_session_id(), '123')
        self.assertEqual(self.connection.get_session(), True)

    @patch.object(connection, 'get')
    @patch.object(connection, 'put')
    def test_login_username_password_sessionID(self, mock_put, mock_get):
        mock_get.side_effect = [{'minimumVersion': 300, 'currentVersion': 400}]
        mock_put.return_value = {'cat': 'task'}, {'sessionID': '123'}

        self.connection.login({"userName": "administrator", "password": "", "sessionID": "123"})

        self.assertEqual(self.connection.get_session_id(), '123')
        self.assertEqual(self.connection.get_session(), True)

    @patch.object(connection, 'get')
    @patch.object(connection, 'put')
    def test_login_with_exception_in_put(self, mock_put, mock_get):
        mock_get.side_effect = [{'minimumVersion': 300, 'currentVersion': 400}]
        mock_put.side_effect = HPOneViewException("Failed")

        self.assertRaises(HPOneViewException, self.connection.login, {"sessionID": "123"})

    @patch.object(connection, 'get')
    @patch.object(connection, 'put')
    def test_login_with_exception_in_put_username_password_sessionID(self, mock_put, mock_get):
        mock_get.side_effect = [{'minimumVersion': 300, 'currentVersion': 400}]
        mock_put.side_effect = HPOneViewException("Failed")

        self.assertRaises(HPOneViewException, self.connection.login, {"userName": "administrator", "password": "", "sessionID": "123"})

    @patch.object(connection, 'get')
    def test_validate_version_exceeding_minimum(self, mock_get):
        self.connection._apiVersion = 300
        mock_get.side_effect = [{'minimumVersion': 400, 'currentVersion': 400}]

        self.assertRaises(HPOneViewException, self.connection.validateVersion)

    @patch.object(connection, 'get')
    def test_validate_version_exceeding_current(self, mock_get):
        self.connection._apiVersion = 400
        mock_get.side_effect = [{'minimumVersion': 200, 'currentVersion': 300}]

        self.assertRaises(HPOneViewException, self.connection.validateVersion)

    @patch.object(shutil, 'copyfileobj')
    @patch.object(connection, '_open')
    def test_encode_multipart_formdata(self, mock_open, mock_copyfileobj):
        mock_in = Mock()
        mock_out = Mock()

        mock_open.side_effect = [mock_in, mock_out]

        self.connection.encode_multipart_formdata('', "/a/path/filename.zip", 'filename.zip')

        mock_open.assert_has_calls([call('/a/path/filename.zip', 'rb'),
                                    call('/a/path/filename.zip.b64', 'wb')])

        mock_out.write.assert_has_calls(
            [call(bytearray(b'------------ThIs_Is_tHe_bouNdaRY_$\r\n')),
             call(bytearray(
                 b'Content-Disposition: form-data; name="file"; filename="filename.zip"\r\n')),
             call(bytearray(b'Content-Type: application/octet-stream\r\n')),
             call(bytearray(b'\r\n')),
             call(bytearray(b'\r\n')),
             call(bytearray(b'------------ThIs_Is_tHe_bouNdaRY_$--\r\n')),
             call(bytearray(b'\r\n'))])

        mock_in.close.assert_called_once()
        mock_out.close.assert_called_once()

    def test_get_connection_ssl_trust_all(self):

        conn = self.connection.get_connection()

        self.assertEqual(conn.host, '127.0.0.1')
        self.assertEqual(conn.port, 443)
        self.assertEqual(conn._context.protocol, ssl.PROTOCOL_TLSv1_2)

    def test_get_connection_ssl_trust_all_with_proxy(self):

        self.connection.set_proxy('10.0.0.1', 3128)

        conn = self.connection.get_connection()

        self.assertEqual(conn.host, '10.0.0.1')
        self.assertEqual(conn.port, 3128)
        self.assertEqual(conn._context.protocol, ssl.PROTOCOL_TLSv1_2)

    @patch.object(ssl.SSLContext, 'load_verify_locations')
    def test_get_connection_trusted_ssl_bundle_with_proxy(self, mock_lvl):

        self.connection.set_proxy('10.0.0.1', 3128)
        self.connection.set_trusted_ssl_bundle('/test')

        conn = self.connection.get_connection()

        self.assertEqual(conn.host, '10.0.0.1')
        self.assertEqual(conn.port, 3128)
        self.assertEqual(conn._context.protocol, ssl.PROTOCOL_TLSv1_2)

    @patch.object(ssl.SSLContext, 'load_verify_locations')
    def test_get_connection_trusted_ssl_bundle(self, mock_lvl):

        self.connection.set_trusted_ssl_bundle('/test')

        conn = self.connection.get_connection()

        self.assertEqual(conn.host, '127.0.0.1')
        self.assertEqual(conn.port, 443)
        self.assertEqual(conn._context.protocol, ssl.PROTOCOL_TLSv1_2)


if __name__ == '__main__':
    unittest.main()
