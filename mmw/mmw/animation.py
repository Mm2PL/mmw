import mmw


class Animation(mmw.Drawable):
    # ------------------------------
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        for f in self.frames:
            f.x = value
        self.requiresRedrawing = True

    # ------------------------------
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        for f in self.frames:
            f.y = value
        self.requiresRedrawing = True

    # ------------------------------
    @property
    def xRel(self):
        return self._xRel

    @xRel.setter
    def xRel(self, value):
        for f in self.frames:
            f.xRel = value
        self.requiresRedrawing = True

    # ------------------------------
    @property
    def yRel(self):
        return self._yRel

    @yRel.setter
    def yRel(self, value):
        for f in self.frames:
            f.yRel = value
        self.requiresRedrawing = True

    # ------------------------------
    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        if value >= len(self.frames):
            raise ValueError('frame cannot be higher than len(self.frames)')
        elif value < 0:
            raise ValueError('frame cannot be lower than 0')
        else:
            self._frame = value
        self.requiresRedrawing = True

    # ------------------------------
    @property
    def frames(self):
        return self._frames

    @frames.setter
    def frames(self, value):
        for i in value:
            if not isinstance(i, mmw.Drawable):
                raise ValueError('Each element of frames must be of type '
                                 'mmw.Drawable or a subclass')
        self._frames = value
        self.requiresRedrawing = True

    def __init__(self):
        super().__init__('Animation')
        self._frame = 0
        self._frames = []
        self.autoAdvance = False

    def draw(self):
        """Return the current frame"""
        retval = self._frames[self._frame].draw()
        self.lastDraw = retval
        if self.autoAdvance:
            self.requiresRedrawing = True
            try:
                self.frame += 1
            except ValueError:
                self.frame = 0
        return retval
