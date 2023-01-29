class Note:
    def __init__(self, lengthDenominator, pitch):
        self.lengthDenominator = lengthDenominator
        self.pitch = pitch
        self.volume = 1

    def frequency(self):
        return 27.5 * (2**((self.pitch - 21) / 12))

    def __str__(self):
        if self.pitch == 0:
            return "pause"
        if self.pitch == 21:
            return "A0"
        if self.pitch == 22:
            return "A0#"
        if self.pitch == 23:
            return "B0"
        octave = (self.pitch - 24) // 12 + 1
        notes = ["C","C#","D","D#","E", "F", "F#", "G", "G#", "A", "A#", "B"]
        note = (self.pitch - 24) % 12
        noteStr = notes[note]
        if len(noteStr) == 1:
            return noteStr + str(octave)
        else:
            return noteStr[0] + str(octave) + noteStr[1]
