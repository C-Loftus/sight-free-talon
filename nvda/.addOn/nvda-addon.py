import speech
from scriptHandler import script
import config
import tones, nvwave, ui
import os, json, socket, threading

commands = ["disableSpeechInterruptForCharacters", "restoreSpeechInterruptForCharacters", "debug", "playWAV"]

def bind_to_available_port(server_socket, start_port, end_port):
    for port in range(start_port, end_port):
        try:
            server_socket.bind(('127.0.0.1', port))
            return port
        except OSError:
            continue
    raise OSError(f"No available ports in the range {start_port}-{end_port}")

interrupt_value = False
def handle_command(command: str):
    global interrupt_value
    debug_message = ""
    if command == "disableSpeechInterruptForCharacters":
        interrupt = config.conf["keyboard"]["speechInterruptForCharacters"]
        interrupt_value = interrupt
        config.conf["keyboard"]["speechInterruptForCharacters"] = False
        debug_message = f"Speech interrupt changed from {interrupt} to False"
    if command == "restoreSpeechInterruptForCharacters": 
        config.conf["keyboard"]["speechInterruptForCharacters"] = interrupt_value
        debug_message = f"Speech interrupt restored to {interrupt_value}"
    elif command == "debug":
        tones.beep(640, 100) 
        debug_message = "Debug connection successful"
    else:
        debug_message = f"Invalid command: '{command}', {type(command)=}"
    print(debug_message)
    return debug_message
        
class IPC_Server():
    port = None

    def handle_client(self, client_socket: socket.socket):
        data = client_socket.recv(1024)
        message = data.decode().strip()
        result = handle_command(message)
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nMessage received. Success: {result}".encode()  # Create a HTTP response
        client_socket.send(response)

    def output_spec_file(self):
        # write a json file to let clients know how to connect and what commands are available
        PATH = os.path.expanduser("~\\AppData\\Roaming\\nvda\\talon_server_spec.json")
        spec = {
            "address": "127.0.0.1",
            "port": str(self.get_port()),
            "valid_commands": commands    
        }
        with open(PATH, "w") as f:
            json.dump(spec, f)
        
    def set_port(self, port):
        self.port = port

    def get_port(self):
        return self.port

    def create_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = bind_to_available_port(server_socket, 8888, 9000)
        self.set_port(port)
        self.output_spec_file()
        
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