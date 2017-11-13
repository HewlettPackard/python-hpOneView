#!/usr/bin/env python3

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

from hpOneView.oneview_client import OneViewClient
from base64 import b64encode
from functools import partial
from pprint import pprint

import amqp
import amqp.spec
import datetime
import http
import json
import ssl
import time

smhost = None
smhead = None


def sm_do_http(method, path, body):
    while True:
        try:
            conn = http.client.HTTPConnection(smhost)
            conn.request(method, path, body, smhead)
            resp = conn.getresponse()
            body = resp.read().decode('utf-8')
            if body:
                try:
                    body = json.loads(body)
                except ValueError:
                    body = resp.read().decode('utf-8')
                conn.close()
                break
        except http.client.BadStatusLine:
            print('Bad Status Line. Trying again...')
            conn.close()
            time.sleep(1)
            continue
    return resp, body


def sm_get(uri):
    resp, body = sm_do_http('GET', uri, '')
    if resp.status >= 400:
        print('Error %s\n' % resp.status)
    return body


def sm_put(uri, body):
    resp, body = sm_do_http('PUT', uri, json.dumps(body))
    if resp.status >= 400:
        print('Error %s\n' % resp.status)
    return body


def sm_post(uri, body):
    resp, body = sm_do_http('POST', uri, json.dumps(body))
    if resp.status >= 400:
        print('Error %s\n' % resp.status)
    return body


def sev_to_urgency(sev):
    return {'OK': '3',
            'Warning': '2',
            'Critical': '1'}.get(sev, 3)


def new_incident(desc, sev):
    body = {'Incident': {'Area': 'hardware',
                         'AssignmentGroup': 'Service Manager',
                         'Category': 'incident',
                         'Description': desc,
                         'Impact': '4',
                         'Service': 'MyDevices',
                         'Subarea': 'hardware failure',
                         'Title': 'OneView Alert',
                         'Urgency': sev_to_urgency(sev)}}
    body = sm_post('/SM/9/rest/incidents', body)
    return body


def print_alert(uri):
    alerts = oneview_client.alerts.get_all()
    for alert in alerts:
        if alert['uri'] == uri:
            pprint(alert)


def update_alert(uri, smid):
    alerts = oneview_client.alerts.get_all()
    notes = 'Case automatically loged in HPE Service Manager with ID: ' + smid
    for alert in alerts:
        if alert['uri'] == uri:
            oneview_client.alerts.update(create_alert_map(notes, alert['eTag']), alert['uris'])
            return True
    return False


def create_alert_map(notes, etag):
    return {
        'alertState': 'Active',
        'assignedToUser': 'None',
        'alertUrgency': 'None',
        'notes': notes,
        'eTag': etag
    }


def get_incidents():
    body = sm_get('/SM/9/rest/incidents?&view=expand')
    pprint(body)


def callback(channel, msg):
    # ACK receipt of message
    channel.basic_ack(msg.delivery_tag)

    # Convert from json into a Python dictionary
    body = json.loads(msg.body)

    # Create a new variable name 'resource' to point to the
    # nested resource dictionary inside of the body
    resource = body['resource']

    # Test to make sure that there is an alertState key
    # in the resource dictionary, if there is continue
    if 'alertState' in list(resource.keys()):
        # Filter only "Active" alerts
        if (('Active' == resource['alertState']) and
                ('Critical' == resource['severity']) and
                ('Created' == body['changeType'])):
            # Print out the requested information
            print('')
            print('original OneView alert:')
            print('------------------------------------------')
            print('changeType: %s' % (body['changeType']))
            print('data: %s' % (body['data']))
            print('eTag: %s' % (body['eTag']))
            print('newState: %s' % (body['newState']))
            print('resourceUri: %s' % (body['resourceUri']))
            print('resource:')
            print('------------------------------------------')
            print('    alertState: %s' % (resource['alertState']))
            print('    alertTypeID: %s' % (resource['alertTypeID']))
            print('    description: %s' % (resource['description']))
            print('    changeLog: %s' % (resource['changeLog']))
            print('    severity: %s' % (resource['severity']))
            print('    resourceName: %s'
                  % (resource['associatedResource']['resourceName']))
            print('    resourceCategory: %s'
                  % (resource['associatedResource']['resourceCategory']))
            print('    uri: %s' % (resource['uri']))
            # The timestamp from the appliance is in ISO 8601 format, convert
            # it to a Python datetime format instead
            atime = (datetime.datetime.strptime(body['timestamp'],
                                                '%Y-%m-%dT%H:%M:%S.%fZ'))
            # Print the timestamp is a simple format (still in UTC)
            print('timestamp: %s' % (atime.strftime('%Y-%m-%d %H:%M:%S')))
            print('resourceUri: %s' % (body['resourceUri']))
            print('')
            print('Service Manager Incident')
            print('------------------------------------------')
            desc = ('resourceName: ' +
                    resource['associatedResource']['resourceName'] +
                    '\nDescription: ' + resource['description'] +
                    '\ncorrectiveAction: ' + resource['correctiveAction'] +
                    '\nhealthCatagory: ' + resource['healthCategory'])
            ret = new_incident(desc, resource['severity'])
            pprint(ret)
            smid = ret['Incident']['IncidentID']
            ret = update_alert(body['resourceUri'], smid)
            print('logged SMID: %s with uri: %s resourceUri: %s' %
                  (smid, resource['uri'], body['resourceUri']))
            if ret is True:
                print('HPE OneView Alert Notes Updated')
                print('------------------------------------------')
                print_alert(body['resourceUri'])

    # Cancel this callback
    if msg.body == 'quit':
        channel.basic_cancel(msg.consumer_tag)


def recv(host, route):
    # Create and bind to queue
    EXCHANGE_NAME = 'scmb'
    dest = host + ':5671'

    # Setup our ssl options
    ssl_options = ({'ca_certs': 'caroot.pem',
                    'certfile': 'client.pem',
                    'keyfile': 'key.pem',
                    'cert_reqs': ssl.CERT_REQUIRED,
                    'server_side': False})

    # Connect to RabbitMQ
    conn = amqp.Connection(dest, login_method='EXTERNAL', ssl=ssl_options)
    conn.connect()

    ch = conn.channel()
    qname, _, _ = ch.queue_declare()
    ch.queue_bind(qname, EXCHANGE_NAME, route)
    ch.basic_consume(qname, callback=partial(callback, ch))

    # Start listening for messages
    while ch.callbacks:
        ch.wait(amqp.spec.Queue.BindOk)

    ch.close()
    conn.close()


def acceptEULA(oneview_client):
    # See if we need to accept the EULA before we try to log in
    eula_status = oneview_client.connection.get_eula_status()
    try:
        if eula_status is True:
            oneview_client.connection.set_eula('no')
    except Exception as e:
        print('EXCEPTION:')
        print(e)


def getCertCa(oneview_client):
    cert = oneview_client.certificate_authority.get()
    ca = open('caroot.pem', 'w+')
    ca.write(cert)
    ca.close()


def genRabbitCa(oneview_client):
    certificate_ca_signed_client = {
        "commonName": "default",
        "type": "RabbitMqClientCertV2"
    }
    oneview_client.certificate_rabbitmq.generate(certificate_ca_signed_client)


def getRabbitKp(oneview_client):
    cert = oneview_client.certificate_rabbitmq.get_key_pair('default')
    ca = open('client.pem', 'w+')
    ca.write(cert['base64SSLCertData'])
    ca.close()
    ca = open('key.pem', 'w+')
    ca.write(cert['base64SSLKeyData'])
    ca.close()


def main():
    global smhost, smhead, oneview_client

    if amqp.VERSION < (2, 1, 4):
        print("WARNING: This script has been tested only with amqp 2.1.4, "
              "we cannot guarantee that it will work with a lower version.\n")

    parser = argparse.ArgumentParser(add_help=True, description='Usage')
    parser.add_argument('-a', '--appliance', dest='host', required=True,
                        help='HPE OneView Appliance hostname or IP')
    parser.add_argument('-u', '--user', dest='user', required=False,
                        default='Administrator', help='HPE OneView Username')
    parser.add_argument('-p', '--pass', dest='passwd', required=True,
                        help='HPE OneView Password')
    parser.add_argument('-r', '--route', dest='route', required=False,
                        default='scmb.alerts.#', help='AMQP Routing Key')
    parser.add_argument('-g', '--gen', dest='gen', required=False,
                        action='store_true',
                        help='Generate the Rabbit MQ keypair and exit')
    parser.add_argument('-d', '--download', dest='down', required=False,
                        action='store_true',
                        help='Download the required keys and certs then exit')
    parser.add_argument('-s', '--sm', dest='sm', required=True,
                        help='Service Manager Appliance hostname or IP')
    parser.add_argument('-i', '--id', dest='id', required=True,
                        help='Service Manager Username')
    parser.add_argument('-x', '--spass', dest='spass', required=False,
                        default='', help='Service Manager Password')
    parser.add_argument('-l', '--list', dest='lst', required=False,
                        action='store_true',
                        help='List all Service Manager incidents and exit')
    args = parser.parse_args()
    smcred = args.id + ':' + args.spass
    userAndPass = b64encode(str.encode(smcred)).decode('ascii')
    smhead = {'Content-Type': 'application/json;charset=utf-8',
              'Authorization': 'Basic %s' % userAndPass}
    smhost = args.sm + ':13080'

    if args.lst:
        get_incidents()
        sys.exit()

    config = {
        "ip": args.host,
        "credentials": {
            "userName": args.user,
            "password": args.passwd
        }
    }

    oneview_client = OneViewClient(config)
    acceptEULA(oneview_client)

    # Generate the RabbitMQ keypair (only needs to be done one time)
    if args.gen:
        genRabbitCa(oneview_client)
        sys.exit()

    if args.down:
        getCertCa(oneview_client)
        getRabbitKp(oneview_client)
        sys.exit()

    recv(args.host, args.route)


if __name__ == '__main__':
    import sys
    import argparse

    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
