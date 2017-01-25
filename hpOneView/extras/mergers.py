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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

import logging

logger = logging.getLogger(__name__)


def merge_list_by_key(original_list, updated_list, key, ignore_when_null=[]):
    """
    Merge two lists by the key. It basically:
    1. Adds the items that are present on updated_list and are absent on original_list.
    2. Removes items that are absent on updated_list and are present on original_list.
    3. For all items that are in both lists, overwrites the values from the original item by the updated item.

    Args:
        original_list: original list.
        updated_list: list with changes.
        key: unique identifier.
        ignore_when_null: list with the keys from the updated items that should be ignored in the merge, if its
        values are null.
    Returns:
        list: Lists merged.
    """
    if not original_list:
        return updated_list

    items_map = {x[key]: x.copy() for x in original_list}
    merged_items = {}

    for item in updated_list:
        item_key = item[key]
        if item_key in items_map:
            for ignored_key in ignore_when_null:
                if ignored_key in item and not item[ignored_key]:
                    item.pop(ignored_key)
            merged_items[item_key] = items_map[item_key].copy()
            merged_items[item_key].update(item)
        else:
            merged_items[item_key] = item.copy()

    return [val for (_, val) in merged_items.items()]
