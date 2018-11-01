# -*- coding: utf-8 -*-
# Pyflakes: NOQA
# Flake8: noqa
import sys
if sys.version[0] == '2':
    print('\033[41mThis version of mmw is not compatible with python2')
    print('Python WILL throw errors, because I used type hinting.')
    try:
        raw_input('\033[40m[Press enter to continue anyway]\033[0m')
    except (EOFError, KeyboardInterrupt):
        exit()
from .drawable import *  # The Drawable class
from .graphic import *  # The Graphic class
from .menu import *  # The Menu class
from .screen import *  # The Screen class
from .window import *  # The Window Class
from .styles import *  # All the styles (as dicts)
from .errors import *  # Exceptions:
#                      # InvalidStateError -- raised when an object is being
#                      #                      rendered while in an
#                      #                      invalid state
#                      # FinalError -- raised when writing to a read-only
#                      #               variable
#                      # FigletError -- raised when exits with a non zero
#                      #                exit-code
#                      # FigletNotInstalledError -- raised when program is
#                      #                            trying to run figlet
from .formatting import *  # fgcolors, bgcolors, effects (dicts)
#                          # getColor(color) -> str(color code),
#                          # rgb(r, g, b) -> str(escape code)
#                          # format(text) -> str
from .consts import *  # Every constant value
from .decoding import *
from .figlet import *  # Everything figlet replated apart
#                      # from FigletError and FigletNotInstalledError
from .formattedstring import *  # The FormattedString class
from .textfield import *  # The TextField class
from .animation import *  # The Animation class
from .progressbar import *  # The Progressbar class
from .screen_options import *  # The Screen_Options class
from .bind import *  # The Bind and MouseBind classes
# Drawable [V]
# Graphic [V]
# Menu [V]
# Screen [V]
# Textarea [-] ## Nie Będe przenosić
# Window [V]
# Styles [V]
# InvalidStateError [V] -> .errors.InvalidStateError
# Formatting [V]
# KeyList [V] -> consts
# KeyMap [V] -> .decoding
