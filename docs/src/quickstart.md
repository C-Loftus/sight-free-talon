# Installing

This repository is in frequent development. I suggest using git to clone the repository into your user directory by running the following,

```
git clone https://github.com/C-Loftus/sight-free-talon
```

and then updating it frequently with `git pull`. On Windows your user directory is located at `%APPDATA%\Talon\user`. On MacOS and Linux your user directory is located at `~/.talon/user`.

For GPT functionality, install the `talon-gpt` repo dependency in your Talon user directory by running

```
git clone https://github.com/C-Loftus/talon-gpt
```

## OS Specific Setup

- Linux
  - Install `spd-say` to play espeak robotic tts.
  - Install `orca` to use the screen reader.
  - Install `piper` to use the `omnx` model for more natural speech
    - run `pipx install piper` to install it (thus `pipx` is a dependency)
- Windows
  - Install NVDA to play tts through the screen reader.
    - Disable `Speech interrupt for typed characters` in NVDA settings to make sure typing text from Talon is not interrupted with every typed character.
