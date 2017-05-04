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

import unittest

import mock

from hpOneView.connection import connection
from hpOneView.resources.security.users import Users
from hpOneView.resources.resource import ResourceClient
<<<<<<< HEAD
from hpOneView.exceptions import HPOneViewException
=======
>>>>>>> Adding users resource and tests


class UsersTest(unittest.TestCase):
    def setUp(self):
        self.host = '127.0.0.1'
        self.connection = connection(self.host)
        self._users = Users(self.connection)

    @mock.patch.object(ResourceClient, 'get_all')
    def test_get_all_called_once(self, mock_get_all):
        filter = 'name=TestName'
        sort = 'name:ascending'

        self._users.get_all(2, 500, filter, sort)

        mock_get_all.assert_called_once_with(2, 500, filter=filter, sort=sort)

    @mock.patch.object(ResourceClient, 'create')
    def test_create_should_use_given_values(self, mock_create):
        resource = {
            'enabled': 'true',
            'fullName': 'testUser101',
            'mobilePhone': '555-2121',
            'officePhone': '555-1212',
            'password': 'myPass1234',
            'roles': ['Read only'],
            'type': 'UserAndRoles',
            'userName': 'testUser'
        }
        resource_rest_call = resource.copy()
        mock_create.return_value = {}

        self._users.create(resource, 30)
        mock_create.assert_called_once_with(resource_rest_call, timeout=30,
                                            default_values=self._users.DEFAULT_VALUES)

    @mock.patch.object(ResourceClient, 'update')
    def test_update_should_use_given_values(self, mock_update):
        resource = {
            'enabled': 'true',
            'fullName': 'testUser101',
            'mobilePhone': '555-2121',
            'officePhone': '555-1212',
            'password': 'myPass1234',
            'roles': ['Read only'],
            'type': 'UserAndRoles',
            'userName': 'testUser'
        }
        resource_rest_call = resource.copy()
        mock_update.return_value = {}

        self._users.update(resource, 60)
        mock_update.assert_called_once_with(resource_rest_call, timeout=60,
                                            default_values=self._users.DEFAULT_VALUES, uri='/rest/users')

    @mock.patch.object(ResourceClient, 'delete')
    def test_delete_called_once(self, mock_delete):
        id = 'fake'
        self._users.delete(id, force=False, timeout=-1)

        mock_delete.assert_called_once_with(id, force=False, timeout=-1)

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_called_once(self, mock_get):
        self._users.get_by('userName', 'OneViewSDK Test User')
        mock_get.assert_called_once_with('/rest/users/OneViewSDK Test User')

<<<<<<< HEAD
    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_called_with_role(self, mock_get):
        self._users.get_by('role', 'fakerole')
        mock_get.assert_called_once_with('/rest/users/roles/users/fakerole')

    @mock.patch.object(ResourceClient, 'get')
    def test_get_by_called_with_something_invalid(self, mock_get):
        try:
            self._users.get_by('test', 'test')
        except HPOneViewException as exception:
            self.assertEqual('Only userName, name and role can be queried for this resource.', exception.args[0])
        else:
            self.fail("Expected Exception was not raised")

=======
>>>>>>> Adding users resource and tests
    @mock.patch.object(ResourceClient, 'create_with_zero_body')
    def test_validate_full_name_called_once(self, mock_create_with_zero_body):

        self._users.validate_full_name('fullname101')

        expected_uri = '/rest/users/validateUserName/fullname101'
        mock_create_with_zero_body.assert_called_once_with(uri=expected_uri, timeout=-1)

    @mock.patch.object(ResourceClient, 'create_with_zero_body')
    def test_validate_user_name_called_once(self, mock_create_with_zero_body):

        self._users.validate_user_name('userName')

        expected_uri = '/rest/users/validateLoginName/userName'
        mock_create_with_zero_body.assert_called_once_with(uri=expected_uri, timeout=-1)
