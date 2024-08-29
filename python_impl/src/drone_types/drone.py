class Drone:
    def __init__(self, id):
        self.id = id
        self.latitude=0
        self.longitude=0
        self.height=0
        self.camera=None
        

    def Update(self):
        print(f"Base Update of drone {self.id}")
        pass

    def Broadcast(self):
        print(f"Base Broadcast of drone {self.id}")
        pass

    def Receive(self):
        print(f"Base Receive of drone {self.id}")
        pass

    def GetPosition(self):
        print(f"Base GetPosition of drone {self.id}")
        return 0,0,0

class MasterDrone(Drone):    
    def Update(self):
        print("MasterDrone Update")
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

class ClusterHeadDrone(Drone):
    
    def Update(self):
        print("ClusterHeadDrone Update")
        pass

    def Broadcast(self):
        print("ClusterHeadDrone Broadcast")
        pass

    def Receive(self):
        print("ClusterHeadDrone Receive")
        pass

    def GetPosition(self):
        print("ClusterHeadDrone GetPosition")
        return 0,0,0


class IntermediateDrone(Drone):
    
    def Update(self):
        print("IntermediateDrone Update")
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


class CommonDrone(Drone):
    
    def Update(self):
        print("CommonDrone Update")
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


