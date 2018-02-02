#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys


def printList(list):
    for i in xrange(len(list)):
        print list[i]


def getDisplayLen(string):
    return len(string.replace("\xc5", "").replace("\xc4", "")
               .replace("\xc3", "").replace("\xc2", "").replace("\xc1", "")
               .replace("\xc0", "").replace("\xc6", "").replace("\xc7", "")
               .replace("\xc7", "").replace("\xc8", "").replace("\xc9", ""))


def longInput(prompt, end="empty"):
    string = ""
    while 1:
        try:
            a = raw_input(prompt)
        except:
            return string
        if a == "" and end.lower() == "empty":
            return string
        else:
            string = string + "\n" + a


class Window():
    def setButtonProfile(self, buttons=[]):
        self.buttons = buttons

    def destroy(self):
        if self.isDestroyed:
            raise Exception(self.name+": This window is already destoryed.")
        self.isDestroyed = True
        self.name = None
        self.x = None
        self.y = None
        self.forcedWidth = None
        self.forcedHeigth = None
        self.buttons = None
        self.selectedButton = None

    def __init__(self, name):
        self.name = name
        self.x = 0
        self.y = 0
        self.isDestroyed = False
        self.forcedWidth = 0
        self.forcedHeigth = 0
        self.buttons = []
        self.selectedButton = -1

    def setCoords(self, x, y):
        if self.isDestroyed:
            raise Exception(self.name+": This window is destoryed.")
        self.x = x
        self.y = y

    def setName(self, name):
        if self.isDestroyed:
            raise Exception(self.name+": This window is destoryed.")
        self.name = name

    def setProperty(self, property, value):
        if self.isDestroyed:
            raise Exception(self.name+": This window is destoryed.")
        if property in ["x", "y", "forcedWidth", "forcedHeigth", "name",
                        "text"]:
            exec("self."+property+" = value")

    def setText(self, text):
        if self.isDestroyed:
            raise Exception(self.name+": This window is destoryed.")
        self.text = text

    def draw(self):
        """Internal use; Use screen.draw(window); Returns a the window in """
        """string form"""
        if self.isDestroyed:
            raise Exception(self.name+": This window is destoryed.")
        width = 0
        w = 0
        if self.forcedWidth <= 0:
            if getDisplayLen(self.name) < getDisplayLen(self.text):
                width = getDisplayLen(self.text)
            elif getDisplayLen(self.name) > getDisplayLen(self.text):
                width = getDisplayLen(self.name)
            else:
                # When display len of self.text and self.name are equal
                width = getDisplayLen(self.name)
            w = width - getDisplayLen(self.name)
            # print "width "+str(width)
            # print "w "+str(w)
        else:
            w = self.forcedWidth
            width = self.forcedWidth + 1
        buttons = ""
        if self.buttons is not None:
            for i in xrange(len(self.buttons)):
                if self.selectedButton == i:
                    buttons = buttons + " [>"+self.buttons[i]+"<] "
                else:
                    buttons = buttons + " [ "+self.buttons[i]+" ] "
            if getDisplayLen(buttons) > width:
                width = getDisplayLen(buttons)
                w = width - getDisplayLen(self.name)
        w1 = w/2
        w2 = w1
        if w1*2 != w:
            w2 = w1+1
        # print w1, w2
        win = ["/"+"-"*w1+self.name+"-"*w2+"\\"]
        # print "win (st)"+repr(win)
        text = self.text.split("\n")
        # temp = 0
        # if self.forcedHeigth != -1:
        #    # temp = self.forcedHeigth - len(text)
        # else:
        #    # temp = len(text)
        # print "temp "+str(temp)
        # print "text "+str(text)
        for i in xrange(len(text)):
            # print "aaa"
            diff = 0
            # try:  # if True:
            # print i
            temptext = text[i]

            # except:
            #    # temptext = ""
            # if temptext.replace(" ", "") == "":
            #     # and not self.forcedHeigth <= i:
            #     continue
            if getDisplayLen(temptext) < width:
                diff = (width) - getDisplayLen(temptext)
                # print "@ line "+str(i)+" diff "+repr(diff)
                temptext = temptext + " "*diff
            win.append("|"+temptext+"|")
            # print "zzz"
        if self.forcedHeigth != -1:
            win.append("|"+" "*(width)+"|")
            # print "aaaa"
        if buttons != [] and buttons != "":
            w = width - getDisplayLen(buttons)
            w1 = w/2
            w2 = w1
            if w % 2 != 0:
                w2 = w1+1
            win.append("|"+(w1*" ")+buttons+(w2*" ")+"|")
        win.append("\\"+"-"*width+"/")
        # print "win en"+repr(win)
        return win


class Screen():
    hide = "\033[8m"
    unhide = "\033[28m"
    try:
        import msvcrt

        def getChar(self):
            return msvcrt.getch()  # noqa: F821
        platform = "win"
    except ImportError:
        def getChar(self):
            import sys
            import tty  # noqa
            import termios  # noqa
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                return sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
            self.platform = "linux"

    def __init__(self, size=[80, 24]):
        self.size = size
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

    def draw(self, window):
        a = window.draw()
        x = window.x
        y = window.y
        for i in xrange(len(a)):
            self.setChar(a[i], x, y+i)

    def setScreen(self, screen):
        sys.stdout.write('\033[2J\033[0;0H')
        y = self.size[1]
        for i in xrange(y):
            try:
                print screen[i]
                # '\033[0;'+i+'H'+
            except:
                raise Exception("WARNING: List smaller than the screen")
        return

    def clear(self):
        print '\033[2J',

    def getColor(self, color, bg=False):
        if bg:
            colors = self.bgcolors
        else:
            colors = self.fgcolors
        if color not in colors[0]:
            return
        for i in xrange(len(colors[0])):
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
        print '\033['+str(y)+';'+str(x)+'H\033['+str(color)+'m'+char,

    def hidden_input(self, input="", call=None):
        # print self.hide,
        a = self.getChar()
        action = ""
        if a == "\r":
            return input
        elif a == "\x7f":  # Backspace
            oldinput = input
            input = input[:-1]
            if call is not None:
                action = call("backspace", input, oldinput)
            if action != "accept":
                input = oldinput
            return self.hidden_input(input, call)
        else:
            oldinput = input
            input = input + a
            if call is not None:
                action = call(a, input, oldinput)
            if action != "accept" and action != "accept-end":
                input = oldinput
            if action == "accept-end":
                return input
            if action == "end":
                return oldinput
            return self.hidden_input(input, call)


# if __name__ == "__main__":
#     s = Screen()
#     s.clear()
#     w = Window("Mały test")
#     w.setText("xDDDDDDDDDDDD\nlololo")
#     w.y = 10
#     w.x = 5
#     w.forcedWidth = 0
#     w.forcedHeigth = 10
#     w.buttons = []
#     w.selectedButton = -1
#     s.draw(w)
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
