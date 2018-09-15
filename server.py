import socket
import os

def listen():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(('127.0.0.1', 5555))
    connection.listen(10)
    print(('=' * 30), 'Main Server', ('=' * 30))
    while True:
        current_connection, address = connection.accept()
        print('Connection accepted')
        pid = os.fork()
        if pid == 0:
            while True:
                data = current_connection.recv(2048)

                if data == 'quit\n':
                    current_connection.shutdown(1)
                    current_connection.close()
                    break

                elif data == 'stop\n':
                    current_connection.shutdown(1)
                    current_connection.close()
                    exit()

                elif data:
                    current_connection.send(data)


if __name__ == "__main__":
    try:
        listen()
    except KeyboardInterrupt:
        pass