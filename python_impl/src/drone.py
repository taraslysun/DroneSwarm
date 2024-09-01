import socket
import time
import threading
import numpy as np

class Drone:
    def __init__(self, 
                 id, 
                 port=12345, 
                 use_tcp=False, 
                 position=(0, 0, 0), 
                 target_coordinates=(0,0,0), 
                 step_distance=1.0
                 ):
        self.id = id
        self.clock = time.time()
        self.camera = None
        self.port = port
        self.is_tcp = use_tcp
        self.ip_addr = self.GetIP()

        self.position = np.array(position).astype(float)
        self.target_coordinates = np.array(target_coordinates).astype(float)
        self.step_distance = step_distance
        self.moving = False


        if use_tcp:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.socket.bind(("", self.port)) 
        print(f"{'TCP' if use_tcp else 'UDP'} {self.__class__.__name__} id:{self.id} ip:{self.ip_addr}/{self.port}")


    def Operation(self):
        """
        Main operation loop of the drone
        """
        while True:
            self.Action()
            # broadcast position to UNITY host for visualization

    def Action(self):
        """
        One iteration of the drone's action loop
        """
        print(f"Base action {self.id}, REDEFINE!")
        pass

    def Broadcast(self, message, addr):
        try:
            if self.is_tcp:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((addr, self.port))
                    s.sendall(message.encode())
            else:
                print(f"Drone {self.id} broadcasting message: {message} to {addr}")
                self.socket.sendto(message.encode(), (addr, self.port))
                print(f"Broadcast sent successfully")
        except Exception as e:
            print(f"Drone {self.id} failed to send message to {addr}: {e}")
            return False

    def Receive(self):
        try:
            if self.is_tcp:
                self.socket.listen(1)
                conn, addr = self.socket.accept()
                with conn:
                    data = conn.recv(1024)
                    if data:
                        message = data.decode()
                        return message, addr[0]
                    else:
                        print(f"Drone {self.id} received no data")
                        return None
            else:
                data, addr = self.socket.recvfrom(1024)
                message = data.decode()
                return message, addr[0]
        except Exception as e:
            print(f"Drone {self.id} failed to receive data: {e}")
            return None

    def GetPosition(self):
        print(f"Base GetPosition of drone {self.id}")
        return self.latitude, self.longitude, self.height

    def SyncClock(self, received_time):
        # Simple clock sync: Adjust own clock to received time
        self.clock = float(received_time)
        print(f"Drone {self.id} synchronized clock to {self.clock}")

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


    def Listen(self):
        while True:
            message, addr = self.Receive()
            if message:
                print(f"Listen {self.id} message: {message} ip:{addr}")
                if message.startswith("SYNC"):
                    _, received_time = message.split()
                    self.SyncClock(received_time)

    def StartListening(self):
        thread = threading.Thread(target=self.Listen)
        thread.start()
