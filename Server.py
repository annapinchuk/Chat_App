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
            data = client_soc.recv(1024).decode()
            print(data)
            if not data: break

            # Connect to server
            if data.startswith("<connect>"):
                data = data.removeprefix("<connect>")
                self.userslist.append(data)
                self.clientslist.append(client_soc)
                print(data, "is connected")
                msg = "<msg>" + data + " is connected"
                self.broadcast(msg)

            # Disconnect a specific user from the server
            if data.startswith("<disconnect>"):
                self.clientslist.remove(client_soc)
                for user, address in self.userslist:
                    if address == client_soc:
                        del self.userslist[user]
                        break
                    client_soc.close()
                self.broadcast("<msg>" + user + "has left the chat !")

            # Return a list of the online users
            if data.startswith("<get_users>"):
                online = []
                for user in self.userList:
                    online.append(self.userslist[user])
                return online

            # send message to all clients
            if data.startswith("<set_msg_all>"):
                data = data.removeprefix("<set_msg_all>")
                msg = "<msg>" + data
                print(msg)
                self.broadcast(msg)

            if data.startswith("<set_msg>" + "<username>"):
                data = data.removeprefix("<set_msg><")
                # TODO: להפריד בין היוזר לבין ההודעה עצמה ואז לשלוח לקליינט שקשור ליוזר
                tmp = data.removesuffix(">")
                msg = "<msg>" + data

    def broadcast(self, message):
        for client in self.clientslist:
            client.send(message.encode())

    def send_to_one(self, target, message):
        for client in self.clientslist:
            if client == target:
                target.send(message.encode())

    # def run_udp(self):

# if __name__ == '__main__':
#     server = Server(50000, 'b', 15, "127.0.0.1")
#     server.run_tcp()
