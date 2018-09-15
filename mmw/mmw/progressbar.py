import mmw


class ProgressBar(mmw.Drawable):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, newval):
        if not isinstance(newval, int):
            raise ValueError('Argument 1(newval) has to be of type int.')
        if newval > self.maxvalue:
            raise ValueError('Argument 1(newval) cannot be bigger than '
                             'self.maxvalue.')
        if newval < 0:
            raise ValueError('Argument 1(newval) cannot be smaller than 0.')
        self._value = newval

    @property
    def maxvalue(self):
        return self._maxvalue

    @maxvalue.setter
    def maxvalue(self, newval):
        if self.mode == mmw.PR_PERCENT:
            raise ValueError('maxvalue cannot be set while self.mode is '
                             'PR_PERCENT')
        if not isinstance(newval, int):
            raise ValueError('Argument 1(newval) has to be of type int.')
        if newval <= 0:
            raise ValueError('Argument 1(newval) cannot be smaller or equal '
                             'to 0')
        if newval < self.value:
            self._value = newval
        self._maxvalue = newval

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if value not in mmw.PR_MODES:
            raise ValueError('Invalid option use one that\'s in mmw.PR_MODES')
        else:
            self._mode = value

    def __init__(self, name='Bar', value=0, mode=mmw.PR_PERCENT):
        """Create a ProgressBar
        Arguments:
          - name
          - value
            - The value of the progress bar
          - mode
            - Change either you want the maxvalue to be automaticly set to 100
              or to be manualy set"""
        super().__init__(name)
        self.mode = mode
        self._value = 0
        self._maxvalue = value+1
        self.value = value
        self.maxvalue = 100
        self.showname = True
        self.showProgressText = True
        self.width = 80

    def draw(self):
        """Draw the progress bar"""
        fraction = self.value/self.maxvalue
        output = ''
        if self.showname:
            output += self.name+' '
        if self.showProgressText:
            if self.mode == mmw.PR_PERCENT:
                temp = '{:>3.0f}%'
                output += temp.format(self.value)
            else:
                temp = str(self.value)+' / '+str(self.maxvalue)+' ({:>3.0f}%)'
                output += temp.format(fraction*100)
        output += self.style['ProgressStart']
        leftwidth = self.width-len(output)-1-len(self.style['ProgressEnd'])
        filled = leftwidth*fraction-1
        empty = leftwidth-filled
        if 'ProgressHead' in self.style:
            temp = ((self.style['ProgressFilled']*round(filled))
                    + (self.style['ProgressHead'])
                    + (self.style['ProgressEmpty']*round(empty-1)))
            output += temp
        else:
            temp = ((self.style['ProgressFilled']*round(filled))
                    + (self.style['ProgressEmpty']*round(empty)))
            output += temp
        output += self.style['ProgressEnd']
        return [output]
