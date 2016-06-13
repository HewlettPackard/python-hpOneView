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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ast
import logging
import traceback

from future import standard_library

standard_library.install_aliases()

from hpOneView.exceptions import HPOneViewException

logger = logging.getLogger(__name__)


def handle_exceptions(exception_type, exception_value, exception_traceback, logger=logger):
    message = __get_message(exception_value, exception_type)
    logger.error("Uncaught Exception: %s with message: %s" % (exception_type.__name__, message))
    traceback.print_exception(exception_type, exception_value, exception_traceback)


def __get_message(exception_value, exception_type):
    # Used to get the Exception message.
    # It is necessary special treatment to HPOneViewException because:
    # Sometimes, the exception caught from Rest API is passed as message argument to HPOneViewException
    # (E.g. connection.put). So is necessary get the key 'message' inside the message that  actually is a dictionary.
    # Other times the exceptions are caught, then joined with the status code and passed as message argument to
    # HPOneViewException (E.g. connection.post). So to get the real message is necessary remove the status code and
    # transform the string into a dictionary. Finally it would be possible to get the Key 'message'.

    message = ""

    if len(exception_value.args) > 0:

        message = exception_value.args[0]

        if issubclass(exception_type, HPOneViewException):
            try:
                if message.__class__.__name__ == 'dict':
                    message = message['message']
                else:
                    message = ast.literal_eval(exception_value.args[0].splitlines()[1])['message']
            except:
                pass
    return message
