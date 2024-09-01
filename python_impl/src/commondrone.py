import socket
import json
import numpy as np
from multiprocessing import Process, Manager
from src.drone import Drone
import time

class CommonDrone(Drone):

    def __init__(self, 
                 id,
                 cluster_head,
                 port=10000, 
                 use_tcp=False, 
                 position=(0, 0, 0), 
                 target_coordinates=(0,0,0), 
                 step_distance=1.0,
                 ):
        self.cluster_head_id = cluster_head[0]
        self.cluster_head_ip = cluster_head[1]
        self.cluster_head_port = cluster_head[2]
        super().__init__(id, port, use_tcp, position, target_coordinates, step_distance)


        manager = Manager()
        self.shared_target_coordinates = manager.list(self.target_coordinates)
        self.shared_moving = manager.Value('b', self.moving)

        self.listener_process = Process(target=self.ListenForCommands)
        self.listener_process.start()


    def ListenForCommands(self):
        """
        Separate process that listens for incoming commands and updates the shared state.
        """
        while True:
            message, addr = self.Receive()
            if message:
                self.ParseCommand(message)


    def ParseCommand(self, message):
        message = json.loads(message)
        if message['command'] == 'MOVE':
            self.shared_moving.value = True
            coordinates = message['coordinates']
            coordinates = [float(coordinates[key]) for key in coordinates.keys()]
            for i in range(3):
                self.shared_target_coordinates[i] = coordinates[i]

    def Action(self):
        '''
        One iteration of the drone's action loop
        '''
        if not self.shared_moving.value:
            time.sleep(0.1)  # Small sleep to reduce CPU usage
        else:
            self.MoveToTarget()


    def Operation(self, num=None, demo_ip=None):
        demo_ip = demo_ip if demo_ip else self.cluster_head_ip
        if num is None:
            while True:
                self.Action()
                self.Demonstrate(demo_ip, 50000 + self.id - 10000)
        else:
            for i in range(num):
                self.Action()
                self.Demonstrate(demo_ip, 50000 + self.id - 10000)
