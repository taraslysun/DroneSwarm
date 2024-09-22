import json
import time
import argparse
from src.drone import Drone
from src.clusterhead import ClusterHead
from src.masterdrone import MasterDrone
from src.intermediatedrone import IntermediateDrone
from src.commondrone import CommonDrone


# def main():
#     master = MasterDrone(0, port=12345, use_tcp=True)
#     message = "Hello, World!"
#     master.Broadcast(message+'1', '192.168.1.90')
    # master.Broadcast(message+'2', '<broadcast>')
demo_ip = '192.168.1.51'
cluster_head_ip = '192.168.1.51'

def main(command, ip, port):
    direction = 1
    master = Drone(0, port=30003, use_tcp=False)


    if command == 'MOVEALL':
        master.Broadcast(json.dumps({'command':'MOVEALL', 'coordinates':{'lat':200, 'lon':direction*100, 'alt':50}}), ip, port)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('command', type=str, help='command')
    argparser.add_argument('ip', type=str, help='ip')
    argparser.add_argument('port', type=int, help='port')
    args = argparser.parse_args()


    main(args.command, args.ip, args.port)