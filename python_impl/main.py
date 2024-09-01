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

def main(id):
    common = CommonDrone(id, 
                         port=30000+id, 
                         use_tcp=False, 
                         cluster_head=(1, cluster_head_ip, 20000), 
                         step_distance=0.1, 
                         position=(10,0,0), 
                         target_coordinates=(20,22,21)
                         )
    common.Operation(1000, demo_ip=demo_ip)



if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('id', type=int, help='Drone ID')
    args = argparser.parse_args()

    main(args.id)