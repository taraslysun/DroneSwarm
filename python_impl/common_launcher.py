from src.commondrone import CommonDrone
import multiprocessing
import random


demo_ip = '192.168.1.51'

def start_common_drone(i, port):
    # start_position = (i*10, 0, 0)
    # target = (i*10, 10+i*10, 0)
    start_position = (random.randint(0, 300), random.randint(0, 300), random.randint(10, 50))
    target = (random.randint(0, 300), random.randint(0, 300), random.randint(10, 50))
    print(start_position, target, i)
    drone = CommonDrone(i+10000, 
                        port=port,
                        use_tcp=False, 
                        cluster_head=(0, '192.168.1.51', 20000),
                        step_distance=0.2, 
                        target_coordinates=target, 
                        position=start_position)
    drone.Operation(demo_ip=demo_ip)


def main(num=12):
    num = 12
    processes = []
    for i in range(1,num+1):
        p = multiprocessing.Process(target=start_common_drone, args=(i, 10000+i))
        p.start()
        processes.append(p)



if __name__ == "__main__":
    main()



    # parser = argparse.ArgumentParser()
    # parser.add_argument('lat', type=float, help='latitude')
    # parser.add_argument('lon', type=float, help='longitude')
    # parser.add_argument('alt', type=float, help='altitude')
    # parser.add_argument('lat1', type=float, help='latitude')
    # parser.add_argument('lon1', type=float, help='longitude')
    # parser.add_argument('alt1', type=float, help='altitude')

    # args = parser.parse_args()
    # main([args.lat, args.lon, args.alt], [args.lat1, args.lon1, args.alt1])
