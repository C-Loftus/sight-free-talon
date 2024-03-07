# Demo Video and General Introduction

<iframe width="560" height="315" src="https://www.youtube.com/embed/i-XcpnVwvR0?si=B5j_301oExt1xlia" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

# Installing

- Clone the repo into your Talon user directory.
- Clone the [Talon community repository](https://github.com/talonhub/community) for general Talon commands

  - This is the sole OS-agnostic dependency of this project.

You should frequently run git pull to update the scripts.

## OS-Specific Dependencies

- Linux
  - Install `spd-say` to play standard tts.
  - Install `piper` to use the `omnx` model for more natural speech
    - run `pipx install piper` to install it (thus `pipx` is a dependency)
- Windows

  - Using NVDA:
    - Install the NVDA addon file from the repo [releases page](https://github.com/C-Loftus/sight-free-talon/releases/)
    - If you do not want to install the addon, disable `Speech interrupt for typed characters` in NVDA settings to make sure typing text from Talon is not interrupted with every typed character.

- Mac
  - No extra dependencies
