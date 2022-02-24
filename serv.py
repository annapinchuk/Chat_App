import threading

from Client import Client
from Server import Server

server = Server(50000, 'b', 15, "127.0.0.1")

# Thread to server receive
server_thread = threading.Thread(target=server.run)
server_thread.start()