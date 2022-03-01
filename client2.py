import threading
from Client import Client
from Server import Server

from datetime import time

import switch as switch

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
    client2.write_to_one()

    # switch case
    isworking = True
    while isworking:

        choise = input("choose one of the following : \n"
                       "1 : send massage to all \n"
                       "2 : send massage to one of users online \n"
                       "3 : see the list of the online users \n"
                       "4 : disconnect from chat \n")
        if choise == '1':
            thread1 = threading.Thread(target=client2.write_to_all)
            thread1.start()
            thread1.join()

        elif choise == '2':
            thread2 = threading.Thread(target=client2.write_to_user, args=input("type the name of the user /n"))
            thread2.start()
            thread2.join()

        elif choise == '3':
            thread3 = threading.Thread(target=client2.list_of_users)
            thread3.start()
            thread3.join()

        elif choise == '4':
            thread4 = threading.Thread(target=client2.disconnect)
            thread4.start()
            thread4.join()
            isworking = False

        else:
            print("pls enter number from 1 to 4")
