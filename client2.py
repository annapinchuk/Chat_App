import threading
from Client import Client
from Server import Server


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client2 = Client('127.0.0.1')
    client2in_thread = threading.Thread(target=client2.connect)
    client2in_thread.start()
    # Thread to client receive
    client2r_thread = threading.Thread(target=client2.receive)
    client2r_thread.start()
    client2.list_of_users()
    client2.write_to_all()
    client2.list_of_users()

