# Technical Contribution

This repository is structured such that every screen reader or unique feature gets its own folder. Each folder contains a `talon` file with the commands for that screen reader or feature. Any features related to global scope or settings are in the root settings `.talon` file. If you would like to add support for a new screen reader I encourage you to follow the format of the other screen readers and implement similar function overrides. All baseline declarations that are contextually overriden are in the `core` folder.

# Non-Technical Contribution

I greatly benefit from general qualitative design feedback and learning more about the particular workflows of users. My intention is for this repository to be useful for people of all abilities and technical skill levels, so I am very interested in hearing about any difficulties you may have with the repository or Talon in general.

If you are a user with a vision impairment, I am curious to hear how you have interacted with voice dictation software in the past. I could also use qualitative feedback regarding things like alternative computer feedback mechanisms, such as braille, haptic feedback, or pitch-based audio feedback. I am curious to explore different ways of providing information to the user, and am excited about exploring more experimental ideas.
