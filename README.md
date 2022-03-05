<img src="https://user-images.githubusercontent.com/92322613/156634960-59bd89e7-5e37-49c3-9fef-51a800687721.png" width="1000" height="250" />


# Chat_App 📱
This is a simple Chat app over TCP with file handeling over reliable UDP as a final project for Network Course.

## <ins>***The Server***<ins> 
  

This class is used to execute the client's requests. 'server.py' contains a set of different fucntions:

  <br />
  
  | **Functions**      |    **Explanation**        |
|-----------------|-----------------------|
| `def run(self):` | Create a connection with the client by openning a socket and using threads. |
| `def receive(self, client_soc, address)` | Receive all the requests of the client. |
| `def send_file(self)` | Send file over UDP protocol. |
| `def broadcast(self, message)` | Send a broadcast message to all online users. |
| `def send_to_one(self, address, message)` | Send a message to a specific client. |


## <ins>***The Client***<ins> 
  
This class is use to communicate with the server in order to create interactions between clients. `client.py` is constituted of several features:  
   <br />
  
  | **Functions**      |    **Explanation**        |
|-----------------|-----------------------|
| `def run(self):` | Create a connection with the client by openning a socket and using threads. |
| `def receive(self, client_soc, address)` | Receive all the requests of the client. |
| `def send_file(self)` | Send file over UDP protocol. |
| `def broadcast(self, message)` | Send a broadcast message to all online users. |
| `def send_to_one(self, address, message)` | Send a message to a specific client. | 
  

## How to run

For running the Chat, you first need to run the `serv.py`, creating a connnection with the client on particular IP and port, the server listens to the client's requests for sending a broadcast message, get all the online users, disconnect a client and serveral other functions. The server is connect to the the ip `127.0.0.1` and to `50000` as a port number. You can also run the server on the command prompt:

    py serv.py
  
 then you will need to run the 'client 1/2/3': client 2 is doing all the functions.
  
    py client 2.py
 
 you can run the clients in the same time and have a nice chat between them.
 
 bugs: somtimes when you dont close the client well you need to kill the process like that:  <br />
 open teminal in the project   <br />
 netstat -ano | find "50000"  <br />
 taskkill /F /PID *add here the reasult from above*  <br />
 
    
Then you can add clients in the Chat, `client.py` contains a lot of features, he sends a key word to the server and the server who is connecting on the same ip,reveive all the queries and execute them. For adding a client on the commamd prompt:

    py client.py
