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
        print('num of common drones:', len(self.common_drones))

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
            print('message:', message)
            if message:
                self.ParseCommand(message)


    def MoveCommonDrones(self):
        # print('num of common drones: MoveCommonDrones ', len(self.common_drones))
        # if not self.coordinates_sent:
        #     # find the direction vector to the target
        #     direction = [self.shared_target_coordinates[i] - self.position[i] for i in range(3)]
        #     # print('direction:', direction)
        # else:
        direction = [0, 0, 0]
        for cd in self.common_drones:
            rand_coords = []
            for i in range(3):
                rand_coords.append(self.position[i] + random.uniform(-self.cluster_radius, self.cluster_radius) + direction[i])


            self.Broadcast(json.dumps({'command': 'MOVE', 
                                        'coordinates': {'latitude': rand_coords[0], 
                                                        'longitude': rand_coords[1], 
                                                        'altitude': rand_coords[2]}}),
                            cd[1], cd[2])
        self.coordinates_sent = True

    def Action(self):
        '''
        One iteration of the drone's action loop
        '''
        if not self.shared_moving.value:
            time.sleep(0.1)  # Small sleep to reduce CPU usage
        else:
            # if not self.coordinates_sent:
            self.MoveToTarget()
            self.MoveCommonDrones()


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
            self.MoveCommonDrones()  # Move the common drones to new random coordinates


    def BroadcastSync(self):
        sync_message = f"SYNC {self.clock}"
        for cd in self.common_drones:
            self.Broadcast(sync_message, cd[1], cd[2])
