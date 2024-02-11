from talon import actions


class Scale:
    def __init__(self, notes: dict[str, float]):
        self.notes = notes

    def play(self, duration=1000):
        for note_name in self.notes:
            tone = self.notes[note_name]
            actions.user.beep(int(tone), duration)


CMajorScale = Scale(
    {
        "C": 261.63,
        "D": 293.66,
        "E": 329.63,
        "F": 349.23,
        "G": 392.00,
        "A": 440.00,
        "B": 493.88,
        "C2": 523.25,
    }
)

CMinorScale = Scale(
    {
        "C": 261.63,
        "D": 293.66,
        "Eb": 311.13,
        "F": 349.23,
        "G": 392.00,
        "Ab": 415.30,
        "Bb": 466.16,
        "C2": 523.25,
    }
)

CPentatonicScale = Scale(
    {
        "C": 261.63,
        "D": 293.66,
        "E": 329.63,
        "G": 392.00,
        "A": 440.00,
        "C2": 523.25,
    }
)

CBluesScale = Scale(
    {
        "C": 261.63,
        "Eb": 311.13,
        "F": 349.23,
        "F#": 369.99,
        "G": 392.00,
        "Bb": 466.16,
        "C2": 523.25,
    }
)

CChromaticScale = Scale(
    {
        "C": 261.63,
        "C#": 277.18,
        "D": 293.66,
        "Eb": 311.13,
        "E": 329.63,
        "F": 349.23,
        "F#": 369.99,
        "G": 392.00,
        "Ab": 415.30,
        "A": 440.00,
        "Bb": 466.16,
        "B": 493.88,
        "C2": 523.25,
    }
)
