# Positions
POS_CENTER = "CENTER"
POS_LEFT = "LEFT"
POS_RIGHT = "RIGHT"
POS_UP = 'UP'
POS_DOWN = 'DOWN'
#
# Keys
ARROW_UP = 'ARROW_UP'
ARROW_DOWN = 'ARROW_DOWN'
ARROW_LEFT = 'ARROW_LEFT'
ARROW_RIGHT = 'ARROW_RIGHT'
INSERT = 'INSERT'
DELETE = 'DELETE'
HOME = 'HOME'
END = 'END'
PAGE_UP = 'PAGE_UP'
PAGE_DOWN = 'PAGE_DOWN'
TAB = 'TAB'
RETURN = 'RETURN'
ESCAPE = 'ESCAPE'
# Textfield types
TF_ONELINE = 'TF_ONELINE'
TF_TYPES = [TF_ONELINE]

PR_PERCENT = 'PR_PERCENT'
PR_CUSTOM = 'PR_CUSTOM'
PR_MODES = [PR_PERCENT, PR_CUSTOM]

SO_DEFAULTS = {
    'cursor_shown': True,
    'scrollbar_shown': False,
    'mouse_tracking': False,  # all or nothing
    'bottom_scroll_on_output': True,
    'bottom_scroll_on_key': True,
    'alternate_screen': False,
    'bracketed_paste': False
}
SO_OPTIONS = {
    'cursor_shown': 25,  # # # # # # #  25 (DECTCEM)
    'scrollbar_shown': 30,  # # # # # # 30 (rxvt)
    'mouse_tracking': 1003,  # all or nothing
    'bottom_scroll_on_output': 1010,  # 1010 (rxvt)
    'bottom_scroll_on_key': 1011,  # #  1011 (rxvt)
    'alternate_screen': 1047,  # # # #  1047
    'bracketed_paste': 2004
}
