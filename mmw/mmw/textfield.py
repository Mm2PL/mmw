import mmw
import typing


class TextField(mmw.Drawable):
    """A Textfield (WIP)"""
    def __repr__(self) -> str:
        if self.useRelativePos:
            return 'mmw.TextField(type=mmw.{}, name={}) at ({}/{}, {}/{})'.\
                format(self._type, repr(self.name), self.xRel, self.x,
                       self.yRel, self.y)
        else:
            return 'mmw.TextField(type=mmw.{}, name={}) at ({}, {})'.format(
                self._type, repr(self.name), self.x, self.y)

    def __init__(self, type=mmw.consts.TF_ONELINE, name=''):
        super().__init__(name)
        self.text = ['']
        self._type = None
        self.field_type = type

    @property
    def field_type(self) -> str:
        return self._type

    @field_type.setter
    def field_type(self, value):
        if value in mmw.consts.TF_TYPES:
            self._type = value
        else:
            raise ValueError(repr(value)+' is not part of mmw.consts.TF_TYPES '
                             'and cannot be used as a type. '
                             'See mmw.consts.TF_TYPES')

    def draw(self) -> typing.List[str]:
        output = ''
        if self.name != '':
            output += self.name+' '
        if self.field_type == mmw.consts.TF_ONELINE:
            if self.forcedWidth <= 0:  # Brak ustawionej wielkosci
                if self.autoResize:  # Automagiczna wielkosc
                    output += self.style['TextLeftBorder']
                    if isinstance(self.text, list):
                        output += self.text[0]
                    elif isinstance(self.text, str):
                        output += self.text
                    else:
                        output += repr(self.text)
                    output += self.style['TextRightBorder']
                    self.width = len(output)
                else:
                    raise mmw.errors.InvalidStateError('self.forcedWidth '
                                                       'is <= 0 '
                                                       'but self.autoResize '
                                                       'is not set.')
            else:
                if self.autoResize:
                    raise mmw.errors.InvalidStateError('self.autoResize '
                                                       'is set and '
                                                       'self.forcedWidth '
                                                       'is set.')
                else:
                    text = ''
                    if isinstance(self.text, list):
                        text = self.text[0][:self.forcedWidth-2]
                    elif isinstance(self.text, str):
                        text = self.text[:self.forcedWidth-2]
                    else:
                        text = repr(self.text)[:self.forcedWidth-2]
                    output += self.style['TextLeftBorder']
                    output += text
                    output += self.style['TextEmpty']\
                        * (self.forcedWidth - len(text) - 2)
                    output += self.style['TextRightBorder']
        return output.split('\n')
