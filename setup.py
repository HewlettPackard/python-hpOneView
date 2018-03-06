# -*- coding: utf-8 -*-
###
#  (C) Copyright (2012-2017) Hewlett Packard Enterprise Development LP
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


from setuptools import find_packages
from setuptools import setup

setup(name='hpOneView',
      version='4.5.0',
      description='HPE OneView Python Library',
      url='https://github.com/HewlettPackard/python-hpOneView',
      download_url="https://github.com/HewlettPackard/python-hpOneView/tarball/v4.5.0",
      author='Hewlett Packard Enterprise Development LP',
      author_email='oneview-pythonsdk@hpe.com',
      license='MIT',
      packages=find_packages(exclude=['examples*', 'tests*']),
      keywords=['oneview', 'hpe'],
      install_requires=['future>=0.15.2'])
