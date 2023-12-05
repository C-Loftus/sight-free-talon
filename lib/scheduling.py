import threading
import queue
import time
import os
import signal
from multiprocessing import Process
from typing import Optional

class Scheduler:
    queue = queue.Queue()
    is_running = False
    processes: list = []

    @classmethod
    def _start(cls):
        if not cls.is_running:
            cls.is_running = True
            cls.thread = threading.Thread(target=cls._handler, daemon=True)
            cls.thread.start()

    @classmethod
    def _handler(cls):
        while cls.is_running:
            try:
                # Get a process from the queue with a timeout
                proc = cls.queue.get(timeout=1)
                (fn, *args) = proc

                # Run fn(*args) in a separate process so it can be interrupted
                cls.process = Process(target=fn, args=args)
                cls.processes.append(cls.process)
                cls.process.start()
                cls.process.join()

            except queue.Empty:
                cls.is_running = False

            time.sleep(0.1)

    @classmethod
    def send(cls, function, *args): 
        if not cls.is_running:
            cls._start()

        cls.queue.put((function, *args))

    @classmethod
    def cancel(cls):
        if len(cls.processes) > 0:
            os.kill(cls.processes[0].pid, signal.SIGINT)

    @classmethod
    def cancel_all(cls):
        for process in cls.processes:
            os.kill(process.pid, signal.SIGINT)




# Make the Mutex generic over the value it stores.
# In this way we can get proper typing from the `lock` method.-
# class Mutex(Generic[T:=TypeVar("T")]):
#   # Store the protected value inside the mutex 
#   def __init__(self, value: T):
#     # Name it with two underscores to make it a bit harder to accidentally
#     # access the value from the outside.
#     self.__value = value
#     self.__lock = Lock()

#   # Provide a context manager `lock` method, which locks the mutex,
#   # provides the protected value, and then unlocks the mutex when the
#   # context manager ends.
#   @contextlib.contextmanager
#   def lock(self) -> ContextManager[T]:
#     self.__lock.acquire()
#     try:
#         yield self.__value
#     finally:
#         self.__lock.release()