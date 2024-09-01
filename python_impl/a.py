from src.masterdrone import MasterDrone
import json

master = MasterDrone(0, port=30000, use_tcp=False)

demo_ip = '192.168.1.51'

drone_port = 10000

num_drones = 7

# master.Broadcast("{'command':'MOVE', 'coordinates':{'lat':10, 'lon':10, 'alt':10}}", demo_ip, drone_port)

for i in range(1,num_drones+1):
    master.Broadcast(json.dumps({'command':'MOVE', 'coordinates':{'lat':0, 'lon':i*10+10, 'alt':i*10+10}}), demo_ip, drone_port+i)
