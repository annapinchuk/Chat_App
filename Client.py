import pickle
import sys
import threading
import time
import socket
from socket import *


class Client:
    def __init__(self, host):
        self.server_addr = ('127.0.0.1', 50000)
        self.port = 0
        self.host = host
        self.pkts = []  # (seq, data)
        self.username = input("Choose your nickname: ")
        self.sock_udp = None
        self.pkts_size = None
        try:
            self.soc = socket(AF_INET, SOCK_STREAM)
        except error as e:
            print("Error creating socket: %s" % e)
            sys.exit(1)
        try:
            self.soc.connect(self.server_addr)
        except error as e:
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

    def request_download(self):
        file_name = input("\ntype the name of the file you want to download\n")  # "ro.txt"
        msg = '<download>' + self.username + ',' + file_name
        self.soc.send(msg.encode())
        # time.sleep(5)
        print(file_name)
        threading.Thread(target=self.get_file, args=[file_name, ]).start()

    def get_file(self, file_name):
        conn = self.udp_handshake()
        while not conn:
            conn = self.udp_handshake()

        file_data = {}  # dict (seq: data)
        addr = None

        while len(file_data) != int(self.pkts_size):
            print(f'len of the received {len(file_data)}')
            pkt = None
            try:
                pkt, addr = self.sock_udp.recvfrom(2000)
            except timeout as to:
                print('time out!')
            seq, data = pickle.loads(pkt)
            print(f'client received pkt seq {seq}')
            if seq not in list(file_data.keys()):
                file_data[seq] = data
            print('sending ack!')
            self.sock_udp.sendto(str(seq).encode(), addr)

        self.sock_udp.sendto('FIN'.encode(), addr)
        self.write_file(file_data, file_name)
        print('file downloaded!')

    def write_file(self, file_data: dict, file_name):
        file_data = sorted(list(file_data.items()), key=lambda x: x[0])
        file = open('C:/Users/אנהפינצוק/Desktop/client_received.png', 'wb')
        for seq, data in file_data:
            file.write(data)
        file.close()





    def sq_not_in_pkts(self, sq_num):  # return True if the sq number is new
        for index in self.pkts:
            if self.pkts[index] == sq_num:
                return False

        # file = open("ro1.txt", "wb")
        # socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # socket_udp.sendto("start".encode(), ("127.0.0.1", 55000))
        # while True:
        #     data, addr = socket_udp.recvfrom(505)
        #     seq = data[:5]
        #     #print(seq)
        #     seq = int.from_bytes(seq, "big")
        #     if seq == 431366235425:
        #         break
        #     socket_udp.sendto(seq.to_bytes(5, "big"), addr)
        #     k = data[5:]
        #     file.write(k)
        # file.close()

    def write_to_user(self, user):
        msg = self.username + " : " + input("")
        message = '<set_msg>' + user + "," + msg
        self.soc.send(message.encode())

    def receive(self):
        while True:
            try:
                data = self.soc.recv(1024).decode()
            except error:
                continue
            if not data: break
            if data.startswith("<msg>"):
                data = data.removeprefix("<msg>")
                if data.startswith("<users>"):
                    data = data.removeprefix("<users>")
                    names = data.split(",")
                    print(names)
                else:

                    print(data)

    # |syn|->|ack syn|->|ack| starting from the server
    def udp_handshake(self):
        try:
            self.sock_udp = socket(AF_INET, SOCK_DGRAM)
            self.sock_udp.bind(('127.0.0.1', 55000))
            syn, server_addr = self.sock_udp.recvfrom(1024)
            if server_addr[0] != self.server_addr[0]:
                return False
            self.pkts_size = syn.decode()[9:].removesuffix('>')
            if syn.decode() == f'<udp-syn-{self.pkts_size}>':
                self.sock_udp.settimeout(3)
                self.sock_udp.sendto('<udp-synAck>'.encode(), server_addr)
            ack, server_addr = self.sock_udp.recvfrom(1024)
            if server_addr[0] != self.server_addr[0]:
                return False
            if ack.decode() == '<udp-ack>':
                print('rdt connection established')
                return True

        except timeout as to:
            print(to)
            return False
        except error as e:
            print(e)
            return False

        return True


