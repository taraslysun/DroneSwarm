from multiprocessing import Process, Manager
import json
import random
import time
import numpy as np

from src.drone import Drone

class MasterDrone(Drone):
    # def __init__(self, id, port=30000, use_tcp=False):
    #     super().__init__(id, port, use_tcp)
    #     self.cluster_heads = []  # List of ClusterHeads in the swarm

    def __init__(self, 
                 id,
                 port=30000,
                 use_tcp=False, 
                 position=(0, 0, 0), 
                 target_coordinates=(0,0,0), 
                 step_distance=1.0,
                 cluster_heads=[],      
                 camera=None,   
                 ):
        super().__init__(id, port, use_tcp, position, target_coordinates, step_distance, camera)
        self.cluster_heads = cluster_heads
        self.common_moving = False
        self.coordinates_sent = False  # Flag to track if coordinates have been sent
        print('num of cluster heads:', len(self.cluster_heads))
        print(self.moving, self.position, self.target_coordinates)

        manager = Manager()
        self.shared_target_coordinates = manager.list(self.target_coordinates)
        self.shared_moving = manager.Value('b', self.moving)
        self.shared_position = manager.list(self.position)  # Shared position

        self.listener_process = Process(target=self.ListenForCommands)
        self.listener_process.start()

        # sync clock process every second
        # self.sync_clock_process = Process(target=self.SyncClocks)
        # self.sync_clock_process.start()


# ----------------------------------------------------------- MAIN LOOPS -----------------------------------------------------------
    def Operation(self, num=None, demo_ip=None):
        demo_ip = demo_ip if demo_ip else self.ip_addr
        if num is None:
            while True:
                self.Action()
                self.Demonstrate(demo_ip, 53000 + self.id - 30000)
        else:
            for i in range(num):
                self.Action()
                self.Demonstrate(demo_ip, 53000 + self.id - 30000)

    
    def Action(self):
        '''
        One iteration of the drone's action loop
        '''
        if not self.shared_moving.value:
            time.sleep(0.1)  # Small sleep to reduce CPU usage
        else:
            # if not self.coordinates_sent:
            self.MoveToTarget()
            # self.MoveClusterHeads()
            self.position = np.array(self.shared_position).astype(float)

# ----------------------------------------------------------- MOVEMENT -----------------------------------------------------------

    def MoveToTarget(self):
        '''
        Move the drone in the direction of the target coordinates by a fixed distance
        '''
        target_coordinates = np.array(self.shared_target_coordinates)
        direction = target_coordinates - np.array(self.shared_position)
        distance_to_target = np.linalg.norm(direction)

        if distance_to_target <= self.step_distance:
            self.shared_position[:] = target_coordinates  # Update shared position
            self.shared_moving.value = False
            print(f"Drone {self.id} has reached the target at {self.shared_position[:]}.")

        else:
            direction_normalized = direction / distance_to_target
            new_position = np.array(self.shared_position) + direction_normalized * self.step_distance
            self.shared_position[:] = new_position  # Update shared position



    def MoveAllClusterHeads(self, *args):
        # print('num of common drones: MoveCommonDrones ', len(self.cluster_heads))
        # if not self.coordinates_sent:
        #     # find the direction vector to the target
        #     direction = [self.shared_target_coordinates[i] - self.position[i] for i in range(3)]
        #     # print('direction:', direction)
        # else:
        # direction = [0, 0, 0]
        # for cd in self.cluster_heads:
        #     rand_coords = []
        #     for i in range(3):
        #         rand_coords.append(self.position[i] + random.uniform(-self.cluster_radius, self.cluster_radius) + direction[i])


        #     self.Broadcast(json.dumps({'command': 'MOVE', 
        #                                 'coordinates': {'latitude': rand_coords[0], 
        #                                                 'longitude': rand_coords[1], 
        #                                                 'altitude': rand_coords[2]}}),
        #                     cd[1], cd[2])
        # self.coordinates_sent = True

        # so here we need to get the target coordinates from the master drone
        # and move the cluster heads to those coordinates but keep the relative positions to the master drone
        target_coordinates = np.array(self.shared_target_coordinates)
        direction = target_coordinates - np.array(self.shared_position)
        distance_to_target = np.linalg.norm(direction)

        for ch in self.cluster_heads:
            relative_position = np.array(self.position)
            new_position = target_coordinates + relative_position
            self.Broadcast(json.dumps({'command': 'MOVE', 
                                        'coordinates': {'latitude': new_position[0]+100, 
                                                        'longitude': new_position[1], 
                                                        'altitude': new_position[2]}}),
                            ch[1], ch[2])
        


    def BroadcastCluster(self):
        for ch in self.cluster_heads:
            self.Broadcast(json.dumps({'command': 'CLUSTER'}), ch[1], ch[2])
# ----------------------------------------------------------- SYNCHRONIZATION -----------------------------------------------------------

    def ListenForCommands(self):
        """
        Separate process that listens for incoming commands and updates the shared state.
        """
        while True:
            message, addr = self.Receive()
            # print('message:', message)
            if message:
                self.ParseCommand(message)


    def ParseCommand(self, message):
        message = json.loads(message)
        command = message['command']
        if command == 'MOVE':
            self.shared_moving.value = True
            coordinates = message['coordinates']
            coordinates = [float(coordinates[key]) for key in coordinates.keys()]
            for i in range(3):
                self.shared_target_coordinates[i] = coordinates[i]
            self.coordinates_sent = False
            drone_id = message['id']
            print(f"Drone {drone_id} is moving to {coordinates}")
            self.MoveClusterHead(coordinates, drone_id)
        if command == 'MOVEALL':
            self.shared_moving.value = True
            coordinates = message['coordinates']
            coordinates = [float(coordinates[key]) for key in coordinates.keys()]
            for i in range(3):
                self.shared_target_coordinates[i] = coordinates[i]
            self.coordinates_sent = False
            self.MoveAllClusterHeads()
        if command == 'SYNC':
            self.clock = max(self.clock, message['clock'])
            self.BroadcastSync()
        if command == 'CLUSTER':
            print('cluster command received')
            self.BroadcastCluster()


    def GetTime(self):
        return time.time()


    def SyncClocks(self):
        while True:
            time.sleep(1)
            self.clock = self.GetTime()
            self.BroadcastSync()
            # print(f"ClusterHead {self.id} clock: {self.clock}")
            

    def BroadcastSync(self):
        sync_message = json.dumps({'command': 'SYNC', 'clock': self.clock})
        for cd in self.cluster_heads:
            self.Broadcast(sync_message, cd[1], cd[2])
