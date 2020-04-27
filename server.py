#!/usr/bin/env python3
"""
Simple http server for zoom webhooks
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
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
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        self._set_response()
        self.wfile.write(b"")

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        message = "{}POST {} request,\nPath: {}\nHeaders:\n{}\n\nBody:\n{}\n".format(bcolors.OKGREEN, bcolors.ENDC, self.path, self.headers, post_data.decode('utf-8'))
        logging.info(message)
        print(message)

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(filename='zoom_meeting.log', filemode='w', level=logging.INFO)

    for i in range(50):
        try :
            server_address = ('', port)
            httpd = server_class(server_address, handler_class)
            break
        except OSError:
            port += 1
            message = f"{bcolors.WARNING}PORT " + str(port-1) + " is unavalible. Trying PORT " + str(port) + f"{bcolors.ENDC}"
            print(message)
            logging.info(message)

    message = f'{bcolors.OKGREEN}Starting HTTP SERVER at PORT ' + str(port) + f'{bcolors.ENDC}'
    print(message)
    logging.info(message)

    try:
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
