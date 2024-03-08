# Sight-Free-Talon

Use Talon non-visually. Intended to be universal for all abilities, but especially helpful for those with eye strain, vision impairment, or blindness. Provides functionality to:

- echo back dictation
- speak info on context switch (mode, app, window, etc.)
- speak user-given text
- provide TTS libraries and other utilities for your own scripts

This repository integrates with:

- screen readers
- text-to-speech
- braille

# Usage

- Watch [my demo video](https://www.youtube.com/watch?v=i-XcpnVwvR0) for a quick overview
- The `.talon` files in each subdirectory contain scoped commands corresponding to each application or specific context

# Installing

- Clone the repo into your Talon user directory.
- Clone the [Talon community repository](https://github.com/talonhub/community) for general Talon commands
  - This is the sole OS-agnostic dependency of this project.

**NOTE FOR SIGHTED USERS**: Please clone the entire repository. The repo is explicitly designed to be helpful for all abilities and the `.talon` files are tightly scoped such that any functionality that isn't relevant to you (i.e. screen reader support) will not impact your general Talon usage or be easy to change in a settings file.

## OS Specific Setup

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

# Contributing / Support

If you benefit from this repo, please star it on GitHub. It helps put more attention on an otherwise niche accessibility challenge.

I appreciate _all contributions in any form_. For more info read [CONTRIBUTING.md](./docs/src/CONTRIBUTING.md). Feel free to reach out personally through the links in my bio if you have any personal inquiries regarding this repo.

# Acknowledgements and Resources

See [ATTRIBUTIONS.md](./docs/src/ATTRIBUTIONS.md)
