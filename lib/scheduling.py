import contextlib
import threading, multiprocessing
import queue
from typing import ContextManager, Generic, TypeVar
from talon import actions
import time, os

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()
        

    def stopped(self):
        return self._stop_event.is_set()


# TTS blocks the main thread. If we spawn multiple threads we get many errors in the log
# Intead of spawning many threads, we use a queue to send the text to a single thread
class Scheduler:
    queue = queue.Queue()
    is_running = False
    is_processing = False

    @classmethod
    def _start(cls):
        if not cls.is_running:
            cls.is_running = True
            cls.thread = StoppableThread(target=cls._handler, daemon=True)
            cls.thread.start()

    @classmethod
    def cancel(cls):
        if not cls.is_processing or not cls.is_running:
            return

        cls.thread.stop()
        cls.is_running = False
        cls.is_processing = False

        
    @classmethod
    def _handler(cls):
        while cls.is_running:
            try:
                # Get a process from the queue with a timeout
                proc = cls.queue.get(timeout=1)
                (fn, *args) = proc
                fn(*args)
                cls.is_processing = False

            except queue.Empty:
                # Handle the case when the queue is empty
                pass
            time.sleep(0.1)

    @classmethod
    def send(cls, function, *args): 
        if not cls.is_running:
            cls._start()

        cls.is_processing = True
        cls.queue.put((function, *args))

# class Scheduler:
#     queue = queue.Queue()
#     is_running = False
#     procs = []

#     @classmethod
#     def _start(cls):
#         if not cls.is_running:
#             cls.is_running = True
#             cls.thread = threading.Thread(target=cls._handler, daemon=True)
#             cls.thread.start()

#     # spawn processes that intentionally block a separate thread and 
#     # can be cancelled (allows for ordered, interruptible tts)
#     @classmethod
#     def _handler(cls):
#         while cls.is_running:
#             try:
#                 # Get a process from the queue with a timeout
#                 proc = cls.queue.get(timeout=1)
#                 (fn, *args) = proc
#                 proc = multiprocessing.Process(target=fn, args=args, daemon=False)
#                 cls.procs.append(proc)
#                 proc.start()
#                 proc.join()
#                 cls.procs.remove(proc)

#             except queue.Empty:
#                 # Handle the case when the queue is empty
#                 pass

#             time.sleep(0.1)

#     @classmethod
#     def send(cls, function, *args): 
#         if not cls.is_running:
#             cls._start()

#         cls.queue.put((function, *args))

#     @classmethod
#     def cancel(cls):
#         if len(cls.procs) == 0:
#             return

#         proc = cls.procs[0]
#         print(type(proc))

#         try:
#             os.kill(proc.pid, 9)
#         except Exception as e:
#             proc.kill()

#         cls.procs.remove(proc)
  

#     @classmethod
#     def cancel_all(cls):
#         try:
#             for proc in cls.procs:
#                 os.kill(proc.pid, 9)
#             cls.procs = []
#         except Exception as e:
#             print(e)

#     # create a contextlib lock that can be used to prevent multiple tts from happening at once
#     @classmethod
#     @contextlib.contextmanager
#     def lock(cls):
#         cls.lock.acquire()
#         try:
#             yield
#         finally:
#             cls.lock.release()

# # Make the Mutex generic over the value it stores.
# # In this way we can get proper typing from the `lock` method.
# class Mutex(Generic[T:=TypeVar("T")]):
#   # Store the protected value inside the mutex 
#   def __init__(self, value: T):
#     # Name it with two underscores to make it a bit harder to accidentally
#     # access the value from the outside.
#     self.__value = value
#     self.__lock = multiprocessing.Lock()

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