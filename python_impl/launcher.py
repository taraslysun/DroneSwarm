import json
import argparse
from src.drone import Drone
from src.clusterhead import ClusterHead
from src.masterdrone import MasterDrone
from src.intermediatedrone import IntermediateDrone
from src.commondrone import CommonDrone
import multiprocessing

# def main():
#     master = MasterDrone(0, port=12345, use_tcp=True)
#     message = "Hello, World!"
#     master.Broadcast(message+'1', '192.168.1.90')
    # master.Broadcast(message+'2', '<broadcast>')

def start_drone(i, port):
    # Initialize the drone instance with a unique ID and port
    start_position = (i*10, 0, 0)
    target = (i*10, i*10, 0)
    drone = CommonDrone(i, port=40000+i, use_tcp=False, cluster_head=(0, '192.168.1.51', 12345), step_distance=0.1, target_coordinates=target, position=start_position)
    drone.StartListening()  # Start the listening thread
    drone.Operation(100)       # Start the drone's operation loop

def main(*args):
    master = MasterDrone(0, port=12345, use_tcp=False)
    ip = ['192.168.1.53', '192.168.1.90', '192.168.1.51']
    start_positions = [(i*10, 0, 0) for i in range(len(args))]
    target_positions = [(i*10, i*10, 0) for i in range(len(args))]
    for i in range(len(args)):
        arg = args[i]
        master.Broadcast(json.dumps({'command': 'MOVE', 'coordinates': {'latitude': arg[0], 'longitude': arg[1], 'altitude': arg[2]}}), ip[i])

# def main():
#     ip = '192.168.1.51'
#     num = 5
#     processes = []
#     for i in range(num):
#         p = multiprocessing.Process(target=start_drone, args=(i, 40000+i))
#         p.start()
#         processes.append(p)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('lat', type=float, help='latitude')
    parser.add_argument('lon', type=float, help='longitude')
    parser.add_argument('alt', type=float, help='altitude')
    parser.add_argument('lat1', type=float, help='latitude')
    parser.add_argument('lon1', type=float, help='longitude')
    parser.add_argument('alt1', type=float, help='altitude')

    args = parser.parse_args()
    main([args.lat, args.lon, args.alt], [args.lat1, args.lon1, args.alt1])
    # main()
