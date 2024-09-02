import json
import argparse
from src.drone import Drone
from src.clusterhead import ClusterHead
from src.masterdrone import MasterDrone
from src.intermediatedrone import IntermediateDrone
from src.commondrone import CommonDrone
import multiprocessing


ip1 = '192.168.1.51'
ip2 = '192.168.1.53'

def start_ch_drone(i, port):
    start_position = (i*10, 0, 0)
    target = (i*200, 10+i*10, 50)
    drones = []
    if i < 2:
        ip = ip1
    else:
        ip = ip2
    for k in range(6*i+1, 6*i+6+1):
        drones.append((10000+k, ip, 10000+k))

    drone = ClusterHead(i + 20000, 
                        port=port,
                        use_tcp=False,
                        step_distance=1,
                        target_coordinates=target, 
                        position=start_position,
                        common_drones=drones,
                        cluster_radius=40)
    # print(drone.common_drones)
    
    drone.Operation()

def main(lower, upper):
    processes = []
    for i in range(lower, upper):
        p = multiprocessing.Process(target=start_ch_drone, args=(i, 20000+i))
        p.start()
        processes.append(p)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('lower', type=int, help='lower bound')
    parser.add_argument('upper', type=int, help='upper bound')
    args = parser.parse_args()
    main(args.lower, args.upper)
