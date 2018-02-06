#!/usr/bin/python
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


def getDisplayLen(string):
    return len(string.replace("\xc5", "").replace("\xc4", "")
               .replace("\xc3", "").replace("\xc2", "").replace("\xc1", "")
               .replace("\xc0", "").replace("\xc6", "").replace("\xc7", "")
               .replace("\xc7", "").replace("\xc8", "").replace("\xc9", ""))


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
    UNICODE = {
        "CornerUpLeft": "\u250C", "CornerUpRight": "\u2510",
        "CornerDownLeft": "\u2514", "CornerDownRight": "\u2518",
        "TitleFiller": "\u2500", "TextFiller": " ",
        "ButtonSelected": " [>{button}<] ",
        "ButtonNotSelected": " [ {button} ] ",
        "BorderVertical": "\u2502", "BorderHorizontal": "\u2500",
        "MenuBar": "  {name}  ", "MenuBarSelected": " [{name}] ",
        "CornerGeneric": "+",
        "MenuChildUnselected": " {name}", "MenuChildSelected": ">{name}"}
    UNICODE_BOLD = {
        "CornerUpLeft": "\u250F", "CornerUpRight": "\u2513",
        "CornerDownLeft": "\u2517", "CornerDownRight": "\u251B",
        "TitleFiller": "\u2501", "TextFiller": " ",
        "ButtonSelected": " [>{button}<] ",
        "ButtonNotSelected": " [ {button} ] ",
        "BorderVertical": "\u2503", "BorderHorizontal": "\u2501",
        "MenuBar": "  {name}  ", "MenuBarSelected": " [{name}] ",
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
        "MenuBar": "  {name}  ", "MenuBarSelected": " [{name}] ",
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

    def destroy(self, destroyChild=False):
        self.checkDestroyed()
        self.x = None
        self.y = None
        self.forcedWidth = None
        self.forcedHeigth = None
        self.isDestroyed = True
        if destroyChild:
            for widget in self.widgets:
                widget.destroy(True)

    def checkDestroyed(self):
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
        self.elements = [{"name": "Nie Wiem", "children": []}]
        self.style = Styles.DEFAULT
        self.open = -1
        self.childopen = -1
        self.x = 1
        self.y = 0

    def draw(self):
        win = ["", ""]
        offset = 0
        for element in self.elements:
            highLen = 0
            for child in element["children"]:
                if len(child["name"]) > highLen:
                    highLen = len(child["name"])
            element["highLen"] = highLen
            element["offset"] = offset
            offset = offset\
                + len(self.style["MenuBar"]
                      .replace("{name}", element["name"]))
        for element in enumerate(self.elements):
            if self.open == element[0]:
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
                           + self.style["BorderVertical"]
                           + (self.style["BorderHorizontal"]
                              * len(element[1]["name"]))
                           + genericCorner
                           + ((element[1]["highLen"]
                               - len(element[1]["name"]))
                              * self.style["BorderHorizontal"])
                           + self.style["BorderVertical"])
                for childE in enumerate(element[1]["children"]):
                    child = childE[1]
                    filler = self.style["TextFiller"]\
                        * (element[1]["highLen"] - len(child["name"]))\
                        if element[1]["highLen"] - len(child["name"]) > 0\
                        else ""
                    name = self.style["MenuChildSelected"].replace(
                        "{name}", child["name"])\
                        if self.childopen == childE[0]\
                        else self.style["MenuChildUnselected"].replace(
                            "{name}", child["name"])
                    win.append(offseter
                               + self.style["BorderVertical"]
                               + name
                               + filler
                               + self.style["BorderVertical"])
                win.append(offseter
                           + self.style["CornerDownLeft"]
                           + (self.style["BorderHorizontal"]
                              * (element[1]["highLen"]+1))
                           + self.style["CornerDownRight"])
            else:
                win[0] = win[0] + self.style["TextFiller"]\
                    + self.style["MenuBar"]\
                    .replace("{name}", element[1]["name"])
        # print(win)
        return win

# db   d8b   db d888888b d8b   db d8888b.  .d88b.  db   d8b   db
# 88   I8I   88   `88'   888o  88 88  `8D .8P  Y8. 88   I8I   88
# 88   I8I   88    88    88V8o 88 88   88 88    88 88   I8I   88
# Y8   I8I   88    88    88 V8o88 88   88 88    88 Y8   I8I   88
# `8b d8'8b d8'   .88.   88  V888 88  .8D `8b  d8' `8b d8'8b d8'
#  `8b8' `8d8'  Y888888P VP   V8P Y8888D'  `Y88P'   `8b8' `8d8'


class Window(Drawable):
    def destroy(self, destroyChild=False):
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
        try:
            char = self.parent.getChar()
        except Exception as e:
            raise Exception("Window Parent is None")
        self.handlers["loop"]({"Character": char, "Window": self})

    def buttonSelectorHandler(self, options):
        print(options)
        if options["Character"] == "\x1b":
            more = self.parent.getChar()
            print(repr(more))
            if more == "[":
                morer = self.parent.getChar()
                print(repr(morer))
                # if morer
        # a = input()

    def draw(self):
        """Internal use; Use screen.draw(window); Returns a the window as a """
        """list of strings"""
        super().checkDestroyed()
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
            if getDisplayLen(buttons) > width:
                width = getDisplayLen(buttons)
        if self.forcedWidth <= 0:
            temp = text.split("\n")
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
            state = self.widgets["menu"].getState()
            self.widgets["menu"].forcedWidth = width
            if not state["hidden"]:
                win.append(self.widgets["menu"].draw())
            if state["hideParent"]:
                textToDraw = self.widgets["menu"].draw()
                for i in textToDraw:
                    win.append(self.style["BorderVertical"] + i
                               + self.style["TextFiller"]*(width - len(i))
                               + self.style["BorderVertical"])
        text = text.split("\n")
        for i in range(len(text)):
            diff = 0
            temptext = text[i]
            if getDisplayLen(temptext) < width:
                diff = (width) - getDisplayLen(temptext)
                # print "@ line "+str(i)+" diff "+repr(diff
                temptext = temptext + self.style["TextFiller"]*diff
            win.append(self.style["BorderVertical"]+temptext
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

    try:
        import msvcrt

        def getChar(self):
            return msvcrt.getch()  # noqa: F821

        platform = "win"
    except ImportError:
        platform = "linux"

        def getChar(self):
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                return sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def __init__(self, size=[80, 24]):
        # self.getChar = self.getGetChar()
        self.size = size
        self.windows = []
        self.background = []
        self.fgcolors = [
            [
                "black", "red", "green", "yellow", "blue", "magenta", "cyan",
                "white", "gray", "bred", "bgreen", "byellow", "bblue",
                "bmagenta", "bcyan", "bwhite", "zero", "0"
            ],
            [
                "30", "31", "32", "33", "34", "35", "36", "37", "30;1",
                "31;1", "32;1", "33;1", "34;1", "35;1", "36;1", "37;1",
                "0", "0"
            ]
        ]
        self.bgcolors = [
            [
                "black", "red", "green", "yellow", "blue", "magenta", "cyan",
                "white", "gray", "bred", "bgreen", "byellow", "bblue",
                "bmagenta", "bcyan", "bwhite", "zero", "0"
            ],
            [
                "40", "41", "42", "43", "44", "45", "46", "47", "100", "101",
                "102", "103", "104", "105", "106", "107", "0", "0"
            ]
        ]

    def setCur(self, x, y, doReturn=False):
        if doReturn is False:
            sys.stdout.write('\033['+str(y)+';'+str(x)+'H')
        else:
            return '\033['+str(y)+';'+str(x)+'H'

    def draw_no_redraw(self, window):
        """Draw a window onto the screen without redrawing other windows.
        Returns True if window was drawn False otherwise."""
        if window.isDestroyed:
            return False
        a = window.draw()
        x = window.x
        y = window.y
        for i in range(len(a)):
            self.setChar(a[i], x, y+i)
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
        if forceRedrawMode.lower() == "oldasbackground":
            print("\033[s")
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
                        self.setChar(windows[i].lastDraw[line], windows[i].x,
                                     windows[i].y+line)
                        # print("zzzzzzzzzzzzzzzz")
                    else:
                        self.draw_no_redraw(windows[i])
        if window is not None:
            self.draw_no_redraw(window)
        if forceRedrawMode.lower() == "oldasbackground":
            print("\033[u")

    def setScreen(self, screen):
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
        print('\033[2J', end='')

    def getColor(self, color, bg=False):
        if bg:
            colors = self.bgcolors
        else:
            colors = self.fgcolors
        if color not in colors[0]:
            return
        for i in range(len(colors[0])):
            if color == colors[0][i]:
                return colors[1][i]

    def setChar(self, char, x, y, color="0"):
        """color
            color name (case insensitive)
            string with \\ as the first char will not be interpreted;""" + \
            """ instead it will be used directly in the ANSI Escape sequence."""  # noqa
        if color[0] != "\\":
            color = self.getColor(color)
        else:
            color = color[1:]
        print('\033['+str(y)+';'+str(x)+'H\033['+str(color)+'m'+char, end='')

    def add_window(self, window):
        self.windows.append(window)

    def hidden_input(self, inputa="", handler=None):
        # print self.hide,
        a = self.getChar()
        action = ""
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
#     import argparse
#     p = argparse.ArgumentParser(description='Generate a window')
#     p.add_argument("-n", "--name", dest='name')
#     p.add_argument("-t", "--text", dest='text')
#     p.add_argument("-b", "--buttons", dest='buttons')
#     p.add_argument('-x', '--posX', dest='x')
#     p.add_argument('-y', '--posY', dest='y')
#     p.add_argument('-fh', '--forcedHeigth', dest='fh')
#     p.add_argument('-fw', '--forcedWidth', dest='fw')
#     p.add_argument('-sb', '--selectedButton', dest='sb')
#     args = p.parse_args()
#     s = Screen()
#
#     s.clear()
#     # s.setChar("Args: "+str(args), 0, 20, color="red")
#     # nazwa = "a"  # raw_input("nazwa>")
#     window = Window(args.name)  # "TEST!!")  #
#     window.setText(args.text.replace("\\n", "\n"))  # "1\n2\n3\n4\n5\n6"
#     # args.text.replace("\\n", "\n"))
#     # longInput("tekst(ctrl+c, lub puste kończy)>"))
#     window.y = int(args.x)  # 1  #
#     window.x = int(args.y)  # 1  #
#     window.forcedHeigth = int(args.fh)  # -1  #
#     window.forcedWidth = int(args.fw)  # -1  #
#     window.buttons = args.buttons.split(",")  # ["OK", "Nie OK"]  #
#     window.selectedButton = int(args.sb)   # \-1  #
#     s.draw(window)
#     # # s.setChar("======Screen Test======", 0, 0, color="red")
