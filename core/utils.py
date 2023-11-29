# import threading
# import queue
# from talon import actions
import time

import threading
# source: https://stackoverflow.com/questions/47912701/python-how-can-i-implement-a-stoppable-thread

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

# # TTS blocks the main thread. If we spawn multiple threads we get many errors in the log
# # Intead of spawning many threads, we use a queue to send the text to a single thread
# class TTSScheduler:
#     def __init__(self):
#         self.queue = queue.Queue()
#         self.thread = threading.Thread(target=self._thread_function, daemon=True)
#         self.is_running = False

#     def start(self):
#         if not self.is_running:
#             self.is_running = True
#             self.thread.start()

#     def stop(self):
#         self.is_running = False
#         self.thread.join()

#     def _thread_function(self):
#         while self.is_running:
#             try:
#                 # Get a string from the queue with a timeout
#                 string_to_process = self.queue.get(timeout=1)
#                 actions.user.windows_robot_tts(string_to_process)
#             except queue.Empty:
#                 # Handle the case when the queue is empty
#                 pass
#             time.sleep(0.1)
    
#     def send(self, string_to_process):
#         self.queue.put(string_to_process)

# # ttsScheduler = TTSScheduler()
# # ttsScheduler.start()
