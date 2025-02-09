import socket
from MySocket import MySocket
import time
import csv
#import threading



HOST, PORT = "127.0.0.1", 3002

#client=MySocket()

#semaphore=threading.Semaphore(1)

def client_thread():

    client=MySocket()
    client.connect((HOST, PORT))
    
    while True:
        try:
            

            #semaphore.acquire()
            data_recv=client.myreceive()
            print("Received: {}".format(data_recv.strip()))
        
            #client.myreceive = str((1024), "utf-8")
        

            # Read data from data.csv
            with open('data.csv', mode='r') as file:
                reader = csv.reader(file)
                data = list(reader)
            
            data = str(data)
            client.mysend(data.encode('utf-8'))
            #client.mysend(bytes(data + "\n", "utf-8"))
            time.sleep(1)
        
        finally:
            print("Sent:     {}".format(data))
           # semaphore.release()

client_thread()






#print("Sent:     {}".format(data))
#print("Received: {}".format(received))


#setup functions to handle client functionality
def send_data(data):
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data + "\n", "utf-8"))
        received = str(sock.recv(1024), "utf-8")
        #save data to file
        with open("received_data.csv", "w") as f:
            f.write(received)
        
    finally:
        sock.close()
    print("Sent:     {}".format(data))
    print("Received: {}".format(received))





    



