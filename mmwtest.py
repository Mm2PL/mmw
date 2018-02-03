import mmw3 as mmw
# import time
print("\033[2J")
# print("Starting...")
# mmw = __import__("mmw3")
s = mmw.Screen()
print("\033[0;0H(mmw test)")
w = mmw.Window("(P3) Nie wiem")
w.priority = 3
w.y = 10
w.x = 10
w.text = "Nie wiem co tu napisać, więc napisze to"
w2 = mmw.Window("(P2) Nie wiem")
w2.priority = 2
w2.y = 9
w2.x = 9
w2.text = "Tu też nie wiem co napisać."
w3 = mmw.Window("(P1) Nie wiem")
w3.text = "I tu - jak zwykle - też nie wiem co napisać."
w3.y = 8
w3.x = 8
w3.priority = 1
w.draw()
w2.draw()
w3.draw()
s.add_window(w)
s.add_window(w2)
s.add_window(w3)
s.draw(w3)
# w.destroy()
# while 1:
#
#     for i in range(2, 0, -1):
#         print("\033[24;0HReloading in "+str(i)+10*" ")
#         time.sleep(1)
#     print("\033[2J")
