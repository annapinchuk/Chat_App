import threading
from socket import *


class Server:
    # Create server
    def __init__(self, port, file, sok_range, host):
        self.userslist = []  # queue of usernames
        self.threadlist = []  # queue of threads
        self.soclist = []  # queue of sockets
        self.addresslist = []  # list of addresses
        self.host = host
        self.sok_range = sok_range
        self.file = []  # {filename:file}[]
        self.port = port
        # starting the sever
        self.soc = socket(AF_INET, SOCK_STREAM)
        self.soc.bind((host, port))

    def run(self):
        self.soc.listen(5)
        while True:
            client_soc, address = self.soc.accept()
            main_server_thread = threading.Thread(target=self.receive, args=(client_soc, address))
            self.threadlist.append(main_server_thread)
            main_server_thread.start()

    def receive(self, client_soc, address):
        data = client_soc.recv(1024).decode()
        print(data)
        self.soclist.append(client_soc)
        self.addresslist.append(address)
        while True:
            # Connect to server
            if data.startswith("<connect>"):
                data = data.removeprefix("<connect>")
                self.userslist.append(data)
                print(data, "is connected")
                msg = "<msg>" + data + " is connected"
                self.broadcast(msg)

            # Disconnect a specific user from the server
            elif data.startswith("<disconnect>"):
                self.threadlist.pop(0)
                for user, address in self.userslist:
                    if address == client_soc:
                        del self.userslist[user]
                        break
                    self.broadcast("<msg>" + user + "has left the chat !")
                    client_soc.close()


            # Return a list of the online users
            elif data.startswith("<get_users>"):
                online = []
                for user in self.userList:
                    online.append(self.userslist[user])
                return online

            # send message to all clients
            elif data.startswith("<set_msg_all>"):
                data = data.removeprefix("<set_msg_all>")
                msg = "<msg>" + data
                print(msg)
                self.broadcast(msg)

            elif data.startswith("<set_msg>" + "<username>"):
                data = data.removeprefix("<set_msg><")
                # TODO: להפריד בין היוזר לבין ההודעה עצמה ואז לשלוח לקליינט שקשור ליוזר
                tmp = data.removesuffix(">")
                msg = "<msg>" + data

    def broadcast(self, message):
        for soc in self.soclist:
            soc.send(message.encode())

    def send_to_one(self, target, message):
        for client in self.threadlist:
            if client == target:
                target.send(message.encode())

    # def run_udp(self):

# if __name__ == '__main__':
#     server = Server(50000, 'b', 15, "127.0.0.1")
#     server.run_tcp()
