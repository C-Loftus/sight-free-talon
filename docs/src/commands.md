# Commands Specific to Sight-Free Talon

Sight-Free-Talon has a series of voice commands and settings to make Talon easier to user alongside screen readers. Any general commands for dictating text or controlling your computer can be found in the central community repo, which you should also have installed.

## Commands

TODO

## Settings

All settings can be set within `.talon` files and contextually scoped to specific applications.

| Setting                            | Description                                                                            | Default Value |
| ---------------------------------- | -------------------------------------------------------------------------------------- | ------------- |
| user.echo_dictation                | Echo the subtitles from talon back via tts                                             | true          |
| user.tts_speed                     | How fast to play back text-to-speech -10 to 10                                         | 8             |
| user.tts_volume                    | How loud to play back text-to-speech from 0 to 100                                     | 80            |
| user.echo_context                  | Automatically echo the context of the focused window when switching applications/tabs  | false         |
| user.tts_via_screenreader          | If a screen reader is enabled, use it for tts instead of the TTS engine in Talon       | true          |
| user.nvda_key                      | Key used for nvda modifier, change to 'insert' if that is your nvda modifier           | 'capslock'    |
| user.start_screenreader_on_startup | Start your screen reader automatically when Talon starts                               | false         |
| user.braille_output                | Output dictated text to braille display through your screen reader                     | false         |
| user.sound_on_keypress             | To prevent errors from accidental key presses, play a sound each time a key is pressed | false         |
| user.disable_keypresses            | Disable keypresses from Talon in high risk contexts that cannot afford typos           | false         |
