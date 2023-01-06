from enum import Enum


class Token:
    class Type(Enum):
        KEYWORD = 0
        INTEGER = 1
        FLOAT = 2
        NAME = 3
        OPERATIONS_SEQ = 4


    def __init__(self, type):
        self.type = type


class NumberToken(Token):
    def __init__(self, type, number):
        if type != Token.Type.FLOAT and type != Token.Type.INTEGER:
            raise TypeError("Incorrect token type to create number token")
        super().__init__(type)
        self.number = number


class NameToken(Token):
    class Label(Enum):
        Italics = 0
        Bold = 1
        Underline = 2


    @staticmethod
    def GetLabelsCommands(label):
        if NameToken.Label.Italics == label:
            return "textit"
        elif NameToken.Label.Bold == label:
            return "textbf"
        elif NameToken.Label.Underline == label:
            return "underline"


    class Colors(Enum):
        NoColor = 0
        Red = 1,
        Green = 2,
        Blue = 3,
        Cyan = 4,
        Magenta = 5,
        Yellow = 6,
        Black = 7,
        Gray = 8,
        White = 9,
        DarkGray = 10,
        LightGray = 11,
        Brown = 12,
        Lime = 13,
        Olive = 14,
        Orange = 15,
        Pink = 16,
        Purple = 17,
        Teal = 18,
        Violet = 19


    COLOR_COMMAND = "textcolor"


    def __init__(self, name, labels, color):
        super().__init__(Token.Type.NAME)
        self.name = name
        self.labels = labels
        self.color = color


class OperationsToken(Token):
    def __init__(self, str):
        super().__init__(Token.Type.OPERATIONS_SEQ)
        self.sequence = str
