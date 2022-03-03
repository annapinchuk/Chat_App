import pickle
import socket
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
        self.file = {}  # {seq:datagrams}[]
        self.port = port
        # starting the sever
        self.soc = socket(AF_INET, SOCK_STREAM)
        self.soc.bind((host, port))
        self.bool_file = True
        self.downloading = False
        self.udp_sock = {}  # address is unique -> socket

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

            # Return a list of the online users
            elif data.startswith("<get_list_file>"):
                files = []
                for f in self.file:
                    files.append(self.file[f])
                return files

            elif data.startswith("<download>"):
                data = data.removeprefix("<download>")
                username, filename = data.split(',')
                self.put_file(filename)
                self.send_file((address[0], 55000), filename)

            elif data.startswith("<set_msg>"):
                data = data.removeprefix("<set_msg>")
                user, tmp = data.split(',')
                msg = "<msg>" + tmp + " (private)"
                self.send_to_one(self.get_key(user), msg)  # send to target
                self.send_to_one(address, msg)  # display on source

    def send_file(self, client_addr: tuple, file_name):
        conn = self.udp_handshake(client_addr)
        while not conn:
            conn = self.udp_handshake(client_addr)

        send_seq = 0  # number of pkts
        sock = self.udp_sock[client_addr]
        size = len(self.file)
        print(f'size of pkts list = {size}')
        ack = ''
        while ack != 'FIN':
            if send_seq < size:
                pkt = pickle.dumps((send_seq, self.file[send_seq]))
                sock.sendto(pkt, client_addr)
            try:
                ack, addr = sock.recvfrom(1024)
            except timeout as to:
                print('timeout!')
                continue
            ack = ack.decode()
            if int(ack) == send_seq:
                send_seq += 1

        # sock_udp = socket(AF_INET, SOCK_DGRAM)
        # sock_udp.bind(('127.0.0.1', 55000))
        # seq = 0
        # print(self.file)
        # while True:
        #     data, addr = sock_udp.recvfrom(5)
        #     if data.decode() == "start":
        #         print(self.file)
        #         self.downloading = True
        #         while len(self.file.keys()):
        #             sock_udp.sendto(seq.to_bytes(5, "big")+self.file[seq], addr)
        #             data, addr = sock_udp.recvfrom(5)
        #             key = int.from_bytes(data, "big")
        #             # check if the key exists
        #             self.file.pop(key)
        #             seq += 1
        #         print("done")
        #         sock_udp.sendto("done!".encode(), addr)

    def udp_handshake(self, client_addr: tuple):
        try:
            sock_udp = socket(AF_INET, SOCK_DGRAM)
            self.udp_sock[client_addr] = sock_udp
            sock_udp.sendto(f'<udp-syn-{len(self.file)}>'.encode(), client_addr)
            sock_udp.settimeout(3)
            syn_ack, addr = sock_udp.recvfrom(1024)
            if client_addr != addr:
                return False
            if syn_ack.decode() == '<udp-synAck>':
                sock_udp.sendto('<udp-ack>'.encode(), client_addr)
                print('udp connection established')
                return True
        except ConnectionResetError as w:
            print(w)
            return False
        except timeout as to:
            print(to)
            return False
        except error as e:
            print(e)
            return False

    # creates dada grams
    def put_file(self, filename):
        with open(filename, "rb") as file:
            packet = file.read(1024)
            ind = 0
            while packet:
                self.file[ind] = packet
                ind += 1
                packet = file.read(1024)

    def broadcast(self, message):
        for address in self.addresslist:
            self.soclist[address].send(message.encode())

    def send_to_one(self, address, message):
        self.soclist[address].send(message.encode())

    # get the key of given value
    def get_key(self, val):
        for key, value in self.userslist.items():
            if val == value:
                return key
        return "key doesn't exist"



if __name__ == '__main__':
    djd = {1:'a', 9:'b', 3:'c', 8:"d"}
    djd = sorted(list(djd.items()), key=lambda x: x[0])
    print(djd)
