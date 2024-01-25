os: windows

-

# Copies text with OCR from the current window
extract text:
    user.extract_text()

reader running:
    res = user.is_nvda_running()
    user.tts("{res}")
