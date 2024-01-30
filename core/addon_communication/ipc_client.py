from talon import Module, Context, actions, settings
import os, ipaddress, json, socket
import threading
from typing import Tuple
from .ipc_schema import IPC_COMMAND

mod = Module()
lock = threading.Lock()

@mod.action_class
class Actions:
    def addon_server_endpoint() -> Tuple[str, str, str]:
        """Returns the address, port, and valid commands for the addon server"""

    def send_ipc_commands(commands: list[str] | str):
        """Sends a command or commands to the screenreader"""


NVDAContext = Context()
NVDAContext.matches = r"""
tag: user.nvda_running
"""

@NVDAContext.action_class("user")
class NVDAActions:

    def addon_server_endpoint() -> Tuple[str, str, str]:
        """Returns the address and port of the addon server"""
        SPEC_FILE = os.path.expanduser("~\\AppData\\Roaming\\nvda\\talon_server_spec.json")

        with open(SPEC_FILE, "r") as f:
            spec = json.load(f)
            address = spec["address"]
            port = spec["port"]
            valid_commands = spec["valid_commands"]
            
        try:
            ip = ipaddress.ip_address(address)
            assert ip.is_private, "Address is not a local IP address"
        except ValueError:
            raise ValueError(f"Invalid IP address: {address}")
        
        return address, port, valid_commands
        

    def send_ipc_commands(commands: list[str] | str):
        """Sends a list of commands or a single command string to the NVDA screenreader"""
        ip, port, valid_commands = actions.user.addon_server_endpoint()

        if isinstance(commands, str):
            commands = [commands]

        for command in commands:
            if command not in valid_commands:
                raise ValueError(f"Invalid command: {command}")
            
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        encoded = json.dumps(commands).encode()

        if settings.get("user.addon_debug"):
            print(f"Sending {commands} to {ip}:{port}")
            
        # Although the screenreader server will block while processing commands,
        # having a lock clientside reduces errors when sending multiple commands
        with lock:
            try:
                sock.connect((ip, int(port)))
                sock.sendall(encoded)
                # Block until we receive a response
                # We don't want to execute commands until
                # we know the screen reader has the proper settings
                response = sock.recv(1024)
                if settings.get("user.addon_debug"):
                    print('Received', repr(response))

                if 'debug' in commands:
                    actions.user.tts("Sent Message to NVDA Successfully")
                    
            except socket.timeout:
                print("NVDA Addon Connection timed out")
            except: 
                print("Error Communicating with NVDA extension")
            finally:
                sock.close()
            

ORCAContext = Context()
ORCAContext.matches = r"""
tag: user.orca_running
"""


JAWSContext = Context()
JAWSContext.matches = r"""
tag: user.jaws_running
"""
