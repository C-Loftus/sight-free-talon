# Sight-Free-Talon

**Non-visually control your entire computer with voice commands. Uses the cross-platform [Talon Voice](https://talon.wiki) dictation engine.**  

Intended to be universal for all abilities, but especially helpful for those with blindness, vision impairment, or eyestrain. 

Provides functionality to:

- echo back dictated text as you speak
- use all [standard Talon commands](https://github.com/talonhub/community) non-visually
- create your own non-visual voice commands using a cross-platform TTS library
- hook into system accessibility APIs (i.e. speak info on context switch of the mode, app, window, etc.)

This repository integrates with:

- screen readers
- text-to-speech
- braille

# Usage

- Watch my demo video for a quick overview
<a href="https://www.youtube.com/watch?v=i-XcpnVwvR0" title="Sight-free-talon overview video">
    <img alt="Sight-free-talon overview video" src="https://github.com/C-Loftus/sight-free-talon/assets/70598503/1c33a46b-9595-4641-a6c1-0bc11b4ea90d" width="400">
</a>

- [Official docs](https://colton.bio/sight-free-talon/) can be found on my website and are in active development
- All voice commands are found in the `.talon` files in each subdirectory and are scoped to each corresponding application or context


# Installing

- Clone this repo into your Talon user directory.
- Clone the [Talon community repository](https://github.com/talonhub/community) for general Talon commands
  - This is the sole OS-agnostic dependency of this project.

_Note for sighted users_: Please clone the entire repository. Any functionality that isn't relevant to you (i.e. screen reader support) will not impact your general Talon usage and each all settings are easy to change or override in a settings file.

## OS Specific Setup


- Windows

  - Using NVDA:
    - Install the NVDA addon file from the repo [releases page](https://github.com/C-Loftus/sight-free-talon/releases/)
    - If you do not want to install the addon, disable `Speech interrupt for typed characters` in NVDA settings to make sure typing text from Talon is not interrupted with every typed character.

- Mac
  - No extra dependencies
 
- Linux
  - Install `spd-say` to play standard tts.
  - Install `piper` to use the `omnx` model for more natural speech
    - run `pipx install piper` to install it (thus `pipx` is a dependency)

# Contributing / Support

If you benefit from this repo, please star it on GitHub. It helps put more attention on an otherwise niche accessibility challenge.

I appreciate _all contributions in any form_. For more info read [CONTRIBUTING.md](./docs/src/CONTRIBUTING.md). Feel free to reach out personally through the links in my bio if you have any personal inquiries regarding this repo.

# Acknowledgements and Resources

See [ATTRIBUTIONS.md](./docs/src/ATTRIBUTIONS.md)
