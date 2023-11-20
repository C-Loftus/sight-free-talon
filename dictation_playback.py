from talon import Module, actions, speech_system, settings

mod = Module()
playback_dictation_setting_name = 'sightless_talon_playback_dictation'
playback_dictation_setting = 'user.' + playback_dictation_setting_name
mod.setting(
    playback_dictation_setting_name,
    type = int,
    default = 1,
    desc = 'If nonzero, plays back dictation with text to speech'
)

def on_phrase(j):
    if actions.speech.enabled() and settings.get(playback_dictation_setting):
        words = j.get('text')
        if words:
            command_chain = ' '.join(words)
            actions.user.robot_tts(command_chain)
speech_system.register('phrase', on_phrase)

#The on_phrase function was based on the on_phrase function in the community repository for its command history.
#The community repository is distributed under the following license
#MIT License

# Copyright (c) 2021 Jeff Knaus, Ryan Hileman, Zach Dwiel, Michael Arntzenius, and others

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.