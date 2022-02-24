from socket import *


class Client:
    def __init__(self, host):
        self.port = 0
        self.host = host
        self.username = input("Choose your nickname: ")
        self.soc = socket(AF_INET, SOCK_STREAM)
        self.soc.connect(('127.0.0.1', 50000))

    def connect(self):
        msg = "<connect>" + self.username
        self.soc.send(msg.encode())

    def write_to_all(self):
            msg = self.username + " : " + input()
            message = '<set_msg_all>' + msg
            self.soc.send(message.encode())
