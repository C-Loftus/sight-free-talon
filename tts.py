from typing import Optional
from talon import Module, actions, Context, settings, cron, ui, registry, scope, clip
import requests
import json, os, time, subprocess, multiprocessing
from pathlib import Path
# from .utils import StoppableThread

if os.name == 'nt':
    import win32com.client

mod = Module()
ctx = Context()

mod.setting(
    "tts_speed",
    type=float,
    default=1.0,
    desc="Speed of text to speech",
)

mod.setting(
    "echo_context",
    type=bool,
    default=False,
    desc="If true, plays back dictation with text to speech",
)

# TTS_IN_PROGRESS: Optional[StoppableThread] = None

@mod.action_class
class Actions:

    def windows_robot_tts(text: str):
        """text to speech with windows voice
         this function should never be overwritten and is used to be called from within the robot
         function which can be overwritten by the user
        """
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.rate = settings.get("user.tts_speed", 1.0)
        cron.after("0s", lambda: speaker.Speak(text))

        # TODO:  this doesn't work to stop text to speech in the middle of speaking
        # # for some reason, TODO fix this
        #  
        # global TTS_IN_PROGRESS
        # if TTS_IN_PROGRESS:
        #     if not TTS_IN_PROGRESS.stopped():
        #         actions.user.notify('stopped')
        #         TTS_IN_PROGRESS.stop()
            
        # TTS_IN_PROGRESS = StoppableThread(target=speaker.Speak, args=(text,))
        # TTS_IN_PROGRESS.start()

    def toggle_echo():
        """Toggles echo dictation on and off"""

        ctx.settings["user.echo_dictation"] = not settings.get("user.echo_dictation")
        if settings.get("user.echo_dictation"):
            actions.user.robot_tts("echo dictation enabled")
        else:
            actions.user.robot_tts("echo dictation disabled")
    
    def toggle_echo_context():
        """Toggles echo context on and off"""

        ctx.settings["user.echo_context"] = not settings.get("user.echo_context")
        if settings.get("user.echo_context"):
            actions.user.robot_tts("echo context enabled")
        else:
            actions.user.robot_tts("echo context disabled")
        

    def toggle_echo_all():
        """Toggles echo dictation and echo context on and off"""

        dictation, context = settings.get("user.echo_dictation"), settings.get("user.echo_context")

        if any([dictation, context]):
            actions.user.robot_tts("echo disabled")
            ctx.settings["user.echo_dictation"] = False
            ctx.settings["user.echo_context"] = False
        else:
            actions.user.robot_tts("echo enabled")
            ctx.settings["user.echo_dictation"] = True
            ctx.settings["user.echo_context"] = True


    def echo_context(include_title: bool = False):
        """Echo the current context"""
        friendly_name = actions.app.name() 
        title = ui.active_window().title 

        if include_title: 
            actions.user.robot_tts(f"{friendly_name} {title}") 
        else:
            actions.user.robot_tts(str(friendly_name))


    def robot_tts(text: str):
        '''text to speech with robot voice'''

    def edge_tts(text: str):
        '''text to speech with edge'''
        # edge-playback --text "Hello, world!"
        #get path of this file
        this_path = os.path.dirname(os.path.realpath(__file__))
        script_path = os.path.join(this_path, 'edge-playback.ps1')

        actions.user.notify('Starting edge TTS')
        p = subprocess.Popen(["powershell.exe", script_path, text], shell=True, env=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p_status = p.wait()
        stdout, stderr = p.communicate()
        print(stdout, stderr)
        return (stdout, stderr)

    def natural_tts(text: str):
        """text to speech with natural voice"""
        # Split the text into batches of 2400 characters since
        # 11 labs has a limit of 2500 characters per request
        ## TODO make it not split a word in the middle
        batch_size = 2400
        batches = [text[i:i+batch_size] 
                   for i in range(0, len(text), batch_size)
                ]
        for batched_text in batches:
            # Define the API endpoint URL
            url = 'https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM?optimize_streaming_latency=0&output_format=mp3_44100_128'
    
            # Define the request headers
            headers = {
                'accept': 'audio/mpeg',
                'xi-api-key': os.environ["11LABS_KEY"],
                'Content-Type': 'application/json',
            }
    
            # Define the request data as a Python dictionary
            data = {
                'text': batched_text,
                'model_id': 'eleven_monolingual_v1',
                'voice_settings': {
                    'stability': 0,
                    'similarity_boost': 0,
                    'style': 0,
                    'use_speaker_boost': True
                }
            }
    
            # Convert the data dictionary to JSON format
            data_json = json.dumps(data)
    
            # Make the POST request
            actions.user.notify('Requesting audio file...')
            response = requests.post(url, headers=headers, data=data_json)
    
            # Check the response status and content
            if response.status_code != 200:
                actions.user.notify(f'Request failed with status code {response.status_code}:')
                print(response.text)
            
            # Request was successful
            basename = f'output-{time.time()}.mp3'

            output_dir = 'tts'
            if len(batches) > 1:
                # first 10 chars
                dir_header = str(batches[0][:10]).strip().replace(' ', '_').replace('\\', '_')

                output_dir = os.path.join(output_dir, dir_header)

            Path(output_dir).mkdir(parents=True, exist_ok=True)
    
            full_name = os.path.join(output_dir, basename)

            with open(full_name, 'wb') as f:
                f.write(response.content)
            print('Audio file saved as ' + full_name)


ctxWindows = Context()
ctxWindows.matches = r"""
os: windows
"""

@ctxWindows.action_class('user')
class UserActions:
    def robot_tts(text: str):
        """text to speech"""
        actions.user.windows_robot_tts(text)

def on_app_switch(app):
    if not settings.get("user.echo_context"):
        return 
    
    actions.user.echo_context()

last_title = None
def on_title_switch(win):
    if not settings.get("user.echo_context"):
        return
    
    window = ui.active_window()
    active_window_title = window.title
    # get just the first two word
    active_window_title = ' '.join(active_window_title.split()[:2])
    #trime the title to 20 characters so super long addresses don't get read
    active_window_title = active_window_title[:20]

    global last_title
    if last_title == active_window_title:
        return
    else:
        last_title = active_window_title

    actions.user.robot_tts(f"{active_window_title}")

last_mode = None
def on_update_contexts():
    global last_mode

    modes = scope.get("mode") or []
    if last_mode == 'sleep' and 'sleep' not in modes:
        actions.user.robot_tts(f'Talon has waken up')
    last_mode = modes
    if "sleep" in modes:
        last_mode  = "sleep"
    else:
        last_mode = "other"
        

registry.register("update_contexts", on_update_contexts)
ui.register("app_activate", on_app_switch)
ui.register("win_title", on_title_switch)
