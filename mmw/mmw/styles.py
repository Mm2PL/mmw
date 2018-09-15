r"""
The default styles.

Examples:
 UNICODE:
  \u250C\u2500TEST\u2500\u2510
  \u2502      \u2502
  \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2518
 UNICODE_BOLD:
  \u250F\u2501TEST\u2501\u2513
  \u2503      \u2503
  \u2517\u2501\u2501\u2501\u2501\u2501\u2501\u251B
 DEFAULT:
  +-TEST-+
  |      |
  +------+
 ALTERNATE:
  /-TEST-\\
  |      |
  \\------/
"""
UNICODE = {
    "CornerUpLeft": "\u250C", "CornerUpRight": "\u2510",
    "CornerDownLeft": "\u2514", "CornerDownRight": "\u2518",
    "TitleFiller": "\u2500", "TextFiller": " ",
    "ButtonSelected": " [>{button}<] ",
    "ButtonNotSelected": " [ {button} ] ",
    "BorderVertical": "\u2502", "BorderHorizontal": "\u2500",
    "MenuBar": "  {name}  ", "MenuBarSelected": " [{name}] ",
    "CornerGeneric": "+",
    "MenuChildUnselected": " {name}", "MenuChildSelected": ">{name}",
    "TextEmpty": "_", 'TextLeftBorder': '[', 'TextRightBorder': ']',
    'ProgressFilled': '\u2588', 'ProgressEmpty': ' ',
    'ProgressStart': '[', 'ProgressEnd': ']'
}
UNICODE_BOLD = {
    "CornerUpLeft": "\u250F", "CornerUpRight": "\u2513",
    "CornerDownLeft": "\u2517", "CornerDownRight": "\u251B",
    "TitleFiller": "\u2501", "TextFiller": " ",
    "ButtonSelected": " [>{button}<] ",
    "ButtonNotSelected": " [ {button} ] ",
    "BorderVertical": "\u2503", "BorderHorizontal": "\u2501",
    "MenuBar": "  {name}  ", "MenuBarSelected": " [{name}] ",
    "CornerGeneric": "+",
    "MenuChildUnselected": " {name}", "MenuChildSelected": ">{name}",
    "TextEmpty": "_", 'TextLeftBorder': '[', 'TextRightBorder': ']',
    'ProgressFilled': '\u2588', 'ProgressEmpty': ' ',
    'ProgressStart': '[', 'ProgressEnd': ']'
}
DEFAULT = {
    "CornerUpLeft": "+", "CornerUpRight": "+",
    "CornerDownLeft": "+", "CornerDownRight": "+",
    "TitleFiller": "-", "TextFiller": " ",
    "ButtonSelected": " [>{button}<] ",
    "ButtonNotSelected": " [ {button} ] ",
    "BorderVertical": "|", "BorderHorizontal": "-",
    "MenuBar": "  {name}  ", "MenuBarSelected": " |{name}| ",
    "CornerGeneric": "+",
    "MenuChildUnselected": " {name}", "MenuChildSelected": ">{name}",
    "TextEmpty": "_", 'TextLeftBorder': '[', 'TextRightBorder': ']',
    'ProgressFilled': '-', 'ProgressHead': '>',
    'ProgressEmpty': ' ',
    'ProgressStart': '[', 'ProgressEnd': ']'
}
ALTERNATE = {
    "CornerUpLeft": "/", "CornerUpRight": "\\",
    "CornerDownLeft": "\\", "CornerDownRight": "/",
    "TitleFiller": "-", "TextFiller": " ",
    "ButtonSelected": " [>{button}<] ",
    "ButtonNotSelected": " [ {button} ] ",
    "BorderVertical": "|", "BorderHorizontal": "-",
    "MenuBar": "  {name}  ", "MenuBarSelected": " [{name}] ",
    "CornerGeneric": "+",
    "MenuChildUnselected": " {name}", "MenuChildSelected": ">{name}",
    "TextEmpty": "_", 'TextLeftBorder': '[', 'TextRightBorder': ']',
    'ProgressFilled': '.', 'ProgressEmpty': ' ',
    'ProgressStart': '[', 'ProgressEnd': ']'
}
STYLE_LIST = ["UNICODE", "UNICODE_BOLD", "DEFAULT", "ALTERNATE"]
