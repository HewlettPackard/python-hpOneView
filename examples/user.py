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
from config_loader import try_load_from_file

config = {
    "ip": "",
    "credentials": {
        "userName": "",
        "password": ""
    }
}

options = {
    'emailAddress': 'testUser@example.com',
    'enabled': 'true',
    'fullName': 'testUser101',
    'mobilePhone': '555-2121',
    'officePhone': '555-1212',
    'password': 'myPass1234',
    'roles': ['Read only'],
    'type': 'UserAndRoles',
    'userName': 'testUser'
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Create a User
user = oneview_client.users.create(options)
print("Created user '%s' successfully.\n  uri = '%s'\n" % (user['userName'], user['uri']))

# Adds different roles to the recently created user
user = oneview_client.users.get_by('userName', 'testUser')
print(user)
print("\n user: %s, roles before update: %s" % (user['userName'], user['roles']))
user['replaceRoles'] = True
user['roles'] = ['Infrastructure administrator']
user = oneview_client.users.update(user)
print("\n user: %s, roles after update: %s" % (user['userName'], user['roles']))

# Get user by role
user = oneview_client.users.get_by('role', 'Read only')
print("Found users by role: '%s'.\n '\n" % (user))

# Get user by name
user = oneview_client.users.get_by('userName', 'testUser')
print("Found user by name: '%s'. uri = '%s'\n" % (user['userName'], user['uri']))

# Get all users
print("Get all users")
users = oneview_client.users.get_all()
pprint(users)

# # Validates if full name is already in use
bol = oneview_client.users.validate_full_name(options['fullName'])
print("Is full name already in use? %s" % (bol))

# # Validates if user name is already in use
bol = oneview_client.users.validate_user_name(options['userName'])
print("Is user name already in use? %s" % (bol))

# Delete the created user
oneview_client.users.delete(user)
print("\nSuccessfully deleted user")
