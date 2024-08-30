from src.drone import Drone
class CommonDrone(Drone):

    def __init__(self, id, cluster_id):
        self.cluster_id = cluster_id
        super().__init__(id)
    
    def Act(self):
        print("CommonDrone Act")
        pass

    def Broadcast(self):
        print("CommonDrone Broadcast")
        pass

    def Receive(self):
        print("CommonDrone Receive")
        pass

    def GetPosition(self):
        print("CommonDrone GetPosition")
        return 0,0,0


