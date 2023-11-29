tag: user.cursorless

-

# TODO: Just get the words directly without copying it to the clipboard
speak <user.cursorless_target>:
    user.cursorless_command('copyToClipboard', cursorless_target)
    user.robot_tts(clip.text())

