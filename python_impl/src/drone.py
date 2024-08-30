class Drone:
    def __init__(self, id):
        self.id = id
        self.latitude=0
        self.longitude=0
        self.height=0
        self.camera=None
        
    def Act(self):
        print(f"Base Act of drone {self.id}")
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

