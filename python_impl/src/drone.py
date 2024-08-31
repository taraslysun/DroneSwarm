import socket
import sys
class Drone:
    def __init__(self, id, port=22):
        self.id = id
        self.latitude=0
        self.longitude=0
        self.height=0
        self.camera=None
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_addr = self.GetIP()
        self.socket.bind(('0.0.0.0', port)) # to bind socket means to associate a socket with a port on your local machine
        

    def Act(self):
        message = self.Receive()
        print("received and now acting")
        self.Broadcast(message)
        pass

    def Broadcast(self, message):
        self.socket.connect((self.ip_addr, self.port))
        self.socket.sendall(message.encode())
        pass

    def Receive(self):
        self.socket.listen()
        conn, addr = self.socket.accept()
        data=conn.recv(1024)
        message = data.decode()
        print(message, "received message for drone", self.id)
        return message

    def GetPosition(self):
        print(f"Base GetPosition of drone {self.id}")
        return 0,0,0

    def GetIP(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(('10.254.254.254', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    