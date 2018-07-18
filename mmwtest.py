import mmw
# import time
# import time
# print("\033[2J")
# print("Starting...")
# mmw = __import__("mmw3")

s = mmw.Screen()
s.inDebug = True

# w = mmw.Window("asd")
# s.add_window(w)
#
# w.useRelativePos = True
# w.text = "To jest test"
# w.recalcPos()
#
# hw = mmw.Window("Ukryte okno")
# s.add_window(hw)
# hw.hidden = True
#
#
# def sigwinch(window, screen):
#     # return
#     print("Nazwa: ", window.name, "Ekran: ", screen)
#
#
# def settext(text):
#     w.text = text
#
#
# hw.handlers["SIGWINCH"] = sigwinch
# s.draw()
# s.bind("\\", lambda evt: exit(0))
# s.bind("\x7f", lambda evt: settext("DUUUUUUUUUUUUUUUUPPPPPPPPPPAAAAAAA"))
# s.loop(w)


def brk():
    # s.clear()
    print(mmw.FormattedString("$(green)Explicit exit$(reset)"))
    exit(0)


w = mmw.Window('DUUPA')
w.buttons = ['1', '2', '3']
w.selectedButton = 0
t = False


def toggle():
    global t
    w.text = str(t)
    t = not t


def disp(a):
    w.text = repr(a)


# w.text = 'DDDDDDDDDDUUUUUUUUUUUUPPPPPPPPPPAAAAAAAAAAAAAAAAAAAAA'
# w.styleOptions["ButtonAlignment"] = mmw.POS_RIGHT
w.styleOptions['ButtonAlignment'] = mmw.POS_RIGHT
s.draw(w)
s.add_window(w)
s.bind("`", lambda a: brk())
s.bind('q', lambda a: toggle())
s.bind(['\\M', {'xStart': 0, 'xEnd': s.size[0], 'yStart': 0,
                'yEnd': s.size[1]}], disp)
s.bind('\x03', disp)
w.forcedWidth = s.size[0] - 3
w.forcedHeight = s.size[1] - 3
s.disableCtrlBackslash = False
s.loop(w)
