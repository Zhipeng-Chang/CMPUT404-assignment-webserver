#  coding: utf-8 
import socketserver
import os
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/ 

# Rference: https://stackoverflow.com/questions/172439/how-do-i-split-a-multi-line-string-into-multiple-lines
# answered by UnkwnTech Oct 5 '08 at 18:50, edited by Demis Apr 28 '16 at 21:55

# Rference: https://stackoverflow.com/questions/29643544/python-a-bytes-like-object-is-required-not-str
# answered by valentin Apr 15 '15 at 7:03

# Reference: https://stackoverflow.com/questions/18563664/socketserver-python
# answered by sberry Sep 1 '13 at 23:39

# Reference: https://eclass.srv.ualberta.ca/pluginfile.php/4549769/mod_resource/content/2/04-HTTP.pdf
# by Abram Hindle

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        self.request.sendall(bytearray("OK",'utf-8'))
        try:
            request_method = self.data.splitlines()[0].decode().split(" ")[0]
            print ("Request method: %s\n" % request_method)
        except Exception as e:
            request_method = " "
            print ("error: %s\n" % e)
            pass
        
        if request_method == 'GET':
            file_path = self.data.splitlines()[0].decode().split(" ")[1]
            if file_path == "/":
                file_path = "/index.html"

            valid_path, html_file = self.valid_path(file_path)

            if valid_path:
                file_type = file_path.split(".")[1]
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n",'utf-8'))
                self.request.sendall(bytearray("Content-Type: text/%s\r\n"% file_type,'utf-8'))
                self.request.sendall(bytearray("Content-Length: %s\r\n"% len(html_file),'utf-8'))
                self.request.sendall(bytearray("Connection: keep-alive\r\n",'utf-8'))
                self.request.sendall(bytearray(html_file,'utf-8'))

            elif not valid_path:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found!\r\n",'utf-8'))
                self.request.sendall(bytearray("Content-Type: text/html\r\n",'utf-8'))
                self.request.sendall(bytearray("Content-Length: %s\r\n"% len(html_file),'utf-8'))
                self.request.sendall(bytearray("Connection: closed\r\n",'utf-8'))
                self.request.sendall(bytearray(html_file,'utf-8'))

        else:
            html_file = open("www/405_error.html").read()
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))
            self.request.sendall(bytearray("Content-Type: text/html\r\n",'utf-8'))
            self.request.sendall(bytearray("Content-Length: %s\r\n"% len(html_file),'utf-8'))
            self.request.sendall(bytearray("Connection: closed\r\n",'utf-8'))                
            self.request.sendall(bytearray(html_file,'utf-8'))

    def valid_path(self, file_path):
        try:
            html_file = open("www"+file_path).read()
            return True, html_file

        except FileNotFoundError:
            html_file = open("www/404_error.html").read()
            return False, html_file



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
