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

from pprint import pprint
from hpOneView.oneview_client import OneViewClient
from config_loader import try_load_from_file

config = {
    "ip": "<oneview_ip>",
    "credentials": {
        "userName": "<username>",
        "password": "<password>"
    }
}

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

oneview_client = OneViewClient(config)

# Lists the appliance time and locale configuration
time_and_locale = oneview_client.appliance_time_and_locale_configuration.get()
print("\n## Got appliance time and locale configurations successfully!")
pprint(time_and_locale)

# Update NTP servers and locale
# Set to use appliance local time and date server
time_and_locale['ntpServers'] = ['127.0.0.1']
# Set locale to Chinese (China) with charset UTF-8
time_and_locale['locale'] = 'zh_CN.UTF-8'
# Remove the date and time, we do not want to update it manually
time_and_locale.pop('dateTime')
time_and_locale = oneview_client.appliance_time_and_locale_configuration.update(time_and_locale)
print("\n## Updated appliance time and locale configurations successfully!")
pprint(time_and_locale)

# Note: Changing the locale will only be fully effective after resetting the appliance

# Revert the changes made
time_and_locale['ntpServers'] = ['16.110.135.123']
time_and_locale['locale'] = 'en_US.UTF-8'
time_and_locale.pop('dateTime')
time_and_locale = oneview_client.appliance_time_and_locale_configuration.update(time_and_locale)
print("\n## Reverted appliance time and locale configurations successfully!")
pprint(time_and_locale)
