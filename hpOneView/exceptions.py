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


from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()

import logging
import traceback
from past.builtins import basestring

logger = logging.getLogger(__name__)


def handle_exceptions(exception_type, exception_value, exception_traceback, logger=logger):
    message = __get_message(exception_value, exception_type)

    logger.error("Uncaught Exception: %s with message: %s" % (exception_type.__name__, message))
    traceback.print_exception(exception_type, exception_value, exception_traceback)


def __get_message(exception_value, exception_type):
    message = ""

    if issubclass(exception_type, HPOneViewException):
        if exception_value.msg:
            message = exception_value.msg
        if exception_value.oneview_response:
            message += "\n" + str(exception_value.oneview_response)
    elif len(exception_value.args) > 0:
        message = exception_value.args[0]

    return message


class HPOneViewException(Exception):
    """
    OneView base Exception.

    Attributes:
       msg (str): Exception message.
       oneview_response (dict): OneView rest response.
   """

    def __init__(self, data, error=None):
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
    """
    OneView Invalid Resource Exception.

    Attributes:
       msg (str): Exception message.
    """
    pass


class HPOneViewTaskError(HPOneViewException):
    """
    OneView Task Error Exception.

    Attributes:
       msg (str): Exception message.
       error_code (str): A code which uniquely identifies the specific error.
    """

    def __init__(self, msg, error_code=None):
        super(HPOneViewTaskError, self).__init__(msg)
        self.error_code = error_code


class HPOneViewUnknownType(HPOneViewException):
    """
    OneView Unknown Type Error.

    Attributes:
       msg (str): Exception message.
    """
    pass


class HPOneViewTimeout(HPOneViewException):
    """
    OneView Timeout Exception.

    Attributes:
       msg (str): Exception message.
    """
    pass


class HPOneViewValueError(HPOneViewException):
    """
    OneView Value Error.
    The exception is raised when the data contains an inappropriate value.

    Attributes:
       msg (str): Exception message.
    """
    pass


class HPOneViewResourceNotFound(HPOneViewException):
    """
    OneView Resource Not Found Exception.
    The exception is raised when an associated resource was not found.

    Attributes:
       msg (str): Exception message.
    """
    pass
