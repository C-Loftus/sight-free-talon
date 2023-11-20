natural speak this:
    key(ctrl-c)
    user.natural_tts(clip.text())

speak this:
    key(ctrl-c)
    user.robot_tts(clip.text())

speak clipboard:
    user.robot_tts(clip.text())

edge speak this:
    key(ctrl-c)
    user.edge_tts(clip.text())

toggle echo:
    user.toggle_echo()

echo context:
    user.echo_context()

toggle echo context:
    user.toggle_echo_context()
