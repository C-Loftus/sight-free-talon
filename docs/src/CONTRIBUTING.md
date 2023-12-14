My goal is to make contributing as easy as possible. If you need help or ideas, feel free to directly reach out to me, either through the Talon Slack or my website, [https://colton.bio](https://colton.bio).

# Technical Contribution

The project repository is structured such that every screen reader or unique feature gets its own folder. Each folder contains a `talon` file with the commands for that screen reader or feature. Any features related to global scope or settings are in the root settings `.talon` file. If you would like to add support for a new screen reader I encourage you to follow the format of the other screen readers and implement similar function overrides. All baseline declarations that are contextually overriden are in the `core` folder.

## Testing with Your Own Setup

I do not have the resources to test every combination of screen reader and operating system. If you would like to contribute to this repository, I encourage you to test the commands on your own setup and provide feedback. If you are not familiar with GitHub, you can directly get in contact with me.

To check for errors, you can send me a copy of your Talon log.

# Non-Technical Contribution

I greatly benefit from general qualitative design feedback and learning more about the particular workflows of users. My intention is for this repository to be useful for people of all abilities and technical skill levels, so I am very interested in hearing about any difficulties you may have with the repository or Talon in general.

If you are a user with a vision impairment, I am curious to hear how you have interacted with voice dictation software in the past. I could also use qualitative feedback regarding things like alternative computer feedback mechanisms, such as braille, haptic feedback, or pitch-based audio feedback. I am curious to explore different ways of providing information to the user, and am excited about exploring more experimental ideas.
