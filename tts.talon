# Global TTS commands that are OS independent
# See each folder for specific contextual commands

toggle echo:
    user.toggle_echo()

echo this:
    key(ctrl-c)
    sleep(0.1)
    user.robot_tts(clip.text())

echo clipboard:
    user.robot_tts(clip.text())

echo line:
    edit.select_line()
    key(ctrl-c)
    sleep(0.1)
    user.robot_tts(clip.text())

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
    user.robot_tts('{level}')

toggle [screen] reader:
    user.toggle_reader()
