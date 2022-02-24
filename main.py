import threading
from Client import Client
from Server import Server


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    server = Server(50000, 'b', 15, "127.0.0.1")
    client1 = Client('127.0.0.1')

    server_thread = threading.Thread(target=server.run)
    server_thread.start()
    client1.connect()
    client1.write_to_all()



