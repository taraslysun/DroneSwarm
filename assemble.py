from src.drone import Drone
import json
import argparse

def main(demo_ip_1, demo_ip_2):
    master = Drone(0, port=30000, use_tcp=False)


    drone_port = 10000

    num_drones = 24

    # master.Broadcast("{'command':'MOVE', 'coordinates':{'lat':10, 'lon':10, 'alt':10}}", demo_ip, drone_port)

    for i in range(1,num_drones//2+1):
        master.Broadcast(json.dumps({'command':'MOVE', 'coordinates':{'lat':0, 'lon':i*10+10, 'alt':10}}), demo_ip_1, drone_port+i)

    for i in range(num_drones//2+1,num_drones+1):
        master.Broadcast(json.dumps({'command':'MOVE', 'coordinates':{'lat':30, 'lon':i*10+10 - i, 'alt':10}}), demo_ip_2, drone_port+i)

    for i in range(4):
        master.Broadcast(json.dumps({'command':'MOVE', 'coordinates':{'lat':50, 'lon':i*10+10, 'alt':10}}), demo_ip_1, 20000+i)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('demo_ip_1', type=str, help='ip of the first half of common drones')
    parser.add_argument('demo_ip_2', type=str, help='ip of the second half of common drones')
    args = parser.parse_args()
    demo_ip_1 = args.demo_ip_1
    demo_ip_2 = args.demo_ip_2
    main(demo_ip_1, demo_ip_2)