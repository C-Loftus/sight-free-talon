# Sight-Free-Talon

Use Talon while not needing to look at your computer. Especially helpful for those with vision impairment, blindness, eye strain, or those who prefer alternative computer interaction. Provides functionality to:

- echo back dictation
- speak info on context switch (mode, app, window, etc.)
- speak user-given text
- provide TTS libraries and other utilities for your own scripts

This repository integrates with:

- screen readers
- text-to-speech
- braille
- software beeps
- hardware rumble / tacile feedback
- pedals

# Usage

View the `.talon` files in each subdirectory for commands corresponding to each application or context. View the settings file at the root of the repository for all relevant settings.

# Installing

Clone the repo into your Talon user directory.

## OS Specific Setup

- Linux
  - Install `spd-say` to play espeak robotic tts.
  - Install `orca` to use the screen reader.
  - Install `piper` to use the `omnx` model for more natural speech
    - run `pipx install piper` to install it (thus `pipx` is a dependency)
- Windows
  - Install NVDA to play tts through the screen reader.
    - Disable `Speech interrupt for typed characters` in NVDA settings to make sure typing text from Talon is not interrupted with every typed character.

## Background and Motivation

Many screen readers and tools for visual impairment are very dependent upon keyboard and hand usage. By leveraging Talon, we can reduce hand usage and automate tasks, especially those that would be difficult with a screen reader. Talon also allows easier integration of tools like foot pedals and the significant pre-existing ecosystem of tools to help automate user input or navigation.

# Contributing

I appreciate all contributions, whether bug reports, feature requests, qualitative design feedback, or code. See the [CONTRIBUTING.md](./CONTRIBUTING.md) for more information. Please feel free to reach out to me personally through the links in my GitHub bio if you have any specific inquiries regarding this repo.

# Acknowledgements and Resources

See [ATTRIBUTIONS.md](./ATTRIBUTIONS.md) for a list of tools, resources, and individuals that have been helpful in the creation of this repository.
