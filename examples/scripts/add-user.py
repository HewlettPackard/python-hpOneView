#!/usr/bin/env python3
###
# (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
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
import sys
if sys.version_info < (3, 2):
    raise Exception("Must use Python 3.2 or later")

import hpOneView as hpov
from pprint import pprint


def acceptEULA(con):
    # See if we need to accept the EULA before we try to log in
    con.get_eula_status()
    try:
        if con.get_eula_status() is True:
            print("EULA display needed")
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


def add_user(sec, name, pswd, roles, fname, email, ophone, mphone, enable):
    # Invert the enable boolean value
    enable = not enable
    roleArray = []

    if len(roles) == 1:
        if roles[0] == 'Full':
            roleArray.append('Infrastructure administrator')
        elif roles[0] == 'RO':
            roleArray.append('Read only')
        else:
            print('Error, invalid role type specified: ', roles[0])
            sys.exit()

    elif len(roles) > 1:
        for role in roles:
            if role == 'Backup':
                roleArray.append('Backup administrator')
            elif role == 'Network':
                roleArray.append('Network administrator')
            elif role == 'Server':
                roleArray.append('Server administrator')
            elif role == 'Storage':
                roleArray.append('Storage administrator')
            else:
                print('Error, invalid role specified: ', role)
                sys.exit()
    else:
        print('Error, invalid role specified: ', roles)
        sys.exit()

    ret = sec.create_user(name, pswd, enable, fname, email, ophone, mphone,
                          roleArray)
    pprint(ret)


def main():
    parser = argparse.ArgumentParser(add_help=True, description='Usage',
                        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-a', dest='host', required=True,
                        help='''
    HP OneView Appliance hostname or IP address''')
    parser.add_argument('-u', dest='user', required=False,
                        default='Administrator',
                        help='''
    HP OneView Username''')
    parser.add_argument('-p', dest='passwd', required=False,
                        help='''
    HP OneView Password''')
    parser.add_argument('-c', dest='cert', required=False,
                        help='''
    Trusted SSL Certificate Bundle in PEM (Base64 Encoded DER) Format''')
    parser.add_argument('-y', dest='proxy', required=False,
                        help='''
    Proxy (host:port format''')
    parser.add_argument('-n', dest='name',
                        required=True,
                        help='''
    The name of the new user account to be created''')
    parser.add_argument('-x', dest='user_pass',
                        required=True,
                        help='''
    The initial password to be assigned to the new user.

    Passwords must be at least 8 characters and not contain any of these
    characters:
              < > ; , \" ' & \\/ | + : = and space ''')
    parser.add_argument('-o', dest='roles',
                        required=True, nargs='+',
                        help='''
    A list of roles to assign the user to. Allowed values are:

        * Full = Full Infrastructure Administrator
        * RO = Read Only
        * Specialized (select one or more roles):
            - Backup = Backup Administrator
            - Network = Network Administrator
            - Server = Server Administrator
            - Storage = Storage Administrator

    For example the user can be assigned as the Infrastructure Administrator
    with full access OR as a user with Read Only access OR as a Specialized
    user with one for more of the specialized roles listed above, encapsulated
    with quotes and seperated by spaces. For example to assign the user to
    the Storage and Network administrator roles it would be specified as:

        -o "Network" "Storage"

    To assign the user to the Infrastructure Administrator role it would be
    specified as:

        -o "Full"''')
    parser.add_argument('-l', dest='full_name', required=False,
                        help='''
    Full name for the user''')
    parser.add_argument('-e', dest='email', required=False,
                        help='''
    Email address of the user''')
    parser.add_argument('-z', dest='ophone', required=False,
                        help='''
    Office phone number''')
    parser.add_argument('-m', dest='mphone', required=False,
                        help='''
    Mobile phone number''')
    parser.add_argument('-d', dest='disable', required=False,
                        action='store_true',
                        help='''
    Disable the account, preventing the user from logging into the
    appliance''')

    args = parser.parse_args()
    credential = {'userName': args.user, 'password': args.passwd}

    con = hpov.connection(args.host)
    sec = hpov.security(con)

    if args.proxy:
        con.set_proxy(args.proxy.split(':')[0], args.proxy.split(':')[1])
    if args.cert:
        con.set_trusted_ssl_bundle(args.cert)

    login(con, credential)
    acceptEULA(con)

    add_user(sec, args.name, args.user_pass, args.roles, args.full_name,
             args.email, args.ophone, args.mphone, args.disable)

if __name__ == '__main__':
    import sys
    import argparse
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
