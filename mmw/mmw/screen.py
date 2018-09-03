import mmw
import typing
# from .errors import InvalidStateError  # noqa: E402
# from .formattedstring import FormattedString  # noqa: E402
# from .decoding import decode, mouseClickDecode, specialChars  # noqa: E402
# from .menu import Menu  # noqa: E402
# from .mmw.formatting import mmw.formatting  # noqa: E402
import os
import signal
import sys
try:
    # Linux
    import termios
    import tty
except ImportError:
    pass


inDebug = False
allowColor = True


class Screen():
    """ A screen object.
        Screen.background - a list of strings that is used with
                          | Screen.draw(window, forceRedrawMode)
                          | (Only with forceRedrawMode == "forcedBackground")

      """

    def getChar(self):
        """Stub method(returns ^C \\x03).
        The real method is defined by the constructor.
        Screen.getChar() returns a single character from STDIN"""
        return "\x03"

    def __init__(self, trapSIGWINCH=True):
        """Screen constructor. Defines Screen.getChar()
        Change trapSIGWINCH to False if you don't want to automaticly update
        the screen on window size change"""
        try:
            import msvcrt

            def getChar(notUsed=False):
                """Get a char from STDIN (using msvcrt)"""
                char = msvcrt.getch()
                if char == '\x1c' and self._lastchar != '\x1c':
                    self.forcefulExit()
                self._lastchar = str(char)
                return char
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
                    char = '==N/A=='
                    if forceBufferReading:
                        char = sys.stdin.buffer.read(1)
                    else:
                        try:
                            char = sys.stdin.read(1)
                        except Exception:
                            char = sys.stdin.buffer.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)
                    if char == '\x1c' and self._lastchar != '\x1c':
                        # print(repr(char), repr(self._lastchar))
                        # input('[DBG]>>>')
                        self.forcefulExit()
                    self._lastchar = str(char)
                    return char
            self.getChar = getChar
        # if self.platform == 'linux':
        #     tty.setcbreak(sys.stdin)
        try:
            self.size = os.get_terminal_size()
        except OSError:
            self.size = (80, 24)
        if trapSIGWINCH and self.platform != 'win':
            signal.signal(signal.SIGWINCH, lambda signal, frame: self.redraw())
        self.windows = []
        self.background = []
        self.binds = []
        self._lastchar = '==N/A=='
        self.clearOnSIGWINCH = True
        self.redrawOnSIGWINCH = True
        self.disableCtrlBackslash = False
        self.bind('\x1c', self.forcefulExit)
        self.oldframe = None

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

    def setCur(self, x: int, y: int, returnTheEscape=False):
        """Move the cursor the x and y.
        Return the ANSI Escape, if returnTheEscape is True"""
        if returnTheEscape:
            return '\033['+str(y)+';'+str(x)+'H'
        else:
            print('\033['+str(y)+';'+str(x)+'H', end='', flush=True)

    def draw_no_redraw(self, window: mmw.Drawable):
        """Draw a window onto the screen without redrawing other windows.
        Returns True if window was drawn, False otherwise."""
        if window.isDestroyed or window.hidden:
            return False
        a = window.draw()
        x = window.x
        y = window.y
        for i in range(len(a)):
            self.setChar(mmw.formatting.format(a[i]), x, y+i)
        return True

    def draw(self, window: mmw.Drawable=None):
        """
        Redraw a window onto the screen with max priority
        """
        # self.clear()
        canvas = []
        for y in range(self.size[1]):
            canvas.append([' ']*self.size[0])
        # canvas = [['']*self.size[0]]*self.size[1]
        windows = sorted(self.windows,
                         key=lambda window: window.priority,
                         reverse=False)
        if window is not None:
            windows.append(window)
        for w in windows:
            if w.hidden:
                continue
            draw = ['']
            if w.requiresRedrawing:
                draw = w.draw()
            else:
                draw = w.lastDraw
                if draw == 'N/A':
                    #      ^~~~~ Default value, window has not been drawn
                    #            before
                    draw = w.draw()
            # print(draw)
            # input('.')
            for y, yelem in enumerate(draw):
                for x, xelem in enumerate(yelem):
                    # print(xelem)
                    try:
                        canvas[y+w.y][x+w.x] = xelem
                    except IndexError:
                        continue
            # print(canvas)
            # input('.2')
        canvas.reverse()
        for i in canvas.copy():
            if ''.join(i).isspace():
                canvas.remove(i)
                continue
            break
            # print(i)
        canvas.reverse()

        print(self.setCur(0, 0, True), end='', flush=True)
        # emptyline = ['']*self.size[0]
        # lastNonEmptyLine = -1
        for y, yelem in enumerate(canvas):
            # if yelem == emptyline:
            #     continue
            line = ''.join(yelem)
            print('\033[2K', line, sep='', end='\n')
            # lastNonEmptyLine = int(y)
            # for x, xelem in enumerate(yelem):
            #     if xelem == '':
            #         continue
            #     print(xelem, end='')
        # print()

        if self.oldframe is not None:
            # print(len(self.oldframe), len(canvas))
            # input('.')
            for i in range(len(self.oldframe) - len(canvas)+1):
                print('\033[2K')
        # print()
        self.oldframe = canvas
        # return canvas
        # ------------------------------------
        # if forceRedrawMode.lower() == "clear":
        #     self.clear()
        # # elif forceRedrawMode.lower() == "oldasbackground":
        # #     self.setCur(0, 0)
        # elif forceRedrawMode.lower() == "forcedbackground":
        #     self.setScreen(self.background)
        # else:
        #     raise mmw.errors.InvalidStateError('forceRedrawMode can only be '
        #                                        '\'clear\' '
        #                                        'or \'forcedBackground\' '
        #                                        '(case insensitive)')
        # windows = sorted(self.windows,
        #                  key=lambda window: window.priority,
        #                  reverse=False)
        # # self.clear()
        # for i in range(len(windows)):
        #     if windows[i].isDestroyed:
        #         continue
        #     if windows[i] is not None:
        #         if window is not None:
        #             if windows[i].id == window.id:
        #                 continue
        #         if windows[i].requiresRedrawing:
        #             if windows[i].lastDraw != "N/A":
        #                 for a in windows[i].lastDraw:
        #                     self.setChar(mmw.format(a),
        #                                  windows[i].x,
        #                                  windows[i].y)
        #             else:
        #                 self.draw_no_redraw(windows[i])
        #         # else:
        #         #     self.draw_no_redraw(windows[i])
        # if window is not None:
        #     self.draw_no_redraw(window)
        # # if forceRedrawMode.lower() == "oldasbackground":
        # #     print("\033[u")

    def setScreen(self, screen: typing.List[str]):
        """
        Set the screen to the list in the screen argument""" \
        + """(a list of strings)"""
        print('\033[0;0H', end='', flush=True)
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

    def setChar(self, string: str, x: int, y: int, flush: bool=True):
        """prints \\033[{y};{x}H{STRING}"""
        print('\033['+str(y)+';'+str(x)+'H'+str(string),
              end='', flush=flush)

    def add_window(self, window: mmw.Drawable, setParent: bool=True):
        """Add the window the the screen
        The window will be drawn unless window.hidden is True."""
        self.windows.append(window)
        if setParent:
            window.parent = self

    def loop(self, activeWindow: mmw.Drawable):
        char = ""
        activeWin = activeWindow
        menuOpen = False
        tabmenu = mmw.menu.Menu("Tab menu")
        # if loggingEnabled:
        #     log.defaultSource = 'loop'
        #     log.log('Screen.loop')
        while 1:
            char = self.getChar()
            # if loggingEnabled:
            #     log.log(repr(char))
            press = {}
            if (char == "\r" or char == "\n") and menuOpen:
                windows = self.windows.copy()
                windows.reverse()
                windows.remove(activeWin)
                windows.insert(1, activeWin)
                activeWin = windows[tabmenu.childopen]
                tabmenu.hidden = True
                menuOpen = False

            if char == "\t":
                if not menuOpen:
                    windows = self.windows.copy()
                    windows.reverse()
                    windows.remove(activeWin)
                    windows.insert(1, activeWin)
                    self.size = os.get_terminal_size()
                    # Repostion the menu if the terminal resized.
                    tabmenu.x = round(self.size[0]/2)
                    tabmenu.y = round(self.size[1]/2)
                    children = []
                    for window in windows:
                        name = window.name if not len(window.name) > 30\
                            else window.name[:30]+"..."
                        children.append({"name": name})
                    tabmenu.elements = [
                        {"name": "Windows", "children": children}]
                    tabmenu.open = 0
                    tabmenu.childopen = 0
                    tabmenu.hidden = False
                    self.draw(tabmenu)
                    menuOpen = True
                    continue
                else:
                    if tabmenu.open == 0:
                        windows = self.windows.copy()
                        windows.reverse()
                        windows.remove(activeWin)
                        windows.insert(1, activeWin)
                        activeWin = windows[0]
                    tabmenu.hidden = True
                    menuOpen = False
            elif char == "\033":
                if menuOpen:
                    b = self.getChar()
                    if b == "[":
                        c = self.getChar()
                        if c == "A":  # ARROW_UP
                            if tabmenu.childopen > 0:
                                tabmenu.childopen -= 1
                        if c == "B":  # ARROW_DOWN
                            if tabmenu.childopen < \
                                    len(tabmenu.elements[0]["children"])-1:
                                tabmenu.childopen += 1
                        if c == "F":  # END
                            tabmenu.childopen = len(
                                tabmenu.elements[0]["children"])-1
                        if c == "H":
                            tabmenu.childopen = 0
                else:  # not menuOpen and char == '\033'
                    # if loggingEnabled:
                    #     log.log('1112 Char: \\033; menuOpen = False')
                    b = self.getChar()
                    # if loggingEnabled:
                    #     log.log('1114', repr(char), ' ', b)
                    if b == "[":
                        c = self.getChar()
                        # if loggingEnabled:
                        #     log.log('1117', repr(char), ' ', b, ' ', c)
                        if c == 'A' or c == 'B' or c == 'C' or c == 'D':
                            activeWin.handlers["loop"](
                                mmw.decoding.decode('\033'+b+c))
                            # if loggingEnabled:
                            #     log.log('1121',
                            #             KeyMap.decode('\033'+b+c))
                        elif c == "M":
                            # if loggingEnabled:
                            #     log.log('\\033[M')
                            t = self.getChar()
                            x = self.getChar()
                            y = self.getChar()
                            press = mmw.decoding.mouseClickDecode([t, x, y])
                            if self.inDebug:
                                print("press:", press)
                            for bind in self.binds:
                                if bind["keySeq"][0] != "\\M":
                                    # if loggingEnabled:
                                    #     log.log("skipping: ", str(bind))
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
                                # if loggingEnabled:
                                #     log.log("x_ok1", x_ok1)
                                #     log.log("x_ok2", x_ok2)
                                #     log.log("x_ok", x_ok)
                                #
                                #     log.log("y_ok1", y_ok1)
                                #     log.log("y_ok2", y_ok2)
                                #     log.log("y_ok", y_ok)

                                if x_ok and y_ok:

                                    o = bind["function"]({"eventType":
                                                          "mouseClick",
                                                          "eventSource":
                                                          "Screen.loop",
                                                          "click": press,
                                                          "bind": bind})
                                    if o == "END":
                                        return
                                    # if self.inDebug:
                                        # if loggingEnabled:
                                        #     log.log("called")
            elif char not in mmw.specialChars and not menuOpen:
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
                self.draw(tabmenu)

    def forcefulExit(self, event=None):
        """This function is triggered on ^\\.
        Displays a window asking if the user realy wants to quit."""
        w = mmw.Window('^\\')
        w.text = 'Are you sure you want to quit\n' \
            + '[Enter] Accept\n' \
            + '[1], [2], [3] Select'
        w.buttons = ['[1] No', "[2] Yes, use os.kill()", '[3] Yes, use exit()']
        w.selectedButton = 0
        w.parent = self
        w.xRel = mmw.POS_CENTER
        w.yRel = mmw.POS_CENTER
        w.useRelativePos = True
        self.clear()
        while 1:
            self.draw_no_redraw(w)
            char = self.getChar()
            if char == '\x1c':
                w.selectedButton = 1
                break
            if char in ['1', '2', '3', '4']:
                w.selectedButton = int(char)-1
            if char == '\n' or char == '\r':
                break
        if w.selectedButton == 0:
            self.draw()
            return
        if w.selectedButton == 1:
            pid = os.getpid()
            print('\n[Screen/forcefulExit()] Killing pid:', pid)
            if self.platform == 'win':
                os.kill(pid, signal.CTRL_BREAK_EVENT)
            else:
                os.kill(pid, signal.SIGKILL)
        if w.selectedButton == 2:
            print('\n[Screen/forcefulExit()] Calling exit()')
            exit()
        if w.selectedButton == 3:
            self.draw()
            ###
            import pdb
            pdb.set_trace()
            ###
            return

    def bind(self, keySeq, function):
        """Bind a key to a function (Screen.loop())
        keySeq - Key to bind to ex. '\\t', 'D', '\\r'
            # WARNING: There is one Exception:
            ['\\M', {'xStart': int, 'xEnd': int,
                     'yStart': int, 'yEnd': int}]
        function - Function to bind ex. 'lambda event: exit(0)', some_func"""
        if keySeq is None:
            raise mmw.InvalidStateError("keySeq cannot be None\n"
                                        "Screen.bind(self, >keySeq...)")
        if function is None:
            raise mmw.InvalidStateError("The function cannot be None\n"
                                        "Screen.bind(self, keySeq, >function)")
        bind = {"keySeq": keySeq, "function": function}
        self.binds.append(bind)
        return bind
# def custom_input(self, prompt, handler=None):
#     inputed = ""
#     waiting = []
#     inMouseMode = False
#     while 1:
#         if not inMouseMode:
#             char = self.getChar()
#         else:
#             char = "x"+str(ord(self.getChar(True)))
#         print("char: ", repr(char), "waiting: ", waiting, "imm",
#               inMouseMode)
#         # Call self.getChar() forcing to output a string with the special
#         # mmw.formatting
#         # ex. "33"(ASCII !)
#         # (required for mouse detection, since there is no char
#         # staring with 0xFF in UTF-8)
#         if char == "\x1c" or char == "x28":
#             print("(Force exiting)")
#             exit(0)
#         if char == "\033":
#             # print('033')
#             b = self.getChar(True)
#             if b == b"[":
#                 # print('[')
#                 c = self.getChar(True)
#                 if c == b"M":
#                     # print("M")
#                     ptype = self.getChar(True)
#                     x = self.getChar(True)
#                     y = self.getChar(True)
#                     etype = "UNKNOWN"
#                     if ptype == b" ":
#                         etype = "LMB_PRESS"
#                     elif ptype == b"#":
#                         etype = "UNPRESS"
#                     elif ptype == b"0":
#                         etype = "CTRL_LMB_PRESS"
#                     elif ptype == b"3":
#                         etype = "CTRL_UNPRESS"
#                     print("event type: "+str(etype)+", x: "+str(ord(x)-33)
#                           + ", y: "
#                           + str(ord(y)-33),
#                           end='\n', flush=True)
#                     result = handler(eventType="Mouse",
#                                      mousePress={"type": etype,
#                                                  "x": ord(x)-33,
#                                                  "y": ord(y)-33})
#         elif char != b"\033":
#             result = handler(eventType="CharInputEvent", char=char,
#                              self=self, string=inputed)
#             if result[0].lower() == "ok":
#                 inputed = inputed + char
#             elif result[0].lower() == "end":
#                 return inputed
#             elif result[0].lower() == "cancel":
#                 pass
#             else:
#                 raise InterruptedError(
#                     result[0].lower()+" is not 'ok', 'end' or 'cancel'")
#         elif char == "~":
#             result = handler(eventType="KeyboardKey", char=waiting,
#                              self=self, string=inputed)
#             if result[0].lower() == "set":
#                 inputed = result[1]
#             waiting = []
#         else:
#             waiting.append(char)
