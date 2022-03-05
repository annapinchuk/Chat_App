import threading

from Client import Client
from Server import Server

server = Server(50000, ['img.png', 'text.txt', 'cat.gif', 'music.mp3', 'playme.mp4'], "127.0.0.1")
# Thread to server receive
server_thread = threading.Thread(target=server.run)
server_thread.start()