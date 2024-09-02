from src.masterdrone import MasterDrone
from src.drone import Drone
import json
import argparse

def main(forward, distance):
    direction = 1 if forward else -1
    master = Drone(0, port=30000, use_tcp=False)

    demo_ip_1 = '192.168.1.51'
    demo_ip_2 = '192.168.1.53'

    ch_port = 20000

    for i in range(4):
        master.Broadcast(json.dumps({'command':'MOVE', 'coordinates':{'lat':i*200, 'lon':i+direction*distance, 'alt':50}}), demo_ip_1, ch_port+i)
        # master.Broadcast(json.dumps({'command':'MOVE', 'coordinates':{'lat':200, 'lon':200, 'alt':50}}), demo_ip_1, ch_port+i)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('forward', type=int, help='direction')
    parser.add_argument('distance', type=int, help='distance')
    args = parser.parse_args()
    main(args.forward, args.distance)
    
