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

MSG_DIFF_AT_KEY = 'Difference found at key \'{0}\'. '


def resource_compare(resource1, resource2):
    """
    Recursively compares dictionary contents, ignoring type and order
    Args:
        resource1: first dictionary
        resource2: second dictionary

    Returns:
        bool: True when equal, False when different.
    """
    debug_resources = "resource1 = {0}, resource2 = {1}".format(resource1, resource2)

    # The first resource is True / Not Null and the second resource is False / Null
    if resource1 and not resource2:
        logger.debug("resource1 and not resource2. " + debug_resources)
        return False

    # Check all keys in first dict
    for key in resource1.keys():
        if key not in resource2:
            # no key in second dict
            if resource1[key] is not None:
                # key inexistent is equivalent to exist and value None
                logger.debug(MSG_DIFF_AT_KEY.format(key) + debug_resources)
                return False
        # If both values are null / empty / False
        elif not resource1[key] and not resource2[key]:
            continue
        elif isinstance(resource1[key], dict):
            # recursive call
            if not resource_compare(resource1[key], resource2[key]):
                # if different, stops here
                logger.debug(MSG_DIFF_AT_KEY.format(key) + debug_resources)
                return False
        elif isinstance(resource1[key], list):
            # change comparison function (list compare)
            if not resource_compare_list(resource1[key], resource2[key]):
                # if different, stops here
                logger.debug(MSG_DIFF_AT_KEY.format(key) + debug_resources)
                return False
        elif _standardize_value(resource1[key]) != _standardize_value(resource2[key]):
            # different value
            logger.debug(MSG_DIFF_AT_KEY.format(key) + debug_resources)
            return False

    # Check all keys in second dict to find missing
    for key in resource2.keys():
        if key not in resource1:
            # not exists in first dict
            if resource2[key] is not None:
                # key inexistent is equivalent to exist and value None
                logger.debug(MSG_DIFF_AT_KEY.format(key) + debug_resources)
                return False

    # no differences found
    return True


def resource_compare_list(resource1, resource2):
    """
    Recursively compares lists contents, ignoring type
    Args:
        resource1: first list
        resource2: second list

    Returns:
        True when equal;
        False when different.

    """
    debug_resources = "resource1 = {0}, resource2 = {1}".format(resource1, resource2)

    # The second list is null / empty  / False
    if not resource2:
        logger.debug("resource 2 is null. " + debug_resources)
        return False

    if len(resource1) != len(resource2):
        # different length
        logger.debug("resources have different length. " + debug_resources)
        return False

    for i, val in enumerate(resource1):
        if isinstance(val, dict):
            # change comparison function
            if not resource_compare(val, resource2[i]):
                logger.debug("resources are different. " + debug_resources)
                return False
        elif isinstance(val, list):
            # recursive call
            if not resource_compare_list(val, resource2[i]):
                logger.debug("lists are different. " + debug_resources)
                return False
        elif _standardize_value(val) != _standardize_value(resource2[i]):
            # value is different
            logger.debug("values are different. " + debug_resources)
            return False

    # no differences found
    return True


def _standardize_value(value):
    """
    Convert value to string to enhance the comparison.

    Args:
        value: Any object type.

    Returns:
        str: Converted value.
    """
    if isinstance(value, float) and value.is_integer():
        # Workaround to avoid erroneous comparison between int and float
        # Removes zero from integer floats
        value = int(value)

    return str(value)
