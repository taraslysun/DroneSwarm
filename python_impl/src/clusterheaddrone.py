from src.drone import Drone
class ClusterHeadDrone(Drone):
    
    # def Act(self):
    #     print("ClusterHeadDrone Act")
    #     pass

    def GetPosition(self):
        print("ClusterHeadDrone GetPosition")
        return 0,0,0