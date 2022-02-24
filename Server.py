import threading
from socket import *


class Server:
    # Create server
    def __init__(self, port, file, sok_range, host):
        self.userslist = []  # {username:client soc}[]
        self.clientslist = []
        self.host = host
        self.sok_range = sok_range
        self.file = []  # {filename:file}[]
        self.port = port
        # starting the sever
        self.soc = socket(AF_INET, SOCK_STREAM)
        self.soc.bind((host, port))
        self.soc.listen(5)

    def run(self):
        client_soc, address = self.soc.accept()
        while True:
            client_soc, addres = self.soc.accept()
            data = client_soc.recv(1024).decode()
            print(data)
            if not data: break
            # connect to server
            if data.startswith("<connect>"):
                data = data.removeprefix("<connect>")
                self.userslist.append(data)
                self.clientslist.append(client_soc)
                print(data, "is connected")
                msg = "<msg>" + data + "is connected"
                self.broadcast(msg)
            # send message to all clients
            if data.startswith("<set_msg_all>"):
                data = data.removeprefix("<set_msg_all>")
                msg = "<msg>" + data
                print(msg)
                self.broadcast(msg)

    def broadcast(self, message):
        for client in self.clientslist:
            client.send(message.encode())

    # def run_udp(self):

# if __name__ == '__main__':
#     server = Server(50000, 'b', 15, "127.0.0.1")
#     server.run_tcp()
