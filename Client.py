import sys
from socket import *


class Client:
    def __init__(self, host):
        self.port = 0
        self.host = host
        self.username = input("Choose your nickname: ")
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

    def list_of_users(self):
        msg = "<get_users>" + self.username
        self.soc.send(msg.encode())

    def write_to_all(self):
        msg = self.username + " : " + input("")
        message = '<set_msg_all>' + msg
        self.soc.send(message.encode())

    def receive(self):
        while True:
            data = self.soc.recv(1024).decode()
            if not data: break
            if data.startswith("<msg>"):
                data = data.removeprefix("<msg>")
                if data.startswith("<users>"):
                    data = data.removeprefix("<users>")
                    names = data.split(",")
                    print(names)
                else:
                    print(data)
