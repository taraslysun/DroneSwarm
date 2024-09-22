from src.masterdrone import MasterDrone
from src.drone import Drone
import json
import argparse

def main(distance, demo_ip):
    master = Drone(0, port=30000, use_tcp=False)


    ch_port = 20000

    for i in range(4):
        master.Broadcast(json.dumps({'command':'MOVE', 'coordinates':{'lat':i*200, 'lon':i+distance, 'alt':50}}), demo_ip, ch_port+i)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('distance', type=int, help='distance')
    parser.add_argument('demo_ip', type=str, help='ip of the demo computer')
    args = parser.parse_args()
    main(args.distance, args.demo_ip)
    
