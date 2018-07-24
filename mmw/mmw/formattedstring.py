import mmw
import re
import typing


class FormattedString(str):
    """A formatted string."""

    def __init__(self, string: str):
        self.allowColor = True
        self.string = mmw.format(string)
        self.unformattedString = string
        self.noCodeString = re.sub(r"\$\([A-Za-z_0-9]*\)", "", string)

    def __len__(self) -> int:
        return len(self.noCodeString)

    def __eq__(self, anotherString: typing.AnyStr) -> bool:
        if isinstance(anotherString, FormattedString):
            return self.unformattedString == anotherString.unformattedString
        else:
            return self.noCodeString == anotherString

    def __str__(self) -> str:
        """returns self.string."""
        return self.string

    def __add__(self, anotherString: typing.AnyStr):
        if isinstance(anotherString, FormattedString):
            return FormattedString(self.unformattedString
                                   + anotherString.unformattedString)
        else:
            return FormattedString(self.unformattedString
                                   + anotherString)
