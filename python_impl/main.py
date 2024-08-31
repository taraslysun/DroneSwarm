from src.drone import Drone
from src.clusterheaddrone import ClusterHeadDrone
from src.masterdrone import MasterDrone
from src.intermediatedrone import IntermediateDrone
from src.commondrone import CommonDrone
def init_field(num_clusters, num_drones, num_intermediate_drones):
    drones = [MasterDrone(0)]
    id_ = 1
    for i in range(1, num_clusters+1):
        drones.append(ClusterHeadDrone(id_))
        id_ += 1
        for _ in range(1, num_drones+1):
            drones.append(CommonDrone(id_, i))
            id_ += 1
        for _ in range(1, num_intermediate_drones+1):
            drones.append(IntermediateDrone(id_, i))
            id_ += 1
    
    return drones
    

def main():
    # master = MasterDrone(0)
    # msg = master.Receive()
    # print(msg)
    # master.Broadcast(msg + " master return")
    cluster_head = ClusterHeadDrone(1, use_tcp=True)
    cluster_head.Broadcast("Hello from cluster_head",'192.168.1.51')
    for i in range(3):
        msg = cluster_head.Receive()
        print(msg)
        cluster_head.Broadcast(msg[0]+str(i), '192.168.1.51')    

    cluster_head.socket.close()
if __name__ == "__main__":
    main()