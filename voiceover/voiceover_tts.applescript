--------------------
set currentDate to current date
say currentDate using "Ava"
delay 2

-----------------------
try
    set doNotShowSplashScreen to (do shell script "defaults read com.apple.VoiceOverTraining doNotShowSplashScreen") as integer as boolean
on error
    set doNotShowSplashScreen to false
end try
if doNotShowSplashScreen then
    do shell script "/System/Library/CoreServices/VoiceOver.app/Contents/MacOS/VoiceOverStarter"
else
    do shell script "defaults write com.apple.VoiceOverTraining doNotShowSplashScreen -bool true && /System/Library/CoreServices/VoiceOver.app/Contents/MacOS/VoiceOverStarter"
end if


--- allow voiceover to be controlled with applescript
tell application "VoiceOver" to say (do shell script "date +\"%l:%M %p\"") using "Karen" speaking rate 270 volume 0.4


-- Set the text you want VoiceOver to speak----------------
set textToSpeak to "Hello, this is a test."
do shell script "say " & quoted form of textToSpeak

----------------
tell application "VoiceOver"
    tell commander to perform command item chooser
end tell


---
tell application "VoiceOver"
    output "VoiceOver is now on"
end tell
