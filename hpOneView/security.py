# -*- coding: utf-8 -*-

"""
security.py
~~~~~~~~~~~~

This module implements Settings HPE OneView REST API.

It has been deprecated and will be removed soon. We strongly recommend to use the OneViewClient class instead.
See more details at: https://github.com/HewlettPackard/python-hpOneView/tree/master/hpOneView/README.md
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

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


from hpOneView.common import get_members, uri, make_user_dict
from warnings import warn


def deprecated(func):
    def wrapper(*args, **kwargs):
        warn("Module security is deprecated, use OneViewClient class instead", DeprecationWarning)
        return func(*args, **kwargs)
    return wrapper


class security(object):
    def __init__(self, con):
        self._con = con

    ###########################################################################
    # User management and Roles
    ###########################################################################
    @deprecated
    def get_users(self):
        body = self._con.get(uri['users'])
        return get_members(body)

    @deprecated
    def get_user(self, user):
        body = self._con.get(uri['users'] + '/' + user)
        return body

    @deprecated
    def get_user_roles(self, user):
        body = self._con.get(uri['userRole'] + '/' + user)
        return get_members(body)

    @deprecated
    def set_user_roles(self, user, roles):
        request = []
        for role in roles:
            req = {'type': 'RoleNameDtoV2', 'roleName': role}
            request.append(req)
        task, body = self._con.put(uri['users'] + '/' + user +
                                   '/roles?multiResource=true', request)
        return body

    @deprecated
    def set_user_role(self, user, role):
        request = {'type': 'RoleNameDtoV2', 'roleName': role}
        task, body = self._con.put(uri['users'] + '/' + user +
                                   '/roles?multiResource=true', [request])
        return body

    @deprecated
    def create_user(self, name, password, enabled=True, fullName='',
                    emailAddress='', officePhone='', mobilePhone='',
                    roles=['Infrastructure administrator']):
        usr = make_user_dict(name, password, enabled, fullName,
                             emailAddress, officePhone, mobilePhone,
                             roles)
        task, body = self._con.post(uri['users'], usr)
        return body

    @deprecated
    def delete_user(self, user):
        task, body = self._con.delete(uri['users'] + '/' + user)
        return body

    @deprecated
    def update_user(self, updateUser):
        task, body = self._con.put(uri['users'], updateUser)
        return body

    @deprecated
    def get_roles(self):
        body = self._con.get(uri['roles'])
        return get_members(body)

    ###########################################################################
    # Certificates
    ###########################################################################
    @deprecated
    def get_certs(self):
        body = self._con.get(uri['certificates'])
        return body

    @deprecated
    def get_cert_https(self):
        body = self._con.get(uri['cert-https'])
        return body

    @deprecated
    def get_cert_ca(self):
        body = self._con.get(uri['ca'])
        return body

    @deprecated
    def get_cert_ca_crl(self):
        body = self._con.get(uri['crl'])
        return body

    @deprecated
    def gen_rabbitmq_internal_signed_ca(self):
        request = {'type': 'RabbitMqClientCertV2', 'commonName': 'default'}
        task, body = self._con.post(uri['rabbitmq'], request)
        return body

    @deprecated
    def gen_rabbitmq_self_signed_ca(self):
        request = {'type': 'RabbitMqClientCertV2', 'commonName': 'any',
                   'signedCert': False}
        task, body = self._con.post(uri['rabbitmq'], request)
        return body

    @deprecated
    def get_rabbitmq_kp(self, alias='default'):
        body = self._con.get(uri['rabbitmq-kp'] + '/' + alias)
        return body

    @deprecated
    def get_rabbitmq_ca(self, alias='default'):
        body = self._con.get(uri['rabbitmq'] + '/' + alias)
        return body

    @deprecated
    def get_active_user_sessions(self):
        body = self._con.get(uri['activeSessions'])
        return body

    @deprecated
    def get_category_actions(self):
        body = self._con.get(uri['category-actions'])
        return body

    @deprecated
    def get_role_category_actions(self):
        body = self._con.get(uri['role-category-actions'])
        return body

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
