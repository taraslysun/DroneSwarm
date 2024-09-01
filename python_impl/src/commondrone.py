import socket
import json
import numpy as np
from src.drone import Drone

class CommonDrone(Drone):

    def __init__(self, 
                 id,
                 port=12345, 
                 use_tcp=False, 
                 position=(0, 0, 0), 
                 target_coordinates=(0,0,0), 
                 step_distance=1.0,
                 cluster_head_ip=None, 
                 cluster_id=None
                 ):
        self.cluster_head_ip = cluster_head_ip
        self.cluster_id = cluster_id
        super().__init__(id,port,use_tcp,position,target_coordinates,step_distance)

    def Action(self):
        '''
        One iteration of the drone's action loop
        '''
        if not self.moving:
            message, addr = self.Receive()
            self.ParseCommand(message)
        else:
            self.MoveToTarget()

    def Broadcast(self, message, addr=None):
        if addr is None:
            addr = self.cluster_head_ip
        try:
            if self.is_tcp:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((addr, self.port))
                    s.sendall(message.encode())
            else:
                self.socket.sendto(message.encode(), (addr, self.port))
            print(f"Broadcast sent successfully")
        except Exception as e:
            print(f"Failed {self.id} receiver:{addr}: {e}")
            return False


    def ParseCommand(self, message):
        message = json.loads(message)
        if message['command'] == 'MOVE':
            self.moving = True
            coordinates = message['coordinates']
            self.target_coordinates = np.array([coordinates['latitude'], coordinates['longitude'], coordinates['altitude']]).astype(float)


    def MoveToTarget(self):
        '''
        Move the drone in the direction of the target coordinates by a fixed distance
        '''
        direction = self.target_coordinates - self.position
        distance_to_target = np.linalg.norm(direction)

        if distance_to_target <= self.step_distance:
            self.position = self.target_coordinates
            self.moving = False
            print(f"Drone {self.id} has reached the target at {self.position}.")
        else:
            direction_normalized = direction / distance_to_target
            self.position += direction_normalized * self.step_distance
            print(f"Drone {self.id} position: {self.position}  target: {self.target_coordinates}")

    def GetPosition(self):
        return self.position
