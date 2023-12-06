settings():
    # echo the subtitles from talon back via tts
    user.echo_dictation = true

    # how fast to play back text-to-speech
    # if using the windows native tts. If
    # using the screenreader tts, this setting
    # is ignored and the screenreader's tts is used
    user.tts_speed = 3

    # Automatically echo the context of the focused window when switching applications/tabs
    user.echo_context = false

    # instead of playing tts via talon, play it via the tts engine in your screenreader
    user.tts_via_screenreader = true

    # key used for nvda modifier, change to 'insert' if that is your nvda modifier
    user.nvda_key = 'capslock'

    user.start_screenreader_on_startup = false

    # setting from community repository
    # Manually typing keys through Talon can jumble the audio output since nvda can also say out
    # keys and/or words. By having this setting enabled, we can echo out the text but
    # not need to disable the screenreader's speech for characters and words for normal typing
    user.paste_to_insert_threshold = -1

    # Requires a 
    user.braille_output = true
