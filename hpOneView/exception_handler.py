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
    message = ""

    if issubclass(exception_type, HPOneViewException):
        if exception_value.msg:
            message = exception_value.msg
        if exception_value.oneview_response:
            message += "\n" + str(exception_value.oneview_response)
    elif len(exception_value.args) > 0:
        message = exception_value.args[0]

    return message
