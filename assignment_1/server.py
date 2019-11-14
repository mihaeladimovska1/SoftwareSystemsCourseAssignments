#!usr/bin/env python3

import socket
import threading
import sys
import signal
import logging
import os
from subprocess import Popen, PIPE, check_output
import logger_setup
from create_index import create_index


HOST, PORT = '', 8888
logger = logging.getLogger(__name__)


class Server(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.valid_methods = ["GET", "POST"]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.root_dir = os.path.curdir
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def ErrorPage(self, path, msg):
        rv = "\n<html>\n<body>\n<h1>Error accessing {path}</h1>\n<p><h3>{msg}</h3></p>\n</body>\n</html>\n"
        return rv.format(path=path, msg=msg)

    def start_server(self):
        try:
            self.sock.bind((self.host, self.port))
            logger.info("Server listening on port: %d" % self.port)
            self.listen()

        except Exception as e:
            logger.error("Server could not bind to port %d" % self.port)
            self.close_server()
            sys.exit(1)

    def close_server(self):
            logger.info("Closing server")
            self.sock.shutdown(socket.SHUT_RDWR)
            sys.exit(0)

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target=self.listenToClient, args=(client, address)).start()


    # create header for the status of the request; the status can be 200 or 404; if image is requested content type is changed
    def header_creation(self, status, img_check=False):

        header = ''
        if status == 200 and img_check is False:
            header += 'HTTP/1.0 200 OK\n'
            header += 'Content-Type: text/html\n\n'

        if status == 200 and img_check is True:
            header += 'HTTP/1.0 200 OK\n'
            header += 'Content-Type: image/apng\n\n'

        if status == 404:
            header += 'HTTP/1.0 404 Not Found\n'
            header += 'Content-Type: text/html\n\n'
        return header

    def query_parsing(self, request):
        print(request)
        check_request_type = request.split(' ')[0]
        if check_request_type not in self.valid_methods:
            logger.info("Invalid HTTP Request")
            print(check_request_type)
            return False

        file_name = request.split(' ')[1]
        file_name = file_name[1:]
        logger.info(file_name)
        if file_name == "":
            file_path = "www/index.html"
        else:
            if "cgi-bin" in file_name and ".py" in file_name:
                print("RDIR", self.root_dir)
                if file_name.count("cgi-bin") > 1:
                    print(file_name.split('/'))
                    file_path = "cgi-bin/" + file_name.split('/')[-1]
                else:
                    file_path = file_name
            elif "cgi-bin" in file_name and ".html" in file_name:
                file_path = "www/" + file_name.split('/')[-1]
            else:
                file_path = "www/" + file_name

        logger.info("File requested: %s" % file_path)
        return file_path, check_request_type

    def parse_get(self, req):
        """get method puts query info in the URL"""
        url = req.split("?")
        tmp = url[-1]
        args = tmp.split("&")
        print("args: ", args)
        return url[0], args

    def parse_post(self, req):
        url = req.split('\r\n\r\n')
        tmp = url[-1]
        args = tmp.split("&")
        print("args: ", args)
        return args

    def run_cgi(self, full_path, req_type, req):
        t1 = False
        if req_type == "POST":
            p = full_path
            t1 = self.parse_post(req)
        elif "?" in full_path:
            p, t1 = self.parse_get(full_path)
        else:
            p = full_path
        cmd = ['python3', p]
        if t1 is not False:
            for i in t1:
                cmd.append(i)
        data = check_output(cmd)
        print(data)
        return data

    def listenToClient(self, client, address):
        size = 4194304
        while True:
            request = client.recv(size).decode()
            parsed_request, req_type = self.query_parsing(request)
            # if invalid request:
            if parsed_request == False:
                response_str = self.header_creation(404, False)
                response = response_str.encode()
            elif "cgi-bin" and ".py" in parsed_request:
                response_str_2 = self.run_cgi(parsed_request, req_type, request)
                response_str_1 = self.header_creation(200, False)
                response = response_str_1.encode()
                response += response_str_2

            elif "index.html" in parsed_request:
                # calling create index file method within www directory
                create_index(self.root_dir + '/www/')
                response_str_1 = self.header_creation(200, False)
                f = open(self.root_dir + '/www/index.html', 'rb')
                response_str_2 = f.read()
                f.close()

                response = response_str_1.encode()
                response += response_str_2

            #a file is requested
            else:
                # if file is an image of these types, generate the appropriate header type
                extensions = ['.gif', '.png', '.jpg', '.jpeg']
                # get the filename extension
                ext = os.path.splitext(parsed_request)[1]
                if ext in extensions:
                    response_str_1 = self.header_creation(200, True)
                    f = open(parsed_request, 'rb')
                    response_str_2 = f.read()
                    f.close()
                    response = response_str_1.encode()
                    response += response_str_2
                # file requested is a txt or html file, generate appropriate header type
                else:

                    try:
                        f = open(parsed_request, 'rb')
                        response_str_1 = self.header_creation(200)
                        response_str_2 = f.read()
                        f.close()
                        response = response_str_1.encode()
                        response += response_str_2
                    except FileNotFoundError:
                        response_str_1 = self.header_creation(404)
                        response = response_str_1.encode()
                        response += self.ErrorPage(path=parsed_request.split('/')[-1], msg="404: Not found").encode()
                        logger.error(response)

            # logger.debug(response)
            client.send(response)
            client.close()
            break


if __name__ == "__main__":
    argCount = 2
    if len(sys.argv) < argCount:
        print("Please input the port number as a command line argument.")
        sys.exit(0)
    try:
        port_num = int(sys.argv[1])

    except ValueError:
        port_num = PORT
        pass


    def close_server_handler(sig, unused):
        server.close_server()
        sys.exit(1)


    signal.signal(signal.SIGINT, close_server_handler)

    server = Server('', port_num)
    server.start_server()
