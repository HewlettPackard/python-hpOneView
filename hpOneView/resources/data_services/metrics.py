# -*- coding: utf-8 -*-


from __future__ import (unicode_literals, print_function, division, absolute_import)

from future import standard_library

standard_library.install_aliases()

__title__ = 'Metrics'
__version__ = '0.0.1'
__copyright__ = '(C) Copyright (2012-2015) Hewlett Packard Enterprise ' \
                ' Development LP'
__license__ = 'MIT'
__status__ = 'Development'


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

class Metrics(object):
    """Metrics can be relayed from OneView for managed resources at a specified interval. The following steps can be
     followed to enable the metric relay in OneView:

    Get the list of resource types and metrics which can be configured for live streaming
    Configure the live metric stream in OneView
    Receive the stream of metric on MSMB
    Note: MSMB(Metric Streaming Message Bus) is an interface that uses asynchronous messaging to notify subscribers the
    most recent metric of the managed resources.
    All messages that are relayed to the exchange msmb can be received by using routing key #.
    The table below describes the structure of message relayed to MSMB

    |---------------------------------------------------------------------------------------------------------|
    |Attribute                   |Description                                                     |Type       |
    ----------------------------------------------------------------------------------------------------------|
    |startTime                   |The starting time of the metric collection.                     |string     |
    ----------------------------------------------------------------------------------------------------------|
    |sampleIntervalInSeconds     |Interval between samples                                        |integer    |
    ----------------------------------------------------------------------------------------------------------|
    |numberOfSamples             |Number of samples in the list for each metric type              |integer    |
    ----------------------------------------------------------------------------------------------------------|
    |resourceType                |Identifies the category of resource. The supported              |string     |
    |                            |devices are server-hardware, enclosures and power-devices       |           |
    ----------------------------------------------------------------------------------------------------------|
    |resourceDataList            |Metric sample list                                              |List       |
    ----------------------------------------------------------------------------------------------------------|
    |uri                         |Canonical URI of the resource                                   |string     |
    ----------------------------------------------------------------------------------------------------------|
    |category                    |Identifies the category of resource. The supported devices are  |string     |
    |                            |server-hardware, enclosures and power-devices                   |           |
    ----------------------------------------------------------------------------------------------------------|
    |created                     |Date and time when the resource was created                     |timestamp  |
    ----------------------------------------------------------------------------------------------------------|
    |modified                    |Date and time when the resource was last modified               |timestamp  |
    ----------------------------------------------------------------------------------------------------------|
    |eTag                        |Entity tag/version ID of the resource, the same value that is   |string     |
    |                            |returned in the ETag header on a GET of the resource            |           |
    ----------------------------------------------------------------------------------------------------------|
    |type                        |Uniquely identifies the type of the JSON object                 |string     |
    ----------------------------------------------------------------------------------------------------------|
    """

    RESOURCE_URI = "/rest/metrics/configuration"

    def __init__(self, connection):
        self._connection = connection

    def update_configuration(self, configuration):
        """Updates the metrics configuration with the new values. Overwrites the existing configuration.
        Args:
            configuration: json with a list of objects which contain frequency, sample interval and source type for each
            resource-type.

            Example:

             {
                "sourceTypeList": [
                    {
                        "sourceType": "/rest/power-devices",
                        "sampleIntervalInSeconds": "300",
                        "frequencyOfRelayInSeconds": "3600"
                    }
                ]
            }
        returns:
            json: The updated list of objects
        """
        _, response = self._connection.put(self.RESOURCE_URI, configuration)
        return response
