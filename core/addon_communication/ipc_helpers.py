import contextlib
import subprocess
from threading import Lock
from typing import ContextManager, Generic, TypeVar


def get_pid_by_port(port):
    try:
        result = subprocess.run(
            ["netstat", "-ano", "-p", "TCP"], capture_output=True, text=True, check=True
        )
        lines = result.stdout.split("\n")

        for line in lines:
            if f":{port}" in line:
                parts = line.split()
                pid = parts[-1]
                return pid
    except subprocess.CalledProcessError:
        print("Error executing netstat command.")

    return None


def kill_process_by_port(port):
    pid = get_pid_by_port(port)

    if pid:
        try:
            subprocess.run(["taskkill", "/F", "/PID", pid], check=True)
            print(f"Process with PID {pid} using port {port} terminated.")
        except subprocess.CalledProcessError:
            print(f"Error terminating process with PID {pid}.")
    else:
        print(f"No process found using port {port}.")


class Mutex(Generic[T := TypeVar("T")]):
    # Store the protected value inside the mutex
    def __init__(self, value: T):
        # Name it with two underscores to make it a bit harder to accidentally
        # access the value from the outside.
        self.__value = value
        self.__lock = Lock()

    # Provide a context manager `lock` method, which locks the mutex,
    # provides the protected value, and then unlocks the mutex when the
    # context manager ends.
    @contextlib.contextmanager
    def lock(self) -> ContextManager[T]:
        self.__lock.acquire()
        try:
            yield self.__value
        finally:
            self.__lock.release()
