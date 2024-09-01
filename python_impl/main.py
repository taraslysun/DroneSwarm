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
    master = CommonDrone(0, port=12345, use_tcp=False, )
    master.Operation()



if __name__ == "__main__":
    main()