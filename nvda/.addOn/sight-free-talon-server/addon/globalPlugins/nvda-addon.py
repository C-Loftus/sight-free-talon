import speech
from scriptHandler import script
import config
import tones, nvwave, ui
import os, json, socket, threading
import globalPluginHandler

schema = [
    "disableSpeechInterruptForCharacters",
    "enableSpeechInterruptForCharacters",

    "disableSpeakTypedWords",
    "enableSpeakTypedWords",

    "disableSpeakTypedCharacters",
    "enableSpeakTypedCharacters",

    "debug"
]


def bind_to_available_port(server_socket, start_port, end_port):
    for port in range(start_port, end_port):
        try:
            server_socket.bind(('127.0.0.1', port))
            return port
        except OSError:
            continue
    raise OSError(f"No available ports in the range {start_port}-{end_port}")

def handle_command(command: str):
    if command not  in schema:
        return f"Invalid command: '{command}', type='{type(command)}'"

    if command == "disableSpeechInterruptForCharacters":
        config.conf["keyboard"]["speechInterruptForCharacters"] = False

    elif command == "enableSpeechInterruptForCharacters": 
        config.conf["keyboard"]["speechInterruptForCharacters"] = True 

    elif command == "disableSpeakTypedWords": 
        config.conf["keyboard"]["speakTypedWords"] = False 

    elif command == "enableSpeakTypedWords":
        config.conf["keyboard"]["speakTypedWords"] = True

    elif command == "disableSpeakTypedCharacters": 
        config.conf["keyboard"]["speakTypedCharacters"] = False 

    elif command == "enableSpeakTypedCharacters":
        config.conf["keyboard"]["speakTypedCharacters"] = True
        
    elif command == "debug":
        tones.beep(640, 100) 

    return f"Success: {command}"
        
class IPC_Server():
    port = None

    def handle_client(self, client_socket: socket.socket):
        data = client_socket.recv(1024)

        messages = json.loads(data.decode().strip())
        result = ""
        for message in messages:
            result += handle_command(message)

        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nMessage received: Result: {result}".encode()  # Create a HTTP response
        client_socket.send(response)

    def output_spec_file(self):
        # write a json file to let clients know how to connect and what commands are available
        PATH = os.path.expanduser("~\\AppData\\Roaming\\nvda\\talon_server_spec.json")
        spec = {
            "address": "127.0.0.1",
            "port": str(self.get_port()),
            "valid_commands": schema    
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


class GlobalPlugin(globalPluginHandler.GlobalPlugin):



    def __init__(self):
        super(GlobalPlugin, self).__init__()


    def terminate(self):
        # delete this file when NVDA exits     
        PATH = os.path.expanduser("~\\AppData\\Roaming\\nvda\\talon_server_spec.json")
        os.remove(PATH)

server = IPC_Server()
server_thread = threading.Thread(target=server.create_server)
server_thread.start()