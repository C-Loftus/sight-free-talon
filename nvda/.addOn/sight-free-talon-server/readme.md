# Sight-free-talon-NVDA-server

This addon creates a command server in NVDA that can recieve socket messages from Talon. It allows you to toggle a few settings in NVDA, and to run a few commands. Namely, it can toggle speech interrupt for typed characters, and speak typed words/characters, so that audio echo back as Talon types your dication doesn't get interrupted by NVDA. This will temporarily disable the interrupt only during dictation, and revert after dictation is finished. This allows you to keep your normal NVDA settings while dictating, but still type with Talon.

You do not need to install this addon to use NVDA alongside the general dictation echo back through NVDA my `sight-free-talon` repo. However, if you want to prevent NVDA from interrupting your dictation, you will need to either disable speech interrupt for typed characters in your NVDA settings or install this addon.

## Installation

First install the sight-free-talon NVDA addon with one click like any other NVDA addon.

Then you will need to install the client side of the addon, by cloning the sight-free-talon repo into your Talon user directory.
