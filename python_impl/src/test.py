import socket
import argparse
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # For TCP
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # For UDP

def main(ip, port, message):
    s.connect((ip, port))
    s.sendall(message.encode())
    s.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # positional arguments
    parser.add_argument("ip", help="IP address of the server")
    parser.add_argument("port", help="Port of the server", type=int)
    parser.add_argument("message", help="Message to send to the server")
    args = parser.parse_args()
    main(args.ip, args.port, args.message)
