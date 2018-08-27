import mmw
import re
import typing
this = typing.TypeVar('this', bound='FormattedString')


class FormattedString(str):
    """A formatted string. (duh)"""

    def __init__(self, string: str):
        self.string = mmw.format(string)
        self.unformattedString = string
        self.noCodeString = re.sub(r"\$\([A-Za-z_0-9]*\)", "", string)

    def __add__(self, anotherString: typing.AnyStr):
        if isinstance(anotherString, FormattedString):
            return FormattedString(self.unformattedString
                                   + anotherString.unformattedString)
        else:
            return FormattedString(self.unformattedString
                                   + anotherString)

    def __contains__(self, anotherString: typing.AnyStr) -> bool:
        if isinstance(anotherString, FormattedString):
            return anotherString.unformattedString in self.unformattedString
        else:
            return anotherString in self.noCodeString

    def __eq__(self, anotherString: typing.AnyStr) -> bool:
        if isinstance(anotherString, FormattedString):
            return self.unformattedString == anotherString.unformattedString
        else:
            return self.noCodeString == anotherString

    def __format__(self, *args, **kwargs) -> this:
        return FormattedString(self.unformattedString.format(*args, **kwargs))

    def __ge__(self, value):
        """return self>=value; NotImplemented"""
        return NotImplemented

    def __getitem__(self, key) -> str:
        return self.noCodeString[key]

    def __gt__(self, value):
        """return self>value; NotImplemented"""
        return NotImplemented

    def __hash__(self):
        return hash((self.string, self.unformattedString))

    def __le__(self, value):
        """return self<=value; NotImplemented"""
        return NotImplemented

    def __len__(self) -> int:
        return len(self.noCodeString)

    def __lt__(self, value):
        """return self<value; NotImplemented"""
        return NotImplemented

    def __mul__(self, value) -> this:
        if isinstance(value, int):
            return FormattedString(self.unformattedString*value)
        else:
            return NotImplemented

    def __ne__(self, value) -> bool:
        return not self.__eq__(value)

    def __repr__(self) -> str:
        return repr(self.noCodeString)

    def __rmul__(self, value) -> this:
        return self.__mul__(value)

    def __str__(self) -> str:
        """returns self.string."""
        return self.string

    def capitalize(self) -> this:
        # offset = 0
        firstchar = self.noCodeString[0]
        newstr = ''
        for num, i in enumerate(self.unformattedString):
            if i == firstchar and newstr == '':
                newstr += i.upper()
            else:
                newstr += i.lower()
        return FormattedString(newstr)

    def center(self, width, fillchar=' ') -> this:
        spl = round((width - len(self))/2)
        spr = width - (spl+len(self))
        return FormattedString((spl*fillchar)
                               + self.unformattedString
                               + (spr+fillchar))

    def count(self, sub, start=None, end=None) -> int:
        if isinstance(sub, FormattedString):
            return self.unformattedString.count(sub.unformattedString,
                                                start, end)
        else:
            return self.noCodeString.count(sub, start, end)

    def encode(self, encoding='utf-8', errors='strict') -> bytes:
        return self.noCodeString.encode(encoding, errors)

    def endswith(self, suffix, start=None, end=None) -> bool:
        if not isinstance(suffix, str):
            raise TypeError('endswith() argument 1 must be str, not '
                            + type(suffix))
        if isinstance(suffix, FormattedString):
            r = self.unformattedString.endswith(suffix.unformattedString,
                                                start, end)
            return r  # Temp variable, because of teh 80 char limit
        else:
            return self.noCodeString.endswith(suffix, start, end)

    def expandtabs(self, tabsize=8) -> this:
        return FormattedString(self.unformattedString.expandtabs(tabsize))

    def find(self, sub, start=None, end=None) -> int:
        if not isinstance(sub, str):
            return NotImplemented
        if isinstance(sub, FormattedString):
            return self.unformattedString.find(sub.unformattedString,
                                               start, end)
        else:
            return self.noCodeString.find(sub, start, end)

    def format(self, *args, **kwargs) -> this:
        return FormattedString(self.unformattedString.format(*args, **kwargs))

    def format_map(self, mapping) -> this:
        return FormattedString(self.unformattedString.format_map(mapping))

    def index(self, sub, start=None, end=None) -> int:
        if not isinstance(sub, str):
            return NotImplemented
        if isinstance(sub, FormattedString):
            return self.unformattedString.index(sub, start, end)
        else:
            return self.noCodeString.index(sub, start, end)

    def isalnum(self) -> bool:
        return self.noCodeString.isalnum()

    def isalpha(self) -> bool:
        return self.noCodeString.isalpha()

    def isdecimal(self) -> bool:
        return self.noCodeString.isdecimal()

    def isdigit(self) -> bool:
        return self.noCodeString.isdigit()

    def isidentifier(self) -> bool:
        return self.noCodeString.isidentifier()

    def islower(self) -> bool:
        return self.noCodeString.islower()

    def isnumeric(self) -> bool:
        return self.noCodeString.isnumeric()

    def isprintable(self) -> bool:
        return self.noCodeString.isprintable()

    def isspace(self) -> bool:
        return self.noCodeString.isspace()

    def istitle(self) -> bool:
        return self.noCodeString.istitle()

    def isupper(self) -> bool:
        return self.noCodeString.isupper()

    def join(self, iterable) -> this:
        newstr = ''
        for num, i in enumerate(iterable):
            if num == 0:
                newstr += i
            else:
                newstr += self.unformattedString + i
        return FormattedString(newstr)

    def ljust(self, width, fillchar=' ') -> this:
        if width <= len(self):
            return FormattedString(self.unformattedString)
        return FormattedString(self.unformattedString
                               + (width - len(self))
                               * ' ')

    def lower(self) -> this:
        return FormattedString(self.unformattedString.lower())

    def lstrip(self, chars=None) -> this:
        return FormattedString(self.unformattedString.lstrip(chars))

    def partition(self, sep) -> typing.Tuple[this]:
        return FormattedString(self.unformattedString.partition(sep))

    def replace(self, old, new, count=None) -> this:
        if not isinstance(old, str):
            raise TypeError('replace() argument 1 must be str, not '+type(old))
        if not isinstance(new, str):
            raise TypeError('replace() argument 2 must be str, not '+type(new))
        if isinstance(old, FormattedString):
            if isinstance(new, FormattedString):
                sufs = self.unformattedString
                oufs = old.unformattedString
                nufs = new.unformattedString
                return FormattedString(sufs.replace(oufs, nufs, count))
            else:
                sufs = self.unformattedString
                oufs = old.unformattedString
                return FormattedString(sufs.replace(oufs, new, count))
        else:  # type(old) -> str
            if isinstance(new, FormattedString):
                sufs = self.unformattedString
                nufs = new.unformattedString
                return FormattedString(sufs.replace(old, nufs, count))
            else:
                sufs = self.unformattedString
                return FormattedString(sufs.replace(old, new, count))
        return FormattedString(self.unformattedString.replace(old, new, count))

    def rfind(self, sub, start=None, end=None) -> int:
        if not isinstance(sub, str):
            raise TypeError('rfind() argument 1 must be str, not '+type(sub))
        if isinstance(sub, FormattedString):
            return self.unformattedString.rfind(sub, start, end)
        else:
            return self.noCodeString.rfind(sub, start, end)

    def rindex(self, sub, start=None, end=None) -> int:
        if not isinstance(sub, str):
            raise TypeError('rindex() argument 1 must be str, not '+type(sub))
        if isinstance(sub, FormattedString):
            return self.unformattedString.rindex(sub.unformattedString,
                                                 start, end)
        else:
            return self.noCodeString.rindex(sub, start, end)

    def rjust(self, width, fillchar=' ') -> this:
        if width <= len(self):
            return FormattedString(self.unformattedString)
        return FormattedString((width - len(self))
                               * ' '
                               + self.unformattedString)

    def rpartition(self, sep) -> typing.Tuple[this]:
        return FormattedString(self.unformattedString.rpartition(sep))

    def rsplit(self, sep=None, maxsplit=-1)\
            -> typing.List[this]:
        tl = []
        for i in self.unformattedString.rsplit(sep, maxsplit):
            tl.append(FormattedString(i))
        return tl

    def rstrip(self, chars=None) -> this:
        return FormattedString(self.unformattedString.rstrip(chars))

    def split(self, sep=None, maxsplit=-1) -> typing.List[this]:
        tl = []
        for i in self.unformattedString.split(sep, maxsplit):
            tl.append(FormattedString(i))
        return tl

    def splitlines(self, keepends=None) -> typing.List[this]:
        tl = self.split('\n')
        if keepends:
            nl = []
            for i in tl:
                nl = FormattedString(i.unformattedString+'$(reset)\n')
            return nl
        else:
            return tl

    def startswith(self, prefix, start=None, end=None) -> bool:
        if not isinstance(prefix, str):
            raise TypeError('startswith() argument 1 must be str, not '
                            + type(prefix))
        if isinstance(prefix, FormattedString):
            r = self.unformattedString.endswith(prefix.unformattedString,
                                                start, end)
            return r  # Temp variable, because of teh 80 char limit
        else:
            return self.noCodeString.endswith(prefix, start, end)

    def strip(self, chars=None) -> this:
        return FormattedString(self.unformattedString.strip(chars))

    def swapcase(self) -> this:
        return FormattedString(self.unformattedString.swapcase())

    def title(self) -> this:
        return FormattedString(self.unformattedString.title())

    def translate(self) -> this:
        return FormattedString(self.unformattedString.translate())

    def upper(self) -> this:
        return FormattedString(self.unformattedString.upper())

    def zfill(self, width) -> this:
        return FormattedString(self.unformattedString.zfill(width))
