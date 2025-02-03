import threading

class ClientThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
       # self.clientsocket = clientsocket
       # self.datastack = datastack

#overriding the run() method in the ClientThread subclass of class Thread
    def run(self,clientsocket):
          # Handle client connection
        
        while True:
            data = clientsocket.myreceive(2048)
            if not data:
                break
            print(f"Received: {data}")
            clientsocket.mysend(data.upper())
        clientsocket.close()
