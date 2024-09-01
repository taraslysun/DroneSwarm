import json
import time
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


def main():
    common = CommonDrone(0, port=12345, use_tcp=False, cluster_head_ip='192.168.1.51', cluster_id=1, step_distance=0.1)
    # common.Operation()
    while True:
        common.Action()
        time.sleep(0.01)      
        position = common.GetPosition()
        print(position)
        # print(list(position))
        common.Broadcast(json.dumps({'id':common.id,
                                     'latitude': position[0], 
                                     'longitude':position[1],
                                     'altitude':position[2]}), common.cluster_head_ip, 50000)


if __name__ == "__main__":
    main()