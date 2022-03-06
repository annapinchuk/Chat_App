import threading
import time
from Client import Client

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ip = input("enter your ip in this format: 0.0.0.0 \n")
    client2 = Client(ip)
    client2in_thread = threading.Thread(target=client2.connect)
    client2in_thread.start()
    # Thread to client receive
    client2r_thread = threading.Thread(target=client2.receive)
    client2r_thread.start()
    # switch case
    isworking = True
    while isworking:
        time.sleep(2)
        choise = input("choose one of the following : \n"
                       "1 : send massage to all \n"
                       "2 : send massage to one of users online \n"
                       "3 : see the list of the online users \n"
                       "4 : see the list of the files \n"
                       "5 : download a file \n"
                       "6 : disconnect from chat \n")
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
            thread4 = threading.Thread(target=client2.list_of_files())
            thread4.start()
            thread4.join()

        elif choise == '5':
            thread4 = threading.Thread(target=client2.request_download())
            thread4.start()
            thread4.join()

        elif choise == '6':
            thread4 = threading.Thread(target=client2.disconnect)
            thread4.start()
            thread4.join()
            isworking = False

        else:
            print("pls enter number from 1 to 6")
