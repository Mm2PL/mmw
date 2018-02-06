import mmw3 as mmw
# import time
# import time
# print("\033[2J")
# print("Starting...")
# mmw = __import__("mmw3")
s = mmw.Screen()
# print("\033[s\033[0;0H(mmw test)\033[u")
# w = mmw.Window("Test")
# w.y = 5
# w.x = 1
# w.text = "Test - Style.DEFAULT"
# w2 = mmw.Window("Test")
# w2.y = 1
# w2.x = 24
# w2.style = mmw.Styles.UNICODE_BOLD
# w2.text = "Test - Styles.UNICODE_BOLD"
#
# w3 = mmw.Window("Test")
# w3.text = "Test - Styles.UNICODE"
# w3.y = 1
# w3.style = mmw.Styles.UNICODE

# w.draw()
# w2.draw()
# w3.draw()
# s.add_window(w)
# s.add_window(w2)
# s.add_window(w3)

# s.background = (("\033[40m"+("-"*80)+"\n")*24).split("\n")
defa = mmw.Window("Test")
defa.style = mmw.Styles.DEFAULT
defa.text = "Test - Styles.DEFAULT"
defa.x = 1
defa.y = 1
defa.draw()
# s.add_window(defa)

alt = mmw.Window("Test")
alt.style = mmw.Styles.ALTERNATE
alt.text = "Test - Styles.ALTERNATE"
alt.y = 1
alt.x = defa.width + 1
alt.draw()
# s.add_window(alt)

un = mmw.Window("Test")
un.style = mmw.Styles.UNICODE
un.text = "Test - Styles.UNICODE"
un.y = 1
un.x = alt.x + alt.width
# s.add_window(un)

unb = mmw.Window("Test")
unb.style = mmw.Styles.UNICODE_BOLD
unb.text = "Test - Styles.UNICODE_BOLD"
unb.y = defa.height + 1
unb.draw()
# s.add_window(unb)
menu = mmw.Menu("Nie Wiem")
elem = [{"name": "Test", "children": [{"name": "Lista 10 Napisow:"}]}]
for a in range(10):
    elem[0]["children"].append({"name": str(a)})
menu.elements = elem
menu.open = 0
s.draw(menu, "clear")
# time.sleep(1)
# w.destroy()
# while 1:
#
#     for i in range(2, 0, -1):
#         print("\033[24;0HReloading in "+str(i)+10*" ")
#         time.sleep(1)
#     print("\033[2J")
