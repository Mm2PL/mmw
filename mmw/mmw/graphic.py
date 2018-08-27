import mmw


class Graphic(mmw.Drawable):
    """Pseudo-graphic drawable object"""
    def __repr__(self):
        if self.useRelativePos:
            return 'mmw.Graphic() at ({}/{}, {}/{})'.format(
                self.xRel, self.x, self.yRel, self.y)
        else:
            return 'mmw.Graphic() at ({}, {})'.format(self.x, self.y)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if len(value) < 1:
            raise mmw.InvalidStateError('Graphic.text cannot have a '
                                        'length of 0 or less')
        nval = value
        if isinstance(value, str):
            nval = value.split('\n')
        self._text = nval
        self.requiresRedrawing = True

    def __init__(self, text):
        super().__init__('Graphic')
        # if len(text) < 1:
        #     raise InvalidStateError('Graphic.__init__(self, >text<) '
        #                             'text cannot have a length of 0 or less')
        self.text = text

    def draw(self) -> str:
        """Return self.text"""
        return self._text

    # def checkSize(self):
    #     """Checks self.text for size weirdness; Returns True
    #     or raises InvalidStateError if something is wrong"""
    #     llen = len(self.text[0])
    #     for num, line in enumerate(self.text):
    #         if len(line) != llen:
    #             raise InvalidStateError('The size of self.text is wierd. '
    #                                     'Line '+str(num)+' has length of '
    #                                     + str(len(line))+' characters, '
    #                                     'but should have '+str(llen)
    #                                     + ' characters')
    #     return True
