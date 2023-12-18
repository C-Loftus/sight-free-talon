# For Better Accessibility, Do Less

There are two main cliches in software accessibility: the first that it is a burden, accomplished only through extra labor, and the second being that we ought to make our applications universal, to include everyone. I wish to say the opposite. If it is a burden, it is because it requires us to limit our product, and scope our features to only that which is essential.

Once content is made accessible to a screen reader, the main problem becomes synthesizing it down into succinct representations. Accessibility is de facto useless if our interfaces are too bloated in the first place. Thus, the goal of an accessibility tool should be not just to allow new forms of interaction, but also reduce the superfluous. For hands-free software like Talon, that means eliminating clicks. For screen readers like NVDA, that means reducing the verbosity of TTS.

Large language models are the future of accessibility not just because they can dynamically create new content, but precisely because they are so good at eliminating that which is unnecessary.

This reason is why I write so much in Markdown. It is not necessarily the most efficient, but it is undoubtedly the most flexible. It is easy to export to HTML, PDFs, and is essentially the thinnest wrapper possible over plaintext while still maintaining a syntactic structure on the document as a whole. And as stated previously, what we need isn't just the ability to read everything aloud, but the ability to tightly scope what _not_ to read. The more abstractions we place over the file that is being edited, the harder it becomes to process programmatically. That is why I do not like PowerPoint or Word. They have inaccessibility by obscurity.

The Unix philosophy on the other hand is true universal design since in it, every program knows its place. Universality is not accomplished by each program individually, but rather by their composition.

No single design is ever universal and it is pernicious to imply such. The vast majority of design prioritizes sighted users and it is understandable to do so. But to qualify it as universal is to imply that it is somehow the best option for a compromise that helps all. As we think about software design, we quickly begin to see how we are flooded with practicalities that trick us into thinking they are universal standards, that nothing else better can be done. Yet through composition and the invitation to customize by the limitation of complexity, we can easily do better than the so-called universal.

As I've thought more about such things, I think it is significant that many of the tools created by blind users for blind users like Emacspeak or Edbrowse do not call themselves screen readers. In some ways, to call one's software a screen reader is to capitulate to the idea that vision is the one true way of computer interaction and all we can do is try to mimic it. There is of course nothing wrong with this in a pragmatic sense, but to build the best software for vision impairment, we can't always be chasing the sighted presuppositions.

Cursorless has been so exciting to me since it proudly stands on its own, independent of the assumptions of keyboard use and is all the better for it. It also knows when to stop. It is an editing program. It does not try to be a version control program, an IDE, and a collaboration tool like Microsoft Word. Because of these self limitations, it is more accessible for a writer like myself, not less. That is why I can use it for my business consulting work, despite the fact it is intended for programmers.

The one exception may come from the central controller itself. Our engine, like Talon or NVDA that calls our compositions. An analogy might be found in Kubernetes: We can only accomplish total decentralization through total centralization.

# For Better Accessibility, Eliminate the Task

Friction is perhaps the most important consideration when building accessibility tools. If a program is accessible, but adds too much friction, it won't actually be used and the user will simply default to other more straightforward, but less accessible methods. In the case of users with chronic pain, this can end up making things worse by giving the illusion of alternative input, when in reality the default tools are the only ones recieving significant usage.

When designing for accessibility, there is often the presupposition that differences in ability are static. Yet in fact, the majority of disabilities are dynamic and constantly changing.

The challenge when designing for chronic pain is that the user can easily chose to just work through pain. One needs to create tools with very little friction in order to have less than simply using one's hands or eyes. It becomes a tug of war between physical pain and the friction of new tools.

As such, the best way to reduce friction to such an extent it to simply eliminate the task all together through scripting. Another point for the Unix philosophy and composition.

<!-- The human body is such a wonderful dynamism of motion and feeling yet when we interact with the computer, we resign ourselves to often nothing but the eyes and hands. Why is this the case? It is friction.

Most users of all backgrounds and abilities don't use all potential input methods for their computer. They simply use the ones with the least friction at the moment. Sighted people generally have abnormally high amounts of mouse usage, often unoptimally so. Whereas visually impaired people generally have abnormally high amounts of keyboard usage, and often do not take advantage of voice commands. -->

The challenge with voice interaction specifically is that it typically requires visual feedback to ensure the command was interpreted properly. Yet we do not want to spam the user with TTS messages after the execution of each command. The more messages we send to the user, the less useful they will be.
