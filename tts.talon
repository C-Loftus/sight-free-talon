natural echo this:
    key(ctrl-c)
    sleep(0.1)
    user.natural_tts(clip.text())

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

echo context:
    user.echo_context(true)

toggle echo context:
    user.toggle_echo_context()

echo line:
    edit.select_line()
    key(ctrl-c)
    user.robot_tts(clip.text())
