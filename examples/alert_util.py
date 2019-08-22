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
            cnt["{alertTypeID}".format(**alert)] += 1
        return cnt.most_common(int(count))

    def print_summary(self, counter, count):
        print("Count\talertTypeID")
        print("-----\t-----------")
        for cnt in counter:
            print("{}\t{}".format(cnt[1], cnt[0]))


class CLI(cmd.Cmd):
    """
    Alerts CLI commands

    Basic Usage:

    1. (optional) use the'filter' command to filter alerts
    2. run the 'get' command to retrieve alerts from OneView
    3. run the 'show' and|or 'export' commands to view|save alert data
    """

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.ov = OneView()
        self.filter = ''
        self.prompt = "\n=>> "
        self.alerts = None

    def do_quit(self, line):
        """
        Exits the cli
        """
        return True

    def do_filter(self, line):
        """\nSets the filter to limit alert retrieval
        \nusage:  filter <filter>\t\t\t\t# sets a filter
        filter ''\t\t\t\t# clears current filter
        filter\t\t\t\t\t# shows current filter
        \nexamples:
        filter alertState='Active'
        filter severity='Critical'
        filter alertState='Active' AND severity='Critical'
        """
        if line:
            self.filter = line
            if line == "''":
                self.filter = ''
        print("Current Filter: {}".format(self.filter))

    def do_get(self, line):
        """\nRetrieves alerts into local object using any filter set by the 'filter' command.
        \rYou can then use: 'show' and 'export' commands.
        \nusage:  get
        """
        self.alerts = self.ov.get_alerts(_filter=self.filter)

    def do_show(self, line):
        """\nShows a summarized count of alerts based on alterTypeID
        \nusage:  show top <number to show>
        \nexamples:
        show top 10
        show top 100
        """
        words = line.split()
        if len(words) != 2:
            self.do_help("show")
            return

        count = words[1]
        if self.alerts:
            self.ov.print_summary(self.ov.summarize_alerts(count, self.alerts), count)
        else:
            print("No alerts to show. You need to run 'get' first.")

    def do_export(self, line):
        """\nExport alert data to .csv file.
        \nusage:  export all\t\t\t# exports all alert data to .csv file
        export top <number>\t\t# export summary data to .csv file
        \nexamples:
        export top 10
        export all
        """
        words = line.split()
        if not words  \
                or words[0] not in ['top', 'all']  \
                or (words[0] == 'top' and len(words) < 2):
            self.do_help("export")
            return

        if self.alerts:
            if words[0] == 'all':
                filename = "detail_{}.csv".format(datetime.now().strftime("%Y%m%d-%H%M%S"))
                with open(filename, 'w', newline='') as csvfile:
                    fieldnames = self.alerts[0].keys()
                    csvwriter = csv.DictWriter(csvfile, fieldnames)
                    csvwriter.writeheader()
                    csvwriter.writerows(self.alerts)
                print("\nExported file available at {0}".format(os.getcwd() + os.sep + filename))

            if words[0] == 'top':
                count = int(words[1])
                cnt = self.ov.summarize_alerts(count, self.alerts)
                filename = "summary_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".csv"
                with open(filename, 'w', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(['AlertTypeID', 'Count'])
                    csvwriter.writerows(cnt)
                print("\nExported file available at {0}".format(os.getcwd() + os.sep + filename))
        else:
            print("No alerts to export. You need to run 'get' first.")

    def emptyline(self):
        pass


if __name__ == '__main__':
    print("[HPE OneView Alert Utility]")
    try:
        CLI().cmdloop()
    finally:
        print("goodbye")
