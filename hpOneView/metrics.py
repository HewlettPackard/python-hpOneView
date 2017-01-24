# -*- coding: utf-8 -*-

"""
metrics.py
~~~~~~~~~~~~

This module implements configurguring the OneView MSMB.

It has been deprecated and will be removed soon. We strongly recommend to use the OneViewClient class instead.
See more details at: https://github.com/HewlettPackard/python-hpOneView/tree/master/hpOneView/README.md
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()


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

from hpOneView.common import uri
from hpOneView.activity import activity
from warnings import warn


def deprecated(func):
    def wrapper(*args, **kwargs):
        warn("Module metrics is deprecated, use OneViewClient class instead", DeprecationWarning)
        return func(*args, **kwargs)
    return wrapper


class metrics(object):
    def __init__(self, con):
        self._con = con
        self._activity = activity(con)

    @deprecated
    def get_metrics_capability(self):
        body = self._con.get(uri['metricsCapabilities'])
        return body

    @deprecated
    def get_metrics_configuration(self):
        body = self._con.get(uri['metricsConfiguration'])
        return body

    @deprecated
    def set_metrics_configuration(self, metrics_config, blocking=True,
                                  verbose=False):
        task, body = self._con.put(uri['metricsConfiguration'], metrics_config)
        if blocking is True:
            task = self._activity.wait4task(task, tout=600, verbose=verbose)
            return body
        return task

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
