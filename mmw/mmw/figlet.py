import mmw
import subprocess as sp


def figletify(text: str, font: str, figletCmd='figlet') -> str:
    """Runs figlet and returns the results"""
    try:
        proc = sp.Popen([figletCmd, '-f', font, text], stdout=sp.PIPE,
                        stderr=sp.PIPE)
    except FileNotFoundError:
        raise mmw.FigletNotInstalledError()
    io = proc.communicate()
    if io[1] != b'':
        raise mmw.FigletError(str(io[1], 'ascii'))
    return str(io[0], 'ascii')


class FigletText(mmw.Graphic):
    """Runs figletify(text, font) and uses the results as the text"""
    def __init__(self, text: str, font: str ='big'):
        figtext = figletify(text, font)
        super().__init__(figtext.split('\n')
                         if figtext != ''
                         else "[FIGlet Error]")
