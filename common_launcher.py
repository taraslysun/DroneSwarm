from src.commondrone import CommonDrone
from src.clusterhead import ClusterHead
import multiprocessing
import random
import argparse



def start_common_drone(i, port, demo_ip):
    # start_position = (i*10, 0, 0)
    # target = (i*10, 10+i*10, 0)
    start_position = (random.randint(0, 300), random.randint(0, 300), 10)
    target = (random.randint(0, 300), random.randint(0, 300), 10)
    print(start_position, target, i)
    drone = CommonDrone(i+10000, 
                        port=port,
                        use_tcp=False, 
                        cluster_head=(0, demo_ip, 20000),
                        step_distance=0.7, 
                        target_coordinates=start_position, 
                        position=start_position)
    drone.Operation(demo_ip=demo_ip)





def main(lower, upper, demo_ip):
    processes = []
    for i in range(lower, upper+1):
        p = multiprocessing.Process(target=start_common_drone, args=(i, 10000+i, demo_ip))
        p.start()
        processes.append(p)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('lower', type=int, help='lower bound')
    parser.add_argument('upper', type=int, help='upper bound')
    parser.add_argument('demo_ip', type=str, help='ip of the master drone')

    args = parser.parse_args()
    main(args.lower, args.upper, args.demo_ip)


#demo_ip = '10.10.247.100'

