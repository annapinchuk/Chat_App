import sys
import threading
from socket import *


class Client:
    def __init__(self, host):
        self.port = 0
        self.host = host
        self.username = input("Enter your name: ")
        try:
            self.soc = socket(AF_INET, SOCK_STREAM)
        except socket.error as e:
            print("Error creating socket: %s" % e)
            sys.exit(1)
        try:
            self.soc.connect(('127.0.0.1', 50000))
        except socket.error as e:
            print("Connection error: %s" % e)
            sys.exit(1)

    def connect(self):
        msg = "<connect>" + self.username
        self.soc.send(msg.encode())

    def disconnect(self):
        msg = "<disconnect>" + self.username
        self.soc.send(msg.encode())

    def write_to_all(self):
        while True:
            msg = self.username + " : " + input('<set_msg_all> ')
            message = '<set_msg_all> ' + msg
            self.soc.send(message.encode())

    def write_to_one(self):
        while True:
            msg = self.username + " : " + input('<set_msg>')
            message = '<set_msg>' + '<username>' + msg
            name = message.removeprefix('<set_msg><') + message.removesuffix('>')
            self.soc.send(message.encode())

    def all_onlineUsers(self):
        while True:
            msg = self.username + " : " + input('<get_users>')
            message = '<get_users>' + msg
            self.soc.send(message.encode())

    def receive(self):
        while True:
            data = self.soc.recv(1024).decode()
            if not data: break
            if data.startswith("<msg>"):
                data = data.removeprefix("<msg>")
                print(data)

#