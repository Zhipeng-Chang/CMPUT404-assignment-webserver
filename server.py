#  coding: utf-8 
import socketserver

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

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        self.request.sendall(bytearray("OK",'utf-8'))
        try:
            request_method = self.data.splitlines()[0].decode().split(" / ")[0]
            print ("Request method: %s\n" % request_method)
        except Exception as e:
            print ("error: %s\n" % e)
            pass
        
        if request_method == 'GET':
            print("Get method")
        else:
            print("405 Method Not Allowed")




if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
