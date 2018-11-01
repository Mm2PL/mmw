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
    import msvcrt


allowColor = True


class Screen():
    """ A screen object.
    """

    def apply_options(self):
        for k in self.options:
            print('\033[?'+str(mmw.SO_OPTIONS[k])
                  + ('h' if self.options[k] else 'l'), end='')

    def get_char(self, force_buffer_reading=False):
        """Return a single character from STDIN
        Arguments:
          force_buffer_reading (default False) -- force reading the buffer.
                                                  Unused on Windows.
        """
        if os.name == 'posix':  # Linux
            return self._get_char_linux(force_buffer_reading)
        else:
            return self._get_char_windows()

    def _get_char_windows(self):
        """Return a signgle character from STDIN (using msvcrt)
        WARNING: Do NOT use this method on Linux, it WILL crash.
        """
        char = msvcrt.getch()  # I said do NOT run this on Linux.
        if char == '\x1c' and self._lastchar != '\x1c':
            self.forcefulExit()
        self._lastchar = str(char)
        return char

    def _get_char_linux(self, force_buffer_reading=False):
        """Get a char from STDIN (using tty, termios, sys)"""
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            char = '==N/A=='
            if force_buffer_reading:
                char = sys.stdin.buffer.read(1)
            else:
                try:
                    char = sys.stdin.read(1)
                except IOError:
                    char = sys.stdin.buffer.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
            if char == '\x1c' and self._lastchar != '\x1c':
                self.forcefulExit()
            self._lastchar = str(char)
            return char

    def __init__(self, trapSIGWINCH=True):
        """Screen constructor. Define Screen.get_char()
        Arguments:
          trapSIGWINCH (default True) -- make changing the window size
                                         redefine self.size
        """
        # Deprecated;
        # This is here for backwards compatibility.

        try:
            self.size = os.get_terminal_size()
        except OSError:
            self.size = (80, 24)
        if trapSIGWINCH and os.name != 'nt':
            signal.signal(signal.SIGWINCH,
                          lambda signal, frame: self._redraw())
        self.windows = []
        self.background = []
        self.binds = []
        self.options = mmw.Screen_Options(mmw.SO_DEFAULTS)
        self.apply_options()
        self._lastchar = '==N/A=='
        self.clearOnSIGWINCH = True
        self.redrawOnSIGWINCH = True
        self.disableCtrlBackslash = False
        self.bind(mmw.Bind('\x1c', self.forcefulExit))
        self.oldframe = None

    def _redraw(self):
        """Redraw the screen
        Triggered when the process gets the SIGWINCH signal"""
        self.size = os.get_terminal_size()
        if self.clearOnSIGWINCH:
            self.clear()
        self.draw()

    def setCur(self, x: int, y: int, return_the_escape=False):
        """Move the cursor the x and y.
        Arguments:
            return_the_escape -- don't print the ansi escape code,
                                 just return it.
        Return None or a string.
        """
        if return_the_escape:
            return '\033['+str(y)+';'+str(x)+'H'
        else:
            print('\033['+str(y)+';'+str(x)+'H', end='', flush=True)

    def draw_no_redraw(self, window: mmw.Drawable):
        """DEPRECATED: do NOT use this, this will render the whole frame,
        and the performance will be VERY BAD.

        Draw a window onto the screen without redrawing other windows.
        Arguments:
            window -- the window that has to be drawn
        Return True if window was drawn, False otherwise."""
        if window.isDestroyed or window.hidden:
            return False
        a = window.draw()
        x = window.x
        y = window.y
        for i in range(len(a)):
            self.setChar(mmw.formatting.format(a[i]), x, y+i)
        return True

    def draw(self, window: mmw.Drawable=None, fullDraw=False):
        """Draw the screen.
        Parameters:
          window (mmw.Drawable) -- the window that will be drawn with
                                   maximum priority
          fullDraw (boolean) -- force drawing the whole screen
                                WARNING: using this option will have an
                                inpact on the performace
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
            for y, yelem in enumerate(draw):
                for x, xelem in enumerate(yelem):
                    # print(xelem)
                    try:
                        canvas[y+w.y][x+w.x] = xelem
                    except IndexError:
                        continue
        canvas.reverse()
        for i in canvas.copy():
            if ''.join(i).isspace():
                canvas.remove(i)
                continue
            break
        canvas.reverse()

        print(self.setCur(0, 0, True), end='', flush=True)
        for y, yelem in enumerate(canvas):
            line = ''.join(yelem).rstrip()
            if self.oldframe is not None and not fullDraw:
                if len(self.oldframe) >= len(canvas):
                    if ''.join(self.oldframe[y]).rstrip() == line:
                        # Do not redraw lines that were drawn last time
                        print('\n', end='')
                        continue
            # Join the list elements and
            # remove trailing whitespace
            print('\033[2K', line, sep='', end='\n')

        if self.oldframe is not None:
            for i in range(len(self.oldframe) - len(canvas)+1):
                print('\033[2K')
        self.oldframe = canvas

    def setScreen(self, screen: typing.List[str]):
        """Draw `screen` on the screen.
        Arguments:
            screen -- list of strings that will be drawn
        Return None
        """
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
        """Put the terminal cursor in a specific place and print a string
        Arguments:
            string -- text that will be drawn
            x -- X coordinate
            y -- Y coordinate
            flush (default True)-- passed down to print; flushes the buffer
        Return None"""
        print('\033['+str(y)+';'+str(x)+'H'+str(string),
              end='', flush=flush)

    def add_window(self, window: mmw.Drawable, setParent: bool=True):
        """Add the window the the screen
        Arguments:
            window -- window that will be added to the list
            setParent (default True) -- automaticly set window.parent to self
        Return None
        """
        self.windows.append(window)
        if setParent:
            window.parent = self

    def loop(self, activeWindow: mmw.Drawable):
        char = ""
        activeWin = activeWindow
        # menuOpen = False
        # tabmenu = mmw.menu.Menu("Tab menu")
        # if loggingEnabled:
        #     log.defaultSource = 'loop'
        #     log.log('Screen.loop')
        while 1:
            char = self.get_char()
            # if loggingEnabled:
            #     log.log(repr(char))
            press = {}
            # if (char == "\r" or char == "\n") and menuOpen:
            #     windows = self.windows.copy()
            #     windows.reverse()
            #     windows.remove(activeWin)
            #     windows.insert(1, activeWin)
            #     activeWin = windows[tabmenu.childopen]
            #     tabmenu.hidden = True
            #     menuOpen = False

            # if char == "\t":
            #     if not menuOpen:
            #         windows = self.windows.copy()
            #         windows.reverse()
            #         windows.remove(activeWin)
            #         windows.insert(1, activeWin)
            #         self.size = os.get_terminal_size()
            #         # Repostion the menu if the terminal resized.
            #         tabmenu.x = round(self.size[0]/2)
            #         tabmenu.y = round(self.size[1]/2)
            #         children = []
            #         for window in windows:
            #             name = window.name if not len(window.name) > 30\
            #                 else window.name[:30]+"..."
            #             children.append({"name": name})
            #         tabmenu.elements = [
            #             {"name": "Windows", "children": children}]
            #         tabmenu.open = 0
            #         tabmenu.childopen = 0
            #         tabmenu.hidden = False
            #         self.draw(tabmenu)
            #         menuOpen = True
            #         continue
            #     else:
            #         if tabmenu.open == 0:
            #             windows = self.windows.copy()
            #             windows.reverse()
            #             windows.remove(activeWin)
            #             windows.insert(1, activeWin)
            #             activeWin = windows[0]
            #         tabmenu.hidden = True
            #         menuOpen = False
            if char == "\033":
                # if menuOpen:
                #     b = self.get_char()
                #     if b == "[":
                #         c = self.get_char()
                #         if c == "A":  # ARROW_UP
                #             if tabmenu.childopen > 0:
                #                 tabmenu.childopen -= 1
                #         if c == "B":  # ARROW_DOWN
                #             if tabmenu.childopen < \
                #                     len(tabmenu.elements[0]["children"])-1:
                #                 tabmenu.childopen += 1
                #         if c == "F":  # END
                #             tabmenu.childopen = len(
                #                 tabmenu.elements[0]["children"])-1
                #         if c == "H":
                #             tabmenu.childopen = 0
                # if loggingEnabled:
                #     log.log('1112 Char: \\033; menuOpen = False')
                b = self.get_char()
                # if loggingEnabled:
                #     log.log('1114', repr(char), ' ', b)
                if b == "[":
                    c = self.get_char()
                    # if loggingEnabled:
                    #     log.log('1117', repr(char), ' ', b, ' ', c)
                    if c in ['A', 'B', 'C', 'D']:
                        activeWin.handlers["loop"](
                            mmw.decoding.decode('\033'+b+c))
                        # if loggingEnabled:
                        #     log.log('1121',
                        #             KeyMap.decode('\033'+b+c))
                    elif c == "M":
                        # if loggingEnabled:
                        #     log.log('\\033[M')
                        t = self.get_char()
                        x = self.get_char()
                        y = self.get_char()
                        press = mmw.decoding.mouseClickDecode([t, x, y])
                        for bind in self.binds:
                            if isinstance(bind, mmw.MouseBind):
                                continue
                            x_ok1 = press["x"] >= \
                                bind.xStart
                            x_ok2 = press["x"] <= \
                                bind.xEnd
                            x_ok = x_ok1 and x_ok2
                            # del x_ok1, x_ok2
                            y_ok1 = press["y"] >= \
                                bind.yStart
                            y_ok2 = press["y"] <= \
                                bind.yEnd
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
                                bind_data = {"eventType": "mouseClick",
                                             "eventSource": "Screen.loop",
                                             "click": press,
                                             "bind": bind}
                                o = bind.function(bind_data)
                                if o == "END":
                                    return
            elif char not in mmw.specialChars:
                for bind in self.binds:
                    if bind.keySeq == char:
                        bind["function"]({"eventType": "keyPress",
                                          "eventSource": "Screen.loop",
                                          "bind": bind})
                        break
                if activeWin.handlers["loop"](char) == 'END':
                    return
            self.draw(activeWin)

    def forcefulExit(self, event=None):
        """This function is triggered on ^\\.
        Display a window asking if the user realy wants to quit.
        """
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
            char = self.get_char()
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
        self.options.update(mmw.SO_DEFAULTS)
        self.apply_options()  # reset the terminal options
        if w.selectedButton == 1:
            pid = os.getpid()
            print('\n[Screen/forcefulExit()] Killing pid:', pid)
            if os.name == 'nt':
                os.kill(pid, signal.CTRL_BREAK_EVENT)
                # This will show an error when linting on linux
                # Please ignore it.
            else:
                os.kill(pid, signal.SIGKILL)
                # And this will probably too but on windows
                # Please ignore this one too.
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

    def bind(self, bind_obj):
        """Bind a key to a function (Screen.loop())
        Arguments:
            bind_obj -- A Bind(or MouseBind) object."""
        if not isinstance(bind_obj, mmw.Bind):
            raise TypeError('bind_obj must be of type mmw.Bind or subclass')
        self.binds.append(bind_obj)
        return bind_obj
# def custom_input(self, prompt, handler=None):
#     inputed = ""
#     waiting = []
#     inMouseMode = False
#     while 1:
#         if not inMouseMode:
#             char = self.get_char()
#         else:
#             char = "x"+str(ord(self.get_char(True)))
#         print("char: ", repr(char), "waiting: ", waiting, "imm",
#               inMouseMode)
#         # Call self.get_char() forcing to output a string with the special
#         # mmw.formatting
#         # ex. "33"(ASCII !)
#         # (required for mouse detection, since there is no char
#         # staring with 0xFF in UTF-8)
#         if char == "\x1c" or char == "x28":
#             print("(Force exiting)")
#             exit(0)
#         if char == "\033":
#             # print('033')
#             b = self.get_char(True)
#             if b == b"[":
#                 # print('[')
#                 c = self.get_char(True)
#                 if c == b"M":
#                     # print("M")
#                     ptype = self.get_char(True)
#                     x = self.get_char(True)
#                     y = self.get_char(True)
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
