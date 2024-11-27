explore tags: user.explore_tags()

explore settings: user.explore_settings()

echo mode: user.echo_mode()

echo website:
    key(ctrl-l)
    sleep(0.3)
    edit.copy()
    text = user.get_website_text(clip.text())
    user.tts(text)
    key(escape)

echo (clip | clipboard):
    text = clip.text()
    user.tts(text)
