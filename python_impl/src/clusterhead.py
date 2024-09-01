from src.drone import Drone
   
class ClusterHead(Drone):
    def __init__(self, id, port=12345, use_tcp=False):
        super().__init__(id, port, use_tcp)
        self.cluster_radius = 100
        self.common_drones = []  # List of CommonDrones in the cluster

    def BroadcastSync(self):
        sync_message = f"SYNC {self.clock}"
        for cd in self.common_drones:
            self.Broadcast(sync_message, cd.ip_addr)

    def GetPosition(self):
        print("ClusterHeadDrone GetPosition")
        return 0,0,0