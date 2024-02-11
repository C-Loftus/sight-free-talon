title: /https://chat.openai.com/
-
Open new chat:
    key(ctrl-shift-o)
Focus chat input:
    key(shift-esc)
Copy last code block:
    key(ctrl-shift-;)
Copy last response:
    key(ctrl-shift-c)

speak [last] (response | output | chat):
    key(ctrl-shift-c)
    sleep(0.3)
    user.tts(clip.text())

speak last code [block]:
    key(ctrl-shift-;)
    sleep(0.3)
    user.tts(clip.text())

Set custom instructions:
    key(ctrl-shift-i)
Toggle sidebar:
    key(ctrl-shift-s)
Delete chat:
    key(ctrl-shift-delete)
