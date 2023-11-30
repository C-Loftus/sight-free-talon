import threading
import queue
from talon import actions
import time

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

    @classmethod
    def start(cls):
        if not cls.is_running:
            cls.is_running = True
            cls.thread = StoppableThread(target=cls._handler, daemon=True)
            cls.thread.start()

    @classmethod
    def cancel(cls):
        cls.is_running = False
        cls.thread.stop()

    @classmethod
    def _handler(cls):
        while cls.is_running:
            try:
                # Get a process from the queue with a timeout
                proc = cls.queue.get(timeout=1)
                (fn, *args) = proc
                fn(*args)

            except queue.Empty:
                # Handle the case when the queue is empty
                pass
            time.sleep(0.1)

    @classmethod
    def send(cls, function, *args):
        cls.queue.put((function, *args))

Scheduler.start()

# Make the Mutex generic over the value it stores.
# In this way we can get proper typing from the `lock` method.
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