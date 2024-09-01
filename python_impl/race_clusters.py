from src.masterdrone import MasterDrone
import json

master = MasterDrone(0, port=30000, use_tcp=False)

demo_ip_1 = '192.168.1.51'
demo_ip_2 = '192.168.1.53'

ch_port = 20000

for i in range(4):
    # master.Broadcast(json.dumps({'command':'MOVE', 'coordinates':{'lat':i*200, 'lon':i+500, 'alt':50}}), demo_ip_1, ch_port+i)
    target = (i*200, i+500, 50)
    
