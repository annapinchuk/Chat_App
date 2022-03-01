import threading
import unittest
from unittest import TestCase

import client1
from Client import Client
from Server import Server


def create_chat():
    server = Server(50000, 'b', 15, "127.0.0.1")
    # Thread to server receive
    server_thread = threading.Thread(target=server.run)
    server_thread.start()

    # First Client
    client1 = Client('127.0.0.1')
    client1in_thread = threading.Thread(target=client1.connect)
    client1in_thread.start()
    # Thread to client receive
    client1r_thread = threading.Thread(target=client1.receive)
    client1r_thread.start()
    client1.write_to_all()

    # Second Client
    client2 = Client('127.0.0.1')
    client2in_thread = threading.Thread(target=client2.connect)
    client2in_thread.start()
    # Thread to client receive
    client2r_thread = threading.Thread(target=client2.receive)
    client2r_thread.start()
    client2.write_to_all()

    # Third Client
    client3 = Client('127.0.0.1')
    client3in_thread = threading.Thread(target=client3.connect)
    client3in_thread.start()
    # Thread to client receive
    client3r_thread = threading.Thread(target=client3.receive)
    client3r_thread.start()
    client3.write_to_all()


class server_client_test(unittest.TestCase):

    def receiveTest(self):
        create_chat()
        list2 = client1.Client.list_of_users
        list1 = ['anna', 'roy', 'niv']
        self.assertEqual(list1, list2)  # add assertion here



