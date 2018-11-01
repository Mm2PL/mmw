import typing


class Bind():
    '''Stores all the information about a bind'''
    def __init__(self, keySeq: str, function: typing.Callable):
        self.keySeq = keySeq
        self.function = function

    def __repr__(self):
        return "<bind ({keySeq!r}); "\
               "handler: {function.__name__}>".format(keySeq=self.keySeq,
                                                      function=self.function)


class MouseBind(Bind):
    '''Stores all the information about a click hitbox'''
    def __init__(self, coordStart: typing.Tuple[int],
                 coordEnd: typing.Tuple[int], function: typing.Callable):
        self.keySeq = 'Mouse: '\
            + repr(coordStart)\
            + ' -> '\
            + repr(coordEnd)
        self.xStart = coordStart[0]
        self.yStart = coordStart[1]

        self.xEnd = coordEnd[0]
        self.yEnd = coordEnd[1]

        self.function = function

    def __repr__(self):
        return "<Click hitbox from ({xStart}, {yStart}) to ({xEnd}, {yEnd}); "\
               "hanlder: {function.__name__}>".format(xStart=self.xStart,
                                                      yStart=self.yStart,
                                                      xEnd=self.xEnd,
                                                      yEnd=self.yEnd,
                                                      function=self.function)
