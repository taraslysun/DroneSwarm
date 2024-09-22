from multiprocessing import Process, Manager
import json
import random
import cv2
import socket
import time
import numpy as np
from src.drone import Drone
from model_training.YOLOvX import YOLOvX
   
class ClusterHead(Drone):
    def __init__(self, 
                 id,
                 port=20000,
                 use_tcp=False,
                 position=(0, 0, 0),
                 target_coordinates=(0,0,0),
                 step_distance=1.0,
                 common_drones=[],
                 cluster_radius=100,
                 camera=None,
                 image_port=None,
                 ):
        super().__init__(id, port, use_tcp, position, target_coordinates, step_distance)
        self.cluster_radius = cluster_radius
        self.common_drones = common_drones
        self.common_moving = False
        self.coordinates_sent = False  # Flag to track if coordinates have been sent
        self.camera = camera  # Assuming the camera object is passed here
        self.model = YOLOvX('python_impl/model_training/yolov8n.onnx')
        self.image_port = image_port if image_port else self.id - 20000 + 7000
        print('num of common drones:', len(self.common_drones))

        manager = Manager()
        self.shared_target_coordinates = manager.list(self.target_coordinates)
        self.shared_position = manager.list(self.position)  # Shared position
        self.shared_moving = manager.Value('b', self.moving)

        self.listener_process = Process(target=self.ListenForCommands)
        self.listener_process.start()

        self.image_listener_process = Process(target=self.ImageListener)
        self.image_listener_process.start()

# ----------------------------------------------------------- MAIN LOOPS -----------------------------------------------------------

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


    def Action(self):
        '''
        One iteration of the drone's action loop
        '''
        if not self.shared_moving.value:
            time.sleep(0.1)  # Small sleep to reduce CPU usage
        else:
            self.MoveToTarget()
            # self.MoveCommonDrones(self.target_coordinates)
            # print('cluster head position:', self.shared_position[:])
            self.position = np.array(self.shared_position).astype(float)

# ----------------------------------------------------------- IMAGE LISTENER -----------------------------------------------------------

    def ImageListener(self):
        """
        Listens for incoming image data on a specified port, processes the image using the YOLOv8 model,
        and makes decisions based on detected objects (e.g., trees).
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', self.image_port))
        server_socket.listen(1)
        print(f"Listening for images on port {self.image_port}...")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr} established.")

            # Receive image data
            data = b''
            while True:
                packet = client_socket.recv(4096)
                if not packet:
                    break
                data += packet

            # Decode the image
            nparr = np.frombuffer(data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Process the image with YOLOv8 model
            detections = self.model.predict(image)

            # Analyze detections (e.g., trees) and make a decision
            for detection in detections:
                if detection['class_name'] == 'tree':
                    self.HandleTreeDetection(detection)
            
            client_socket.close()

# ----------------------------------------------------------- MOVEMENT -----------------------------------------------------------

    def MoveToTarget(self):
        '''
        Move the drone in the direction of the target coordinates by a fixed distance
        '''
        target_coordinates = np.array(self.shared_target_coordinates)
        direction = target_coordinates - np.array(self.shared_position)
        distance_to_target = np.linalg.norm(direction)
        self.MoveCommonDrones(target_coordinates)

        if distance_to_target <= self.step_distance:
            self.shared_position[:] = target_coordinates  # Update shared position
            self.shared_moving.value = False
            print(f"Drone {self.id} has reached the target at {self.shared_position[:]}.")

        else:
            direction_normalized = direction / distance_to_target
            new_position = np.array(self.shared_position) + direction_normalized * self.step_distance
            self.shared_position[:] = new_position  # Update shared position


    def MoveCommonDrones(self, target=None):
        for cd in self.common_drones:
            self.Broadcast(json.dumps({'command': 'MOVE', 
                                        'coordinates': {'latitude': float(target[0]),
                                                        'longitude': float(target[0]),
                                                        'altitude': float(target[0])},
                                        'ch_coordinates': {'latitude': self.shared_position[0],
                                                           'longitude': self.shared_position[1],
                                                           'altitude': self.shared_position[2]}
                                        }), cd[1], cd[2])
        self.coordinates_sent = True

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
            self.MoveCommonDrones(coordinates)
        if command == 'SYNC':
            self.clock = max(self.clock, message['clock'])
            self.BroadcastSync()
        if command == 'CLUSTER':
            print('cluster command received')
            print(self.id, self.common_drones, self.shared_position[:])
            self.MoveCommonDrones(self.shared_position[:])

    def BroadcastSync(self):
        sync_message = json.dumps({'command': 'SYNC', 'clock': self.clock})
        for cd in self.common_drones:
            self.Broadcast(sync_message, cd[1], cd[2])
