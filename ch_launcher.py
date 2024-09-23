import json
import argparse
from src.clusterhead import ClusterHead
import multiprocessing



def start_ch_drone(i, port, ip1):
    start_position = (i*10, 0, 0)
    target = (i*200, 10+i*10, 50)
    drones = []
    if i < 2:
        for k in range(6*i+1, 6*i+6+1):
            drones.append((10000+k, ip1, 10000+k))
    else:
        for k in range(6*i+1, 6*i+6+1):
            drones.append((10000+k, ip1, 10000+k))
    

    drone = ClusterHead(i + 20000, 
                        port=port,
                        use_tcp=False,
                        step_distance=1,
                        target_coordinates=target, 
                        position=start_position,
                        common_drones=drones,
                        cluster_radius=40)
    # print(drone.common_drones)
    
    
    drone.Operation(demo_ip=ip1)

def main(lower, upper, ip_1):
    processes = []
    for i in range(lower, upper+1):
        p = multiprocessing.Process(target=start_ch_drone, args=(i, 20000+i, ip_1))
        p.start()
        processes.append(p)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('lower', type=int, help='lower bound')
    parser.add_argument('upper', type=int, help='upper bound')
    parser.add_argument('ip_1', type=str, help='ip of the first half of common drones')
    args = parser.parse_args()
    main(args.lower, args.upper, args.ip_1)
