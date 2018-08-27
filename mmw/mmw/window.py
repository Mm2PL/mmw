import mmw
import typing
# import consts
# import drawable
# import errors
# import styles
# from .styles import Styles
import re


class Window(mmw.Drawable):
    """a window class
    attributes (own):
        text (default = "")
        buttons (default = [])
        selectedButton (default = -1)
        handlers (default = {"loop": self.buttonSelectorHandler})
        style (default = styles.DEFAULT)
         *check mmw.styles for more info
    """
    def __repr__(self):
        if self.useRelativePos:
            return 'mmw.Window(name={}) at ({}/{}, {}/{})'.format(
                repr(self.name), self.xRel, self.x, self.yRel, self.y)
        else:
            return 'mmw.Window(name={}) at ({}, {})'.format(
                repr(self.name), self.x, self.y)

    def destroy(self, destroyChild=False):
        """Destroy the window"""
        super().destroy(destroyChild)
        self.isDestroyed = True
        self.text = None
        self.buttons = None
        self.selectedButton = None

    def __init__(self, name: str):
        super().__init__(name)
        self.text = ""
        self.buttons = []
        self.widgets = {}
        self.selectedButton = -1
        self.handlers["loop"] = self.buttonSelectorHandler
        self.handlers["SIGWINCH"] = lambda a, b: None
        # True - expand the window to the texts size,
        # False - Don't expand

        self.style = mmw.styles.DEFAULT
        self.styleOptions = {"ButtonAlignment": "N/A"}

    def loop(self):
        """Run self.handlers["loop"] unless it
returns something that is not "OK" """
        while 1:
            if self.parent is None:
                raise mmw.errors.InvalidStateError("Window Parent is None")
            self.parent.draw(self, "clear")
            print()
            seq = []
            char = self.parent.getChar()
            seq.append(char)
            if char == '\x1b':
                exit()
            if char == '\033':
                char = self.parent.getChar()
                seq.append(char)
                if char == '[':
                    char = self.parent.getChar()
                    seq.append(char)
            a = self.handlers["loop"](mmw.decode(seq))
            if a != "OK":
                break

    def buttonSelectorHandler(self, char: str) -> str:
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
        if char == "\r":
            return "END"
        return "OK"
        # a = input()

    def draw(self) -> typing.List[str]:
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
            if self.autoResize:
                for i in range(len(temp)):
                    if len(temp[i]) > width:
                        width = len(temp[i])
                if len(self.name) > width:
                    width = len(self.name)
            else:
                raise mmw.errors.InvalidStateError("forcedWidth is required, "
                                                   "if text wrap is on.")
        else:
            if self.autoResize:
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

        visname = self.name
        spl = round((width - len(visname))/2)
        spr = width - (spl+len(visname))
        win = [self.style["CornerUpLeft"]
               + (self.style["TitleFiller"]*spl)
               + str(self.name)
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
                        mmw.consts.POS_LEFT:
                    fillerL = " "
                    fillerR = self.style["TextFiller"]\
                        * (width - len(visbuttons) - 1)
                elif self.styleOptions["ButtonAlignment"] == \
                        mmw.consts.POS_RIGHT:
                    fillerL = self.style["TextFiller"]\
                        * (width - len(visbuttons) - 1)
                    fillerR = " "
                elif self.styleOptions["ButtonAlignment"] == \
                        mmw.consts.POS_CENTER:
                    pass
                else:
                    raise mmw.errors.InvalidStateError(
                        "ButtonAlignment can only be mmw.POS_RIGHT "
                        "or POS_LEFT or POS_CENTER.")

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
