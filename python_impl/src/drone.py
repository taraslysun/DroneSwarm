import socket
import time
import threading
import numpy as np
import json
from multiprocessing import Process, Manager


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
        self.moving = False if np.all(self.position == self.target_coordinates) else True

        if use_tcp:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.bind((self.ip_addr, self.port)) 
        print(f"{'TCP' if use_tcp else 'UDP'} {self.__class__.__name__} id:{self.id} ip:{self.ip_addr}/{self.port}")



    def MoveToTarget(self):
        '''
        Move the drone in the direction of the target coordinates by a fixed distance
        '''
        target_coordinates = np.array(self.shared_target_coordinates)
        direction = target_coordinates - self.position
        distance_to_target = np.linalg.norm(direction)

        if distance_to_target <= self.step_distance:
            self.position = target_coordinates
            self.shared_moving.value = False
            print(f"Drone {self.id} has reached the target at {self.position}.")
        else:
            direction_normalized = direction / distance_to_target
            self.position += direction_normalized * self.step_distance
            # print(f"Drone {self.id} position: {self.position}  target: {target_coordinates}")


    def Operation(self):
        """
        Main operation loop of the drone
        """
        print(f"Base operation {self.id}, REDEFINE!")
        pass


    def Action(self):
        """
        One iteration of the drone's action loop
        """
        print(f"Base action {self.id}, REDEFINE!")
        pass



    def ParseCommand(self, message):
        """
        Parse a received command message
        """
        print(f"Base parse command {self.id}, REDEFINE!")
        pass



    def Broadcast(self, message, addr=None, port=None):
        if addr is None:
            addr = self.ip_addr
        if port is None:
            port = self.port
        try:
            if self.is_tcp:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((addr, port))
                    s.sendall(message.encode())
            else:
                self.socket.sendto(message.encode(), (addr, port))
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
                        return message, addr
                    else:
                        print(f"Drone {self.id} received no data")
                        return None
            else:
                data, addr = self.socket.recvfrom(1024)
                message = data.decode()
                return message, addr
        except Exception as e:
            print(f"{self.__class__.__name__} {self.id} failed to receive data: {e}")
            return None



    def GetPosition(self):
        return self.position



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



    def Demonstrate(self, demonstrator_ip, demonstrator_port):
        time.sleep(0.01)
        position = self.GetPosition()
        self.Broadcast(json.dumps({'id':self.id,
                                'latitude': position[0], 
                                'longitude':position[1],
                                'altitude':position[2]}),
                        demonstrator_ip, 
                        demonstrator_port)