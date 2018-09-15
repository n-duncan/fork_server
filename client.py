import socket
import os
from time import sleep

def start_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.connect(('127.0.0.1', 5555))  # Connect
    print('connected')

    os.system("gnome-terminal -e 'bash -c \"python3 printer.py; read\"'")  # Open printing server
    sleep(1.0)  # Wait for server to get established

    print_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print_sock.connect(('127.0.0.1', 6000))  # Connect to printing server
    pid = os.fork()  # Fork

    while True:  # Iterate until interrupt 
        if pid == 0:
            while True:  # Continuously recieve and forward to print server
                data = sock.recv(2048, socket.MSG_PEEK)
                if len(data) == 0:
                    os._exit(0)
                if '<child>' in data.decode():
                    print_sock.send(sock.recv(2048))  # Send data from buffer into the print server
        else:
            send_data = input('Enter data to be sent: ').encode()
            if send_data.decode() == 'connect':
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                sock.connect(('127.0.0.1', 5555))  # Connect
                continue
            sock.send(send_data)
            data = sock.recv(2048, socket.MSG_PEEK)
            if '<parent>' in data.decode():
                print('Parent: ', data.decode())
                data = sock.recv(2048) # Clear out data
            if '<parent>' not in data.decode() and '<child>' not in data.decode():
                print('Not addressed for parent or child, clearing buffer')
                data = sock.recv(2048)



if __name__ == "__main__":
    try:
        start_connection()
    except KeyboardInterrupt:
        pass