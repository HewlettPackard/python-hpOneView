# -*- coding: utf-8 -*-
###
# (C) Copyright (2016) Hewlett Packard Enterprise Development LP
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

from hpOneView import transform_list_to_dict, extract_id_from_uri


class CommonFunctionsTest(unittest.TestCase):
    def test_transform_list_to_dict(self):
        list = ['one', 'two', {'tree': 3}, 'four', 5]

        dict_transformed = transform_list_to_dict(list=list)

        self.assertEqual(dict_transformed,
                         {'5': True,
                          'four': True,
                          'one': True,
                          'tree': 3,
                          'two': True})

    def test_extract_id_from_uri(self):
        uri = '/rest/plan-scripts/3518be0e-17c1-4189-8f81-83f3724f6155'
        id = '3518be0e-17c1-4189-8f81-83f3724f6155'
        extracted_id = extract_id_from_uri(uri)
        self.assertEqual(id, extracted_id)

    def test_extract_id_from_uri_with_extra_slash(self):
        uri = '/rest/plan-scripts/3518be0e-17c1-4189-8f81-83f3724f6155/'
        extracted_id = extract_id_from_uri(uri)
        self.assertEqual(extracted_id, '')

    def test_extract_id_from_uri_passing_id(self):
        uri = '3518be0e-17c1-4189-8f81-83f3724f6155'
        extracted_id = extract_id_from_uri(uri)
        self.assertEqual(extracted_id, '3518be0e-17c1-4189-8f81-83f3724f6155')

    def test_extract_id_from_uri_unsupported(self):
        # This example is not supported yet
        uri = '/rest/plan-scripts/3518be0e-17c1-4189-8f81-83f3724f6155/otherthing'
        extracted_id = extract_id_from_uri(uri)
        self.assertEqual(extracted_id, 'otherthing')


if __name__ == '__main__':
    unittest.main()
