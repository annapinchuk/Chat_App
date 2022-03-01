import threading
from socket import *


class Server:
    # Create server
    def __init__(self, port, file, sok_range, host):
        self.userslist = {}  # address is unique -> userlist is string
        self.threadlist = {}  # address is unique -> boolean for if the thread is running
        self.soclist = {}  # address is unique -> socket
        self.addresslist = []  # list of addresses
        self.host = host
        self.sok_range = sok_range
        self.file = {}  # {filename:file}[]
        self.port = port
        # starting the sever
        self.soc = socket(AF_INET, SOCK_STREAM)
        self.soc.bind((host, port))
        self.bool_file = True
        self.downloading = False


    def run(self):
        self.soc.listen(5)
        while True:
            client_soc, address = self.soc.accept()
            main_server_thread = threading.Thread(target=self.receive, args=(client_soc, address))
            self.threadlist[address] = True  # address is unique -> boolean for
            # if the thread is running
            main_server_thread.start()

    def receive(self, client_soc, address):
        self.soclist[address] = client_soc
        self.addresslist.append(address)
        while self.threadlist[address]:
            data = client_soc.recv(1024).decode()
            # Connect to server
            if data.startswith("<connect>"):
                data = data.removeprefix("<connect>")
                self.userslist[address] = data
                print(data, "is connected")
                msg = "<msg>" + data + " is connected"
                self.broadcast(msg)

            # Disconnect a specific user from the server
            elif data.startswith("<disconnect>"):
                self.threadlist[address] = False
                self.broadcast("<msg>" + self.userslist[address] + "  has left the chat !")
                del self.userslist[address]
                del self.soclist[address]
                self.addresslist.remove(address)
                client_soc.close()

            # Return a list of the online users
            elif data.startswith("<get_users>"):
                msg = self.userslist[address]
                for addr in self.addresslist:
                    if addr != address:
                        msg += "," + self.userslist[addr]
                self.send_to_one(address, "<msg>" + "<users>" + msg)

            # send message to all clients
            elif data.startswith("<set_msg_all>"):
                data = data.removeprefix("<set_msg_all>")
                msg = "<msg>" + data
                self.broadcast(msg)

            if data.startswith("<set_msg> <username>"):
                data = data.removeprefix("<set_msg>")
                tmp = data.removesuffix(">")
                msg = "<msg>" + data
                self.send_to_one(tmp, msg)

            # Return a list of the online users
            if data.startswith("<get_list_file>"):
                files = []
                for f in self.file:
                    files.append(self.file[f])
                return files

            if data.startswith("<download>"):
                print("test")
                filename = "ro.txt"
                self.put_file(filename)
                self.send_file()

    def send_file(self):
        sock_udp = socket(AF_INET, SOCK_DGRAM)
        sock_udp.bind(('127.0.0.1', 55000))
        seq = 0
        print(self.file)
        while True:
            data, addr = sock_udp.recvfrom(5)
            if data.decode() == "start":
                print(self.file)
                self.downloading = True
                while len(self.file.keys()):
                    sock_udp.sendto(seq.to_bytes(5, "big")+self.file[seq], addr)
                    data, addr = sock_udp.recvfrom(5)
                    key = int.from_bytes(data, "big")
                    # check if the key exists
                    self.file.pop(key)
                    seq += 1
                print("done")
                sock_udp.sendto("done!".encode(), addr)

    def put_file(self, filename):
        file = open(filename, "rb")
        packet = file.read(500)
        ind = 0
        while packet:
            self.file[ind] = packet
            ind +=1
            packet = file.read(500)

        file.close()

    def broadcast(self, message):
        for address in self.addresslist:
            self.soclist[address].send(message.encode())

    def send_to_one(self, address, message):
        self.soclist[address].send(message.encode())

