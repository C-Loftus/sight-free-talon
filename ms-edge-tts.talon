os: windows
and app.name: Microsoft Edge
os: windows
and app.exe: msedge.exe

-
# This file takes advantage of the functionality for more natural text to speech within Microsoft edge
# as of 2023,  this functionality is not present on Linux

toggle read aloud:
    key(ctrl-shift-u)

toggle immersive reader:
    key(f9)

toggle both:
    key(ctrl-shift-u)
    sleep(1)
    key(f9)
