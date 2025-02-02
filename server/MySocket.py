import socket
# SERVER 



#MySocket class inherits from socket.socket (subclass)
class MySocket(socket.socket):
    
    def __init__(self, sock=None):
        
        if sock is None:
            # If no socket provided, create a new one
            super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        else:
            # If socket provided, use its file descriptor to initialize
            super().__init__(fileno=sock.fileno())
    
    # def connect(self, host, port):
     #   self.sock.connect((host, port))

    def mysend(self, msg,MSGLEN=1024):
        # Pad the message to the fixed length
        msg = msg.ljust(MSGLEN)
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self,MSGLEN=1024):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)
 
    def myaccept(self):
        """
        Override accept to return MySocket instance instead of regular socket.
        Returns: (MySocket, address)
        """
        client_socket, address = super().accept()
        return client_socket, address
