# Philosophy

In this repository, we want to create a solution that is low friction and feels natural and unintrusive for all users. For users with eyestrain or a vision impairment, we want our repository not to feel like a begrudgingly accepted accommodation, but an exciting improvement that unlocks new forms of human computer interaction. This is similar to what Cursorless has accomplished with voice programming. It is not simply a way to code when you do not have access to your hands, but rather it is a full new way to think about coding, one that is often more efficient to begin with. By using Talon's scripting potential and various community tools and AI integrations, we have the potential to realize this within low vision tools as well. After all, the most accessible tasks are the ones which can be automated away, and don't need to be done in the first place.

As such, repository is designed around a series of core principles:

- Keep as much behavior directly in Talon as possible and make as few screen-reader specific changes as possible.
  - This makes development easier and more maintainable.
- Make our Talon code well integrated with the rest of the Talon community.
  - This means using the same conventions and style as the rest of the community and not dynamically loading specialized libraries or doing low level hacks if it can be avoided.
- Create a solution that can be used for people of all abilities
  - This means that we want to make sure that the solution is usable for people who are blind, low vision, or sighted.
  - Make sure that the solution is usable for people who are new to Talon and people who are experienced.
- On install, the solution should work out of the box with minimal configuration.
  - Settings should not change other parts of the user's Talon configuration.
- All settings should be located in a central settings file.
- Application specific voice commands should be located in their own specific file and contextually scoped
- Feature creep is bad and hurts the long term maintainability of the project.
  - If a feature is not used by a large number of people, it should be removed.
  - Focus on a few popular screen readers and make sure they work well.
