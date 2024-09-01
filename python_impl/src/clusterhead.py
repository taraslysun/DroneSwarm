from multiprocessing import Process, Manager
import json
import random
import time
from src.drone import Drone
   
class ClusterHead(Drone):
    def __init__(self, 
                 id,
                 port=20000,
                 use_tcp=False, 
                 position=(0, 0, 0), 
                 target_coordinates=(0,0,0), 
                 step_distance=1.0,
                 common_drones=[],
                 cluster_radius=100                 
                 ):
        super().__init__(id, port, use_tcp, position, target_coordinates, step_distance)
        self.cluster_radius = cluster_radius
        self.common_drones = common_drones
        self.common_moving = False
        self.coordinates_sent = False  # Flag to track if coordinates have been sent


    def MoveCommonDrones(self):
        if not self.coordinates_sent:
            for cd in self.common_drones:
                rand_coords = []
                for i in range(3):
                    rand_coords.append(self.shared_target_coordinates[i] + random.uniform(-self.cluster_radius, self.cluster_radius))
                self.Broadcast(json.dumps({'command': 'MOVE', 
                                           'coordinates': {'latitude': rand_coords[0], 
                                                           'longitude': rand_coords[1], 
                                                           'altitude': rand_coords[2]}}),
                               cd[1], cd[2])
            self.coordinates_sent = True  # Set the flag to indicate that coordinates have been sent

    def Action(self):
        '''
        One iteration of the drone's action loop
        '''
        if not self.shared_moving.value:
            time.sleep(0.1)  # Small sleep to reduce CPU usage
        else:
            if not self.coordinates_sent:
                self.MoveCommonDrones()
            self.MoveToTarget()


    def Operation(self, num=None, demo_ip=None):
        demo_ip = demo_ip if demo_ip else self.ip_addr
        if num is None:
            while True:
                self.Action()
                self.Demonstrate(demo_ip, 52000 + self.id - 20000)
        else:
            for i in range(num):
                self.Action()
                self.Demonstrate(demo_ip, 52000 + self.id - 20000)


    def ParseCommand(self, message):
        message = json.loads(message)
        if message['command'] == 'MOVE':
            self.shared_moving.value = True
            coordinates = message['coordinates']
            coordinates = [float(coordinates[key]) for key in coordinates.keys()]
            for i in range(3):
                self.shared_target_coordinates[i] = coordinates[i]
            self.coordinates_sent = False  # Reset the flag when a new move command is received


    def BroadcastSync(self):
        sync_message = f"SYNC {self.clock}"
        for cd in self.common_drones:
            self.Broadcast(sync_message, cd.ip_addr)
