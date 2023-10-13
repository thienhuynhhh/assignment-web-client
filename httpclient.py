#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
     # Extract the first line of the response, which is the status line
        status_line= data.split('\r\n')
        # Split the status line into parts and extract the status code
        status_code = status_line[0].split(' ')
        return status_code[1]

    def get_headers(self,data):
        status_line= data.split("\r\n\r\n") #separate (header) and body
   
        return status_line[0]     #extract header

    def get_body(self, data):
        status_line= data.split("\r\n\r\n")
        return status_line[1]
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            #print(part.decode('utf-8')+"hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')
    def get_host(self,url):
        return urllib.parse.urlparse(url).hostname
    def get_port(self,url):
        port=urllib.parse.urlparse(url).port
        if port is None:
            if urllib.parse.urlparse(url).scheme=="http":
                port=80
            elif urllib.parse.urlparse(url).scheme=="https":
                port=443
        return port
    def get_path(self,url):
        path=urllib.parse.urlparse(url).path
        if path=="":
            path="/"
        return path
    def GET(self, url, args=None):
        code = 500
        body = ""
        host=self.get_host(url) #get host from url
        port=self.get_port(url)   #get port from url
        path=self.get_path(url)  
        request="GET "+path+" HTTP/1.1\r\nHost: "+host+"\r\nConnection: close\r\n\r\n"
        self.connect(host,port)
        self.sendall(request)
        response=self.recvall(self.socket)
        self.close()
        print("**********************The reponse from the server for the GET request of this url "+url+" is:")
        print(response)
        print("*******************end reponse*********************************************************\r\n\r\n\r\n")
        code=int(self.get_code(response))
        body=self.get_body(response)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        host=self.get_host(url) #get host from url
        port=self.get_port(url)   #get port from url
        path=self.get_path(url)  
        if args != None:

            request="POST "+path+" HTTP/1.1\r\nHost: "+host+"\r\nContent-Length: "+str(len(str(args)))+"\r\nContent-Type: application/x-www-form-urlencoded"+"\r\nConnection: close\r\n\r\n"
            request=request+urllib.parse.urlencode(args)
        else:
            request="POST "+path+" HTTP/1.1\r\nHost: "+host+"\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"
        self.connect(host,port)
        self.sendall(request)
        self.socket.shutdown(socket.SHUT_WR)
        response=self.recvall(self.socket)
        self.close()
        print("**********************The reponse  from the server for the POST request of this url "+url+" is:")
        print(response)
        print("*******************end reponse*********************************************************\r\n\r\n\r\n")
        code=int(self.get_code(response))
        body=self.get_body(response)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
