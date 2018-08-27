# from .drawable import Drawable
# import mmw.styles as styles
import mmw
import typing
# from .styles import Styles
# import re


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
        if char == "ARROW_RIGHT":
            if self.open < len(self.elements)-1:
                self.open += 1
                if self.childopen > len(self.elements[self.open]['children']):
                    self.childopen = len(self.elements[self.open]
                                         ['children'])-1
        if char == "ARROW_LEFT":
            if self.open > 0:
                self.open -= 1
                if self.childopen > len(self.elements[self.open]['children']):
                    self.childopen = len(self.elements[self.open]
                                         ['children'])-1
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
        # self.elements =
        # [
        # {'name': 'NAME', 'children':
        #   [
        #       {'name': 'CHILD NAME'}
        #   ]}
        # ]
        for element in self.elements:  # Iterate thru the top menu elements
            highLen = 0
            for child in element["children"]:  # Iterate thru the sub elements
                child["vislen"] = len(child["name"])  # FormattedStrings exist
                if child["vislen"] > highLen:
                    highLen = child["vislen"]
            element["highLen"] = highLen
            element["offset"] = offset+2
            offset = offset\
                + len(self.style["MenuBar"]
                      .replace("{name}", element["name"]))
        for num, element in enumerate(self.elements):
            if self.open == num:
                # print(element)
                # import pdb
                # pdb.Pdb()
                # if self.hasTitle:
                win[0] = win[0] + self.style["TextFiller"]\
                    + self.style["MenuBarSelected"]\
                    .replace("{name}", element["name"])
                # win[0] = re.sub(r"^\s*", r"", win[0])
                genericCorner = self.style["CornerGeneric"]\
                    if len(element["name"]) < element["highLen"]\
                    else ""
                offseter = self.style["TextFiller"]\
                    * (element["offset"]+1) if element["offset"] > 0\
                    else ""

                win.append(offseter
                           + self.style["CornerUpLeft"]
                           + (self.style["BorderHorizontal"]
                              * len(element["name"]))
                           + (genericCorner if self.hasTitle
                              else self.style["BorderHorizontal"])
                           + ((element["highLen"]
                               - len(element["name"]))
                              * self.style["BorderHorizontal"])
                           + self.style["CornerUpRight"])
                if len(element['children']) == 0:
                    win.append(offseter
                               + self.style['CornerDownLeft']
                               + (self.style["BorderHorizontal"]
                                  * (len(element["name"])))
                               + self.style['CornerDownRight'])
                    continue
                for childNum, child in enumerate(element["children"]):
                    filler = self.style["TextFiller"]\
                        * (element["highLen"] - child["vislen"])\
                        if element["highLen"] - child["vislen"] > 0\
                        else ""

                    name = self.style["MenuChildSelected"].replace(
                        "{name}", child["name"])\
                        + ""\
                        if self.childopen == childNum\
                        else self.style["MenuChildUnselected"].replace(
                            "{name}", child["name"])
                    win.append(offseter
                               + self.style["BorderVertical"]
                               + name
                               + filler
                               + self.style["BorderVertical"])
                win.append(offseter
                           + self.style["CornerDownLeft"]
                           + (self.style["BorderHorizontal"]
                              * (element["highLen"]+1))
                           + self.style["CornerDownRight"])
            else:
                win[0] = win[0] + self.style["TextFiller"]\
                    + self.style["MenuBar"]\
                    .replace("{name}", element["name"])
            # print(win)
        # print(win)
        self.lastDraw = win
        return win
