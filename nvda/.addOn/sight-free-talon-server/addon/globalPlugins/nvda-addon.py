import config
import tones
import globalPluginHandler
import os, json, socket, threading

# Exhaustive list of valid commands
schema = [
    "disableSpeechInterruptForCharacters",
    "enableSpeechInterruptForCharacters",

    "disableSpeakTypedWords",
    "enableSpeakTypedWords",

    "disableSpeakTypedCharacters",
    "enableSpeakTypedCharacters",

    "debug"
]

# Bind to an open port in case the specified port is not available
def bind_to_available_port(server_socket, start_port, end_port):
    for port in range(start_port, end_port):
        try:
            server_socket.bind(('127.0.0.1', port))
            return port
        except OSError:
            continue
    raise OSError(f"No available ports in the range {start_port}-{end_port}")

# Change a setting based on a message from the client
def handle_command(command: str):
    if command not in schema:
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
    server_socket = None

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
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = bind_to_available_port(self.server_socket, 8888, 9000)
        self.set_port(port)
        self.output_spec_file()
        
        self.server_socket.listen(1)
        self.server_socket.settimeout(None)  # Set the timeout to None
        print(f'Serving on {self.server_socket.getsockname()}')

        while True:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f"Connection from {addr}")
                self.handle_client(client_socket)
            except Exception as e:
                print(f"Error handling message from client: {e}")
            finally:
                client_socket.close()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    def __init__(self):
        super(GlobalPlugin, self).__init__()

    def terminate(self):
        # clean up when NVDA exits     
        PATH = os.path.expanduser("~\\AppData\\Roaming\\nvda\\talon_server_spec.json")
        os.remove(PATH)
        if server.server_socket:
            server.server_socket.close()
        

server = IPC_Server()
server_thread = threading.Thread(target=server.create_server)
server_thread.start()
