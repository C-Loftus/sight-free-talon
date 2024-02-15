# Global TTS commands that are OS independent
# See each folder for specific contextual commands

tag(): user.sightFreeTalonInstalled

toggle echo:
    user.toggle_echo()

# Echo and interrupt the current speaker
echo this:
    key(ctrl-c)
    sleep(0.1)
    user.tts(clip.text())

echo no interrupt:
    key(ctrl-c)
    sleep(0.1)
    interrupt = false
    user.tts(clip.text(), interrupt)

echo clipboard:
    user.tts(clip.text())

echo line:
    edit.select_line()
    key(ctrl-c)
    sleep(0.1)
    user.tts(clip.text())

echo context:
    user.echo_context(true)

toggle echo context:
    user.toggle_echo_context()

# Toogles both echo on dictation and echo on context
toggle echo all:
    user.toggle_echo_all()

echo tab level:
    key(ctrl-l)
    sleep(0.1)
    key(ctrl-c)
    sleep(0.1)
    level = user.indentation_level(clip.text())
    user.tts('{level}')

toggle [screen] reader:
    user.toggle_reader()

toggle (key | keypress) sound:
    user.toggle_keypress_sound()

(switch | change) voice:
    user.switch_voice()

toggle braille:
    user.toggle_braille()
