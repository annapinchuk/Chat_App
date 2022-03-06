import pickle
import socket
import sys
import threading
from socket import *


class Server:
    #
    # Create server
    def __init__(self, port, files, host):
        self.userslist = {}  # address is unique -> userlist is string
        self.threadlist = {}  # address is unique -> boolean for if the thread is running
        self.soclist = {}  # address is unique -> socket
        self.addresslist = []  # list of addresses
        self.host = host
        self.file = {}  # {seq:datagrams}[]
        self.fileslist = files  # list of files in the server
        self.port = port
        self.udp_sock = {}  # address is unique -> socket

        # starting the sever
        try:
            self.soc = socket(AF_INET, SOCK_STREAM)  # TCP SOCKET
        except error as e:
            print("Error creating socket: %s" % e)
            sys.exit(1)
        try:
            self.soc.bind((host, port))
        except error as e:
            print("Connection error: %s" % e)
            sys.exit(1)

    # runs the server
    def run(self):
        self.soc.listen(5)
        while True:
            client_soc, address = self.soc.accept()
            main_server_thread = threading.Thread(target=self.receive, args=(client_soc, address))
            self.threadlist[address] = True  # address is unique -> boolean for
            # if the thread is running
            main_server_thread.start()

    # receiving tcp connection
    def receive(self, client_soc, address):
        self.soclist[address] = client_soc
        self.addresslist.append(address)
        while self.threadlist[address]:
            try:
                data = client_soc.recv(1024).decode()
            except error as e:
                print(e)
                break
            else:
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
                    print(self.userslist[address] + " left the chat \n")
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

                # Return a list of available files
                elif data.startswith("<get_files>"):
                    msg = str(self.fileslist)
                    self.send_to_one(address, "<msg>" + "<files>" + msg)

                # send message to all clients
                elif data.startswith("<set_msg_all>"):
                    data = data.removeprefix("<set_msg_all>")
                    msg = "<msg>" + data
                    self.broadcast(msg)

                # Return a list of the files
                elif data.startswith("<get_list_file>"):
                    files = []
                    for f in self.file:
                        files.append(self.file[f])
                    return files

                # downloads the wanted file
                elif data.startswith("<download>"):
                    data = data.removeprefix("<download>")
                    username, filename = data.split(',')
                    self.put_file(filename)
                    self.send_file((address[0], 55000))

                # send message in private chat
                elif data.startswith("<set_msg>"):
                    data = data.removeprefix("<set_msg>")
                    user, tmp = data.split(',')
                    msg = "<msg>" + tmp + " (private)"
                    self.send_to_one(self.get_key(user), msg)  # send to target
                    self.send_to_one(address, msg)  # display on source

    # sends given file stop and wait implementation
    def send_file(self, client_addr: tuple):
        conn = self.udp_handshake(client_addr)
        while not conn:
            conn = self.udp_handshake(client_addr)

        send_seq = 0  # number of pkts
        sock = self.udp_sock[client_addr]
        size = len(self.file)
        ack = ''
        i = 0  # timeout index
        while (ack != 'FIN') or (ack != 'NOFIN'):  # send file until the finish syn
            if send_seq < size:
                pkt = pickle.dumps((send_seq, self.file[send_seq]))  # pkt contains seq number and data gram
                sock.sendto(pkt, client_addr)
            try:
                ack, addr = sock.recvfrom(1024)
            except timeout:
                print('timeout!')
                i += 1
                self.udp_sock[client_addr].settimeout(3 + i)
                continue
            ack = ack.decode()
            try:
                i = 0
                if int(ack) == send_seq:
                    send_seq += 1
            except Exception:  # the final ack is "FIN" or "NOFIN
                if str(ack).startswith('FIN'):
                    print('file sent!')
                    ack = 'FIN'
                    break
                else:
                    print('download stoped')
                    break

    # 3 way hand shake starting in the sever
    def udp_handshake(self, client_addr: tuple):
        try:
            sock_udp = socket(AF_INET, SOCK_DGRAM)
            self.udp_sock[client_addr] = sock_udp
            sock_udp.sendto(f'<udp-syn-{len(self.file)}>'.encode(), client_addr)  # sending the size of the file in
            # data grams
            sock_udp.settimeout(3)
            addr = None
            try:
                syn_ack, addr = sock_udp.recvfrom(1024)
            except error as e:
                print(e)
            if client_addr != addr:  # not the client we want
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

    # creates data grams
    def put_file(self, filename):
        file = open(filename, 'rb')
        packet = file.read(1024)
        ind = 0
        while packet:
            self.file[ind] = packet
            ind += 1
            packet = file.read(1024)
        file.close()

    # send message to all online
    def broadcast(self, message):
        for address in self.addresslist:
            self.soclist[address].send(message.encode())

    # send message to one member
    def send_to_one(self, address, message):
        self.soclist[address].send(message.encode())

    # get the key of given value
    def get_key(self, val):
        for key, value in self.userslist.items():
            if val == value:
                return key
        return "key doesn't exist"
