class InvalidStateError(RuntimeError):
    """This error is raised when an object is in an invalid state during
    running a method"""
    def __init__(self, message):
        self.message = message


class FinalError(RuntimeError):
    """This error is raised when you assign to a final variable"""
    def __init__(self, message):
        self.message = message


class FigletError(Exception):
    """Errors from figlet, including FigletNotInstalledError"""
    def __init__(self, stderr):
        self.stderr = stderr

    def __str__(self):
        return "(stderr) "+self.stderr


class FigletNotInstalledError(FigletError):
    """This exception is raised when the figletify() function cannot find
    figlet"""
    def __init__(self):
        pass

    def __str__(self):
        return "FIGlet is not installed."
