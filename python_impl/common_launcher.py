from src.commondrone import CommonDrone
from src.clusterhead import ClusterHead
import multiprocessing
import random
import argparse


demo_ip = '192.168.1.51'

def start_common_drone(i, port):
    # start_position = (i*10, 0, 0)
    # target = (i*10, 10+i*10, 0)
    start_position = (random.randint(0, 300), random.randint(0, 300), random.randint(10, 50))
    target = (random.randint(0, 300), random.randint(0, 300), random.randint(10, 50))
    print(start_position, target, i)
    drone = CommonDrone(i+10000, 
                        port=port,
                        use_tcp=False, 
                        cluster_head=(0, '192.168.1.51', 20000),
                        step_distance=0.4, 
                        target_coordinates=target, 
                        position=start_position)
    drone.Operation(demo_ip=demo_ip)





def main(lower, upper):
    processes = []
    for i in range(lower, upper):
        p = multiprocessing.Process(target=start_common_drone, args=(i, 10000+i))
        p.start()
        processes.append(p)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('lower', type=int, help='lower bound')
    parser.add_argument('upper', type=int, help='upper bound')
    args = parser.parse_args()
    main(args.lower, args.upper)



