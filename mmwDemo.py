import mmw
import os
import time
ekran: mmw.Screen
if os.name == "nt":
    ekran = mmw.Screen(False)
else:
    ekran = mmw.Screen(True)
ekran.clearOnSIGWINCH = False
ekran.redrawOnSIGWINCH = False
menu = mmw.Menu("Menu")
menu.elements = [
    {"name": 'Wybierz jedno', 'children': [
        {"name": 'Kaskadujące okna'},
        {"name": 'Poruszanie oknem'},
        {'name': 'Zmiana styli okna'},
        {'name': 'Tęcza'},
        {'name': '----------------'},
        {'name': 'Wyjdź'}
    ]}
]
menu.open = 0
menu.childopen = 0


def styleHandler(char, okno):
    # m = mmw.KeyList  # Skrót do klasy, nie definicja obiektu
    if char.lower() == 'u':
        okno.style = mmw.styles.UNICODE
    elif char.lower() == 'a':
        okno.style = mmw.styles.ALTERNATE
    elif char.lower() == 'd':
        okno.style = mmw.styles.DEFAULT
    elif char.lower() == 'b':
        okno.style = mmw.styles.UNICODE_BOLD
    elif char == '\r':
        return 'END'
    # .


def windowHandler(char, okno):
    # m = mmw.KeyList  # Skrót do klasy, nie definicja obiektu
    if char == mmw.ARROW_UP:
        okno.y -= 1
    elif char == mmw.ARROW_DOWN:
        okno.y += 1
    elif char == mmw.ARROW_LEFT:
        okno.x -= 1
    elif char == mmw.ARROW_RIGHT:
        okno.x += 1
    elif char == '\r':
        return 'END'


def handler(menu):
    ekran2: mmw.Screen
    if os.name == "nt":
        ekran2 = mmw.Screen(False)
    else:
        ekran2 = mmw.Screen(True)
    ekran2.clearOnSIGWINCH = False
    ekran2.redrawOnSIGWINCH = False
    if menu.childopen == 0:
        okna = []
        for num in range(10):
            w = mmw.Window('Okno')
            w.text = 'test'
            w.x = num
            w.y = num
            okna.append(w)
            ekran2.add_window(w)
        ekran2.draw()
        string = mmw.FormattedString(
            '$(yellow)[Naciśnij $(green)coś$(yellow)]')
        ekran2.setChar(str(string), 0, ekran2.size[1]-2)
        ekran2.getChar()
    if menu.childopen == 1:
        w = mmw.Window("Okno")
        w.text = "Przesuń to okno za pomocą strzałek"
        w.x = 1
        w.y = 1
        w.handlers['loop'] = lambda char: windowHandler(char, w)
        ekran2.add_window(w)
        ekran2.draw(w)
        ekran2.loop(w)
    if menu.childopen == 2:
        w = mmw.Window("Okno")
        w.text = 'u -- Unicode\nd -- Domyślny\na -- Alternatywny\n'\
            'b -- Unicode pogrubiony'
        w.useRelativePos = True
        w.handlers['loop'] = lambda char: styleHandler(char, w)
        ekran2.add_window(w)
        ekran2.draw(w)
        ekran2.loop(w)
    if menu.childopen == 3:
        ekran2.clear()
        ekran2.setCur(0, 0)
        import math
        r = 0
        g = 0
        b = 0

        def mrange(stop, step):
            for i in range(round(stop/step)):
                yield i*step
        try:
            i = 0
            while 1:
                s = math.sin(i)
                if s <= 0:
                    s = 0
                r = round(s*255)

                s = math.sin(i+2)
                if s <= 0:
                    s = 0
                g = round(s*255)

                s = math.sin(i+4)
                if s <= 0:
                    s = 0
                b = round(s*255)
                ekran2.setCur(0, 0)
                print(mmw.rgb(r, g, b)+'To jest tęczowe.\n', end='')
                print('r', r, '/ 255', '| g', g, '/ 255', '| b', b, '/ 255',
                      end='\033[K')
                time.sleep(0.005)
                i += 0.01
        except KeyboardInterrupt:
            pass
    if menu.childopen == len(menu.elements[0]['children'])-1:
        exit(0)


menu.handlers["menuClicked"] = handler
ekran.add_window(menu)
ekran.draw()
ekran.loop(menu)