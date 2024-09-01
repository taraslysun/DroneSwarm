import socket
import json
import numpy as np
from src.drone import Drone
import time

class CommonDrone(Drone):

    def __init__(self, 
                 id,
                 cluster_head,
                 port=12345, 
                 use_tcp=False, 
                 position=(0, 0, 0), 
                 target_coordinates=(0,0,0), 
                 step_distance=1.0,
                 ):
        self.cluster_head_id = cluster_head[0]
        self.cluster_head_ip = cluster_head[1]
        self.cluster_head_port = cluster_head[2]
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


    def Operation(self, num=None):

        if num is None:
            while True:
                self.Action()
                self.Demonstrate(self.cluster_head_ip, 50000+self.id)
        else:
            for i in range(num):
                self.Action()
                self.Demonstrate(self.cluster_head_ip, 50000+self.id)

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
