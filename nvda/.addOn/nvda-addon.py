import globalPluginHandler
from scriptHandler import script
import config
import tones
import os, json, socket, threading


commands = ["disableSpeechInterruptForCharacters", "restoreSpeechInterruptForCharacters"]

interrupt_value = False

def handle_command(command: str):
	global interrupt_value
	if command == "disableSpeechInterruptForCharacters":
		interrupt = config.conf["keyboard"]["speechInterruptForCharacters"]
		interrupt_value = interrupt
		config.conf["keyboard"]["speechInterruptForCharacters"] = False
	if command == "restoreSpeechInterruptForCharacters": 
		config.conf["keyboard"]["speechInterruptForCharacters"] = interrupt_value
	else:
		print("Invalid command: {command}")
		
	tones.beep(440, 100) 


class IPC_Server():

    def handle_client(self, client_socket: socket.socket):
        data = client_socket.recv(1024)
        message = data.decode().strip()
        print(f"Received {message}")
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nMessage received. Success".encode()  # Create a HTTP response
        client_socket.send(response)

    def output_spec_file(self):
        # write a json file to os.path.expanduser("~\\AppData\\Roaming\\nvda\\talon_server_spec.json")
        # with ip address and port as well as commands
        PATH = os.path.expanduser("~\\AppData\\Roaming\\nvda\\talon_server_spec.json")
        spec = {
            "ip": "127.0.0.1",
            "port": "8888",
            "commands": commands    
        }
        with open(PATH, "w") as f:
            json.dump(spec, f)

    def create_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('127.0.0.1', 8888))
        server_socket.listen(1)
        server_socket.settimeout(None)  # Set the timeout to None
        print(f'Serving on {server_socket.getsockname()}')

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            self.handle_client(client_socket)
            client_socket.close()

server = IPC_Server()
server_thread = threading.Thread(target=server.create_server)
server_thread.start()