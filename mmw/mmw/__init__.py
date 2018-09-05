# -*- coding: utf-8 -*-
# Pyflakes: NOQA
# Flake8: noqa
import sys
if sys.version[0] == '2':
    print('\033[41mThis version of mmw is not compatible with python2')
    print('Use may experience syntax errors, because I used type hinting')
    try:
        raw_input('\033[40m[Press enter to continue anyway]\033[0m')
    except (EOFError, KeyboardInterrupt):
        exit()
from .drawable import *
from .graphic import *
from .menu import *
from .screen import *
from .window import *
from .styles import *
from .errors import *
from .formatting import *
from .consts import *
from .decoding import *
from .figlet import *
from .formattedstring import *
from .textfield import *
from .animation import *
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
