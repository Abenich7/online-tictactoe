import socket
from MySocket import MySocket
import time
import csv
import threading



HOST, PORT = "127.0.0.1", 3002

#client=MySocket()

#semaphore=threading.Semaphore(1)

def client_thread():

    client=MySocket()
    client.connect((HOST, PORT))
    
    #while True:
    try:


            data_recv=threading.Thread(target=client.myreceive).start()

            #semaphore.acquire()
            #data_recv=client.myreceive()
            #print("Received: {}".format(data_recv.strip()))
        
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

if __name__ == "__main__":  
    client_thread()






#print("Sent:     {}".format(data))
#print("Received: {}".format(received))


#setup functions to handle client functionality




    



