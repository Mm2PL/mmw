import mmw
import re
__doc__ = """This class contains:
 a list of foreground colors
 a list of background colors
 a list of effects(The mostly supported ones)
 format: <NAME>(<DISABLE_NAME>)
 colors:
  black, red, green, yellow, blue, magenta, cyan, white, gray, bright_red,
  bright_green, bright_yellow, bright_blue, bright_magenta, bright_cyan,
  bright_white
 effects:
  bold(reset_intensity), faint(reset_intensity),
  italic(italic_off), underline(underline_off), slow_blink(blink_off),
  rapid_blink(blink_off), reverse(reverse_off),
  conceal/hide(conceal_off/reveal/show), crossed_out(crossed_out_off),
  reset(N/A)
"""
fgcolors = {
    "black": "30", "red": "31", "green": "32", "yellow": "33",
    "blue": "34", "magenta": "35", "cyan": "36", "white": "37",
    "grey": "30;1",  # 100 spellings of gray/grey
    "gray": "30;1", "bright_red": "31;1", "bright_green": "32;1",
    "bright_yellow": "33;1", "bright_blue": "34;1",
    "bright_magenta": "35;1", "bright_cyan": "36;1",
    "bright_white": "37;1"  # If you think this makes no sense, you're
                            # right. This is here to provide a
                            # [strikethru] more white white [end-strikethru]
                            # whiter white, since some
                            # terminals treated white as gray/grey
}
bgcolors = {
    "black": "40", "red": "41", "green": "42", "yellow": "43",
    "blue": "44", "magenta": "45", "cyan": "46", "white": "47",
    "gray": "100", 'grey': '100', "bright_red": "101", "bright_green": "102",
    "bright_yellow": "103", "bright_blue": "104", "bright_magenta": "105",
    "bright_cyan": "106", "bright_white": "107"
    # bright_white Same as in foreground colors.
}
effects = {
    "bold": "1", "faint": "2", "italic": "3", "underline": "4",
    "slow_blink": "5", "rapid_blink": '6', 'reverse': '7',
    'conceal': '8', 'hide': '8', 'crossed_out': '9', 'italic_off': '23',
    'underline_off': '24', 'bold_off': '22', 'faint_off': '22',
    'blink_off': '25', 'reset_intensity': '22',
    'reverse_off': '27', 'conceal_off': '28', 'reveal': '28',
    'show': '28', 'crossed_out_off': '29', 'reset': "0"
}


def getColor(color, bg=False):
    """Check fgcolors and bgcolors and return the code, returns '0' if fails"""
    try:
        if bg:
            return bgcolors[color]
        else:
            return fgcolors[color]
    except Exception:
        return "0"


def rgb(red: int, green: int, blue: int, background=False) -> str:
    """Return the ANSI escape that generates the color"""
    if background:
        return "\033[48;2;"+str(red)+";"+str(green)+";"+str(blue)+"m"
    else:
        return "\033[38;2;"+str(red)+";"+str(green)+";"+str(blue)+"m"


def format(string):
    """Format the STRING.
    ex.:
    $(COLOR) - This will be replaced with a foreground color
    $(b_COLOR) - But this will be replaced with a background color
    $(EFFECT) - And this will be replaced with a effect code
    $(rgbINT;INT;INT) - This will be replaced with a rgb color code"""
    if not mmw.screen.allowColor:
        return re.sub(r"\$\([A-Za-z_0-9]*\)", "", string)
    for effect in effects.keys():
        string = string.replace("$("+effect.lower()+")",
                                "\033["+effects[effect]+"m")
    for color in bgcolors.keys():
        string = string.replace("$(b_"+color.lower()+")",
                                "\033["
                                + bgcolors[color.lower()]+"m")
    for color in fgcolors.keys():
        string = string.replace("$("+color.lower()+")",
                                "\033["
                                + fgcolors[color.lower()]+"m")
    pat = re.compile(r'\$\(rgb([0-9]+);([0-9]+);([0-9]+)\)')
    string = re.sub(pat, "\033[38;2;\\1;\\2;\\3m", string)
    pat = re.compile(r'\$\(b_rgb([0-9]+);([0-9]+);([0-9]+)\)')
    string = re.sub(pat, "\033[48;2;\\1;\\2;\\3m", string)
    return string
