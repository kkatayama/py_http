#!/usr/bin/env python3
"""
Simple http server for zoom webhooks
Usage::
    ./server.py [<port>]
"""
try:
    from http.server import BaseHTTPRequestHandler, HTTPServer
except:
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler as BaseHTTPRequestHandler
try:
    import configparser
except:
    from six.moves import configparser

# import ssl
import tweepy
import urllib.parse
import json
import logging
from gmail import GMail, Message

def get_twurl(medium_url):
    creds = {}
    with open('api_keys') as f:
        for l in f.readlines():
            if l[0].isalpha():
                k,v = l.strip().replace('"', '').split(' = ')
                creds[k] = v

    auth = tweepy.OAuthHandler(creds['api_key'], creds['api_secret_key'])
    auth.set_access_token(creds['access_token'], creds['access_token_secret'])

    api = tweepy.API(auth)
    tweet = api.update_status(medium_url)
    twurl = tweet.entities['urls'][0]['url']

    return twurl.encode('utf-8')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.server_version = 'customHTTP/1.0'
        self.sys_version = ''
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        message = "{}GET {} request,\nPath: {}\nHeaders:\n{}\n".format(bcolors.OKBLUE, bcolors.ENDC, self.path, self.headers)
        logging.info(message)
        print(message)

        # -- blank response 
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        # self._set_response()
        # self.wfile.write(b"")


    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        message = "{}POST {} request,\nPath: {}\nHeaders:\n{}\n\nBody:\n{}\n".format(bcolors.OKGREEN, bcolors.ENDC, self.path, self.headers, post_data.decode('utf-8'))
        logging.info(message)
        print(message)


        # -- get zoom data, send email and sms
        if 'meeting.participant_jbh_joined' in post_data.decode('utf-8'):
            zoom_data = json.loads(post_data.decode('utf-8'))
            config = configparser.ConfigParser()
            config.read('config.ini')
            email = config['gmail']['email']
            password = config['gmail']['password']
            pmail = config['gmail']['pmail']
            mail = GMail(email, password)

            # -- send email
            subject = '{} has joined your Zoom Meeting'.format(zoom_data['payload']['object']['participant']['user_name'])
            msg_body = json.dumps(zoom_data)
            msg = Message(subject, email, text=msg_body)
            mail.send(msg)
            print('sent email...')

            # -- send sms messge
            if pmail == 'NO':
                pass
            else:
                msg = Message(subject, pmail, text='')
                mail.send(msg)
                print('sent sms...')
            self._set_response()
            self.wfile.write("Received zoom webhook".encode('utf-8'))
        elif 'tweet' in post_data.decode('utf-8'):
            medium_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            twurl = get_twurl(medium_data['tweet'][0])
            print("\n{}\n".format(medium_data['tweet']))
            self._set_response()
            self.wfile.write(twurl)
        else:
            self._set_response()
            self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=8888):
    logging.basicConfig(filename='zoom_meeting.log', filemode='w', level=logging.INFO)

    for i in range(50):
        try :
            break
        except OSError:
            port += 1
            message = "{}PORT {} is unavalible. Trying PORT {}{}".format(bcolors.WARNING, port-1, port, bcolors.ENDC)
            print(message)
            logging.info(message)

    message = '{}Starting HTTP SERVER at PORT {}{}'.format(bcolors.OKGREEN, port, bcolors.ENDC)
    print(message)
    logging.info(message)

    try:
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        # httpd.socket = ssl.wrap_socket(httpd.socket, certfile="server.pem", server_side=True)
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    message = 'Stopping httpd...\n'
    print(message)
    logging.info(message)

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
