# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2016) Hewlett Packard Enterprise Development LP
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
import mock
import unittest
import uuid
import json
 
from hpOneView.common import make_server_dict
from hpOneView.common import make_ServerProfileTemplateV1
from hpOneView.common import uri
from hpOneView.connection import *
from hpOneView.servers import *
from hpOneView.activity import *

class ServersTest(unittest.TestCase):
    
    def setUp(self):
        super(ServersTest, self).setUp()
        self.host = 'http://1.2.3.4'
        self.connection = connection(self.host)
        self.servers = servers(self.connection)
        self.activity = activity(self.connection)

    @mock.patch.object(connection, 'get')
    def test_get_connections(self, mock_get):
        # Testing with filter
        filter = '?start=0&count=10'
        self.servers.get_connections(filter=filter)
        mock_get.assert_called_once_with(uri['conn'] + filter)

    @mock.patch.object(connection, 'get')
    def test_get_connection(self, mock_get):
        settings_test = {"uri": "/rest/servers/9b1380ee-a0bb-4388-af35-2c5a05e84c47"}
        self.servers.get_connection(settings_test)
        mock_get.assert_called_once_with(settings_test['uri'])

    @mock.patch.object(connection, 'get')
    def test_get_utilization(self, mock_get):
        settings_test = {"uri": "/rest/servers/9b1380ee-a0bb-4388-af35-2c5a05e84c47"}
        self.servers.get_utilization(settings_test)
        mock_get.assert_called_once_with(settings_test['uri'] + '/utilization')

    @mock.patch.object(connection, 'get')
    def test_get_bios(self, mock_get):
        settings_test = {"uri": "/rest/servers/9b1380ee-a0bb-4388-af35-2c5a05e84c47"}
        self.servers.get_bios(settings_test)
        mock_get.assert_called_once_with(settings_test['uri'] + '/bios')

    @mock.patch.object(connection, 'get')
    def test_get_envconf(self, mock_get):
        settings_test = {"uri": "/rest/servers/9b1380ee-a0bb-4388-af35-2c5a05e84c47"}
        self.servers.get_env_conf(settings_test)
        mock_get.assert_called_once_with(settings_test['uri'] + '/environmentalConfiguration')

    @mock.patch.object(connection, 'get')
    def test_get_ilo(self, mock_get):
        settings_test = {"uri": "/rest/servers/9b1380ee-a0bb-4388-af35-2c5a05e84c47"}
        self.servers.get_ilo_sso_url(settings_test)
        mock_get.assert_called_once_with(settings_test['uri'] + '/iloSsoUrl')

    @mock.patch.object(connection, 'get')
    def test_get_server_schema(self, mock_get):
        self.servers.get_server_schema()
        mock_get.assert_called_once_with(uri['servers'] + '/schema')

    @mock.patch.object(connection, 'get')
    def test_get_java_remote(self, mock_get):
        settings_test = {"uri": "/rest/servers/9b1380ee-a0bb-4388-af35-2c5a05e84c47"}
        self.servers.get_java_remote_console_url(settings_test)
        mock_get.assert_called_once_with(settings_test['uri'] + '/javaRemoteConsoleUrl')

    @mock.patch.object(connection, 'get')
    def test_get_remote_console(self, mock_get):
        settings_test = {"uri": "/rest/servers/9b1380ee-a0bb-4388-af35-2c5a05e84c47"}
        self.servers.get_remote_console_url(settings_test)
        mock_get.assert_called_once_with(settings_test['uri'] + '/remoteConsoleUrl')

    @mock.patch.object(connection, 'post')
    @mock.patch.object(activity, 'wait4task') 
    def test_create_server_profile_template(self, mock_wait4task, mock_post):        
        name = 'spt'
        description = 'description'
        sht = '/rest/server-hardware-types/1234'
        eg = '/rest/enclosure-groups/1'
        affinity = 'Bay'
        hideFlex = False;
        
        # build the V1 SPT
        spt = make_ServerProfileTemplateV1(name, description, None, sht, eg, affinity, hideFlex, None)
        
        # build a OV task for the create SPT operation
        task = self.build_spt_add_task_resource()  
        
        # return the task when waiting for completion      
        mock_post.return_value = [task, None]
                
        self.servers.create_server_profile_template(name, description, None, sht, eg, affinity, hideFlex, None)
        mock_post.assert_called_once_with(uri['profile-templates'], spt)         

    @mock.patch.object(connection, 'post')
    @mock.patch.object(activity, 'wait4task')    
    def test_add_server(self, mock_wait4task, mock_post):     
        
        # build the server to add
        server = make_server_dict('hostname', 'username', 'password', False, 'OneView')
        
        # build a OV task for the server add operation
        task = self.build_server_add_task_resource()        
        mock_post.return_value = [task, None]
        
        # return the task when waiting for completion
        mock_wait4task(task).return_value = task
                
        self.servers.add_server(server)
        mock_post.assert_called_once_with(uri['servers'], server)
        
    # helper functions for building Task responses for server operations
    def build_server_add_task_resource(self):
        task = {
                'type': 'TaskResourceV2',
                'taskType': 'User',
                'stateReason': None,
                'associatedResource': {
                    'resourceUri': '/rest/server-hardware/31393736',
                    'resourceCategory': 'server-hardware',
                    'associationType': 'MANAGED_BY',
                    'resourceName': 'Encl1, bay 2'
                },
                'hidden': False,
                'category': 'tasks',
                'data': {
                    'EncUri': '/rest/enclosures/09SGH100X6J'
                },
                'percentComplete': 100,
                'taskState': 'Complete',
                'taskStatus': 'Add server: Encl1, bay 2.',
                'taskErrors': [],
                'parentTaskUri': '/rest/tasks/7A4F318D-AD78-4F68-879E-DF317E66008E',
                'taskOutput': [],
                'associatedTaskUri': None,
                'completedSteps': 20,
                'computedPercentComplete': 100,
                'expectedDuration': 480,
                'progressUpdates': [],
                'totalSteps': 20,
                'userInitiated': True,
                'name': 'Add',
                'owner': 'Administrator',
                'eTag': '18',
                'uri': '/rest/tasks/6BAFD214-A6CE-4D3A-9E77-C266444CE517'
            }
        return json.dumps(task)
    
    def build_spt_add_task_resource(self):
        task = {
                'type': 'TaskResourceV2',
                'taskType': 'User',
                'stateReason': 'Completed',
                'associatedResource': {
                    'resourceUri': '/rest/server-profile-templates/bc9b8b32',
                    'resourceCategory': 'server-profile-templates',
                    'associationType': 'MANAGED_BY',
                    'resourceName': ''
                },
                'hidden': False,
                'category': 'tasks',
                'data': None,
                'percentComplete': 100,
                'taskState': 'Completed',
                'taskStatus': 'Created server profile template:',
                'taskErrors': [],
                'parentTaskUri': None,
                'taskOutput': [],
                'associatedTaskUri': None,
                'completedSteps': 0,
                'computedPercentComplete': 100,
                'expectedDuration': 0,
                'progressUpdates': [],
                'totalSteps': 0,
                'userInitiated': False,
                'name': 'Create ',
                'owner': 'Administrator',
                'eTag': '3',
                'uri': '/rest/tasks/339A4D47-757B-4425-8495-6ECFCFEF88B5'
            }
        return json.dumps(task)
    
if __name__ == '__main__':
    unittest.main()