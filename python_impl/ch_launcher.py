import json
import argparse
from src.drone import Drone
from src.clusterhead import ClusterHead
from src.masterdrone import MasterDrone
from src.intermediatedrone import IntermediateDrone
from src.commondrone import CommonDrone
import multiprocessing


def start_ch_drone(i, port):
    start_position = (i*10, 0, 0)
    target = (i*10, 10+i*10, 0)
    drone = ClusterHead(i, 
                        port=port,
                        use_tcp=False,
                        step_distance=0.4,
                        target_coordinates=target, 
                        position=start_position)
    drone.Operation()


def main():
    ip = '192.168.1.51'
    num = 6
    processes = []
    # for i in range(num):
    #     p = multiprocessing.Process(target=start_ch_drone, args=(i, 30000+i))
    #     p.start()
    #     processes.append(p)



if __name__ == "__main__":
    main()



    # parser = argparse.ArgumentParser()
    # parser.add_argument('lat', type=float, help='latitude')
    # parser.add_argument('lon', type=float, help='longitude')
    # parser.add_argument('alt', type=float, help='altitude')
    # parser.add_argument('lat1', type=float, help='latitude')
    # parser.add_argument('lon1', type=float, help='longitude')
    # parser.add_argument('alt1', type=float, help='altitude')

    # args = parser.parse_args()
    # main([args.lat, args.lon, args.alt], [args.lat1, args.lon1, args.alt1])
