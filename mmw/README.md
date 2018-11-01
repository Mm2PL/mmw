# mmw
Github link: http://github.com/Mm2PL/mmw
## What is it?
It is a library that generates simple pseudo-graphic windows.

## How to use it?
Examples:

1. Code:
```python
import mmw
screen = mmw.Screen()
window = mmw.Window('Our window')
screen.add_window(window)  # Link the window to the screen
window.text = "Let's add some text"
window.buttons = ['And', 'some', 'buttons']
window.selectedButton = 0  # Select the first button
screen.clear()  # Screen.draw() doesn't clear the screen by itself
screen.draw()  # Draw the screen
screen.get_char()  # Wait until the user presses a key
```
Output:
```
+-----------Our window-----------+
|Let's add some text             |
|                                |
| [>And<]  [ some ]  [ buttons ] |
+--------------------------------+
```
2. See [mmwDemo.py on github](https://github.com/Mm2PL/mmw/blob/master/mmwDemo.py)
