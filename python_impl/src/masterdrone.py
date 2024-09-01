from src.drone import Drone
class MasterDrone(Drone):
    def __init__(self, id, port=12345, use_tcp=False):
        super().__init__(id, port, use_tcp)
        self.cluster_heads = []  # List of ClusterHeads in the swarm

    def BroadcastSync(self):
        sync_message = f"SYNC {self.clock}"
        for ch in self.cluster_heads:
            self.Broadcast(sync_message, ch.ip_addr)
