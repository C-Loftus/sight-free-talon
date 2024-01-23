from talon import Module, Context, actions
import os, ipaddress, json, socket
from .ipc_helpers import Mutex
import threading


mod = Module()
mutex = threading.Lock()

communication_socket = None

@mod.action_class
class Actions:
    def addon_server_endpoint() -> (str, str):
        """Returns the address and port of the addon server"""

    def send_ipc_command(command: str):
        """Sends a command to the screenreader"""

    def sanitize_ipc_command(command: str):
        """Make sure the IPC command is valid"""

NVDAContext = Context()
NVDAContext.matches = r"""
tag: user.nvda_running
"""

@NVDAContext.action_class("user")
class NVDAActions:

    def addon_server_endpoint() -> (str, str):
        """Returns the address and port of the addon server"""
        SPEC_FILE = os.path.expanduser("~\\AppData\\Roaming\\nvda\\talon_server_spec.json")

        with open(SPEC_FILE, "r") as f:
            spec = json.load(f)
            address = spec["address"]
            port = spec["port"]
            valid_commands = spec["valid_commands"]
            
        # assert the address is a valid IP address
        try:
            ip = ipaddress.ip_address(address)
            assert ip.is_private, "Address is not a local IP address"
        except ValueError:
            raise ValueError(f"Invalid IP address: {address}")
        
        return address, port, valid_commands

    
    def send_ipc_command(command: str):
        """Sends a command to the NVDA screenreader"""
        ip, port, valid_commands = actions.user.addon_server_endpoint()
        
        if command not in valid_commands:
            raise ValueError(f"Invalid NVDA IPC command: '{command}'")


        with mutex:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, int(port)))
            try:
                encoded = command.encode("utf-8")
                sock.sendall(encoded)
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


