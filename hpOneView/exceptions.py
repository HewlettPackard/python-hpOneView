# -*- coding: utf-8 -*-

"""
exceptions.py
~~~~~~~~~~~~~~

This module implements exceptions of the HPE OneView REST API.
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()

__title__ = 'exceptions'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2015) Hewlett Packard Enterprise ' \
                ' Development LP'
__license__ = 'MIT'
__status__ = 'Development'

###
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
###
from past.builtins import basestring


class HPOneViewException(Exception):
    """
    OneView base Exception.

    Attributes:
       msg (str): Exception message.
       oneview_response (dict): OneView rest response.
   """

    def __init__(self, data):
        self.msg = None
        self.oneview_response = None

        if isinstance(data, basestring):
            self.msg = data
        else:
            self.oneview_response = data

            if data and isinstance(data, dict):
                self.msg = data.get('message')

        if self.oneview_response:
            Exception.__init__(self, self.msg, self.oneview_response)
        else:
            Exception.__init__(self, self.msg)


class HPOneViewInvalidResource(HPOneViewException):
    pass


class HPOneViewTaskError(HPOneViewException):
    def __init__(self, msg, error_code=None):
        super(HPOneViewTaskError, self).__init__(msg)
        self.error_code = error_code


class HPOneViewUnknownType(HPOneViewException):
    pass


class HPOneViewTimeout(HPOneViewException):
    pass
