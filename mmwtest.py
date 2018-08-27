import mmw
s = mmw.Screen()
s.inDebug = True
w = mmw.Window('TEST')
w.text = 'T.E.S.T'
s.add_window(w)
s.draw()
