import socket
import os, sys
import signal

def start_connection():
	PORT = 6000
	print(('=' * 30), 'Printer Server', ('=' * 30))
	connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	try:
		connection.bind(('127.0.0.1', PORT))
	except:
		print('agas')
		os.kill(os.getppid(), signal.SIGHUP)
	connection.listen(10)
	print('Waiting for connections ...')
	ppid = os.getppid()
	while True:
		current_connection, address = connection.accept()
		print('Connection accepted')
		pid = os.fork()
		if pid == 0:
			while True:
				data = current_connection.recv(2048)
				if 'kill_print' in data.decode():
					os.kill(ppid, signal.SIGHUP)
				if len(data) == 0:
					print('Connection closed')
					break
				print(data.decode())
		else:
			current_connection.close()

if __name__ == "__main__":
	start_connection()
