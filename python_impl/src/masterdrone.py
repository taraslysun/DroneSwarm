from src.drone import Drone
class MasterDrone(Drone):    
    def Act(self):
        print("MasterDrone Act")
        pass

    def Broadcast(self):
        print("MasterDrone Broadcast")
        pass

    def Receive(self):
        print("MasterDrone Receive")
        pass

    def GetPosition(self):
        print("MasterDrone GetPosition")
        return 0,0,0
