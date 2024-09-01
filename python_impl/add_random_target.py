import random
import argparse
import json
from src.masterdrone import MasterDrone

# target = (random.randint(0, 300), random.randint(0, 300), random.randint(10, 50))

def add_random_target():
    target = (random.randint(0, 300), random.randint(0, 300), random.randint(10, 50))
    return target

ips = ['192.168.1.51', '192.168.1.53']

def main(lower, upper):
    master = MasterDrone(0, port=12345, use_tcp=False)
    for i in range(lower, upper):
        ip = ips[0] if i <= 12 else ips[1]
        target = add_random_target()
        master.Broadcast(json.dumps({'command':'MOVE', 'coordinates':{'lat':target[0], 
                                                                      'lon':target[1], 
                                                                      'alt':target[2]}}),
                            ip, 10000+i)

                         




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('lower', type=int, help='lower bound')
    parser.add_argument('upper', type=int, help='upper bound')
    args = parser.parse_args()
    main(args.lower, args.upper)
