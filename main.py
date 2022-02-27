import threading
from Client import Client
from Server import Server


client1 = Client('127.0.0.1')
client1.connect()
# Thread to client receive
client1r_thread = threading.Thread(target=client1.receive)
write_thread = threading.Thread(target=client1.write_to_all())
write_thread.start()
client1r_thread.start()



