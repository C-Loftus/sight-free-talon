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