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
from pprint import pprint

from hpOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file

config = {
    "ip": "172.16.102.59",
    "credentials": {
        "userName": "administrator",
        "password": ""
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

resource_uri = "/rest/enclosures/09SGH100X6J1"

print("\nSet the labels assigned to a resource")
labels_to_create = dict(
    resourceUri=resource_uri,
    labels=["labelSample2", "enclosureDemo"]
)

resource_labels = oneview_client.labels.create(labels_to_create)
pprint(resource_labels)

print("\nUpdate the resource labels")
labels_to_update = dict(
    uri="/rest/labels/resources/" + resource_uri,
    resourceUri=resource_uri,
    type="ResourceLabels",
    labels=[
        dict(name="new label"),
        dict(name="enclosureDemo")
    ]
)
updated_resource_labels = oneview_client.labels.update(labels_to_update)
pprint(updated_resource_labels)

print("\nGet all labels")
all_labels = oneview_client.labels.get_all()
pprint(all_labels)

label_uri = all_labels[0]["uri"]

print("\nGet a label by uri")
label_by_uri = oneview_client.labels.get(label_uri)
pprint(label_by_uri)

print("\nGet all the labels for the resource %s" % resource_uri)
labels_by_resource = oneview_client.labels.get_by_resource(resource_uri)
pprint(labels_by_resource)

print("\nDelete all the labels for a resource")
oneview_client.labels.delete(dict(uri="/rest/labels/resources/" + resource_uri))
print("Done!")
