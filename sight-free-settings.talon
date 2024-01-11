settings():
    # Echo the subtitles from talon back via tts
    user.echo_dictation = true

    # How fast to play back text-to-speech -10 to 10
    # Ignored if using screenreader tts
    user.tts_speed = 8

    # How loud to play back text-to-speech from 0 to 100
    # Ignored if using screenreader tts
    user.tts_volume = 80

    # Automatically echo the context of the focused window when switching applications/tabs
    user.echo_context = false

    # If a screen reader is enabled, use it for tts instead of the TTS engine in Talon
    user.tts_via_screenreader = true

    # Key used for nvda modifier, change to 'insert' if that is your nvda modifier
    user.nvda_key = 'capslock'

    # Starts NVDA automatically with Talon
    user.start_screenreader_on_startup = false

    # Output dictated text to braille display through your screen reader
    user.braille_output = false

    # To prevent errors from accidental key presses, play a sound each time a key is pressed
    user.sound_on_keypress = false

    # Disable keypresses from Talon in high risk contexts that cannot afford typos
    user.disable_keypresses = false

    # Speak Talon's mode (command, dictation, mixed) whenever it is changed
    user.announce_mode_updates = true

    # Every given number of minutes, send a notification, prompting you to rest your eyes
    # user.enable_break_timer = true
    # user.user.min_until_break = 10

    ### Relevant Community Settings Below ###
    # Change key_wait if you want the screen reader to speak words
    # at the same pace as if you were typing them manually.
    # key_wait = 0

    # Setting from community repository
    # Manually typing keys through Talon can jumble the audio output since nvda can also say out
    # keys and/or words. By having this setting enabled, we can echo out the text but
    # not need to disable the screenreader's speech for characters and words for normal typing
    # user.paste_to_insert_threshold = -1
