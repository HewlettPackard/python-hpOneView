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

from hpOneView.resources.resource import ResourceClient


class MetricStreaming(object):
    """
    Metrics API client.

    Metrics can be relayed from OneView for managed resources at a specified interval. The following steps can be
    followed to enable the metric relay in OneView:

        * Get the list of resource types and metrics which can be configured for live streaming
        * Configure the live metric stream in OneView
        * Receive the stream of metric on MSMB

    The list below describes the structure of message relayed to MSMB:
        startTime (str):
            The starting time of the metric collection.
        sampleIntervalInSeconds (int):
            Interval between samples.
        numberOfSamples (int):
            Number of samples in the list for each metric type.
        resourceType (str):
            Identifies the resource type.
        resourceDataList (list):
            Metric sample list.
        uri (str):
            Canonical URI of the resource.
        category (str):
            Identifies the category of resource. The supported devices are server-hardware, enclosures, and
            power-devices.
        created (timestamp):
            Date and time when the resource was created.
        modified (timestamp):
            Date and time when the resource was last modified.
        eTag (str):
            Entity tag/version ID of the resource, the same value that is returned in the ETag header on a GET of the
            resource.
        type (str):
            Uniquely identifies the type of the JSON object.

    """
    URI = '/rest/metrics'

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_capability(self):
        """
        Fetches the list of resource types and supported metrics that OneView is capable of relaying.

        Returns:
            list: List of resource types and supported metrics.
        """
        return self._client.get(self.URI + "/capability")

    def get_configuration(self):
        """
        Fetches the current configuration for which metrics are being relayed.

        Returns:
            list: List of objects which contain frequency, sample interval, and source type for each resource-type.

        """
        return self._client.get(self.URI + "/configuration")

    def update_configuration(self, configuration):
        """
        Updates the metrics configuration with the new values. Overwrites the existing configuration.

        Args:
            configuration (dict):
                Dictionary with a list of objects which contain frequency, sample interval, and source type for each
                resource-type.

        Returns:
            dict: The current configuration for which metrics are being relayed.

        """
        return self._client.update(configuration, uri=self.URI + "/configuration")
