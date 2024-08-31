import socket

class Drone:
    def __init__(self, id, port=12345, use_tcp=False):
        self.id = id
        self.latitude = 0
        self.longitude = 0
        self.height = 0
        self.camera = None
        self.port = port
        self.is_tcp = use_tcp
        if use_tcp:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.ip_addr = self.GetIP()

        # Bind the socket to the IP address and port
        self.socket.bind((self.ip_addr, self.port))
        print(f"Drone {self.id} initialized with IP {self.ip_addr} on port {self.port}")

    def Act(self):
        if self.is_tcp:
            message = self.Receive()
            print(f"Drone {self.id} received: {message}")
        else:
            message, addr = self.Receive()
            print(f"Drone {self.id} received: {message} from {addr}")
        response = f"Acknowledged: {message}"
        self.Broadcast(response, addr)

    def Broadcast(self, message, addr):
        try:
            if self.is_tcp:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((addr, self.port))
                    s.sendall(message.encode())
            else:
                self.socket.sendto(message.encode(), (addr, self.port))
        except Exception as e:
            print(f"Drone {self.id} failed to send message to {addr}: {e}")
            return False

    def Receive(self):
        if self.is_tcp:
            self.socket.listen(1)
            conn, addr = self.socket.accept()
            with conn:
                data = conn.recv(1024)
                if data:
                    message = data.decode()
                    return message
                else:
                    print(f"Drone {self.id} received no data")
                    return None
        else:
            data, addr = self.socket.recvfrom(1024)
            message = data.decode()
            return message, addr

    def GetPosition(self):
        print(f"Base GetPosition of drone {self.id}")
        return self.latitude, self.longitude, self.height

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
