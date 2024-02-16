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

SPEC_PATH = os.path.expanduser("~\\AppData\\Roaming\\nvda\\talon_server_spec.json")

# Bind to an open port in case the specified port is not available
def bind_to_available_port(server_socket, start_port, end_port):
    for port in range(start_port, end_port):
        try:
            server_socket.bind(('localhost', port))
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
    running = False 
    client_socket = None

    def handle_client(self, client_socket: socket.socket):
        data = client_socket.recv(1024)

        try:
            messages = json.loads(data.decode().strip())
        except json.JSONDecodeError:
            print("Invalid JSON")
            response = f"HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nInvalid JSON".encode()
            client_socket.sendall(response)
            return
        
        result = ""
        for message in messages:
            result += handle_command(message)

        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nMessage received: Result: {result}".encode()  # Create a HTTP response
        client_socket.sendall(response)

    def output_spec_file(self):
        # write a json file to let clients know how to connect and what commands are available
        spec = {
            "address": "localhost",
            "port": str(self.get_port()),
            "valid_commands": schema    
        }
        with open(SPEC_PATH, "w") as f:
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
        self.server_socket.settimeout(5)
        print(f'\n\n\n\n\nSERVING TALON SERVER with {self.server_socket.getsockname()}')

        self.running = True

        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f"\n\n\n\n\nConnection from {addr}")

                self.client_socket = client_socket
                self.client_socket.settimeout(2)
                self.handle_client(self.client_socket) 
            except socket.timeout:
                pass
            except Exception as e:
                print(f"\n\n\n\nTALON NVDA CRASH: {e}")
                self.stop()
                break
            finally:
                if self.client_socket:
                    self.client_socket.close()

        print("\n\n\n\n\nSERVER STOPPED")
        
    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        if self.client_socket:
            self.client_socket.close()
        if os.path.exists(SPEC_PATH):
            os.remove(SPEC_PATH)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    def __init__(self):
        super(GlobalPlugin, self).__init__()

    def terminate(self):
        # clean up when NVDA exits     
        server.stop()
        

server = IPC_Server()
server_thread = threading.Thread(target=server.create_server)
server_thread.start()
    