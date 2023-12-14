natural echo this:
    key(ctrl-c)
    sleep(0.1)
    user.elevenlabs_tts(clip.text())

# Save the text as a .mp3 file that is transcribed by openai tts
# Sounds very natural but costs money
open save this:
    key(ctrl-c)
    sleep(0.1)
    user.openai_tts(clip.text())
