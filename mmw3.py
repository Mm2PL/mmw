#!/usr/bin/python
# -*- coding: utf-8 -*-
# Name: Maciek's aMazing Windows
# Author: Maciek
import sys


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


lastid = 0


class Window():
    # def setButtonProfile(self, buttons=[]):
    #     self.buttons = buttons

    def destroy(self):
        if self.isDestroyed:
            raise RuntimeError(self.name+": This window is already destoryed.")
        self.isDestroyed = True
        self.text = None
        self.x = None
        self.y = None
        self.forcedWidth = None
        self.forcedHeigth = None
        self.buttons = None
        self.selectedButton = None

    def __init__(self, name):
        self.name = name
        self.text = ""
        self.x = 0
        self.y = 0
        self.isDestroyed = False
        self.forcedWidth = 0
        self.forcedHeigth = 0
        self.buttons = []
        self.selectedButton = -1
        self.autoWindowResize = True
        # True - expand the window to the texts size,
        # False - Don't expand
        self.parent = None
        self.handlers = {"loop": self.buttonSelectorHandler}
        global lastid
        self.id = lastid + 1
        lastid = lastid + 1
        self.priority = 0
        self.lastDraw = "N/A"
        self.area = {"x": 0, "y": 0}
    # def setCoords(self, x, y):
    #     if self.isDestroyed:
    #         raise RuntimeError(self.name+": This window is destoryed.")
    #     self.x = x
    #     self.y = y
    #
    # def setName(self, name):
    #     if self.isDestroyed:
    #         raise RuntimeError(self.name+": This window is destoryed.")
    #     self.name = name
    #
    # def setProperty(self, property, value):
    #     if self.isDestroyed:
    #         raise RuntimeError(self.name+": This window is destoryed.")
    #     if property in ["x", "y", "forcedWidth", "forcedHeigth", "name",
    #                     "text"]:
    #         exec("self."+property+" = value")
    #
    # def setText(self, text):
    #     if self.isDestroyed:
    #         raise RuntimeError(self.name+": This window is destoryed.")
    #     self.text = text

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
        if self.isDestroyed:
            raise RuntimeError(self.name+": This window is destoryed.")
        width = 0
        # w = 0
        text = self.text
        buttons = ""
        if self.buttons is not None:
            for i in range(len(self.buttons)):
                if self.selectedButton == i:
                    buttons = buttons + " [>"+self.buttons[i]+"<] "
                else:
                    buttons = buttons + " [ "+self.buttons[i]+" ] "
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
            # if getDisplayLen(self.name) < getDisplayLen(self.text):
            #     width = getDisplayLen(self.text)
            # elif getDisplayLen(self.name) > getDisplayLen(self.text):
            #     width = getDisplayLen(self.name)
            # else:
            #     # When display len of self.text and self.name are equal
            #     width = getDisplayLen(self.name)
            # w = width - getDisplayLen(self.name)
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
        win = ["/"+("-"*spl)+self.name+("-"*spr)+"\\"]
        text = text.split("\n")
        for i in range(len(text)):
            diff = 0
            temptext = text[i]
            if getDisplayLen(temptext) < width:
                diff = (width) - getDisplayLen(temptext)
                # print "@ line "+str(i)+" diff "+repr(diff
                temptext = temptext + " "*diff
            win.append("|"+temptext+"|")
            # print "zzz"
        if self.forcedHeigth != -1:
            win.append("|"+" "*(width)+"|")
            # print "aaaa"
        if buttons != [] and buttons != "":
            # w = width - len(buttons)
            spl = round((width - len(buttons))/2)
            spr = width - (spl+len(buttons))
            # w1 = round(w/2)
            # w2 = w1
            # if w % 2 != 0:
            #     w2 = w1+1
            win.append("|"+(spl*" ")+buttons+(spr*" ")+"|")
        win.append("\\"+"-"*width+"/")
        self.lastDraw = win
        self.area["x"] = len(win[0])
        self.area["y"] = len(win)-1
        # print(win)
        return win


class Screen():
    hide = "\033[8m"
    unhide = "\033[28m"

    def getGetChar(self):
        pass  # Windows compatibility
    try:
        import msvcrt

        def getChar(self):
            return msvcrt.getch()  # noqa: F821
        platform = "win"
    except ImportError:
        def getGetChar(self):  # noqa F811
            self.sys  = __import__("sys")  # noqa
            self.tty  = __import__("tty")  # noqa
            self.termios = __import__("termios")  # noqa

            def getChar():
                fd = sys.stdin.fileno()
                old = self.termios.tcgetattr(fd)
                try:
                    self.tty.setraw(fd)
                    return sys.stdin.read(1)
                finally:
                    self.termios.tcsetattr(fd, self.termios.TCSADRAIN, old)
                self.platform = "linux"
            return getChar

    def __init__(self, size=[80, 24]):
        self.getChar = self.getGetChar()
        self.size = size
        self.windows = []
        self.fgcolors = [
            [
                "black",
                "red",
                "green",
                "yellow",
                "blue",
                "magenta",
                "cyan",
                "white",
                "gray",
                "bred",
                "bgreen",
                "byellow",
                "bblue",
                "bmagenta",
                "bcyan",
                "bwhite",
                "zero",
                "0"
            ],
            [
                "30",  # black
                "31",  # red
                "32",  # green
                "33",   # yellow
                "34",  # blue
                "35",  # magenta
                "36",  # cyan
                "37",  # white
                "30;1",  # bright colors v same order as ^
                "31;1",
                "32;1",
                "33;1",
                "34;1",
                "35;1",
                "36;1",
                "37;1",
                "0",
                "0"
            ]
        ]
        self.bgcolors = [
            [
                "black",
                "red",
                "green",
                "yellow",
                "blue",
                "magenta",
                "cyan",
                "white",
                "gray",
                "bred",
                "bgreen",
                "byellow",
                "bblue",
                "bmagenta",
                "bcyan",
                "bwhite",
                "zero",
                "0"
            ],
            [
                "40",
                "41",
                "42",
                "43",
                "44",
                "45",
                "46",
                "47",
                "100",
                "101",
                "102",
                "103",
                "104",
                "105",
                "106",
                "107",
                "0",
                "0"
            ]
        ]

    def setCur(self, x, y, doReturn=False):
        if doReturn is False:
            sys.stdout.write('\033['+str(y)+';'+str(x)+'H')
        else:
            return '\033['+str(y)+';'+str(x)+'H'

    def draw_no_redraw(self, window):
        """Drow a window onto the screen without redrawing other windows"""
        a = window.draw()
        x = window.x
        y = window.y
        for i in range(len(a)):
            self.setChar(a[i], x, y+i)

    def draw(self, window=None):
        """Redraw a window onto the screen with max priority"""
        windows = sorted(self.windows,
                         key=lambda window: window.priority,
                         reverse=False)
        # self.clear()
        for i in range(len(windows)):
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
    # def re_draw(self, windowToUpdate):
    #     windows = sorted(self.windows, key=lambda window: window.priority,
    #                      reverse=True)
    #     x = windowToUpdate.x
    #     y = windowToUpdate.y
    #     toX = windowToUpdate.area["x"] + x
    #     toY = windowToUpdate.area["y"] + y
    #     for window in windows:
    #         if(window.x > x and window.x < toX) and \
    #                 (window.y > y and window.y < toY):
    #             toDraw.append(window.draw())

    def setScreen(self, screen):
        sys.stdout.write('\033[2J\033[0;0H')
        y = self.size[1]
        for i in range(y):
            try:
                print(screen[i])
                # '\033[0;'+i+'H'+
            except Exception as e:
                raise Exception("WARNING: List smaller than the screen")
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
    import argparse
    p = argparse.ArgumentParser(description='Generate a window')
    p.add_argument("-n", "--name", dest='name')
    p.add_argument("-t", "--text", dest='text')
    p.add_argument("-b", "--buttons", dest='buttons')
    p.add_argument('-x', '--posX', dest='x')
    p.add_argument('-y', '--posY', dest='y')
    p.add_argument('-fh', '--forcedHeigth', dest='fh')
    p.add_argument('-fw', '--forcedWidth', dest='fw')
    p.add_argument('-sb', '--selectedButton', dest='sb')
    args = p.parse_args()
    s = Screen()

    s.clear()
    # s.setChar("Args: "+str(args), 0, 20, color="red")
    # nazwa = "a"  # raw_input("nazwa>")
    window = Window(args.name)  # "TEST!!")  #
    window.setText(args.text.replace("\\n", "\n"))  # "1\n2\n3\n4\n5\n6"
    # args.text.replace("\\n", "\n"))
    # longInput("tekst(ctrl+c, lub puste kończy)>"))
    window.y = int(args.x)  # 1  #
    window.x = int(args.y)  # 1  #
    window.forcedHeigth = int(args.fh)  # -1  #
    window.forcedWidth = int(args.fw)  # -1  #
    window.buttons = args.buttons.split(",")  # ["OK", "Nie OK"]  #
    window.selectedButton = int(args.sb)   # \-1  #
    s.draw(window)
    # # s.setChar("======Screen Test======", 0, 0, color="red")
