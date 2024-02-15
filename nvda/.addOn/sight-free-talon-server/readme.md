# Sight-free-talon-NVDA-server

This addon creates a command server in NVDA that can recieve socket messages from Talon. It allows you to toggle a few settings in NVDA, and to run a few commands. Namely, it can toggle speech interrupt for typed characters, and speak typed words/characters, so that audio echo back as Talon types your dication doesn't get interrupted by NVDA. This will temporarily disable the interrupt only during dictation, and revert after dictation is finished. This allows you to keep your normal NVDA settings while dictating, but still type with Talon.

You do not need to install this addon to use NVDA alongside the general dictation echo back through NVDA my `sight-free-talon` repo. However, if you want to prevent NVDA from interrupting your dictation, you will need to either disable speech interrupt for typed characters in your NVDA settings or install this addon.

## Installation

For the time being, install the addon via the github release page. You can then simply install the addon by clicking on the file while NVDA is running. Note, please manually remove the old version of the addon before installing the new one, as I am not currently managing the version number in the addon until I reach a stable beta.

To install the client side of the addon, you will need to clone the sight-free-talon repo into your Talon user directory.

# Attributions

Copyright (C) 2012-2023 NVDA Add-on team contributors.
This package is distributed under the terms of the GNU General Public License, version 2 or later. Please see the file COPYING.txt for further details.
[alekssamos](https://github.com/alekssamos/) added automatic package of add-ons through Github Actions.
For details about Github Actions please see the [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions).
Copyright (C) 2022 alekssamos
