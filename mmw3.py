#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Name: Maciek's aMazing Windows
# Author: Maciek
import sys
import re
try:
    import termios
    import tty
except ImportError as e:
    pass


def printList(list):
    for i in range(len(list)):
        print(list[i])


def longInput(prompt, end="empty"):
    string = ""
    while 1:
        try:
            a = input(prompt)
        except Exception as e:
            return string
        if a == "" and end.lower() == "empty":
            return string
        else:
            string = string + "\n" + a

# Font: Basic
# Styles
# .d8888. d888888b db    db db      d88888b .d8888.
# 88'  YP `~~88~~' `8b  d8' 88      88'     88'  YP
# `8bo.      88     `8bd8'  88      88ooooo `8bo.
#   `Y8b.    88       88    88      88~~~~~   `Y8b.
# db   8D    88       88    88booo. 88.     db   8D
# `8888Y'    YP       YP    Y88888P Y88888P `8888Y'


class Styles():
    """The default styles
    examples:
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
        "MenuBar": "{name}  ", "MenuBarSelected": " [{name}] ",
        "CornerGeneric": "+",
        "MenuChildUnselected": " {name}", "MenuChildSelected": ">{name}"}
    UNICODE_BOLD = {
        "CornerUpLeft": "\u250F", "CornerUpRight": "\u2513",
        "CornerDownLeft": "\u2517", "CornerDownRight": "\u251B",
        "TitleFiller": "\u2501", "TextFiller": " ",
        "ButtonSelected": " [>{button}<] ",
        "ButtonNotSelected": " [ {button} ] ",
        "BorderVertical": "\u2503", "BorderHorizontal": "\u2501",
        "MenuBar": "{name}   ", "MenuBarSelected": " [{name}] ",
        "CornerGeneric": "+",
        "MenuChildUnselected": " {name}", "MenuChildSelected": ">{name}"}
    DEFAULT = {
        "CornerUpLeft": "+", "CornerUpRight": "+",
        "CornerDownLeft": "+", "CornerDownRight": "+",
        "TitleFiller": "-", "TextFiller": " ",
        "ButtonSelected": " [>{button}<] ",
        "ButtonNotSelected": " [ {button} ] ",
        "BorderVertical": "|", "BorderHorizontal": "-",
        "MenuBar": "{name}  ", "MenuBarSelected": "|{name}| ",
        "CornerGeneric": "+",
        "MenuChildUnselected": " {name}", "MenuChildSelected": ">{name}"}
    ALTERNATE = {
        "CornerUpLeft": "/", "CornerUpRight": "\\",
        "CornerDownLeft": "\\", "CornerDownRight": "/",
        "TitleFiller": "-", "TextFiller": " ",
        "ButtonSelected": " [>{button}<] ",
        "ButtonNotSelected": " [ {button} ] ",
        "BorderVertical": "|", "BorderHorizontal": "-",
        "MenuBar": "{name}  ", "MenuBarSelected": " [{name}] ",
        "CornerGeneric": "+",
        "MenuChildUnselected": " {name}", "MenuChildSelected": ">{name}"}
    STYLE_LIST = ["UNICODE", "UNICODE_BOLD", "DEFAULT", "ALTERNATE"]

# Drawable
# d8888b. d8888b.  .d8b.  db   d8b   db  .d8b.  d8888b. db      d88888b
# 88  `8D 88  `8D d8' `8b 88   I8I   88 d8' `8b 88  `8D 88      88'
# 88   88 88oobY' 88ooo88 88   I8I   88 88ooo88 88oooY' 88      88ooooo
# 88   88 88`8b   88~~~88 Y8   I8I   88 88~~~88 88~~~b. 88      88~~~~~
# 88  .8D 88 `88. 88   88 `8b d8'8b d8' 88   88 88   8D 88booo. 88.
# Y8888D' 88   YD YP   YP  `8b8' `8d8'  YP   YP Y8888P' Y88888P Y88888P


lastid = 0


class Drawable():
    """A drawable base"""
    def __init__(self, name):
        self.name = name
        self.isDestroyed = False
        self.x = 0
        self.y = 0
        self.forcedWidth = 0
        self.forcedHeigth = 0
        self.parent = None
        global lastid
        self.id = lastid + 1
        lastid = lastid + 1
        self.priority = 0
        self.lastDraw = "N/A"
        self.hidden = False

    def draw(self):
        """This is an empty method that returns []"""
        win = []
        self.lastDraw = win
        return win

    def destroy(self, destroyChild=False):
        """Destroy the object"""
        self.checkDestroyed()
        self.x = None
        self.y = None
        self.forcedWidth = None
        self.forcedHeigth = None
        self.isDestroyed = True
        self.hidden = True
        if destroyChild:
            for widget in self.widgets:
                widget.destroy(True)

    def checkDestroyed(self):
        """Check if this object is already destoryed"""
        if self.isDestroyed:
            raise RuntimeError(self.name+": This Object is already destoryed.")
        return
# .88b  d88. d88888b d8b   db db    db
# 88'YbdP`88 88'     888o  88 88    88
# 88  88  88 88ooooo 88V8o 88 88    88
# 88  88  88 88~~~~~ 88 V8o88 88    88
# 88  88  88 88.     88  V888 88b  d88
# YP  YP  YP Y88888P VP   V8P ~Y8888P'


class Menu(Drawable):
    def __init__(self, name):
        super().__init__(name)
        self.elements = []
        self.style = Styles.DEFAULT
        self.open = -1
        self.childopen = -1
        self.x = 1
        self.y = 1
        self.hasTitle = False

    def draw(self):
        """Return a list of strings"""
        win = [""]
        offset = 0
        for element in self.elements:
            highLen = 0
            for child in element["children"]:
                if len(re.sub(r"\$\([A-Za-z_0-9]*\)", "", child["name"])) \
                        > highLen:
                    highLen = len(re.sub(r"\$\([A-Za-z_0-9]*\)", "",
                                         child["name"]))
            element["highLen"] = highLen
            element["offset"] = offset
            offset = offset\
                + len(self.style["MenuBar"]
                      .replace("{name}", element["name"]))
        for element in enumerate(self.elements):
            if self.open == element[0]:
                # if self.hasTitle:
                win[0] = win[0] + self.style["TextFiller"]\
                    + self.style["MenuBarSelected"]\
                    .replace("{name}", element[1]["name"])
                win[0] = re.sub(r"^\s*", r"", win[0])
                genericCorner = self.style["CornerGeneric"]\
                    if len(element[1]["name"]) < element[1]["highLen"]\
                    else ""
                offseter = self.style["TextFiller"]\
                    * (element[1]["offset"]+1) if element[1]["offset"] > 0\
                    else ""
                win.append(offseter
                           + self.style["CornerUpLeft"] + "\033[0m"
                           + (self.style["BorderHorizontal"]
                              * len(element[1]["name"]))
                           + "\033[0m"
                           + genericCorner  # if self.hasTitle
                           # else self.style["BorderHorizontal"]
                           + "\033[0m"
                           + ((element[1]["highLen"]
                               - len(element[1]["name"]))
                              * self.style["BorderHorizontal"])
                           + "\033[0m"
                           + self.style["CornerUpRight"]
                           + "\033[0m")
                for childE in enumerate(element[1]["children"]):
                    child = childE[1]
                    filler = self.style["TextFiller"]\
                        * (element[1]["highLen"] - len(child["name"]))\
                        if element[1]["highLen"] - len(child["name"]) > 0\
                        else ""
                    name = "\033[0m" + self.style["MenuChildSelected"].replace(
                        "{name}", child["name"])\
                        + "\033[0m"\
                        if self.childopen == childE[0]\
                        else self.style["MenuChildUnselected"].replace(
                            "{name}", child["name"]) + "\033[0m"
                    win.append(offseter
                               + "\033[0m"
                               + self.style["BorderVertical"]
                               + "\033[0m"
                               + name
                               + "\033[0m"
                               + filler
                               + "\033[0m"
                               + self.style["BorderVertical"]
                               + "\033[0m")
                win.append(offseter
                           + "\033[0m"
                           + self.style["CornerDownLeft"]
                           + "\033[0m"
                           + (self.style["BorderHorizontal"]
                              * (element[1]["highLen"]+1))
                           + "\033[0m"
                           + self.style["CornerDownRight"]
                           + "\033[0m")
            else:
                win[0] = win[0] + self.style["TextFiller"]\
                    + "\033[0m"\
                    + self.style["MenuBar"]\
                    .replace("{name}", element[1]["name"])\
                    + "\033[0m"
                # print(win)
        # print(win)
        self.lastDraw = win
        return win

# db   d8b   db d888888b d8b   db d8888b.  .d88b.  db   d8b   db
# 88   I8I   88   `88'   888o  88 88  `8D .8P  Y8. 88   I8I   88
# 88   I8I   88    88    88V8o 88 88   88 88    88 88   I8I   88
# Y8   I8I   88    88    88 V8o88 88   88 88    88 Y8   I8I   88
# `8b d8'8b d8'   .88.   88  V888 88  .8D `8b  d8' `8b d8'8b d8'
#  `8b8' `8d8'  Y888888P VP   V8P Y8888D'  `Y88P'   `8b8' `8d8'


class Window(Drawable):
    """- a window class
    attributes (own):
        text (default = "")
        buttons (default = [])
        selectedButton (default = -1)
        autoWindowResize (default = True)
         True - expand the window to the texts size,
         False - Don't expand
        handlers (default = {"loop": self.buttonSelectorHandler})
        style (default = Styles.DEFAULT)
         *check the class Styles for more info
    """
    def destroy(self, destroyChild=False):
        """Destroy the window"""
        super().destroy(destroyChild)
        self.isDestroyed = True
        self.text = None
        self.buttons = None
        self.selectedButton = None

    def __init__(self, name):
        super().__init__(name)
        self.text = ""
        self.buttons = []
        self.widgets = {}
        self.selectedButton = -1
        self.autoWindowResize = True
        # True - expand the window to the texts size,
        # False - Don't expand
        self.handlers = {"loop": self.buttonSelectorHandler}
        self.style = Styles.DEFAULT

    def loop(self):
        """Run self.handlers["loop"] unless it
returns something that is not "OK" """
        while 1:
            self.parent.draw(self, "clear")
            print()
            try:
                char = self.parent.getChar()
            except Exception as e:
                raise Exception("Window Parent is None")
            a = self.handlers["loop"]({"Character": char, "Window": self})
            if a != "OK":
                break

    def buttonSelectorHandler(self, options):
        """Select a button"""
        # print(options)
        key = ""
        if options["Character"] == "\x1b":
            more = self.parent.getChar()
            if more == "[":
                evenMore = self.parent.getChar()
                if evenMore == "A":
                    key = "ARROW_UP"
                elif evenMore == "B":
                    key = "ARROW_DOWN"
                elif evenMore == "C":
                    key = "ARROW_RIGHT"
                elif evenMore == "D":
                    key = "ARROW_LEFT"
        if key == "ARROW_RIGHT":
            if self.selectedButton < len(self.buttons)-1:
                self.selectedButton = self.selectedButton + 1
        if key == "ARROW_LEFT":
            if self.selectedButton > 0:
                self.selectedButton = self.selectedButton - 1
        if options["Character"] == "\r":
            return "END"
        return "OK"
        # a = input()

    def draw(self):
        """Internal use; Use screen.draw(window); Returns a the window as a
list of strings"""
        super().checkDestroyed()
        if self.hidden:
            return ['']
        width = 0
        # w = 0
        text = self.text
        buttons = ""
        if self.buttons is not None:
            for i in range(len(self.buttons)):
                if self.selectedButton == i:
                    buttons = buttons + \
                        self.style["ButtonSelected"].\
                        replace("{button}", self.buttons[i])
                    # " [>"+self.buttons[i]+"<] "
                else:
                    buttons = buttons + \
                        self.style["ButtonNotSelected"].\
                        replace("{button}", self.buttons[i])
                    # " [ "+self.buttons[i]+" ] "
            visbuttons = re.sub(r"\$\([A-Za-z_0-9]\)", "", buttons)
            if len(visbuttons) > width:
                width = len(visbuttons)
        if self.forcedWidth <= 0:
            temp = re.sub(r"\$\([a-zA-Z_0-9]*\)", "", text)
            temp = temp.split("\n")
            if self.autoWindowResize:
                for i in range(len(temp)):
                    if len(temp[i]) > width:
                        width = len(temp[i])
                if len(self.name) > width:
                    width = len(self.name)
            else:
                raise Exception("forcedWidth is required, "
                                "if text wrap is on.")
        else:
            if self.autoWindowResize:
                temp = text.split("\n")
                i = -1
                for elem in temp:
                    i = i + 1
                    if len(temp[i]) > self.forcedWidth:
                        string = temp.pop(i)
                        for char in range(len(string)):
                            if char == self.forcedWidth:
                                temp.insert(i+1, string[:char])
                                temp.insert(i+1, string[char+1:])
                                print(temp)
                newtext = ""
                for i in temp:
                    newtext = newtext + "\n" + i
                text = newtext
            # w = self.forcedWidth
            width = self.forcedWidth + 1

        spl = round((width - len(self.name))/2)
        spr = width - (spl+len(self.name))
        win = [self.style["CornerUpLeft"]
               + (self.style["TitleFiller"]*spl)
               + self.name
               + (self.style["TitleFiller"]*spr)
               + self.style["CornerUpRight"]]
        if "menu" in self.widgets.keys():
            # state = self.widgets["menu"].open
            self.widgets["menu"].forcedWidth = width
            if not self.widgets["menu"].hidden:
                self.widgets["menu"].x = self.x + 1
                self.widgets["menu"].y = self.y + 1
                menu = self.widgets["menu"].draw()
                win.append(self.style["BorderVertical"]
                           + menu[0]
                           + (self.style["TextFiller"] *
                              (width - len(menu[0]))
                              )
                           + self.style["BorderVertical"])

            # if state["hideParent"]:
            #     textToDraw = self.widgets["menu"].draw()
            #     for i in textToDraw:
            #         win.append(self.style["BorderVertical"] + i
            #                    + self.style["TextFiller"]*(width - len(i))
            #                    + self.style["BorderVertical"])
        vistext = re.sub(r"\$\([A-Za-z_0-9]*\)", "", text).split("\n")
        text = text.split("\n")
        print('vtxt', vistext)
        print('w', width)
        for i in range(len(vistext)):
            diff = 0
            temptext = vistext[i]
            print('lvtxt', len(temptext))
            if len(temptext) < width:
                diff = (width) - len(temptext)
                # print("@ line "+str(i)+" diff "+repr(diff))
                text[i] = text[i] + self.style["TextFiller"]*diff
            win.append(self.style["BorderVertical"]+text[i]
                       + self.style["BorderVertical"])
            # print "zzz"
        if self.forcedHeigth != -1:
            win.append(self.style["BorderVertical"]
                       + self.style["TextFiller"]*(width)
                       + self.style["BorderVertical"])
            # print "aaaa"
        if buttons != [] and buttons != "":
            spl = round((width - len(buttons))/2)
            spr = width - (spl+len(buttons))
            win.append(self.style["BorderVertical"]
                       + (spl*self.style["TextFiller"])
                       + buttons
                       + (spr*self.style["TextFiller"])
                       + self.style["BorderVertical"])
        win.append(self.style["CornerDownLeft"]
                   + (self.style["BorderHorizontal"]*width)
                   + self.style["CornerDownRight"])
        if "menu" in self.widgets.keys():
            if not self.widgets["menu"].hidden:
                menu = self.widgets["menu"].draw()
                # print(menu)
                lwin = []
                offseter = 2
                voffset = 1
                for line in win:
                    lwin.append(list(line))
                for lineNum, line in enumerate(menu):
                    # print(lineNum, line)
                    try:
                        for charNum, char in enumerate(line):
                            try:
                                lwin[lineNum+voffset][charNum+offseter] = char
                            except IndexError:
                                lwin[lineNum+voffset].append(char)
                    except IndexError:
                        lwin.append(list(offseter*" ")+list(line))
                win = []
                for line in lwin:
                    newline = ""
                    for char in line:
                        newline = newline + char
                    win.append(newline)
                    # print(newline)
        self.lastDraw = win
        # print(win)

        self.width = len(win[0])
        self.height = len(win)
        return win


# .d8888.  .o88b. d8888b. d88888b d88888b d8b   db
# 88'  YP d8P  Y8 88  `8D 88'     88'     888o  88
# `8bo.   8P      88oobY' 88ooooo 88ooooo 88V8o 88
#   `Y8b. 8b      88`8b   88~~~~~ 88~~~~~ 88 V8o88
# db   8D Y8b  d8 88 `88. 88.     88.     88  V888
# `8888Y'  `Y88P' 88   YD Y88888P Y88888P VP   V8P


class Screen():
    hide = "\033[8m"
    unhide = "\033[28m"
    # fgcolors = [
    #     [
    #         "black", "red", "green", "yellow", "blue", "magenta", "cyan",
    #         "white", "gray", "bred", "bgreen", "byellow", "bblue",
    #         "bmagenta", "bcyan", "bwhite", "zero", "0"
    #     ],
    #     [
    #         "30", "31", "32", "33", "34", "35", "36", "37", "30;1",
    #         "31;1", "32;1", "33;1", "34;1", "35;1", "36;1", "37;1",
    #         "0", "0"
    #     ]
    # ]
    # bgcolors = [
    #     [
    #         "black", "red", "green", "yellow", "blue", "magenta", "cyan",
    #         "white", "gray", "bred", "bgreen", "byellow", "bblue",
    #         "bmagenta", "bcyan", "bwhite", "zero", "0"
    #     ],
    #     [
    #         "40", "41", "42", "43", "44", "45", "46", "47", "100", "101",
    #         "102", "103", "104", "105", "106", "107", "0", "0"
    #     ]
    # ]
    fgcolors = {
        "black": "30",
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "magenta": "35",
        "cyan": "36",
        "white": "37",
        "gray": "30;1",
        "bred": "31;1",
        "bgreen": "32;1",
        "byellow": "33;1",
        "bblue": "34;1",
        "bmagenta": "35;1",
        "bcyan": "36;1",
        "bwhite": "37;1",
        "zero": "0",
        "0": "0"
    }
    bgcolors = {
        "black": "40",
        "red": "41",
        "green": "42",
        "yellow": "43",
        "blue": "44",
        "magenta": "45",
        "cyan": "46",
        "white": "47",
        "gray": "100",
        "bred": "101",
        "bgreen": "102",
        "byellow": "103",
        "bblue": "104",
        "bmagenta": "105",
        "bcyan": "106",
        "bwhite": "107",
    }
    effects = {
        "bold": "1",
        "faint": "2",
        "italic": "3",
        "underline": "4",
        "slow_blink": "5",
        "rapid_blink": '6',
        'reverse': '7',
        'conceal': '8',
        'hide': '8',
        'crossed_out': '9',
        'blink_off': '25',
        'reverse_off': '27',
        'conceal_off': '28',
        'reveal': '28',
        'show': '28',
        'crossed_out_off': '29',


    }

    def __init__(self, size=[80, 24]):
        # self.getChar = self.getGetChar()
        self.size = size
        self.windows = []
        self.background = []
        try:
            import msvcrt

            def getChar():
                """Get a char from STDIN (msvcrt)"""
                return msvcrt.getch()  # noqa: F821

            self.platform = "win"
            self.getChar = getChar
        except ImportError:
            self.platform = "linux"

            def getChar():
                """Get a char from STDIN (tty, termios, sys)"""
                fd = sys.stdin.fileno()
                old = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    return sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)
            self.getChar = getChar

    def setCur(self, x, y, returnTheEscape=False):
        """Move the cursor the x and y.
        Return the ANSI Escape, if returnTheEscape is True"""
        if returnTheEscape:
            return '\033['+str(y)+';'+str(x)+'H'
        else:
            print('\033['+str(y)+';'+str(x)+'H', end='', flush=True)

    def draw_no_redraw(self, window):
        """Draw a window onto the screen without redrawing other windows.
        Returns True if window was drawn False otherwise."""
        if window.isDestroyed:
            return False
        a = window.draw()
        x = window.x
        y = window.y
        for i in range(len(a)):
            self.setChar(self.format(a[i]), x, y+i)
        return True

    def draw(self, window=None, forceRedrawMode="clear"):
        """
        Redraw a window onto the screen with max priority
        forceRedrawMode can be:
            - "clear"
            - "oldAsBackground"
            - "forcedBackground"
        """
        if forceRedrawMode.lower() == "clear":
            self.clear()
        # if forceRedrawMode.lower() == "oldasbackground":
        #     print("\033[s")
        if forceRedrawMode.lower() == "forcedbackground":
            self.setScreen(self.background)
        windows = sorted(self.windows,
                         key=lambda window: window.priority,
                         reverse=False)
        # self.clear()
        for i in range(len(windows)):
            if windows[i].isDestroyed:
                continue
            if windows[i] is not None:
                if window is not None:
                    if windows[i].id == window.id:
                        continue
                for line in range(len(windows[i].lastDraw)):
                    # print(windows[i].lastDraw)
                    if not windows[i].lastDraw == "N/A":
                        self.setChar(self.format(windows[i].lastDraw[line]),
                                     windows[i].x,
                                     windows[i].y+line)
                        # print("zzzzzzzzzzzzzzzz")
                    else:
                        self.draw_no_redraw(windows[i])
        if window is not None:
            self.draw_no_redraw(window)
        # if forceRedrawMode.lower() == "oldasbackground":
        #     print("\033[u")

    def setScreen(self, screen, alternateScreen=False):
        """Set the screen to the list in the screen variable"""
        sys.stdout.write('\033[2J\033[0;0H')
        y = self.size[1]
        for i in range(y):
            try:
                print(screen[i])
                # '\033[0;'+i+'H'+
            except Exception as e:
                pass
                # raise Exception("WARNING: List smaller than the screen")
        return

    def clear(self):
        """Clear the screen(print \\033[2J)"""
        print('\033[2J', end='', flush=True)

    def getColor(self, color, bg=False):
        """Return a color"""
        try:
            if bg:
                return self.bgcolors[color]
            else:
                return self.fgcolors[color]
        except Exception:
            return "0"

    def format(self, string):
        for effect in self.effects.keys():
            string = string.replace("$("+effect.lower()+")",
                                    "\033["+self.effects[effect]+"m")
        for color in self.bgcolors.keys():
            string = string.replace("$(b_"+color.lower()+")",
                                    "\033["+self.bgcolors[color.lower()]+"m")
        for color in self.fgcolors.keys():
            string = string.replace("$("+color.lower()+")",
                                    "\033["+self.fgcolors[color.lower()]+"m")
        return string

    def setChar(self, char, x, y, color="0"):
        """ color - color name (case insensitive)
            string with \\ as the first char will not be interpreted
            instead it will be used directly in the ANSI Escape sequence."""  # noqa
        if color[0] != "\\":
            color = self.getColor(color)
        else:
            color = color[1:]
        print('\033['+str(y)+';'+str(x)+'H\033['+str(color)+'m'+char,
              end='', flush=True)

    def add_window(self, window, setParent=True):
        """Add the window the the screen
        The window will be drawn unless window.hidden is True."""
        self.windows.append(window)
        if setParent:
            window.parent = self

    def hidden_input(self, inputa="", handler=None):
        # print self.hide,
        a = self.getChar()
        action = "accept"
        if a == "\r":
            return inputa
        elif a == "\x7f":  # Backspace
            oldinput = inputa
            inputa = inputa[:-1]
            if handler is not None:
                action = handler("backspace", inputa, oldinput)
            if action != "accept":
                inputa = oldinput
            return self.hidden_input(inputa, handler)
        else:
            oldinput = inputa
            inputa = inputa + a
            if handler is not None:
                action = handler(a, inputa, oldinput)
            if action != "accept" and action != "accept-end":
                inputa = oldinput
            if action == "accept-end":
                return inputa
            if action == "end":
                return oldinput
            return self.hidden_input(inputa, handler)


if __name__ == "__main__":
    print("This is not a normal python(3) program.")
    print("This is a library for creating ncurses-like windows")
    exit(0)
