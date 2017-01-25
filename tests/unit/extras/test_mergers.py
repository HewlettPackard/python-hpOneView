# -*- coding: utf-8 -*-
###
# (C) Copyright (2016-2017) Hewlett Packard Enterprise Development LP
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

from hpOneView.extras.mergers import merge_list_by_key


class MergersTest(unittest.TestCase):
    def test_merge_list_by_key_when_original_list_is_empty(self):
        original_list = []
        list_with_changes = [dict(id=1, value="123")]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id")

        expected_list = [dict(id=1, value="123")]
        self.assertEqual(merged_list, expected_list)

    def test_merge_list_by_key_when_original_list_is_null(self):
        original_list = None
        list_with_changes = [dict(id=1, value="123")]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id")

        expected_list = [dict(id=1, value="123")]
        self.assertEqual(merged_list, expected_list)

    def test_merge_list_by_key_with_same_lenght_and_order(self):
        original_list = [dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=3500),
                         dict(id=2, allocatedMbps=1000, mac="E2:4B:0D:30:00:0B", requestedMbps=1000)]

        list_with_changes = [dict(id=1, requestedMbps=2700, allocatedVFs=3500),
                             dict(id=2, requestedMbps=1005)]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id")

        expected_list = [dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=2700, allocatedVFs=3500),
                         dict(id=2, allocatedMbps=1000, mac="E2:4B:0D:30:00:0B", requestedMbps=1005)]

        self.assertEqual(merged_list, expected_list)

    def test_merge_list_by_key_with_different_order(self):
        original_list = [dict(id=2, allocatedMbps=1000, mac="E2:4B:0D:30:00:0B", requestedMbps=1000),
                         dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=3500)]

        list_with_changes = [dict(id=1, requestedMbps=2700, allocatedVFs=3500),
                             dict(id=2, requestedMbps=1005)]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id")

        expected_list = [dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=2700, allocatedVFs=3500),
                         dict(id=2, allocatedMbps=1000, mac="E2:4B:0D:30:00:0B", requestedMbps=1005)]

        self.assertEqual(merged_list, expected_list)

    def test_merge_list_by_key_with_removed_items(self):
        original_list = [dict(id=2, allocatedMbps=1000, mac="E2:4B:0D:30:00:0B", requestedMbps=1000),
                         dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=3500)]

        list_with_changes = [dict(id=1, requestedMbps=2700, allocatedVFs=3500)]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id")

        expected_list = [dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=2700, allocatedVFs=3500)]

        self.assertEqual(merged_list, expected_list)

    def test_merge_list_by_key_with_added_items(self):
        original_list = [dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=3500)]

        list_with_changes = [dict(id=1, requestedMbps=2700, allocatedVFs=3500),
                             dict(id=2, requestedMbps=1005)]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id")

        expected_list = [dict(id=1, allocatedMbps=2500, mac="E2:4B:0D:30:00:09", requestedMbps=2700, allocatedVFs=3500),
                         dict(id=2, requestedMbps=1005)]

        self.assertEqual(merged_list, expected_list)

    def test_merge_list_by_key_should_ignore_key_when_null(self):
        original_list = [dict(id=1, value1="123", value2="345")]
        list_with_changes = [dict(id=1, value1=None, value2="345-changed")]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id",
                                        ignore_when_null=['value1', 'value2'])

        expected_list = [dict(id=1, value1="123", value2="345-changed")]

        self.assertEqual(merged_list, expected_list)

    def test_merge_list_by_key_should_not_fail_when_ignored_key_absent(self):
        original_list = [dict(id=1, value1="123", value2="345")]
        list_with_changes = [dict(id=1, value3="678")]

        merged_list = merge_list_by_key(original_list, list_with_changes, key="id",
                                        ignore_when_null=['value1'])

        expected_list = [dict(id=1, value1="123", value2="345", value3="678")]

        self.assertEqual(merged_list, expected_list)


if __name__ == '__main__':
    unittest.main()
