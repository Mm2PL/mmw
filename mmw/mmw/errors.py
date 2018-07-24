class InvalidStateError(Exception):
    def __init__(self, message):
        self.message = message


class FigletError(Exception):
    def __init__(self, stderr):
        self.stderr = stderr

    def __str__(self):
        return "(stderr) "+self.stderr


class FigletNotInstalledError(FigletError):
    def __init__(self):
        pass

    def __str__(self):
        return "FIGlet is not installed."
