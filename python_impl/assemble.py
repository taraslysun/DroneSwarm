from src.masterdrone import MasterDrone
import json

master = MasterDrone(0, port=30000, use_tcp=False)

demo_ip_1 = '192.168.1.51'
demo_ip_2 = '192.168.1.53'

drone_port = 10000

num_drones = 24

# master.Broadcast("{'command':'MOVE', 'coordinates':{'lat':10, 'lon':10, 'alt':10}}", demo_ip, drone_port)

for i in range(1,num_drones//2+1):
    master.Broadcast(json.dumps({'command':'MOVE', 'coordinates':{'lat':0, 'lon':i*10+10, 'alt':10}}), demo_ip_1, drone_port+i)

for i in range(num_drones//2+1,num_drones+1):
    master.Broadcast(json.dumps({'command':'MOVE', 'coordinates':{'lat':30, 'lon':i*10+10 - i, 'alt':10}}), demo_ip_2, drone_port+i)

for i in range(4):
    master.Broadcast(json.dumps({'command':'MOVE', 'coordinates':{'lat':50, 'lon':i*10+10, 'alt':10}}), demo_ip_1, 20000+i)
