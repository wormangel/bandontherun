class Error(Exception):
    pass

class SongAlreadyOnSetlistError(Error):
    def __init__(self, song, message):
        self.song = song
        self.message = message

class BatchParseError(Error):
    def __init__(self, line):
        self.line = line

class BandHasActiveVotingError(Error):
    def __init__(self, message):
        self.message = message

class InvalidVotingDate(Error):
    def __init__(self, message):
        self.message = message