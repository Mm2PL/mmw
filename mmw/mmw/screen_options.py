import copy
import mmw


class Screen_Options:
    """This is a class intended for saving screen options"""
    def keys(self):
        return self._options.keys()

    def __iter__(self, *args):
        return self._options.__iter__(*args)

    def __setitem__(self, key, item):
        if key in self._options:
            if isinstance(item, type(self._options[key])):
                self._options[key] = item
            else:
                raise TypeError(repr(item)+' is of type: '+repr(type(item))
                                + ', but the type required is '
                                + repr(type(self._options[key])))

    def __getitem__(self, key):
        if key not in self._options:
            raise KeyError(key)
        return self._options[key]

    def __init__(self, defaults):
        if not isinstance(defaults, dict):
            raise TypeError('Valid type for defaults is dict')
        self._options = copy.copy(defaults)

    def update(self, other):
        for k in other:
            if k not in self._options:
                raise mmw.FinalError('The key list of Screen_Options is '
                                     'immutable')
            else:
                self._options[k] = other[k]

    def __delitem__(self, item):
        raise mmw.FinalError('The key list of Screen_Options is immutable.')

    def __dict__(self):
        return self._options

    def __repr__(self):
        return 'Screen_Options({})'.format(repr(self._options))

    def __str__(self):
        return self.__repr__()
