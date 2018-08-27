import mmw
import typing
lastid = 0


class Drawable():
    """A drawable base."""
    # autoWindowResize (default = True)
    #  True - Expand the window to the texts size,
    #  False - Don't expand

    def __repr__(self):
        if self.useRelativePos:
            return 'mmw.Drawable(name={}) at ({}/{}, {}/{})'.format(
                repr(self.name), self.xRel, self.x, self.yRel, self.y)
        else:
            return 'mmw.Drawable(name={}) at ({}, {})'.format(
                repr(self.name), self.x, self.y)

    # ---------------------------------
    # self.name
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value
        self.requiresRedrawing = True

    # ---------------------------------
    # self.y
    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = value
        self.requiresRedrawing = True

    # ---------------------------------
    # self.x
    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value
        self.requiresRedrawing = True

    # ---------------------------------
    # self.xRel
    @property
    def xRel(self):
        return self._xRel

    @xRel.setter
    def xRel(self, value):
        self._xRel = value
        self.requiresRedrawing = True
        self.recalcPos()

    # ---------------------------------
    # self.yRel
    @property
    def yRel(self):
        return self._yRel

    @yRel.setter
    def yRel(self, value):
        self._yRel = value
        self.requiresRedrawing = True
        self.recalcPos()

    # ---------------------------------
    def __init__(self, name: str):
        global lastid
        self._name = name
        self.isDestroyed = False

        self._x = 1
        self._y = 1
        self._xRel = mmw.POS_CENTER
        self._yRel = mmw.POS_CENTER

        self.forcedWidth = 0
        self.forcedHeight = 0
        self.width = 0
        self.height = 0
        self.autoResize = True

        self.parent = None

        self.id = lastid + 1
        lastid = lastid + 1
        self.priority = 0
        self.lastDraw = "N/A"
        self.hidden = False
        self.requiresRedrawing = False
        self.useRelativePos = False
        self._xRel = mmw.POS_CENTER
        self._yRel = mmw.POS_CENTER
        self.handlers = {"loop": lambda *args: None,
                         "SIGWINCH": lambda this, caller: self.recalcPos()}
        self.style = mmw.styles.DEFAULT

    def check_parent(self) -> bool:
        """Check if the parent is not None and is has a size property"""
        if self.parent is None:
            return False
        try:
            if self.parent.size:
                return True
        except NameError:
            return False
        # return True

    def recalcPos(self) -> typing.Tuple[int]:
        """Recalculate the posistion, using the parent's size property"""
        self.draw()
        if not self.check_parent():
            raise mmw.InvalidStateError('Cannot recalculate the position, '
                                        'because '
                                        'either the parent is None or '
                                        'has no size '
                                        'attribute')
        if self.xRel == mmw.POS_CENTER:
            self.x = round(self.parent.size[0]/2)-round(self.width/2)
        elif self.xRel[0] == mmw.POS_LEFT:
            self.x = round(self.xRel[1]*self.parent.size[0])\
                - round(self.width/2)
        elif self.xRel[0] == mmw.POS_RIGHT:
            self.x = round(self.xRel[1]*self.parent.size[0])\
                - round(self.width/2)
        else:
            raise mmw.InvalidStateError(
                "mmw3.Drawable.xRel can only be mmw3.POS_CENTER or "
                "[mmw3.POS_LEFT, float] or [mmw3.POS_RIGHT, float]")

        if self.yRel == mmw.POS_CENTER:
            self.y = round(self.parent.size[1]/2)-round(self.height/2)
        elif self.yRel[0] == mmw.POS_UP:
            self.y = round(self.xRel[1]*self.parent.size[1])\
                - round(self.height/2)
        elif self.yRel[0] == mmw.POS_DOWN:
            self.y = round(self.xRel[1]*self.parent.size[1])\
                - round(self.height/2)
        else:
            raise mmw.InvalidStateError(
                "mmw3.Drawable.yRel can only be mmw3.POS_CENTER or "
                "[mmw3.POS_LEFT, float] or [mmw3.POS_RIGHT, float]")
        return self.x, self.y

    def draw(self) -> typing.List[str]:
        """**Stub**
        This method should return a list of strings(rendered object)"""
        win = ['']
        self.lastDraw = win
        return win

    def destroy(self, destroyChild=False):
        """Destroy the object"""
        self.checkDestroyed()
        self.x = None
        self.y = None
        self.forcedWidth = None
        self.forcedHeight = None
        self.isDestroyed = True
        self.hidden = True
        self.lastDraw = "N/A"
        if destroyChild:
            for widget in self.widgets:
                widget.destroy(True)

    def checkDestroyed(self) -> bool:
        """Check if this object is destoryed"""
        if self.isDestroyed:
            raise mmw.InvalidStateError(self.name
                                        + ": This Object is destoryed.")
        return
