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

# Reference: https://stackoverflow.com/questions/9823936/python-how-do-i-know-what-type-of-exception-occurred
# answered by Lauritz V. Thaulow Mar 22 '12 at 14:14, edited by Community♦ May 23 '17 at 12:34

# Reference: https://stackoverflow.com/questions/2104080/how-to-check-file-size-in-python?rq=1
# answered by danben Jan 20 '10 at 18:59, edited by coldspeed Mar 30 '18 at 2:03

# Reference: https://stackoverflow.com/questions/28387469/python3-last-character-of-the-string
# answered by Martijn Pieters♦ Feb 7 '15 at 21:17, edited by Martijn Pieters♦ Feb 7 '15 at 21:31

# Reference: https://stackoverflow.com/questions/4967580/how-to-get-the-size-of-a-string-in-python
# answered by Igor Bendrup May 16 '16 at 20:06, edited by Max Garner Jun 13 '17 at 0:40
class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("OK",'utf-8'))
        try:
            request_method = self.data.splitlines()[0].decode().split(" ")[0]
        except Exception as e:
            request_method = " "
            print ("error: %s\n" % e)
            pass
        
        if request_method == 'GET':
            file_path = self.data.splitlines()[0].decode().split(" ")[1]
            valid_path, file, real_path = self.valid_path(file_path)
            valid_file_type, file_type = self.valid_file_type(real_path)

            if valid_path and valid_file_type:
                self.return_status("HTTP/1.1 200 OK\n", file_type, "keep-alive", file)

            elif real_path == "www/301_error.html":

                self.return_status("HTTP/1.1 301 Permanently moved\r\n", "html", "closed", file)

            else:
                self.return_status("HTTP/1.1 404 Not Found\r\n", "html", "closed", file)

        else:
            file = open("www/405_error.html").read()
            real_path = "www/405_error.html"
            self.return_status("HTTP/1.1 405 Method Not Allowed\r\n", "html", "closed", file)


    def valid_path(self, file_path):
        try:
            real_path = "www"+file_path
            file = open(real_path).read()
            return True, file, real_path

        except Exception as ex:
            exception_type = type(ex).__name__
            end_character = real_path[-1]
            if exception_type == "IsADirectoryError":
                if end_character != "/":
                    file = "<!DOCTYPE html> <html><body>HTTP/1.1 301 Moved Permanently<br/> Location: %s/ <br/></body></html>"%file_path
                    real_path = "www/301_error.html"
                    return False, file, real_path

                elif end_character == "/":
                    real_path = "www"+file_path+"index.html"
                    try:
                        file = open(real_path).read()
                        return True, file, real_path

                    except:
                        real_path = "www/404_error.html"
                        file = open(real_path).read()
                        return False, file, real_path

            else:
                real_path = "www/404_error.html"
                file = open(real_path).read()
                return False, file, real_path


    def valid_file_type(self, file_path):
        file_type = file_path.split(".")[1]
        if file_type == "html" or file_type == "css":
            return True, file_type
        else:
            return False, "not_valid"


    def return_status(self,status, content_type, connection, content_file):
        self.request.sendall(bytearray(status,'utf-8'))
        self.request.sendall(bytearray("Content-Type: text/%s;\r\n"%content_type,'utf-8'))
        self.request.sendall(bytearray("Connection: %s\r\n\r\n"%connection,'utf-8'))                
        self.request.sendall(bytearray(content_file,'utf-8'))
        return

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()