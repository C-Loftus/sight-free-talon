settings():
    # echo the subtitles from talon back via tts
    user.echo_dictation = true

    # how fast to play back text-to-speech
    # if using the windows native tts. If
    # using the screenreader tts, this setting
    # is ignored and the screenreader's tts is used
    user.tts_speed = 5

    # Automatically echo the context of the focused window when switching applications/tabs
    user.echo_context = false

    # instead of playing tts via talon, play it via the tts engine in your screenreader
    user.tts_via_screenreader = true

    # key used for nvda modifier, change to 'insert' if that is your nvda modifier
    user.nvda_key = 'capslock'
