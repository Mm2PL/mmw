# from .drawable import Drawable
# import mmw.styles as styles
import mmw
import typing
# from .styles import Styles
import re


class Menu(mmw.Drawable):
    def __repr__(self):
        if self.useRelativePos:
            return 'mmw.Menu(name={}) at ({}/{}, {}/{})'.format(
                repr(self.name), self.xRel, self.x, self.yRel, self.y)
        else:
            return 'mmw.Menu(name={}) at ({}, {})'.format(
                repr(self.name), self.x, self.y)

    def selectorHandler(self, char: str):
        """Select a button"""
        # log.slog('selectorHandler', repr(char))
        # key = ""
        # if char == "\x1b":
        #     more = self.parent.getChar()
        #     log.slog('selectorHandler', 'more '+repr(more))
        #     if more == "[":
        #         evenMore = self.parent.getChar()
        #         log.slog('selectorHandler', 'evenmore '+repr(evenMore))
        #         if evenMore == "A":
        #             key = "ARROW_UP"
        #         elif evenMore == "B":
        #             key = "ARROW_DOWN"
        #         elif evenMore == "C":
        #             key = "ARROW_RIGHT"
        #         elif evenMore == "D":
        #             key = "ARROW_LEFT"
        if char == "ARROW_RIGHT":
            if self.open < len(self.elements)-1:
                self.open += 1
        if char == "ARROW_LEFT":
            if self.open > 0:
                self.open -= 1
        if char == "ARROW_DOWN":
            if self.childopen < len(self.elements[self.open]['children'])-1:
                self.childopen += 1
        if char == "ARROW_UP":
            if self.childopen > 0:
                self.childopen -= 1
        if char == "\r":
            return self.handlers["menuClicked"](self)

    def __init__(self, name: str):
        super().__init__(name)
        self.elements = []
        self.handlers = {'menuClicked': lambda self: None,
                         'loop': self.selectorHandler}
        self.style = mmw.styles.DEFAULT
        self.open = -1
        self.childopen = -1
        self.x = 1
        self.y = 1
        self.hasTitle = False

    def draw(self) -> typing.List[str]:
        """Return a list of strings"""
        win = [""]
        offset = 0
        for element in self.elements:
            highLen = 0
            for child in element["children"]:
                child["vislen"] = len(re.sub(r"\$\([A-Za-z_0-9]*\)", "",
                                             child["name"]))
                if child["vislen"] > highLen:
                    highLen = child["vislen"]
            element["highLen"] = highLen
            element["offset"] = offset
            offset = offset\
                + len(self.style["MenuBar"]
                      .replace("{name}", element["name"]))
        for element in enumerate(self.elements):
            if self.open == element[0]:
                # if self.hasTitle:
                win[0] = win[0] + self.style["TextFiller"]\
                    + self.style["MenuBarSelected"]\
                    .replace("{name}", element[1]["name"])
                win[0] = re.sub(r"^\s*", r"", win[0])
                genericCorner = self.style["CornerGeneric"]\
                    if len(element[1]["name"]) < element[1]["highLen"]\
                    else ""
                offseter = self.style["TextFiller"]\
                    * (element[1]["offset"]+1) if element[1]["offset"] > 0\
                    else ""
                win.append(offseter
                           + self.style["CornerUpLeft"] + "\033[0m"
                           + (self.style["BorderHorizontal"]
                              * len(element[1]["name"]))
                           + "\033[0m"
                           + (genericCorner if self.hasTitle
                              else self.style["BorderHorizontal"])
                           + "\033[0m"
                           + ((element[1]["highLen"]
                               - len(element[1]["name"]))
                              * self.style["BorderHorizontal"])
                           + "\033[0m"
                           + self.style["CornerUpRight"]
                           + "\033[0m")
                for childE in enumerate(element[1]["children"]):
                    child = childE[1]
                    filler = self.style["TextFiller"]\
                        * (element[1]["highLen"] - child["vislen"])\
                        if element[1]["highLen"] - child["vislen"] > 0\
                        else ""
                    name = "\033[0m" + self.style["MenuChildSelected"].replace(
                        "{name}", child["name"])\
                        + "\033[0m"\
                        if self.childopen == childE[0]\
                        else self.style["MenuChildUnselected"].replace(
                            "{name}", child["name"]) + "\033[0m"
                    win.append(offseter
                               + "\033[0m"
                               + self.style["BorderVertical"]
                               + "\033[0m"
                               + name
                               + "\033[0m"
                               + filler
                               + "\033[0m"
                               + self.style["BorderVertical"]
                               + "\033[0m")
                win.append(offseter
                           + "\033[0m"
                           + self.style["CornerDownLeft"]
                           + "\033[0m"
                           + (self.style["BorderHorizontal"]
                              * (element[1]["highLen"]+1))
                           + "\033[0m"
                           + self.style["CornerDownRight"]
                           + "\033[0m")
            else:
                win[0] = win[0] + self.style["TextFiller"]\
                    + "\033[0m"\
                    + self.style["MenuBar"]\
                    .replace("{name}", element[1]["name"])\
                    + "\033[0m"
                # print(win)
        # print(win)
        self.lastDraw = win
        return win
