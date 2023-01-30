class PlayConfig:

    def __init__(self,score = None, bpm = 60, seconds_to_display = 3, staves_to_display = ["TREBLE"], bottom_note_diatonic = 23, top_note_diatonic = 46):
        self.score = score
        self.bpm = bpm
        self.seconds_to_display = seconds_to_display
        self.staves_to_display = staves_to_display
        self.bottom_note_diatonic = bottom_note_diatonic
        self.top_note_diatonic = top_note_diatonic

    class Builder:

        def __init__(self):
            self.score = None
            self.bpm = 60
            self.seconds_to_display = 3
            self.staves_to_display = ["TREBLE"]
            self.bottom_note_diatonic = 23
            self.top_note_diatonic = 46

        def set_score(self, score):
            self.score = score
            return self

        def set_bpm(self, bpm):
            self.bpm = bpm
            return self

        def set_seconds_to_display(self, seconds_to_display):
            self.seconds_to_display = seconds_to_display
            return self

        def set_staves_to_display(self, staves_to_display):
            self.staves_to_display = staves_to_display
            return self

        def set_bottom_note_diatonic(self, bottom_note_diatonic):
            self.bottom_note_diatonic = bottom_note_diatonic
            return self

        def set_top_note_diatonic(self, top_note_diatonic):
            self.top_note_diatonic = top_note_diatonic
            return self

        def build(self):
            return PlayConfig(self.score, self.bpm, self.seconds_to_display, self.staves_to_display, self.bottom_note_diatonic, self.top_note_diatonic)

    def newBuilder(self):
        return self.Builder()
