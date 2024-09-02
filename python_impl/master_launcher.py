import json
from src.masterdrone import MasterDrone


demo_ip = '192.168.1.51'


def main():
    cluster_heads = []
    for i in range(4):
        cluster_heads.append((20000+i, demo_ip, 20000+i))

    master = MasterDrone(30000,
                        port=30000,
                        use_tcp=False,
                        position=(0, 0, 0),
                        target_coordinates=(0, 0, 0),
                        step_distance=1,
                        cluster_heads=cluster_heads)
    master.Operation()

if __name__ == "__main__":
    main()
    