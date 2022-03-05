import threading
from Client import Client
from Server import Server


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client1 = Client('127.0.0.1')
    client1in_thread = threading.Thread(target=client1.connect)
    client1in_thread.start()
    # Thread to client receive
    client1r_thread = threading.Thread(target=client1.receive)
    client1r_thread.start()
    client1.list_of_files()
    client1.request_download()


