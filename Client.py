import pickle
import sys
import threading
import time
import socket
from socket import *


class Client:
    def __init__(self, host):
        self.server_addr = ('127.0.0.1', 50000)
        self.host = host
        self.pkts = []  # (seq, data)
        self.username = input("Choose your nickname: ")
        self.sock_udp = None
        self.pkts_size = None  # size of data grams in file,String
        # starting the client
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

    # sending request to connect
    def connect(self):
        msg = "<connect>" + self.username
        self.soc.send(msg.encode())

    # sending request to disconnect
    def disconnect(self):
        msg = "<disconnect>" + self.username
        self.soc.send(msg.encode())

    # sending request to see online members
    def list_of_users(self):
        msg = "<get_users>" + self.username
        self.soc.send(msg.encode())

    # sending request to see available files
    def list_of_files(self):
        msg = "<get_files>" + self.username
        self.soc.send(msg.encode())

    # sending request to send massage to all online members
    def write_to_all(self):
        msg = self.username + " : " + input("")
        message = '<set_msg_all>' + msg
        self.soc.send(message.encode())

    # sending request to send massage to one member
    def write_to_user(self, user):
        msg = self.username + " : " + input("")
        message = '<set_msg>' + user + "," + msg
        self.soc.send(message.encode())

    # sending request to download a file
    def request_download(self):
        file_name = input("\ntype the name of the file you want to download\n")
        msg = '<download>' + self.username + ',' + file_name
        self.soc.send(msg.encode())
        th = threading.Thread(target=self.get_file, args=[file_name, ])
        th.start()
        th.join()

    # TCP receive function
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
                    print('the online users are:' + data)
                elif data.startswith("<files>"):
                    data = data.removeprefix("<files>")
                    print(data)
                else:
                    print(data)

    # receiving file in UDP connection from server
    def get_file(self, file_name):
        conn = self.udp_handshake()
        while not conn:  # while the connection is not stable ask for connection
            conn = self.udp_handshake()

        file_data = {}  # dict (seq: data)
        addr = None
        isstop = False
        while (len(file_data) != int(self.pkts_size)) and (not isstop):
            pkt = None
            try:
                pkt, addr = self.sock_udp.recvfrom(2000)  # receive 2000 bytes
            except timeout:
                print('time out!')
            if pkt is not None:
                seq, data = pickle.loads(pkt)  # convert bytes to objects
                if seq not in file_data.keys():
                    file_data[seq] = data
                    print(f'client received pkt seq {seq}')
                    print('sending ack!')
                self.sock_udp.sendto(str(seq).encode(), addr)
            if int(seq) == int(int(self.pkts_size) / 2):  # asks to stop after 50%
                stop = input("Do you want to continue? type YES/NO \n")
                if stop == "NO":
                    self.sock_udp.sendto('NOFIN'.encode(), addr)
                    print("You stopped the downloading \n")
                    isstop = True
                    break
                elif stop == "YES":
                    pass
        if isstop is False:
            self.sock_udp.sendto('FIN'.encode(), addr)
            name, filetype = str(file_name).split(".")
            last = file_data[int(self.pkts_size) - 1]
            self.write_file(file_data, filetype)
            last = bytes(last)
            if (filetype != "mp4") and (filetype != "mp3") and (filetype != "png"):
                print('file downloaded!, your file is in "files" dictionary' + " the last byte is: " + bytes(
                    last[-8:]).decode())  # prints the last byte
            else:
                print('file downloaded!, your file is in "files" dictionary')

    # write file to given place in computer
    def write_file(self, file_data: dict, filetype):
        file_data = sorted(list(file_data.items()), key=lambda x: x[0])
        if filetype == "png":
            # $$change code here to save where ever you want$$
            file = open('C:/Users/אנהפינצוק/Desktop/תואר/שנה_ב/מונחה עצמים/Chat_App/files/client_received.png', 'wb')
            for seq, data in file_data:
                file.write(data)
        elif filetype == "txt":
            # $$change code here to save where ever you want$$
            file = open('C:/Users/אנהפינצוק/Desktop/תואר/שנה_ב/מונחה עצמים/Chat_App/files/client_received.txt', 'wb')
            for seq, data in file_data:
                file.write(data)
        elif filetype == "gif":
            # $$change code here to save where ever you want$$
            file = open('C:/Users/אנהפינצוק/Desktop/תואר/שנה_ב/מונחה עצמים/Chat_App/files/client_received.gif', 'wb')
            for seq, data in file_data:
                file.write(data)
        elif filetype == "mp3":
            # $$change code here to save where ever you want$$
            file = open('C:/Users/אנהפינצוק/Desktop/תואר/שנה_ב/מונחה עצמים/Chat_App/files/client_received.mp3', 'wb')
            for seq, data in file_data:
                file.write(data)
        elif filetype == "mp4":
            # $$change code here to save where ever you want$$
            file = open('C:/Users/אנהפינצוק/Desktop/תואר/שנה_ב/מונחה עצמים/Chat_App/files/client_received.mp4', 'wb')
            for seq, data in file_data:
                file.write(data)
        file.close()

    def sq_not_in_pkts(self, sq_num):  # return True if the sq number is new
        for index in self.pkts:
            if self.pkts[index] == sq_num:
                return False

    # |server syn|->|client ack syn|->|sever ack|
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
