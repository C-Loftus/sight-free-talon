natural echo this:
    key(ctrl-c)
    user.natural_tts(clip.text())

echo this:
    key(ctrl-c)
    user.robot_tts(clip.text())

echo clipboard:
    user.robot_tts(clip.text())

edge echo this:
    key(ctrl-c)
    user.edge_tts(clip.text())

toggle echo:
    user.toggle_echo()

echo context:
    user.echo_context(true)

toggle echo context:
    user.toggle_echo_context()
