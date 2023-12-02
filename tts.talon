natural echo this:
    key(ctrl-c)
    sleep(0.1)
    user.elevenlabs_tts(clip.text())

echo this:
    key(ctrl-c)
    sleep(0.1)
    user.robot_tts(clip.text())

echo clipboard:
    user.robot_tts(clip.text())

edge echo this:
    key(ctrl-c)
    sleep(0.1)
    user.edge_tts(clip.text())

toggle echo:
    user.toggle_echo()

toggle echo all:
    user.toggle_echo_all()

echo context:
    user.echo_context(true)

toggle echo context:
    user.toggle_echo_context()

echo line:
    edit.select_line()
    key(ctrl-c)
    sleep(0.1)
    user.robot_tts(clip.text())

echo tab level:
    key(ctrl-l)
    sleep(0.1)
    key(ctrl-c)
    sleep(0.1)
    level = user.indentation_level(clip.text())
    user.robot_tts('{level}')

extract text:
    user.extract_text()

toggle reader:
    user.toggle_nvda()

echo tags:
    user.echo_tags()
