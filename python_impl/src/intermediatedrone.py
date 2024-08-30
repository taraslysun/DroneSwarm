from src.drone import Drone

class IntermediateDrone(Drone):
    def __init__(self, id, cluster_id):
        self.cluster_id = cluster_id
        super().__init__(id)
    
    def Act(self):
        print("IntermediateDrone Act")
        pass

    def Broadcast(self):
        print("IntermediateDrone Broadcast")
        pass

    def Receive(self):
        print("IntermediateDrone Receive")
        pass

    def GetPosition(self):
        print("IntermediateDrone GetPosition")
        return 0,0,0
