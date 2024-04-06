os: windows
and app.name: Microsoft Edge
os: windows
and app.exe: msedge.exe
-
# This file takes advantage of the functionality for more natural text to speech within Microsoft edge
# as of 2023,  this functionality is not present on Linux

read aloud:
    key(ctrl-shift-u)
    sleep(1)
    key(ctrl)

toggle immersive reader:
    key(f9)

toggle immersive reader and read aloud:
    key(ctrl-shift-u)
    sleep(1)
    key(f9)
    sleep(1)
    # press ctrl to stop nvda from reading the page simultaneously
    key(ctrl)
