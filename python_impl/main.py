from src.drone_types.drone import Drone, MasterDrone, ClusterHeadDrone, IntermediateDrone, CommonDrone


drones = [Drone(0), MasterDrone(1), ClusterHeadDrone(2), IntermediateDrone(3), CommonDrone(4)]

for d in drones:
    d.Update()