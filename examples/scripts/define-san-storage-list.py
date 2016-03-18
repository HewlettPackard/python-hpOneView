#!/usr/bin/env python
###
# (C) Copyright (2012-2015) Hewlett Packard Enterprise Development LP
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
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import range
from future import standard_library
standard_library.install_aliases()
import sys

PYTHON_VERSION = sys.version_info[:3]
PY2 = (PYTHON_VERSION[0] == 2)
if PY2:
    if PYTHON_VERSION < (2, 7, 9):
        raise Exception('Must use Python 2.7.9 or later')
elif PYTHON_VERSION < (3, 4):
    raise Exception('Must use Python 3.4 or later')

import hpOneView as hpov
from pprint import pprint
import json


HOST_OS = {'CitrixXen': 'Citrix Xen Server 5.x/6.x',
           'AIX': 'AIX',
           'IBMVIO': 'IBM VIO Server',
           'RHEL4': 'RHE Linux (Pre RHEL 5)',
           'RHEL3': 'RHE Linux (Pre RHEL 5)',
           'RHEL': 'RHE Linux (5.x, 6.x)',
           'RHEV': 'RHE Virtualization (5.x, 6.x)',
           'VMware': 'ESX 4.x/5.x',
           'Win2k3': 'Windows 2003',
           'Win2k8': 'Windows 2008/2008 R2',
           'Win2k12': 'Windows 2012 / WS2012 R2',
           'OpenVMS': 'OpenVMS',
           'Egenera': 'Egenera',
           'Exanet': 'Exanet',
           'Solaris9': 'Solaris 9/10',
           'Solaris10': 'Solaris 9/10',
           'Solaris11': 'Solaris 11',
           'ONTAP': 'NetApp/ONTAP',
           'OEL': 'OE Linux UEK (5.x, 6.x)',
           'HPUX11iv1': 'HP-UX (11i v1, 11i v2)',
           'HPUX11iv2': 'HP-UX (11i v1, 11i v2)',
           'HPUX11iv3': 'HP-UX (11i v3)',
           'SUSE': 'SuSE (10.x, 11.x)',
           'SUSE9': 'SuSE Linux (Pre SLES 10)',
           'Inform': 'InForm'}


def acceptEULA(con):
    # See if we need to accept the EULA before we try to log in
    con.get_eula_status()
    try:
        if con.get_eula_status() is True:
            print('EULA display needed')
            con.set_eula('no')
    except Exception as e:
        print('EXCEPTION:')
        print(e)


def login(con, credential):
    # Login with givin credentials
    try:
        con.login(credential)
    except:
        print('Login failed')


def define_san(sto, name, san_list, conn_list, append, hostos, lun, del_vol):

    volumes = sto.get_attachable_volumes()
    vol = None
    for volume in volumes['members']:
        if volume['name'] == name:
            vol = volume

    if not vol:
        print('Error, could not locate attachable volume:', name)
        sys.exit(2)

    if lun:
        lun_type = 'Manual'
    else:
        lun_type = 'Auto'

    net_ids = []
    conn = json.loads(open(conn_list).read())
    for item in conn:
        if item['functionType'] == 'FibreChannel':
            net_ids.append(item['id'])

    if not net_ids:
        print('Error, cound not locate FibreChannel connections to attach'
              ' volumes')
        sys.exit()

    paths = []
    for nid in net_ids:
        paths.append(hpov.common.make_StoragePathV2(storageTargetType='Auto',
                                                    storageTargets=[],
                                                    connectionId=nid,
                                                    isEnabled=True))

    vols = hpov.common.make_VolumeAttachmentV2(lun=None,
                                               lunType=lun_type,
                                               volumeUri=vol['uri'],
                                               volumeStoragePoolUri=vol['storagePoolUri'],
                                               volumeStorageSystemUri=vol['storageSystemUri'],
                                               storagePaths=paths)

    san_storage = hpov.common.make_SanStorageV3(HOST_OS[hostos], True, vols)

    if append:
        data = json.loads(open(san_list).read())
        if 'volumeAttachments' not in data:
            print('Error, can not locate exsisting volumeAttachments to '
                  'append')
            sys.exit(3)
        vol_attach = data['volumeAttachments']
        vol_attach.append(vols)
    else:
        data = san_storage
    f = open(san_list, 'w')
    out = json.dumps(data, indent=4)
    f.write(out)
    f.close()


def main():
    parser = argparse.ArgumentParser(add_help=True,
                        formatter_class=argparse.RawTextHelpFormatter,
                                     description='''
    Define a OneView SAN Storage connection list for use with defining a
    server profile with managed SAN storage connections.

    Usage: ''')
    parser.add_argument('-a', dest='host', required=True,
                        help='''
    HP OneView Appliance hostname or IP address''')
    parser.add_argument('-u', dest='user', required=False,
                        default='Administrator',
                        help='''
    HP OneView Username''')
    parser.add_argument('-p', dest='passwd', required=True,
                        help='''
    HP OneView Password''')
    parser.add_argument('-c', dest='cert', required=False,
                        help='''
    Trusted SSL Certificate Bundle in PEM (Base64 Encoded DER) Format''')
    parser.add_argument('-y', dest='proxy', required=False,
                        help='''
    Proxy (host:port format''')
    parser.add_argument('-j', dest='domain', required=False,
                        default='Local',
                        help='''
    HP OneView Authorized Login Domain''')
    parser.add_argument('-sl', dest='san_list',
                        required=True,
                        help='''
    Name of file for SAN storage list''')
    parser.add_argument('-cl', dest='conn_list',
                        required=True,
                        help='''
    Name of server profile connection list file to import''')
    parser.add_argument('-app', dest='append',
                        required=False,
                        action='store_true',
                        help='''
    Causes SAN list to be appended to the file''')
    parser.add_argument('-o', dest='hostos',
                        required=True,
                        choices=['CitrixXen', 'AIX', 'IBMVIO', 'RHEL4',
                                 'RHEL3', 'RHEL', 'RHEV', 'VMware', 'Win2k3',
                                 'Win2k8', 'Win2k12', 'OpenVMS', 'Egenera',
                                 'Exanet', 'Solaris9', 'Solaris10',
                                 'Solaris11', 'ONTAP', 'OEL', 'HPUX11iv1',
                                 'HPUX11iv2', 'HPUX11iv3', 'SUSE', 'SUSE9',
                                 'Inform'],
                        help='''
    Specify the Host OS type, which will set the Host OS value when HP OneView
    created the Host object on the Storage System. Accepted values:

         . CitrixXen = "Citrix Xen Server 5.x/6.x"
         . AIX       = "AIX"
         . IBMVIO    = "IBM VIO Server"
         . RHEL4     = "RHE Linux (Pre RHEL 5)"
         . RHEL3     = "RHE Linux (Pre RHEL 5)"
         . RHEL      = "RHE Linux (5.x, 6.x)"
         . RHEV      = "RHE Virtualization (5.x, 6.x)"
         . VMware    = "ESX 4.x/5.x"
         . Win2k3    = "Windows 2003"
         . Win2k8    = "Windows 2008/2008 R2"
         . Win2k12   = "Windows 2012 / WS2012 R2"
         . OpenVMS   = "OpenVMS"
         . Egenera   = "Egenera"
         . Exanet    = "Exanet"
         . Solaris9  = "Solaris 9/10"
         . Solaris10 = "Solaris 9/10"
         . Solaris11 = "Solaris 11"
         . ONTAP     = "NetApp/ONTAP"
         . OEL       = "OE Linux UEK (5.x, 6.x)"
         . HPUX11iv1 = "HP-UX (11i v1, 11i v2)"
         . HPUX11iv2 = "HP-UX (11i v1, 11i v2)"
         . HPUX11iv3 = "HP-UX (11i v3)"
         . SUSE      = "SuSE (10.x, 11.x)"
         . SUSE9     = "SuSE Linux (Pre SLES 10)"
         . Inform    = "InForm"

    ''')
    parser.add_argument('-n', dest='name', required=True,
                        help='''
    Name of the exsisting storage volume to attach''')
    parser.add_argument('-l', dest='lun_id', required=False,
                        type=int,
                        help='''
    Manual entry for the LUN number. Auto, will be used if this
    value is not specified.''')
    parser.add_argument('-del', dest='del_vol', required=False,
                        action='store_false',
                        help='''
    Indicates that the volume will be deleted when the profile is deleted.''')

    args = parser.parse_args()
    credential = {'authLoginDomain': args.domain.upper(), 'userName': args.user, 'password': args.passwd}

    con = hpov.connection(args.host)
    sto = hpov.storage(con)

    if args.proxy:
        con.set_proxy(args.proxy.split(':')[0], args.proxy.split(':')[1])
    if args.cert:
        con.set_trusted_ssl_bundle(args.cert)

    login(con, credential)
    acceptEULA(con)

    if args.lun_id:
        if args.lun_id < 0 or args.lun_id > 255:
            print('Error: boot lun value must be between 0 and 255')
            sys.exit(1)

    define_san(sto, args.name, args.san_list, args.conn_list, args.append,
               args.hostos, args.lun_id, args.del_vol)


if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
