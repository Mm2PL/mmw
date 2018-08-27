import mmw
import typing
specialChars = ["\033", "\xe0", '\x00']


def decode(keySeq: typing.List[str]) -> str:
    """Check the keylist and return the key name"""
    try:
        keySeq = str(''.join(keySeq), 'ansi')
    except TypeError:
        pass  # keySeq is a string (not byte)
    if keySeq[0] == '\t':
        return mmw.consts.TAB
    if keySeq[0] == '\r':
        return mmw.consts.RETURN
    if keySeq[0] == '\xe0':
        # Arrow keys
        if keySeq[1] == 'H':
            return mmw.consts.ARROW_UP
        if keySeq[1] == 'P':
            return mmw.consts.ARROW_DOWN
        if keySeq[1] == 'K':
            return mmw.consts.ARROW_LEFT
        if keySeq[1] == 'M':
            return mmw.consts.ARROW_RIGHT

        # Special keys
        if keySeq[1] == 'R':
            return mmw.consts.INSERT
        if keySeq[1] == 'G':
            return mmw.consts.HOME
        if keySeq[1] == 'I':
            return mmw.consts.PAGE_UP
        if keySeq[1] == 'S':
            return mmw.consts.DELETE
        if keySeq[1] == 'O':
            return mmw.consts.END
        if keySeq[1] == 'Q':
            return mmw.consts.PAGE_DOWN
    if keySeq[0] == '\033':
        if keySeq[1] == '[':
            # pointer = 2
            # if keySeq[pointer] == '1':
            #     pointer += 1
            #     modifier += '?'
            # if keySeq[pointer] == ';':
            #     pointer += 1
            #     modifier += ' '
            if keySeq[-1] == 'H':
                return mmw.consts.HOME
            if keySeq[-1] == 'A':
                return mmw.consts.ARROW_UP
            if keySeq[-1] == 'B':
                return mmw.consts.ARROW_DOWN
            if keySeq[-1] == 'D':
                return mmw.consts.ARROW_LEFT
            if keySeq[-1] == "C":
                return mmw.consts.ARROW_RIGHT
            if keySeq[2] == '2':
                if keySeq[-1] == '~':
                    return mmw.consts.INSERT


def mouseClickDecode(charSeq) -> dict:
    """Check where the user clicked the mouse
    -> dict,
    keys: 'button', 'modifiers', 'x', 'y'
    """
    space = charSeq[0]
    x = charSeq[1]
    y = charSeq[2]
    code = format(ord(space), "=7b").replace(" ", "0")
    # R0CMSXX
    # R scRoll
    # M Meta/Alt
    # C Control
    # S Shift
    # XX Mouse bttn vvv
    #  00 LMB
    #  01 MMB
    #  11 RMB
    modifiers = ""
    bttn = "?"
    if code[-2:] == "00" and code[0] == "0":
        bttn = "LEFT"
    elif code[-2:] == "01" and code[0] == "0":
        bttn = "MIDDLE"
    elif code[-2:] == "10":
        bttn = "RIGHT"
    elif code[-2:] == "11":
        bttn = "UNPRESS"
    elif code[-2:] == "00" and code[0] == "1":
        bttn = "SCROLL_UP"
    elif code[-2:] == "01" and code[0] == "1":
        bttn = "SCROLL_DOWN"
    if code[-3] == "1":
        modifiers = modifiers + ", SHIFT" if len(modifiers) > 1\
            else "SHIFT"
    if code[-4] == "1":
        modifiers = modifiers + ", META" if len(modifiers) > 1\
            else "META"
    if code[-5] == "1":
        modifiers = modifiers + ", CONTROL" if len(modifiers) > 1\
            else "CONTROL"
    etype = {}
    etype["button"] = bttn
    etype["modifiers"] = modifiers.split(", ")
    etype["x"] = ord(x)-33
    etype["y"] = ord(y)-33
    # if loggingEnabled:
    #     log.slog("KeyMap.mouseClickDecode", "bttn: ", str(bttn))
    #     log.slog("KeyMap.mouseClickDecode", "mod: ", str(modifiers))
    #     log.slog("KeyMap.mouseClickDecode", "X: ", str(etype["x"]))
    #     log.slog("KeyMap.mouseClickDecode", "Y: ", str(etype["y"]))
    return etype
