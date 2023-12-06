# Sight-Free-Talon

Use Talon while not needing to look at your computer. Especially helpful for those with vision impairment, blindness, eye strain, or those who prefer alternative computer interaction. Integrates tools like:

- screen readers
- text-to-speech
- braille
- software beeps
- hardware rumble / tacile feedback
- pedals

# Installing

Clone the repo into your Talon user directory.

## OS Specific Setup

- Linux
  - Install `spd-say` to play tts.
  - Install `orca` to use the screen reader.
  - Install `piper` to use the `omnx` model
    - run `pipx install piper` to install (thus `pipx` is a dependency)
- Windows
  - Install NVDA to play tts through the screen reader.
    - Disable `Speech interrupt for typed characters` in NVDA settings to make sure typing text from Talon is not interrupted with every typed character.

## Background and Motivation

Many screen readers and tools for visual impairment are very dependent upon keyboard and hand usage. By leveraging Talon, we can reduce hand usage and automate tasks, especially those that would be difficult with a screen reader. Talon also allows easier integration of tools like foot pedals and the significant pre-existing ecosystem of tools to help automate user input or navigation.

# Contributing

I am developing this as I deal with my own eye strain issues. Thus, **I greatly appreciate any user contributions no matter how big or small, in any capacity technical or not.** Please feel free to file issues for any functionality you would like, even if you cannot implement them. For those who wish to contribute, any of the open issues are a good place to start. If you are a user with a visual impairment please get in touch with me I would love to get your design feedback.

For any other inquiries regarding this project contact me via the methods in my GitHub bio.

# Acknowledgements and Resources

NVDA Controller client `.dll` file can be found at: [https://www.nvaccess.org/files/nvda/releases/stable/](https://www.nvaccess.org/files/nvda/releases/stable/)

Documentation for this controller client can be found at
[https://github.com/nvaccess/nvda/blob/master/extras/controllerClient/readme.md](https://github.com/nvaccess/nvda/blob/master/extras/controllerClient/readme.md)

## Various Other Resources

- https://www.afb.org/aw/19/4/15104
- https://github.com/dictationbridge
- http://www.hartgen.org/j-say
- http://www.eklhad.net/philosophy.html
- https://tvraman.github.io/emacspeak/manual/
- https://emacspeak.blogspot.com/
- https://www.emacswiki.org/emacs/BrailleMode
- https://www.emacswiki.org/emacs/EmacSpeak
- https://github.com/nvaccess/nvda/wiki/
- https://github.com/EmpowermentZone/EdSharp
- https://github.com/accessibleapps/accessible_output2
- https://github.com/qtnc/UniversalSpeech
- https://www.techrxiv.org/articles/preprint/Image_Captioning_for_the_Visually_Impaired_and_Blind_A_Recipe_for_Low-Resource_Languages/22133894
  - contains JAWS dll
- https://rhasspy.github.io/piper-samples/
  - more voices
