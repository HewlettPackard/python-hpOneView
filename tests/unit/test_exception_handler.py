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
import logging
import traceback
import unittest

import mock

from hpOneView.exception_handler import handle_exceptions
from hpOneView.exceptions import HPOneViewException


class ExceptionHandlerTest(unittest.TestCase):
    @mock.patch.object(logging, 'error')
    def test_should_log_message(self, mock_logging_error):
        message = "test message"
        exception = HPOneViewException(message)
        traceback_ex = {}
        handle_exceptions(exception.__class__, exception, traceback_ex, mock_logging_error)

        log_message = "Uncaught Exception: HPOneViewException with message: test message"
        mock_logging_error.error.assert_called_once_with(log_message,
                                                         exc_info=(exception.__class__, exception, traceback_ex))

    @mock.patch.object(traceback, 'print_exception')
    @mock.patch.object(logging, 'error')
    def test_should_print_exception(self, mock_logging_error, mock_traceback):
        message = "test message"
        exception = HPOneViewException(message)
        traceback_ex = {}
        handle_exceptions(exception.__class__, exception, traceback_ex, mock_logging_error)

        mock_traceback.assert_called_once_with(exception.__class__, exception, traceback_ex)
