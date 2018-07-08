#!/usr/bin/python3
"""A library for generating ncurses-like windows."""
# -*- coding: utf-8 -*-
# Name: Maciek's aMazing Windows
# Author: Maciek
from __future__ import print_function
import sys
import re
import os
import signal

try:
    # Linux
    import termios
    import tty
except ImportError:
    # Windows and other (DOS?)
    pass
try:
    import logger as log
    loggingEnabled = True
except ImportError:
    loggingEnabled = False

# Font: Basic
# Styles
# .d8888. d888888b db    db db      d88888b .d8888.
# 88'  YP `~~88~~' `8b  d8' 88      88'     88'  YP
# `8bo.      88     `8bd8'  88      88ooooo `8bo.
#   `Y8b.    88       88    88      88~~~~~   `Y8b.
# db   8D    88       88    88booo. 88.     db   8D
# `8888Y'    YP       YP    Y88888P Y88888P `8888Y'


POS_CENTER = "center"
POS_LEFT = "left"
POS_RIGHT = "right"
POS_UP = 'up'
POS_DOWN = 'down'


# Z: Styles
class Styles():
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
        "MenuBar": "{name}  ", "MenuBarSelected": " [{name}] ",
        "CornerGeneric": "+",
        "MenuChildUnselected": " {name}", "MenuChildSelected": ">{name}",
        "Format": "N/A", "EmptyText": "_"}
    UNICODE_BOLD = {
        "CornerUpLeft": "\u250F", "CornerUpRight": "\u2513",
        "CornerDownLeft": "\u2517", "CornerDownRight": "\u251B",
        "TitleFiller": "\u2501", "TextFiller": " ",
        "ButtonSelected": " [>{button}<] ",
        "ButtonNotSelected": " [ {button} ] ",
        "BorderVertical": "\u2503", "BorderHorizontal": "\u2501",
        "MenuBar": "{name}   ", "MenuBarSelected": " [{name}] ",
        "CornerGeneric": "+",
        "MenuChildUnselected": " {name}", "MenuChildSelected": ">{name}",
        "Format": "N/A", "EmptyText": "_"}
    DEFAULT = {
        "CornerUpLeft": "+", "CornerUpRight": "+",
        "CornerDownLeft": "+", "CornerDownRight": "+",
        "TitleFiller": "-", "TextFiller": " ",
        "ButtonSelected": " [>{button}<] ",
        "ButtonNotSelected": " [ {button} ] ",
        "BorderVertical": "|", "BorderHorizontal": "-",
        "MenuBar": "{name}  ", "MenuBarSelected": "|{name}| ",
        "CornerGeneric": "+",
        "MenuChildUnselected": " {name}", "MenuChildSelected": ">{name}",
        "Format": "N/A", "EmptyText": "_"}
    ALTERNATE = {
        "CornerUpLeft": "/", "CornerUpRight": "\\",
        "CornerDownLeft": "\\", "CornerDownRight": "/",
        "TitleFiller": "-", "TextFiller": " ",
        "ButtonSelected": " [>{button}<] ",
        "ButtonNotSelected": " [ {button} ] ",
        "BorderVertical": "|", "BorderHorizontal": "-",
        "MenuBar": "{name}  ", "MenuBarSelected": " [{name}] ",
        "CornerGeneric": "+",
        "MenuChildUnselected": " {name}", "MenuChildSelected": ">{name}",
        "Format": "N/A", "EmptyText": "_"}
    STYLE_LIST = ["UNICODE", "UNICODE_BOLD", "DEFAULT", "ALTERNATE"]

# Z: class Drawable
# d8888b. d8888b.  .d8b.  db   d8b   db  .d8b.  d8888b. db      d88888b
# 88  `8D 88  `8D d8' `8b 88   I8I   88 d8' `8b 88  `8D 88      88'
# 88   88 88oobY' 88ooo88 88   I8I   88 88ooo88 88oooY' 88      88ooooo
# 88   88 88`8b   88~~~88 Y8   I8I   88 88~~~88 88~~~b. 88      88~~~~~
# 88  .8D 88 `88. 88   88 `8b d8'8b d8' 88   88 88   8D 88booo. 88.
# Y8888D' 88   YD YP   YP  `8b8' `8d8'  YP   YP Y8888P' Y88888P Y88888P


lastid = 0


class Drawable():
    """A drawable base."""

    # ---------------------------------
    # self.name
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.requiresRedrawing = True

    # ---------------------------------
    # self.y
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.requiresRedrawing = True

    # ---------------------------------
    # self.x
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.requiresRedrawing = True

    # ---------------------------------
    # self.xRel
    @property
    def xRel(self):
        return self._xRel

    @xRel.setter
    def xRel(self, value):
        self._xRel = value
        self.requiresRedrawing = True
        self.recalcPos()

    # ---------------------------------
    # self.yRel
    @property
    def yRel(self):
        return self._yRel

    @yRel.setter
    def yRel(self, value):
        self._yRel = value
        self.requiresRedrawing = True
        self.recalcPos()

    # ---------------------------------
    def __init__(self, name):
        global lastid
        self._name = name
        self.isDestroyed = False

        self._x = 1
        self._y = 1
        self._xRel = POS_CENTER
        self._yRel = POS_CENTER

        self.forcedWidth = 0
        self.forcedHeight = 0
        self.width = 0
        self.height = 0

        self.parent = None

        self.id = lastid + 1
        lastid = lastid + 1
        self.priority = 0
        self.lastDraw = "N/A"
        self.hidden = False
        self.requiresRedrawing = False
        self.useRelativePos = False
        self._xRel = POS_CENTER
        self._yRel = POS_CENTER
        self.handlers = {"loop": lambda *args: None,
                         "SIGWINCH": lambda this, caller: self.recalcPos()}

    def check_parent(self):
        if self.parent is None:
            return False
        try:
            if self.parent.size:
                return True
        except NameError:
            return False
        return True

    def recalcPos(self):
        self.draw()
        if not self.check_parent():
            raise InvalidStateError('Cannot recalculate the position, because '
                                    'either the parent is None or has no size '
                                    'attribute')
        if self.xRel == POS_CENTER:
            self.x = round(self.parent.size[0]/2)-round(self.width/2)
        elif self.xRel[0] == POS_LEFT:
            self.x = round(self.xRel[1]*self.parent.size[0])\
                - round(self.width/2)
        elif self.xRel[0] == POS_RIGHT:
            self.x = round(self.xRel[1]*self.parent.size[0])\
                - round(self.width/2)
        else:
            raise InvalidStateError(
                "mmw3.Drawable.xRel can only be mmw3.POS_CENTER or "
                "[mmw3.POS_LEFT, float] or [mmw3.POS_RIGHT, float]")

        if self.yRel == POS_CENTER:
            self.y = round(self.parent.size[1]/2)-round(self.height/2)
        elif self.yRel[0] == POS_UP:
            self.y = round(self.xRel[1]*self.parent.size[1])\
                - round(self.height/2)
        elif self.yRel[0] == POS_DOWN:
            self.y = round(self.xRel[1]*self.parent.size[1])\
                - round(self.height/2)
        else:
            raise InvalidStateError(
                "mmw3.Drawable.yRel can only be mmw3.POS_CENTER or "
                "[mmw3.POS_LEFT, float] or [mmw3.POS_RIGHT, float]")
        return self.x, self.y

    def draw(self):
        """**Stub**
        This method should return a list of strings(rendered object)"""
        win = []
        self.lastDraw = win
        return win

    def destroy(self, destroyChild=False):
        """Destroy the object"""
        self.checkDestroyed()
        self.x = None
        self.y = None
        self.forcedWidth = None
        self.forcedHeight = None
        self.isDestroyed = True
        self.hidden = True
        self.lastDraw = "N/A"
        if destroyChild:
            for widget in self.widgets:
                widget.destroy(True)

    def checkDestroyed(self):
        """Check if this object is already destoryed"""
        if self.isDestroyed:
            raise InvalidStateError(self.name
                                    + ": This Object is already destoryed.")
        return


# Z: class Graphic
#  d888b  d8888b.  .d8b.  d8888b. db   db d888888b  .o88b.
# 88' Y8b 88  `8D d8' `8b 88  `8D 88   88   `88'   d8P  Y8
# 88      88oobY' 88ooo88 88oodD' 88ooo88    88    8P
# 88  ooo 88`8b   88~~~88 88~~~   88~~~88    88    8b
# 88. ~8~ 88 `88. 88   88 88      88   88   .88.   Y8b  d8
#  Y888P  88   YD YP   YP 88      YP   YP Y888888P  `Y88P'
class Graphic(Drawable):
    """Pseudo-graphic drawable object"""

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if len(value) < 1:
            raise InvalidStateError('Graphic.text cannot have a '
                                    'length of 0 or less')
        nval = value
        if len(value[0]) == 1:
            nval = value.split('\n')
        self._text = nval

    def __init__(self, text):
        super().__init__('Graphic')
        # if len(text) < 1:
        #     raise InvalidStateError('Graphic.__init__(self, >text<) '
        #                             'text cannot have a length of 0 or less')
        self.text = text

    def draw(self):
        return self._text

    # def checkSize(self):
    #     """Checks self.text for size weirdness; Returns True
    #     or raises InvalidStateError if something is wrong"""
    #     llen = len(self.text[0])
    #     for num, line in enumerate(self.text):
    #         if len(line) != llen:
    #             raise InvalidStateError('The size of self.text is wierd. '
    #                                     'Line '+str(num)+' has length of '
    #                                     + str(len(line))+' characters, '
    #                                     'but should have '+str(llen)
    #                                     + ' characters')
    #     return True

# Z: class Menu
# .88b  d88. d88888b d8b   db db    db
# 88'YbdP`88 88'     888o  88 88    88
# 88  88  88 88ooooo 88V8o 88 88    88
# 88  88  88 88~~~~~ 88 V8o88 88    88
# 88  88  88 88.     88  V888 88b  d88
# YP  YP  YP Y88888P VP   V8P ~Y8888P'


class Menu(Drawable):
    def selectorHandler(self, char):
        """Select a button"""
        # log.slog('selectorHandler', repr(char))
        # key = ""
        # if char == "\x1b":
        #     more = self.parent.getChar()
        #     log.slog('selectorHandler', 'more '+repr(more))
        #     if more == "[":
        #         evenMore = self.parent.getChar()
        #         log.slog('selectorHandler', 'evenmore '+repr(evenMore))
        #         if evenMore == "A":
        #             key = "ARROW_UP"
        #         elif evenMore == "B":
        #             key = "ARROW_DOWN"
        #         elif evenMore == "C":
        #             key = "ARROW_RIGHT"
        #         elif evenMore == "D":
        #             key = "ARROW_LEFT"
        if char == "ARROW_RIGHT":
            if self.open < len(self.elements)-1:
                self.open += 1
        if char == "ARROW_LEFT":
            if self.open > 0:
                self.open -= 1
        if char == "ARROW_DOWN":
            if self.childopen < len(self.elements[self.open]['children'])-1:
                self.childopen += 1
        if char == "ARROW_UP":
            if self.childopen > 0:
                self.childopen -= 1
        if char == "\r":
            return self.handlers["menuClicked"](self)

    def __init__(self, name):
        super().__init__(name)
        self.elements = []
        self.handlers = {'menuClicked': lambda self: None,
                         'loop': self.selectorHandler}
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
                child["vislen"] = len(re.sub(r"\$\([A-Za-z_0-9]*\)", "",
                                             child["name"]))
                if child["vislen"] > highLen:
                    highLen = child["vislen"]
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
                           + (genericCorner if self.hasTitle
                              else self.style["BorderHorizontal"])
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
                        * (element[1]["highLen"] - child["vislen"])\
                        if element[1]["highLen"] - child["vislen"] > 0\
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
# Z: class Window
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
        self.handlers["loop"] = self.buttonSelectorHandler
        self.handlers["SIGWINCH"] = lambda a, b: None
        # True - expand the window to the texts size,
        # False - Don't expand

        self.style = Styles.DEFAULT
        self.styleOptions = {"ButtonAlignment": "N/A"}

    def loop(self):
        """Run self.handlers["loop"] unless it
returns something that is not "OK" """
        while 1:
            if self.parent is None:
                raise InvalidStateError("Window Parent is None")
            self.parent.draw(self, "clear")
            print()
            try:
                char = self.parent.getChar()
            except Exception:
                raise InvalidStateError("Window Parent is None")
            a = self.handlers["loop"]({"Character": char, "Window": self})
            if a != "OK":
                break

    def buttonSelectorHandler(self, char):
        """Select a button"""
        # print(options)
        # key = ""
        # log.log('handler ', repr(char))
        if char == "ARROW_RIGHT":
            if self.selectedButton < len(self.buttons)-1:
                self.selectedButton = self.selectedButton + 1
            return
        if char == "ARROW_LEFT":
            if self.selectedButton > 0:
                self.selectedButton = self.selectedButton - 1
            return
        # if char == "\x1b":
        #     more = self.parent.getChar()
        #     if more == "[":
        #         evenMore = self.parent.getChar()
        #         if evenMore == "A":
        #             key = "ARROW_UP"
        #         elif evenMore == "B":
        #             key = "ARROW_DOWN"
        #         elif evenMore == "C":
        #             key = "ARROW_RIGHT"
        #         elif evenMore == "D":
        #             key = "ARROW_LEFT"
        # if key == "ARROW_RIGHT":
        #     if self.selectedButton < len(self.buttons)-1:
        #         self.selectedButton = self.selectedButton + 1
        # if key == "ARROW_LEFT":
        #     if self.selectedButton > 0:
        #         self.selectedButton = self.selectedButton - 1
        if char == "\r":
            return "END"
        return "OK"
        # a = input()

    def draw(self):
        """Internal use; Use screen.draw(window) to display a window;
        Returns a the window as a list of strings"""
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
                raise InvalidStateError("forcedWidth is required, "
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

        visname = re.sub(r"\$\([A-Za-z_0-9]*\)", "", self.name)
        spl = round((width - len(visname))/2)
        spr = width - (spl+len(visname))
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
                           + (self.style["TextFiller"]
                              * (width - len(menu[0]))
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
        # print('vtxt', vistext)
        # print('w', width)
        for i in range(len(vistext)):
            diff = 0
            temptext = vistext[i]
            # print('lvtxt', len(temptext))
            if len(temptext) < width:
                diff = (width) - len(temptext)
                # print("@ line "+str(i)+" diff "+repr(diff))
                text[i] = text[i] + self.style["TextFiller"]*diff
            win.append(self.style["BorderVertical"]+text[i]
                       + self.style["BorderVertical"])
            # print "zzz"
        if self.forcedHeight != -1:
            win.append(self.style["BorderVertical"]
                       + self.style["TextFiller"]*(width)
                       + self.style["BorderVertical"])
            # print "aaaa"
        visbuttons = re.sub(r"\$\([A-Za-z_0-9]*\)", "", buttons)
        if buttons != [] and buttons != "":
            fillerL = ""
            fillerR = ""
            if self.styleOptions["ButtonAlignment"] != "N/A":
                if self.styleOptions["ButtonAlignment"] == \
                        POS_LEFT:
                    fillerL = " "
                    fillerR = self.style["TextFiller"]\
                        * (width - len(visbuttons) - 1)
                elif self.styleOptions["ButtonAlignment"] == \
                        POS_RIGHT:
                    fillerL = self.style["TextFiller"]\
                        * (width - len(visbuttons) - 1)
                    fillerR = " "
                elif self.styleOptions["ButtonAlignment"] == \
                        POS_CENTER:
                    pass
                else:
                    raise InvalidStateError("ButtonAlignment can only be right"
                                            " or left or center.")

            spl = round((width - len(visbuttons))/2)
            # spl = spl - len(fillerL)
            spr = width - (spl+len(visbuttons))
            # spr = spr - len(fillerR)
            # print("spl:", spl)
            # print("spr:", spr)
            win.append(self.style["BorderVertical"]
                       + ((spl*self.style["TextFiller"]) if fillerL == ""
                       else "")
                       + fillerL
                       + buttons
                       + fillerR
                       + ((spr*self.style["TextFiller"]) if fillerR == ""
                       else "")
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
# Z: class Textarea
# d888888b d88888b db    db d888888b    .d8b.  d8888b. d88888b  .d8b.
# `~~88~~' 88'     `8b  d8' `~~88~~'   d8' `8b 88  `8D 88'     d8' `8b
#    88    88ooooo  `8bd8'     88      88ooo88 88oobY' 88ooooo 88ooo88
#    88    88~~~~~  .dPYb.     88      88~~~88 88`8b   88~~~~~ 88~~~88
#    88    88.     .8P  Y8.    88      88   88 88 `88. 88.     88   88
#    YP    Y88888P YP    YP    YP      YP   YP 88   YD Y88888P YP   YP


class TextArea(Drawable):
    def __init__(self, name, startPoint=(0, 0), endPoint=(80, 24)):
        """Init the TextArea obj. Custructor's parameters (in order):
         self,
         name - name/title that will be displayed,
         startPoint - a tuple of coordinates that indicate the first point of
          a rectagle
         endPoint - same as startPoint but indicates the other needed point
          to draw a rectagle
         ex. TextArea("This is a TextArea", (0,0), (80, 24))

         self.name - The name ofc
         self.text - The text (overrides the self.height )
         self.startPoint - First point needed to draw a rectangle
         self.endPoint - Second --||--
         self.parent - A parent Screen
         self.handlers - The handler list
           * 'loop' the function called when a key is pressed in Screen.loop()
                    handler(key)
                    - key an escape or
                        ARROW_UP, ARROW_DOWN, ARROW_LEFT or ARROW_RIGHT
         self.curpos - The position of the cursor inside this object
            = [x, y]
         self.width - The width of this object when it was last drawn
         self.height - Same as above but height
         self.enableAsciiArt - Enables you to move the cursor even when it is
           already at the end of a line, but the object is still bigger
           eg. (| is the cursor)
           * Enabled  ["A line|"] ---[RIGHT_ARROW]> ["A line |"]
           * Disabled ["A line|"] ---[RIGHT_ARROW]> ["A line|"]
         """
        super().__init__(name)
        self.name = name
        self.text = []
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.parent = None
        self.handlers["loop"] = self.inputhandler
        self.style = Styles.DEFAULT
        self.curpos = [0, 0]
        self.width = self.endPoint[0] - self.startPoint[0]
        self.height = self.endPoint[1] - self.startPoint[1]
        self.enableAsciiArt = False

    def inputhandler(self, char):
        if loggingEnabled:
            log.slog("TextArea.inputHandler", "cpos: ", str(self.curpos))
        if char == 'ARROW_UP':
            if self.curpos[1] > 0:
                self.curpos[1] = self.curpos[1] - 1
        elif char == 'ARROW_DOWN':
            if self.curpos[1] < self.height:
                self.curpos[1] = self.curpos[1] + 1
                if self.curpos[1] <= len(self.text):
                    self.text.append("")
        elif char == "ARROW_LEFT":
            if self.curpos[0] > 0:
                self.curpos[0] = self.curpos[0] - 1
        elif char == 'ARROW_RIGHT':
            if self.enableAsciiArt:
                if self.curpos[0] < self.width:
                    self.curpos[0] = self.curpos[0] + 1
            else:
                if self.curpos[0] < len(self.text[self.curpos[1]]):
                    self.curpos[0] = self.curpos[0] + 1
        elif char == "\x7f":
            if len(self.text) == 0:
                return
            if len(self.text[self.curpos[1]]) == 0:
                self.text.pop(self.curpos[1])
                self.curpos[1] = self.curpos[1] - 1
            else:
                self.text[self.curpos[1]] = self.text[self.curpos[1]][:-1]
        else:
            try:
                self.text[self.curpos[1]] = \
                    self.text[self.curpos[1]][:self.curpos[0]-1]\
                    + char\
                    + self.text[self.curpos[1]][self.curpos[0]:]
                self.curpos[0] += 1
                #
            except IndexError:
                self.text[self.curpos[1]] = \
                    self.text[self.curpos[1]][:self.curpos[0]-1]\
                    + char
                self.curpos[0] += 1

    def draw(self):
        self.width = self.endPoint[0] - self.startPoint[0]
        self.height = self.endPoint[1] - self.startPoint[1]
        output = []
        output.append(self.name)
        if loggingEnabled:
            log.log("TextArea.draw (width)- "+str(self.width))
            log.log("TextArea.draw (height)- "+str(self.height))
            log.log("TextArea.draw (text)- "+str(self.text))
        for line in self.text:
            nline = ""
            if loggingEnabled:
                log.log("TextArea.draw (loop)- "+str(line))
            if len(line) >= self.width:
                nline = line[:self.width-1]
            if len(line) < self.width:
                nline = line + (
                    self.style["EmptyText"]
                    * (self.width - len(line)))
            output.append(nline)
        if loggingEnabled:
            log.log("TextArea.draw (ltext)- "+str(len(self.text)))
        if len(self.text) < self.height:
            output.extend([self.style["EmptyText"]*self.width]
                          * (self.height - len(self.text)))
        if loggingEnabled:
            log.log("TextArea.draw (output)- "+str(output))
        return output
# Z: class Screen
# .d8888.  .o88b. d8888b. d88888b d88888b d8b   db
# 88'  YP d8P  Y8 88  `8D 88'     88'     888o  88
# `8bo.   8P      88oobY' 88ooooo 88ooooo 88V8o 88
#   `Y8b. 8b      88`8b   88~~~~~ 88~~~~~ 88 V8o88
# db   8D Y8b  d8 88 `88. 88.     88.     88  V888
# `8888Y'  `Y88P' 88   YD Y88888P Y88888P VP   V8P


class Screen():
    """ A screen object.
        Screen.background - a list of strings that is used with
                          | Screen.draw(window, forceRedrawMode)
                          | (Only with forceRedrawMode == "forcedBackground")

      """
    inDebug = False
    allowColor = True

    def getChar(self):
        """Stub method(returns ^C). The real one is defined by the constructor.
        Screen.getChar() returns a single character from STDIN"""
        return "\x03"

    def __init__(self, trapSIGWINCH=True):
        """Screen constructor. Defines Screen.getChar()
        Change trapSIGWINCH to False if you don't want to automaticly update
        the screen on window size change"""
        # self.getChar = self.getGetChar()
        try:
            self.size = os.get_terminal_size()
        except OSError:
            self.size = (80, 24)
        if trapSIGWINCH:
            signal.signal(signal.SIGWINCH, lambda signal, frame: self.redraw())
        self.windows = []
        self.background = []
        self.binds = []
        self.clearOnSIGWINCH = True
        self.redrawOnSIGWINCH = True
        self.disableCtrlBackslash = False
        try:
            import msvcrt

            def getChar():
                """Get a char from STDIN (using msvcrt)"""
                return msvcrt.getch()  # noqa: F821
            self.platform = "win"
            self.getChar = getChar
        except ImportError:
            self.platform = "linux"

            def getChar(forceBufferReading=False):
                """Get a char from STDIN (using tty, termios, sys)"""
                fd = sys.stdin.fileno()
                old = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    if forceBufferReading:
                        return sys.stdin.buffer.read(1)
                    try:
                        return sys.stdin.read(1)
                    except Exception:
                        return sys.stdin.buffer.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)
            self.getChar = getChar

    def redraw(self):
        self.size = os.get_terminal_size()
        if self.clearOnSIGWINCH:
            self.clear()
        for w in self.windows:
            if w.useRelativePos:
                w.recalcPos()
            else:
                w.handlers["SIGWINCH"](w, self)
            if self.redrawOnSIGWINCH:
                w.requiresRedrawing = True
                self.draw_no_redraw(w)

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
        if window.isDestroyed or window.hidden:
            return False
        a = window.draw()
        x = window.x
        y = window.y
        for i in range(len(a)):
            self.setChar(Formatting.format(a[i]), x, y+i)
        return True

    def draw(self, window=None, forceRedrawMode="clear"):
        """
        Redraw a window onto the screen with max priority
        forceRedrawMode can be (case insensitive):
            - "clear"             - Clears the screen before drawing on it
            - "forcedBackground"  - Doesn't clear the screen
                                  |  (uses Screen.background)
        """
        if forceRedrawMode.lower() == "clear":
            self.clear()
        # if forceRedrawMode.lower() == "oldasbackground":
        #     print("\033[s")
        elif forceRedrawMode.lower() == "forcedbackground":
            self.setScreen(self.background)
        else:
            raise InvalidStateError('forceRedrawMode can only be \'clear\' '
                                    'or \'forcedBackground\' '
                                    '(case insensitive)')
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
                    if not windows[i].lastDraw == "N/A" and \
                            not windows[i].requiresRedrawing:
                        self.setChar(Formatting.format(
                                     windows[i].lastDraw[line]),
                                     windows[i].x,
                                     windows[i].y+line)
                        # print("zzzzzzzzzzzzzzzz")
                    else:
                        self.draw_no_redraw(windows[i])
        if window is not None:
            self.draw_no_redraw(window)
        # if forceRedrawMode.lower() == "oldasbackground":
        #     print("\033[u")

    def setScreen(self, screen):
        """
        Set the screen to the list in the screen argument (a list of string)"""
        print('\033[2J\033[0;0H', end='', flush=True)
        y = self.size[1]
        for i in range(y):
            try:
                print(screen[i])
                # '\033[0;'+i+'H'+
            except Exception:
                pass
                # raise Exception("WARNING: List smaller than the screen")
        return

    def clear(self):
        """Clear the screen(print \\033[2J)"""
        print('\033[2J', end='', flush=True)

    def setChar(self, char, x, y, color="0"):
        """ color - color name (case insensitive)
            string with \\ as the first char will not be interpreted
            instead it will be used directly in the ANSI Escape sequence."""  # noqa
        if color[0] != "\\":
            color = Formatting.getColor(color)
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

    def loop(self, activeWindow, **kwargs):
        char = ""
        activeWin = activeWindow
        menuOpen = False
        menu = Menu("Tab menu")
        if loggingEnabled:
            log.defaultSource = 'loop'
            log.log('Screen.loop')
        while 1:
            char = self.getChar()
            if loggingEnabled:
                log.log(repr(char))
            press = {}
            if (char == "\r" or char == "\n") and menuOpen:
                windows = self.windows.copy()
                windows.reverse()
                windows.remove(activeWin)
                windows.insert(1, activeWin)
                activeWin = windows[menu.childopen]
                menu.hidden = True
                menuOpen = False

            if char == "\t":
                if not menuOpen:
                    windows = self.windows.copy()
                    windows.reverse()
                    windows.remove(activeWin)
                    windows.insert(1, activeWin)
                    self.size = os.get_terminal_size()
                    # Repostion the menu if the terminal resized.
                    menu.x = round(self.size[0]/2)
                    menu.y = round(self.size[1]/2)
                    children = []
                    for window in windows:
                        name = window.name if not len(window.name) > 30\
                            else window.name[:30]+"..."
                        children.append({"name": name})
                    menu.elements = [{"name": "Windows", "children": children}]
                    menu.open = 0
                    menu.childopen = 0
                    menu.hidden = False
                    self.draw(menu)
                    menuOpen = True
                    continue
                else:
                    if menu.open == 0:
                        windows = self.windows.copy()
                        windows.reverse()
                        windows.remove(activeWin)
                        windows.insert(1, activeWin)
                        activeWin = windows[0]
                    menu.hidden = True
                    menuOpen = False
            elif char == "\033":
                if menuOpen:
                    b = self.getChar()
                    if b == "[":
                        c = self.getChar()
                        if c == "A":  # ARROW_UP
                            if menu.childopen > 0:
                                menu.childopen -= 1
                        if c == "B":  # ARROW_DOWN
                            if menu.childopen < \
                                    len(menu.elements[0]["children"])-1:
                                menu.childopen += 1
                        if c == "F":  # END
                            menu.childopen = len(
                                menu.elements[0]["children"])-1
                        if c == "H":
                            menu.childopen = 0
                else:  # not menuOpen and char == '\033'
                    if loggingEnabled:
                        log.log('1112 Char: \\033; menuOpen = False')
                    b = self.getChar()
                    if loggingEnabled:
                        log.log('1114', repr(char), ' ', b)
                    if b == "[":
                        c = self.getChar()
                        if loggingEnabled:
                            log.log('1117', repr(char), ' ', b, ' ', c)
                        if c == 'A' or c == 'B' or c == 'C' or c == 'D':
                            activeWin.handlers["loop"](
                                KeyMap.decode('\033'+b+c))
                            if loggingEnabled:
                                log.log('1121',
                                        KeyMap.decode('\033'+b+c))
                        elif c == "M":
                            if loggingEnabled:
                                log.log('\\033[M')
                            t = self.getChar()
                            x = self.getChar()
                            y = self.getChar()
                            press = KeyMap.mouseClickDecode([t, x, y])
                            if self.inDebug:
                                print("press:", press)
                            for bind in self.binds:
                                if bind["keySeq"][0] != "\\M":
                                    if loggingEnabled:
                                        log.log("skipping: ", str(bind))
                                    continue
                                x_ok1 = press["x"] >= \
                                    bind["keySeq"][1]["xStart"]
                                x_ok2 = press["x"] <= \
                                    bind["keySeq"][1]["xEnd"]
                                x_ok = x_ok1 and x_ok2
                                # del x_ok1, x_ok2
                                y_ok1 = press["y"] >= \
                                    bind["keySeq"][1]["yStart"]
                                y_ok2 = press["y"] <= \
                                    bind["keySeq"][1]["yEnd"]
                                y_ok = y_ok1 and y_ok2
                                # del y_ok1, y_ok2
                                if loggingEnabled:
                                    log.log("x_ok1", x_ok1)
                                    log.log("x_ok2", x_ok2)
                                    log.log("x_ok", x_ok)

                                    log.log("y_ok1", y_ok1)
                                    log.log("y_ok2", y_ok2)
                                    log.log("y_ok", y_ok)

                                if x_ok and y_ok:

                                    o = bind["function"]({"eventType":
                                                          "mouseClick",
                                                          "eventSource":
                                                          "Screen.loop",
                                                          "click": press,
                                                          "bind": bind})
                                    if o == "END":
                                        return
                                    if self.inDebug:
                                        if loggingEnabled:
                                            log.log("called")
            elif char == "\x1c":
                if self.disableCtrlBackslash:
                    self.clear()
                    print(FormattedString(
                        "$(red)^\\ is disabled. Use SIGQUIT.$(reset)"))
                    print(FormattedString(
                        "$(rapid_blink)Press any key to resume$(reset)"))
                    self.getChar()
                else:
                    exit(0)
            elif char not in KeyMap.specialChars and not menuOpen:
                for bind in self.binds:
                    if bind["keySeq"] == char:
                        bind["function"]({"eventType": "keyPress",
                                          "eventSource": "Screen.loop",
                                          "bind": bind})
                        break
                if activeWin.handlers["loop"](char) == 'END':
                    return
            if not menuOpen:
                self.draw(activeWin)
            else:
                self.draw(menu)

    def bind(self, keySeq, function):
        """Bind a key to a function (Screen.loop())
        keySeq - Key to bind to ex. '\\t', 'q', '\\r'
        function - Function to bind ex. 'lambda event: exit(0)', some_func"""
        if keySeq is None:
            raise InvalidStateError("keySeq cannot be None\n"
                                    "Screen.bind(self, >keySeq...)")
        if function is None:
            raise InvalidStateError("The function cannot be None\n"
                                    "Screen.bind(self, keySeq, >function)")
        bind = {"keySeq": keySeq, "function": function}
        self.binds.append(bind)
        return bind

    def custom_input(self, prompt, handler=None):
        inputed = ""
        waiting = []
        inMouseMode = False
        while 1:
            if not inMouseMode:
                char = self.getChar()
            else:
                char = "x"+str(ord(self.getChar(True)))
            print("char: ", repr(char), "waiting: ", waiting, "imm",
                  inMouseMode)
            # Call self.getChar() forcing to output a string with the special
            # formatting
            # ex. "33"(ASCII !)
            # (required for mouse detection, since there is no char
            # staring with 0xFF in UTF-8)
            if char == "\x1c" or char == "x28":
                print("(Force exiting)")
                exit(0)
            if char == "\033":
                # print('033')
                b = self.getChar(True)
                if b == b"[":
                    # print('[')
                    c = self.getChar(True)
                    if c == b"M":
                        # print("M")
                        ptype = self.getChar(True)
                        x = self.getChar(True)
                        y = self.getChar(True)
                        etype = "UNKNOWN"
                        if ptype == b" ":
                            etype = "LMB_PRESS"
                        elif ptype == b"#":
                            etype = "UNPRESS"
                        elif ptype == b"0":
                            etype = "CTRL_LMB_PRESS"
                        elif ptype == b"3":
                            etype = "CTRL_UNPRESS"
                        print("event type: "+str(etype)+", x: "+str(ord(x)-33)
                              + ", y: "
                              + str(ord(y)-33),
                              end='\n', flush=True)
                        result = handler(eventType="Mouse",
                                         mousePress={"type": etype,
                                                     "x": ord(x)-33,
                                                     "y": ord(y)-33})
            elif char != b"\033":
                result = handler(eventType="CharInputEvent", char=char,
                                 self=self, string=inputed)
                if result[0].lower() == "ok":
                    inputed = inputed + char
                elif result[0].lower() == "end":
                    return inputed
                elif result[0].lower() == "cancel":
                    pass
                else:
                    raise InterruptedError(
                        result[0].lower()+" is not 'ok', 'end' or 'cancel'")
            elif char == "~":
                result = handler(eventType="KeyboardKey", char=waiting,
                                 self=self, string=inputed)
                if result[0].lower() == "set":
                    inputed = result[1]
                waiting = []
            else:
                waiting.append(char)

            # if len(waiting) > 10:
                # print("Ups Move Mode triggered")


# Z: InvalidStateError
class InvalidStateError(Exception):
    def __init__(self, message):
        self.message = message


# Z: Formatting
class Formatting():
    """This class contains:
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
      italic, underline(underline_off), slow_blink(blink_off),
      rapid_blink(blink_off), reverse(reverse_off),
      conceal(conceal_off/reveal), crossed_out(crossed_out_off)
    """
    fgcolors = {
        "black": "30", "red": "31", "green": "32", "yellow": "33",
        "blue": "34", "magenta": "35", "cyan": "36", "white": "37",
        "grey": "31;1",
        "gray": "30;1", "bright_red": "31;1", "bright_green": "32;1",
        "bright_yellow": "33;1", "bright_blue": "34;1",
        "bright_magenta": "35;1", "bright_cyan": "36;1",
        "bright_white": "37;1"  # If you think this makes no sense, you're
                                # right. This is here to provide a more white
                                # white, since some terminals treated white as
                                # gray
    }
    bgcolors = {
        "black": "40", "red": "41", "green": "42", "yellow": "43",
        "blue": "44", "magenta": "45", "cyan": "46", "white": "47",
        "gray": "100", "bright_red": "101", "bright_green": "102",
        "bright_yellow": "103",
        "bright_blue": "104", "bright_magenta": "105", "bright_cyan": "106",
        "bright_white": "107"  # Same as in foreground colors.
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

    @staticmethod
    def getColor(color, bg=False):
        """Return a color"""
        try:
            if bg:
                return Formatting.bgcolors[color]
            else:
                return Formatting.fgcolors[color]
        except Exception:
            return "0"

    @staticmethod
    def rgb(red, green, blue, background=False):
        if background:
            return "\033[48;2;"+str(red)+";"+str(green)+";"+str(blue)+"m"
        else:
            return "\033[38;2;"+str(red)+";"+str(green)+";"+str(blue)+"m"

    @staticmethod
    def format(string):
        """Format the STRING.
        ex.:
        $(COLOR) - This will be replaced with a foreground color
        $(b_COLOR) - But this will be replaced with a background color
        $(EFFECT) - And this will be replaced with a effect code"""
        if not Screen.allowColor:
            return re.sub(r"\$\([A-Za-z_0-9]*\)", "", string)
        for effect in Formatting.effects.keys():
            string = string.replace("$("+effect.lower()+")",
                                    "\033["+Formatting.effects[effect]+"m")
        for color in Formatting.bgcolors.keys():
            string = string.replace("$(b_"+color.lower()+")",
                                    "\033["
                                    + Formatting.bgcolors[color.lower()]+"m")
        for color in Formatting.fgcolors.keys():
            string = string.replace("$("+color.lower()+")",
                                    "\033["
                                    + Formatting.fgcolors[color.lower()]+"m")
        pat = re.compile(r'\$\(rgb([0-9]+);([0-9]+);([0-9]+)\)')
        string = re.sub(pat, "\033[38;2;\\1;\\2;\\3m", string)
        pat = re.compile(r'\$\(b_rgb([0-9]+);([0-9]+);([0-9]+)\)')
        string = re.sub(pat, "\033[48;2;\\1;\\2;\\3m", string)
        return string


class FormattedString(str):
    """A formatted string."""

    def __init__(self, string):
        """Init self."""
        self.allowColor = True
        self.string = Formatting.format(string)
        self.unformattedString = string
        self.noCodeString = re.sub(r"\$\([A-Za-z_0-9]*\)", "", string)

    def __len__(self):
        """."""
        return len(self.noCodeString)

    def __eq__(self, anotherString):
        """."""
        if isinstance(anotherString, FormattedString):
            return self.unformattedString == anotherString.unformattedString
        else:
            return self.noCodeString == anotherString

    def __str__(self):
        """-> self.string."""
        return self.string


# Z: consts -> KeyList
class KeyList():
    """ A List of keys."""
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


# Z: KeyMap
class KeyMap():
    """A keymap."""
    specialChars = ["\033", "\xe0", '\x00']

    @staticmethod
    def decode(keySeq):
        """."""
        keySeq = str(''.join(keySeq), 'ansi')
        if keySeq[0] == '\t':
            return KeyList.TAB
        if keySeq[0] == '\r':
            return KeyList.RETURN
        if keySeq[0] == '\xe0':
            # Arrow keys
            if keySeq[1] == 'H':
                return KeyList.ARROW_UP
            if keySeq[1] == 'P':
                return KeyList.ARROW_DOWN
            if keySeq[1] == 'K':
                return KeyList.ARROW_LEFT
            if keySeq[1] == 'M':
                return KeyList.ARROW_RIGHT

            # Special keys
            if keySeq[1] == 'R':
                return KeyList.INSERT
            if keySeq[1] == 'G':
                return KeyList.HOME
            if keySeq[1] == 'I':
                return KeyList.PAGE_UP
            if keySeq[1] == 'S':
                return KeyList.DELETE
            if keySeq[1] == 'O':
                return KeyList.END
            if keySeq[1] == 'Q':
                return KeyList.PAGE_DOWN
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
                    return KeyList.HOME
                if keySeq[-1] == 'A':
                    return KeyList.ARROW_UP
                if keySeq[-1] == 'B':
                    return KeyList.ARROW_DOWN
                if keySeq[-1] == 'D':
                    return KeyList.ARROW_LEFT
                if keySeq[-1] == "C":
                    return KeyList.ARROW_RIGHT
                if keySeq[2] == '2':
                    if keySeq[-1] == '~':
                        return KeyList.INSERT

    @staticmethod
    def mouseClickDecode(charSeq):
        """."""
        space = charSeq[0]
        x = charSeq[1]
        y = charSeq[2]
        code = format(ord(space), "=7b").replace(" ", "0")
        # code = code
        # print(code)
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
        if loggingEnabled:
            log.slog("KeyMap.mouseClickDecode", "bttn: ", str(bttn))
            log.slog("KeyMap.mouseClickDecode", "mod: ", str(modifiers))
            log.slog("KeyMap.mouseClickDecode", "X: ", str(etype["x"]))
            log.slog("KeyMap.mouseClickDecode", "Y: ", str(etype["y"]))
        return etype


# dupa.8
if __name__ == "__main__":
    s = Screen()
    w = Window("$(slow_blink)$(red)MMW for Python 3$(reset)")
    w.text = "$(green)[$(cyan)Do not adjust your TV$(green)]$(reset)"\
        "\nThis is $(red)not$(reset) a normal python program."\
        "\nThis is a library for creating ncurses-like windows"\
        "\nPress $(red)RETURN$(reset) to click this button and exit."\
        "\nOr you can press the $(red)LEFT ARROW$(reset) to select "\
        "the other button"
    w.x = 1
    w.y = 1
    w.buttons = ["$(cyan)Show me the docs$(reset)", "$(green)EXIT$(reset)"]
    w.styleOptions["ButtonAlignment"] = POS_CENTER
    w.selectedButton = 1
    s.add_window(w)
    w.useRelativePos = False
    w.draw()
    # w.recalcPos()

    s.draw(w)
    s.allowColor = True

    def endWinExit():
        w.selectedButton = 1
        return "END"

    def endWinDocs():
        w.selectedButton = 0
        return "END"
    s.bind(["\\M", {"xStart": 41, "xEnd": 49, "yStart": 7, "yEnd": 8}],
           endWinExit)
    s.bind(["\\M", {"xStart": 19, "xEnd": 39, "yStart": 7, "yEnd": 8}],
           endWinExit)
    s.loop(w)
    if w.selectedButton == 1:
        print(s.size)
        print(s.size[0]/2-w.width)
        print(s.size[1]/2-w.height)
        exit(0)
    else:
        help(__file__[:-3])
        w.name = "$(cyan)Info - mmw(py3)$(reset)"
        w.text = "$(b_bright_blue)$(bright_white)Type \"python3 -m pydoc"\
            "mmw3\" to see the documentation$(reset)"
        for key in w.style.keys():
            w.style[key] = "$(b_bright_blue)$(bright_white)"+w.style[key]
        w.style["CornerDownRight"] = w.style["CornerDownRight"]+"$(reset)"
        w.buttons = []
        w.selectedButton = -1
        w.requiresRedrawing = True
        s.draw()
        print()
        exit(0)
