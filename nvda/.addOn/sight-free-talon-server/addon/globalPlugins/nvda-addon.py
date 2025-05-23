import enum
import json
import os
import socket
import threading
import time
import traceback
from datetime import datetime

import config
import globalPluginHandler
import globalVars
import tones

# Exhaustive list of valid commands
valid_commands = [
    "disableSpeechInterruptForCharacters",
    "enableSpeechInterruptForCharacters",
    "getSpeechInterruptForCharacters",
    "disableSpeakTypedWords",
    "enableSpeakTypedWords",
    "getSpeakTypedWords",
    "disableSpeakTypedCharacters",
    "enableSpeakTypedCharacters",
    "getSpeakTypedCharacters",
    "debug",
]


class ResponseSchema:
    def __init__(self):
        self.processedCommands = []
        self.returnedValues = []
        self.statusResults = []

    def generate():
        return {"processedCommands": [], "returnedValues": [], "statusResults": []}


# Handles both portable and installed versions of NVDA
SPEC_PATH = os.path.join(globalVars.appArgs.configPath, "talon_server_spec.json")


class StatusResult(enum.Enum):
    SUCCESS = "success"
    INTERNAL_SERVER_ERROR = "serverError"
    INVALID_COMMAND_ERROR = "commandError"
    RUNTIME_ERROR = "runtimeError"
    JSON_ENCODE_ERROR = "jsonEncodeError"


# Bind to an open port in case the specified port is not available
def bind_to_available_port(server_socket, start_port, end_port):
    for port in range(start_port, end_port):
        try:
            server_socket.bind(("localhost", port))
            return port
        except OSError:
            continue
    raise OSError(f"No available ports in the range {start_port}-{end_port}")


# Process a command, return the command and result as well as the retrieved value, if applicable
# Yes this is a big if/else block, but it's the most efficient way to handle the commands
def handle_command(command: str):
    command, value, result = command, None, None

    if command == "getSpeechInterruptForCharacters":
        value, result = (
            config.conf["keyboard"]["speechInterruptForCharacters"],
            StatusResult.SUCCESS,
        )

    elif command == "getSpeakTypedWords":
        value, result = config.conf["keyboard"]["speakTypedWords"], StatusResult.SUCCESS

    elif command == "getSpeakTypedCharacters":
        value, result = (
            config.conf["keyboard"]["speakTypedCharacters"],
            StatusResult.SUCCESS,
        )

    elif command == "disableSpeechInterruptForCharacters":
        config.conf["keyboard"]["speechInterruptForCharacters"] = False
        value, result = None, StatusResult.SUCCESS

    elif command == "enableSpeechInterruptForCharacters":
        config.conf["keyboard"]["speechInterruptForCharacters"] = True
        value, result = None, StatusResult.SUCCESS

    elif command == "disableSpeakTypedWords":
        config.conf["keyboard"]["speakTypedWords"] = False
        value, result = None, StatusResult.SUCCESS

    elif command == "enableSpeakTypedWords":
        config.conf["keyboard"]["speakTypedWords"] = True
        value, result = None, StatusResult.SUCCESS

    elif command == "disableSpeakTypedCharacters":
        config.conf["keyboard"]["speakTypedCharacters"] = False
        value, result = None, StatusResult.SUCCESS

    elif command == "enableSpeakTypedCharacters":
        config.conf["keyboard"]["speakTypedCharacters"] = True
        value, result = None, StatusResult.SUCCESS

    elif command == "debug":
        tones.beep(640, 100)
        value, result = None, StatusResult.SUCCESS

    else:
        value, result = None, StatusResult.INVALID_COMMAND_ERROR

    return command, value, result


class IPC_Server:
    port = None
    server_socket = None
    running = False
    client_socket = None

    def handle_client(self, client_socket: socket.socket):
        data = client_socket.recv(1024)

        response = ResponseSchema.generate()

        try:
            messages = json.loads(data.decode().strip())

            for message in messages:
                command, value, result = handle_command(message)
                response["processedCommands"].append(command)
                response["returnedValues"].append(value)
                # We can't pickle the StatusResult enum, so we have to convert it to a string
                response["statusResults"].append(result.value)

        except json.JSONDecodeError as e:
            print(f"RECEIVED INVALID JSON FROM TALON: {e}")
            response["statusResults"] = [StatusResult.JSON_ENCODE_ERROR.value]

        finally:
            client_socket.sendall(json.dumps(response).encode("utf-8"))

    def output_spec_file(self):
        # write a json file to let clients know how to connect and what commands are available
        spec = {
            "address": "localhost",
            "port": str(self.get_port()),
            "valid_commands": valid_commands,
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
        print(f"\n\n\n\n\nTALON SERVER SERVING ON {self.server_socket.getsockname()}")

        self.running = True

        while self.running:
            try:
                # If it was closed from another thread, we want to break out of the loop
                if not self.server_socket:
                    break

                client_socket, _ = self.server_socket.accept()
                self.client_socket = client_socket
                self.client_socket.settimeout(0.3)
                self.handle_client(self.client_socket)
            # If the socket times out, we just want to keep looping
            except socket.timeout:
                pass
            except Exception as e:
                print(f"\n\n\n\nTALON SERVER CRASH: {e}")
                self.stop()
                with open(
                    os.path.join(
                        globalVars.appArgs.configPath, "talon_server_error.log"
                    ),
                    "a",
                ) as f:
                    f.write(
                        f"\nERROR AT {datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')}: {e}"
                    )
                    f.write(f"\n{traceback.format_exc()}")
                    f.write(f"\nINTERNAL STATE: {self.__dict__}\n")
                break
            finally:
                # Called no matter what even after a break
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
