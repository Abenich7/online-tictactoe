import socket
import multiprocessing
from MySocket import MySocket
#from ClientThread import ClientThread
#from DataStack import DataStack
import threading
import time
import csv

MAIN_ADDRESS = '127.0.0.1'
MAIN_PORT = 3000

#counter =0
#def handle_client(client_socket, data_stack, address):
 #   """Handle individual client in a thread"""
  #  try:
   #     client_thread = ClientThread()
       #client_thread.run(client_socket)
    #    client_thread.start()
     #   client_thread.join()
    #finally:
     #   client_socket.close()

data_str="hello"

def client_thread_communication(client_socket,child_socket):
    while True:
       
       
       # data_str=str(data)
        #print(data_str)
        client_socket.mysend(data_str.encode('utf-8'))
        #client_socket.mysend(bytes(available_ports + "\n", "utf-8"))
        data_recv=client_socket.myreceive()
        
        print("Received: {}".format(data_recv.decode("utf-8")).strip())
        print('hello')
        time.sleep(1)
        #client_socket.close()
        #wait for new client to connect to running thread

        #client_socket_temp, address = child_socket.myaccept()
        #client_socket = MySocket(sock=client_socket_temp)
        #client_socket.listen(5)
        #client_socket.accept()

        #client_socket.myreceive = str((1024), "utf-8")
        # client_socket.send(str(available_ports).encode())
            
      #  client_socket.close()
    

def child_server(port):
    """
    Run a child server process that can accept multiple clients.
    Each client is handled in its own thread.
    """
    try:
        # Create server socket for this child process
        child_socket = MySocket()
        child_socket.bind((MAIN_ADDRESS, port))
        child_socket.listen(5)  # Allow multiple pending connections
        
        # Shared DataStack for all clients connecting to this child server
       # data_stack = DataStack()
        
        print(f"[*] Child server started on port {port}")
        
        threads = []
        while True:
            try:
                #accept socket connection from client
                client_socket_temp, address = child_socket.myaccept()
                client_socket = MySocket(sock=client_socket_temp)
                print(f"[*] Child server on port {port} accepted connection from {address}")
                #dispatch a new thread to handle the client
                client_thread=threading.Thread(group=None,target=client_thread_communication,args=[client_socket,child_socket])
                client_thread.start()
                client_thread.join()

                #handle_client(client_socket, data_stack, address)
                #client_thread.start()
               
                threads.append(client_thread)
                
                # Clean up completed threads
                threads = [t for t in threads if t.is_alive()]
                
            except Exception as e:
                print(f"[!] Error accepting client in child server: {e}")
                
    except Exception as e:
        print(f"[!] Error in child server: {e}")
    finally:
        child_socket.close()

def main():
    # List to store child server processes
    child_servers = []
    
    try:
        # Create multiple child servers on different ports
        start_port = MAIN_PORT + 1
        num_child_servers = 3  # Adjust as needed
        
        for i in range(num_child_servers):
            port = start_port + i
            process = multiprocessing.Process(
                target=child_server,
                args=(port,)
            )
            process.start()
            child_servers.append(process)
            print(f"[*] Started child server process on port {port}")
        
        # Main server to provide information about available child servers
        main_socket = MySocket()
        main_socket.bind((MAIN_ADDRESS, MAIN_PORT))
        main_socket.listen(1)
        
        print(f"[*] Main server listening on {MAIN_ADDRESS}:{MAIN_PORT}")
        
        while True:
            try:
                # When a client connects to main server, send them the list of available child servers
                client_socket_temp, address = main_socket.myaccept()
                client_socket = MySocket(sock=client_socket_temp) 
                print(f"[*] Main server received connection from {address}")
                
                # Send list of available child server ports
                available_ports = [start_port + i for i in range(num_child_servers)]
                available_ports_str=str(available_ports)
                print(available_ports_str)
                client_socket.mysend(available_ports_str.encode('utf-8'))
                #client_socket.mysend(bytes(available_ports + "\n", "utf-8"))
                data_recv=client_socket.myreceive()
                print("Received: {}".format(data_recv.decode("utf-8")).strip())
                #client_socket.myreceive = str((1024), "utf-8")
               # client_socket.send(str(available_ports).encode())
            
                client_socket.close()
                
            except KeyboardInterrupt:
                print("\n[*] Shutting down servers")
                break
            except Exception as e:
                print(f"[!] Error in main server: {e}")
                continue
                
    finally:
        # Clean up
        for process in child_servers:
            process.terminate()
            process.join()
        main_socket.close()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
#while True:
    #steps to implement:
    #1. accept connection from client
    #2. fork a child server to handle the client
    #3. create a new thread to handle the client
    #4. wait for another client to connect and repeat step 3
    #5. instantiate DataStack object in child process to be accessed by threads 
    #6. repeat steps 1-5 until all clients are connected
    

    # fork a child server when a client connects
    
    
    #override accept method to fork a new server process
    #(clientsocket, address) = server.accept()
    #clientsocket=MySocket(clientsocket)
    #print(f"[*] Accepted connection from {address}")
    # create new thread to handle client
    #ct=ClientThread(clientsocket)

    #ct.start()





