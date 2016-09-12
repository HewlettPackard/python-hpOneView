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
import unittest

from hpOneView.exceptions import HPOneViewException, HPOneViewInvalidResource


class ExceptionsTest(unittest.TestCase):
    def test_exception_constructor_with_string(self):
        exception = HPOneViewException("A message string")
        self.assertEqual(exception.msg, "A message string")
        self.assertEqual(exception.oneview_response, None)
        self.assertEqual(exception.args[0], "A message string")

    def test_exception_constructor_with_valid_dict(self):
        exception = HPOneViewException({'message': "A message string"})
        self.assertEqual(exception.msg, "A message string")
        self.assertEqual(exception.oneview_response, {'message': "A message string"})
        self.assertEqual(exception.args[0], "A message string")

    def test_exception_constructor_with_invalid_dict(self):
        exception = HPOneViewException({'msg': "A message string"})
        self.assertEqual(exception.msg, None)
        self.assertEqual(exception.oneview_response, {'msg': "A message string"})
        self.assertEqual(exception.args[0], None)

    def test_exception_constructor_with_invalid_type(self):
        exception = HPOneViewException(['msg', "A message string"])
        self.assertEqual(exception.msg, None)
        self.assertEqual(exception.oneview_response, ['msg', "A message string"])
        self.assertEqual(exception.args[0], None)

    def test_invalid_resource_exception_inheritance(self):
        exception = HPOneViewInvalidResource({'message': "A message string"})
        self.assertEqual(exception.msg, "A message string")
        self.assertEqual(exception.oneview_response, {'message': "A message string"})
        self.assertEqual(exception.args[0], "A message string")

    def test_exception_constructor_with_unicode(self):
        exception = HPOneViewException(u"A message string")
        self.assertEqual(exception.msg, "A message string")
        self.assertEqual(exception.oneview_response, None)
        self.assertEqual(exception.args[0], "A message string")
