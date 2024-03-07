# Talon Installing

You should have already installed Talon and the [community](https://github.com/talonhub/community/) repository. If not, see the [Talon docs](https://talonvoice.com/docs/) for instructions. In order to best use this repository you should be familiar with the basics of Talon and basic commands from the community repository.

This document is not a replacement for the wiki but is intended to be used as a quick way to briefly get an overview of the most important commands and most relevant behavior.

## Talon Brief Overview

Talon is a voice control engine. In order to have any behavior, you need to install scripts, the standard of which comes from the [community](https://github.com/talonhub/community/) repository. Each time you say a command within Talon, the voice model will try to match the command to the closest one that is defined and is contextually in scope. So, for instance, if there are specific commands to control Gmail, but you are not within Gmail, the command will likely be misrecognized. For this same reason, it is also very important to be in the proper mode. By default, there are two main modes: dictation mode and command mode. The former is for dictating raw text and the latter is for calling specific commands. If you are not in the proper mode but try to say a command that is defined in a different mode, Talon will likely still try to interpret the phrase, but it will be matched to something in the wrong mode.

### Debugging Talon Issues

If you are not getting the proper behavior within Talon, most of the time it is likely due to a poor microphone or an error in your scripts. You do not need a fancy microphone to have good performance with Talon; however, too much background noise, static, or fans are likely to cause issues. You should check the "save recordings" option within the Talon tray icon menu if you are getting poor recognition. This will allow you to hear what Talon hears for a given phrase.

## Helpful Standard Talon Commands

| Command                                                                                                                         | Description                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `command mode`                                                                                                                  | Switches Talon into command mode, where your words are interpreted as commands   |
| `dictation mode`                                                                                                                | Switches Talon into dictation mode, where your words are interpreted as raw text |
| `launch`                                                                                                                        | Launches the specified application                                               |
| `focus`                                                                                                                         | Focuses the specified application                                                |
| `talon wake`                                                                                                                    | Wakes Talon up if it is asleep                                                   |
| `talon sleep`                                                                                                                   | Puts Talon to sleep                                                              |
| `press`                                                                                                                         | Presses the specified key                                                        |
| `air bat cap drum each fine gust harp sit jury crunch look made near odd pit quench red sun trap urge vest whale plex yank zip` | The Talon phonetic alphabet                                                      |
| `sentence`                                                                                                                      | Dictate a sentence with the first word capitalized                               |
| `title`                                                                                                                         | Dictate a sentence with all words capitalized                                    |
| `word`                                                                                                                          | Dictate a single word                                                            |
| `scratch that`                                                                                                                  | Undoes the last thing you said                                                   |
| `wipe`                                                                                                                          | Presses backspace                                                                |
