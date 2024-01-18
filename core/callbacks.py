from talon import scope, registry, ui, actions, settings, speech_system, app

def on_phrase(parsed_phrase):
    if actions.speech.enabled() and actions.user.echo_dictation_enabled():
        words = parsed_phrase.get("text")
        if words:
            command_chain = " ".join(words)

            # Not all tts engines support canceling
            # Easier to just catch the exception
            try:
                actions.user.cancel_current_speaker()
            except Exception as e:
                pass

            actions.user.tts(command_chain)

            if settings.get("user.braille_output"):
                actions.user.braille(command_chain)


def on_app_switch(app):
    if not actions.user.echo_context_enabled():
        return
    actions.user.echo_context()


# We have to keep track of the last title so we don't repeat it
# since sometimes Talon triggers a "title switch" when
# the title actually hasn't changed, i.e. when a text file is saved
last_title = None
def on_title_switch(win):
    if not actions.user.echo_context_enabled():
        return
    window = ui.active_window()
    active_window_title = window.title
    # get just the first two words
    active_window_title = " ".join(active_window_title.split()[:2])
    # trime the title to 20 characters so super long addresses don't get read
    active_window_title = active_window_title[:20]

    global last_title
    if last_title == active_window_title:
        return

    last_title = active_window_title
    actions.user.tts(f"{active_window_title}")


last_mode = None
def on_update_contexts():
    global last_mode
    modes = scope.get("mode") or []

    MIXED =  ("command" in modes and "dictation" in modes)
    COMMAND = ("command" in modes and "dictation" not in modes)
    DICTATION = ("dictation" in modes and "command" not in modes)
    SLEEP = ("sleep" in modes)
    ANNOUNCE = settings.get("user.announce_mode_updates")

    if last_mode == "sleep" and not SLEEP:
        # Always announce wake up
        # Cancel any current speaker, weird edge case where it will speak twice otherwise
        actions.user.cancel_current_speaker()
        actions.user.tts(f"Talon now listening")   

    elif last_mode != "sleep" and SLEEP:
        # Always announce sleep
        actions.user.tts(f"Talon asleep")

    elif last_mode != "sleep" and MIXED and last_mode != "mixed":
        if ANNOUNCE:
            actions.user.tts(f"Talon mixed mode")

    elif last_mode != "sleep" and COMMAND \
        and not DICTATION and not SLEEP and last_mode != "command":
        if ANNOUNCE:
            actions.user.tts(f"Talon command mode")

    elif last_mode != "sleep" and \
        DICTATION and not COMMAND \
        and not SLEEP and \
        last_mode != "dictation" \
        and last_mode != "mixed":
        if ANNOUNCE:
            actions.user.tts(f"Talon dictation mode") 

    if SLEEP:
        last_mode = "sleep"
    elif MIXED:
        last_mode = "mixed"
    elif COMMAND:
        last_mode = "command"
    elif DICTATION:
        last_mode = "dictation"

def on_ready():
    # Only register these callbacks once all user settings and Talon
    # files have been loaded
    registry.register("update_contexts", on_update_contexts)
    ui.register("app_activate", on_app_switch)
    ui.register("win_title", on_title_switch)
    speech_system.register("phrase", on_phrase)

    if settings.get("user.start_screenreader_on_startup"):
        actions.user.toggle_reader()
    actions.user.tts("Talon user scripts loaded")


app.register("ready", on_ready)
