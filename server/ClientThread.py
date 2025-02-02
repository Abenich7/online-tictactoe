import threading

class ClientThread(threading.Thread):
    def __init__(self, clientsocket):
        threading.Thread.__init__(self)
        self.clientsocket = clientsocket

    def run(self):
          # Handle client connection
        while True:
            data = self.clientsocket.recv(2048)
            if not data:
                break
            print(f"Received: {data}")
            self.clientsocket.send(data.upper())
        self.clientsocket.close()
