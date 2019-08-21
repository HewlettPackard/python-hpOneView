# -*- coding: utf-8 -*-
###
# (C) Copyright (2012-2019) Hewlett Packard Enterprise Development LP
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
import cmd
import csv
import os
from datetime import datetime
from collections import Counter
from hpOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file


CONFIG = {}


class OneView(object):
    """
    OneView methods
    """

    def __init__(self):
        self.client = self.connect(CONFIG)

    def connect(self, config):
        # Try load config from a file (if there is a config file)
        config = try_load_from_file(config)
        return OneViewClient(config)

    def get_alerts(self, _filter='', _view=''):
        print("\nFilter: {}\n".format(_filter))
        resp = self.client.alerts.get('/rest/alerts?filter={}'.format(_filter))
        total = resp['total']
        print("\nRetrieving {} alerts...\n".format(total))
        return self.client.alerts.get_all(0, total, filter=_filter, view=_view)

    def summarize_alerts(self, count, alerts):
        cnt = Counter()
        for alert in alerts:
            cnt["{alertTypeID} {severity}".format(**alert)] += 1
        print("Count\talertTypeID")
        print("-----\t-----------")
        for c in cnt.most_common(int(count)):
            print("{}\t{}".format(c[1], c[0]))
        print("\nExport summary as csv? y|n")
        choice = input()
        if choice in ['y', 'Y', 'yes', 'Yes']:
            filename = "summary_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".csv"
            with open(filename, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['AlertTypeID', 'Count'])
                csvwriter.writerows(cnt.most_common(int(count)))
        print("\nExported file available at {0}".format(os.getcwd() + "\\" + filename))


class CLI(cmd.Cmd):
    """ Alerts CLI commands"""

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.ov = OneView()
        self.filter = ''
        self.prompt = "\n=>> "

    def do_quit(self, line):
        """
        Exits the cli
        """
        return True

    def do_filter(self, line):
        """\nSets the filter to limit alert retrieval for 'list' and 'save'
        \nusage:  filter <filter> (empty shows current filter)
        \nex:     filter alertState='Active'
        \nex:     filter severity='Critical'
        \nex:     filter alertState='Active' AND severity='Critical'
        """
        if line:
            self.filter = line
        return print("Filter: {}".format(self.filter))

    def do_list(self, line):
        """\nLists alerts
        \nusage:  list top <number to list>
        \nex:     list top 10
        """
        words = line.split()
        if len(words) != 2:
            print("Invalid parameters")
            print("Usage: list top <number to list>")
            print("ex:    list top 10")
            return

        count = words[1]
        alerts = self.ov.get_alerts(_filter=self.filter)
        if alerts:
            self.ov.summarize_alerts(count, alerts)

    def do_save(self, line):
        """\nSaves all filtered alert data to .csv file
        \nusage:  save
        """
        alerts = self.ov.get_alerts(_filter=self.filter)
        filename = "detail_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".csv"

        if alerts:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = alerts[0].keys()
                csvwriter = csv.DictWriter(csvfile, fieldnames)
                csvwriter.writeheader()
                csvwriter.writerows(alerts)
        print("\nExported file available at {0}".format(os.getcwd() + "\\" + filename))

    def emptyline(self):
        pass


if __name__ == '__main__':
    print("HPE OneView Alert Utility")

    try:
        CLI().cmdloop()
    finally:
        print("goodbye")
