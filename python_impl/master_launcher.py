import json
from src.masterdrone import MasterDrone


demo_ip = '192.168.1.51'


def main():
    cluster_heads = []
    for i in range(4):
        cluster_heads.append((20000+i, demo_ip, 20000+i))

    master = MasterDrone(0,
                        port=30000,
                        use_tcp=False,
                        position=(0, 0, 0),
                        step_distance=1,
                        cluster_heads=cluster_heads)
    # master.Operation()
    # for i in range(4):
    #     master.Broadcast(json.dumps({'command':'CLUSTER'}), demo_ip, 20000+i)
    for id, ip, port in cluster_heads:
        master.Broadcast(json.dumps({'command':'CLUSTER'}), ip, port)

if __name__ == "__main__":
    main()
    