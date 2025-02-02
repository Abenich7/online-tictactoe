import socket
import selectors
import os
import sys
import threading
from io import BufferedIOBase
from time import monotonic as time
import socketserver
from socketserver import BaseRequestHandler


class RequestHandler1(BaseRequestHandler):
    
    def handle(self):
        self.data=self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        self.request.sendall(self.data.upper())

if __name__=="__main__":
    HOST,PORT="localhost",9999

    with socketserver.TCPServer((HOST,PORT),RequestHandler1) as server:
        server.serve_forever()

        #how to connect to localhost
        