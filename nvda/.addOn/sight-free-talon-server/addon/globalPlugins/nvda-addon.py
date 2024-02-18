import config
import tones
import globalPluginHandler
import os, json, socket, threading
import globalVars

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

# Handles both portable and installed versions of NVDA
SPEC_PATH = os.path.join(globalVars.appArgs.configPath, "talon_server_spec.json") 

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
        except json.JSONDecodeError as e:
            print(f"RECEIVED INVALID JSON FROM TALON: {e}")
            response = f"TALON SERVER ERROR: {e}".encode()
            client_socket.sendall(response)
            return
        
        result = ""
        for message in messages:
            result += handle_command(message)

        response = f"TALON COMMAND PROCESSED: {result}".encode()
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
        # Need a time short enough that we can reboot NVDA and the old socket will be closed and won't interfere
        self.server_socket.settimeout(0.5)
        print(f'\n\n\n\n\nTALON SERVER SERVING ON {self.server_socket.getsockname()}')

        self.running = True

        while self.running:
            try:
                client_socket, _ = self.server_socket.accept()
                self.client_socket = client_socket
                self.client_socket.settimeout(0.3)
                self.handle_client(self.client_socket) 
            except socket.timeout:
                pass
            except Exception as e:
                print(f"\n\n\n\nTALON SERVER CRASH: {e}")
                self.stop()
                break
            finally:
                if self.client_socket:
                    self.client_socket.close()

    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        if self.client_socket:
            self.client_socket.close()
        if os.path.exists(SPEC_PATH):
            os.remove(SPEC_PATH)
        print("\n\n\n\n\nTALON SERVER STOPPED")

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    def __init__(self):
        super(GlobalPlugin, self).__init__()

    def terminate(self):
        # clean up when NVDA exits     
        server.stop()
        

server = IPC_Server()
server_thread = threading.Thread(target=server.create_server)
server_thread.start()
    