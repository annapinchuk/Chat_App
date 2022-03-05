import threading
from Client import Client
from Server import Server


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client3 = Client('127.0.0.1')
    client3in_thread = threading.Thread(target=client3.connect)
    client3in_thread.start()
    # Thread to client receive
    client3r_thread = threading.Thread(target=client3.receive)
    client3r_thread.start()
    client3.write_to_all()
    client3.disconnect()
