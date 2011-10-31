class Error(Exception):
    pass

class SongAlreadyOnSetlistError(Error):
    def __init__(self, song, message):
        self.song = song
        self.message = message

class BatchParseError(Error):
    def __init__(self, line):
        self.line = line
    