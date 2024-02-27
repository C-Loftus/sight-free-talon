from talon import Module, Context, actions, settings
import os
import ipaddress
import json
import socket
import threading
from typing import Tuple
from .ipc_schema import IPC_COMMAND

mod = Module()
lock = threading.Lock()


@mod.action_class
class Actions:
    def addon_server_endpoint() -> Tuple[str, str, str]:
        """Returns the address, port, and valid commands for the addon server"""

    def send_ipc_commands(commands: list[IPC_COMMAND]):
        """Sends a command or commands to the screenreader"""
        actions.user.tts("No screenreader running to send commands to")
        raise NotImplementedError

    def send_ipc_command(command: IPC_COMMAND):
        """
        Sends a single command to the screenreader.
        This is its own function since old versions of talon
        don't support union type hints and having a separate
        function is a workaround a clearer API than passing in a list
        for a single command
        """
        actions.user.tts("No screenreader running to send commands to")
        raise NotImplementedError


NVDAContext = Context()
NVDAContext.matches = r"""
tag: user.nvda_running
"""


@NVDAContext.action_class("user")
class NVDAActions:

    def addon_server_endpoint() -> Tuple[str, str, str]:
        """Returns the address, port, and valid commands for the addon server"""
        SPEC_FILE = os.path.expanduser(
            "~\\AppData\\Roaming\\nvda\\talon_server_spec.json"
        )

        with open(SPEC_FILE, "r") as f:
            spec = json.load(f)
            address = spec["address"]
            port = spec["port"]
            valid_commands = spec["valid_commands"]

        try:
            if address == "localhost":
                ip = ipaddress.ip_address(socket.gethostbyname(address))
            else:
                ip = ipaddress.ip_address(address)
            assert ip.is_private, "Address is not a local IP address"
        except ValueError:
            raise ValueError(f"Invalid NVDA IP address: {address}")

        return address, port, valid_commands

    def send_ipc_commands(commands: list[IPC_COMMAND]):
        """Sends a list of commands or a single command string to the NVDA screenreader"""
        ip, port, valid_commands = actions.user.addon_server_endpoint()

        for command in commands:
            if command not in valid_commands:
                raise ValueError(f"Invalid command: {command}")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.2)
        encoded = json.dumps(commands).encode()

        if settings.get("user.addon_debug"):
            print(f"Sending {commands} to {ip}:{port}")

        # Although the screenreader server will block while processing commands,
        # having a lock client-side prevents errors when sending multiple commands
        with lock:
            try:
                sock.connect((ip, int(port)))
                sock.sendall(encoded)
                # Block until we receive a response
                # We don't want to execute commands until
                # we know the screen reader has the proper settings
                response = sock.recv(1024)
                if settings.get("user.addon_debug"):
                    print("Received", repr(response))

                if "debug" in commands:
                    actions.user.tts(
                        f"Sent Message to NVDA Successfully with server response: {response.decode('utf-8')}"
                    )

            except socket.timeout as e:
                print(f"Clientside connection with {ip}:{port} timed out")
                print(e)
                if "debug" in commands:
                    actions.user.tts("Clientside connection timed out")
            except:
                print("Error Communicating with NVDA extension")
                if "debug" in commands:
                    actions.user.tts("Error Communicating with NVDA extension")
            finally:
                sock.close()

    def send_ipc_command(command: IPC_COMMAND):
        """Sends a single command to the screenreader"""
        actions.user.send_ipc_commands([command])


ORCAContext = Context()
ORCAContext.matches = r"""
tag: user.orca_running
"""


JAWSContext = Context()
JAWSContext.matches = r"""
tag: user.jaws_running
"""
