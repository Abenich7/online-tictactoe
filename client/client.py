import socket
from MySocket import MySocket


HOST, PORT = "127.0.0.1", 3000

client=MySocket()

data="Hello, World!"
try:
    client.connect((HOST, PORT))
    data_recv=client.myreceive()
    print("Received: {}".format(data_recv.strip()))
    
    #client.myreceive = str((1024), "utf-8")
    client.mysend(data.encode('utf-8'))
    #client.mysend(bytes(data + "\n", "utf-8"))

    print("Sent:     {}".format(data))
    print("Received: {}".format(client.myreceive))
finally:
    client.close()






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





    



