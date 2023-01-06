import sys
from enum import Enum

from dsl_token import *


__ITALICS_KEYWORD = "textit"
__BOLD_KEYWORD = "textbf"
__UNDERLINE_KEYWORD = "underline"
__COLOR_KEYWORD = "textcolor"


class __DetectedKeyword(Enum):
    NotDetected = 0
    Italics = 1
    Bold = 2
    Underline = 3
    Color = 4


def __CheckKeyword(str, curPos):
    def ModifiedFinder(keyword, str, curPos):
        return str.find(keyword, curPos, curPos + len(keyword))
    if -1 != ModifiedFinder(__ITALICS_KEYWORD, str, curPos):
        return __DetectedKeyword.Italics
    if -1 != ModifiedFinder(__BOLD_KEYWORD, str, curPos):
        return __DetectedKeyword.Bold
    if -1 != ModifiedFinder(__UNDERLINE_KEYWORD, str, curPos):
        return __DetectedKeyword.Underline
    if -1 != ModifiedFinder(__COLOR_KEYWORD, str, curPos):
        return __DetectedKeyword.Color
    return __DetectedKeyword.NotDetected


def __CheckEscapeSequence(str, curPos):
    if str[curPos] != '\\':
        return __DetectedKeyword.NotDetected
    return __CheckKeyword(str, curPos + 1)


def __SkipSpaces(str, curPos):
    for i in range(curPos, len(str)):
        if not str[i].isspace():
            return i
    return len(str)


def __GetNumber(str, pos):
    number = 0.0

    if str[pos] != '.':
        number = int(str[pos])
        pos += 1
        while pos != len(str) and str[pos].isdigit():
            number = 10 * number + int(str[pos])
            pos += 1
        if pos == len(str) or '.' != str[pos]:
            token = NumberToken(Token.Type.INTEGER, number)
            return pos, token
        number = float(number)

    pos += 1
    diver = 10
    while pos != len(str) and str[pos].isdigit():
        number += float(str[pos]) / diver
        pos += 1
        diver *= 10
    return pos, NumberToken(Token.Type.FLOAT, number)


def __GetName(str, pos):
    modCount = 0
    labels = set()
    color = NameToken.Colors.NoColor

    while not str[pos].isalpha():
        detection = __CheckKeyword(str, pos + 1)
        if __DetectedKeyword.NotDetected == detection:
            raise SyntaxError("Failed to recognize escape sequence")
        elif __DetectedKeyword.Italics == detection:
            pos += 1 + len(__ITALICS_KEYWORD)
            labels.add(NameToken.Label.Italics)
        elif __DetectedKeyword.Bold == detection:
            pos += 1 + len(__BOLD_KEYWORD)
            labels.add(NameToken.Label.Bold)
        elif __DetectedKeyword.Underline == detection:
            pos += 1 + len(__UNDERLINE_KEYWORD)
            labels.add(NameToken.Label.Underline)
        elif __DetectedKeyword.Color == detection:
            if NameToken.Colors.NoColor != color:
                raise SyntaxError("Only one color can be applied")
            pos += 1 + len(__COLOR_KEYWORD)
            if pos == len(str) or '[' != str[pos]:
                raise SyntaxError("Failed to find '[' in color modifier")
            pos += 1
            closePos = str.find(']', pos)
            if -1 == closePos:
                raise SyntaxError("Failed to find ']' in color modifier")
            selectingColor = [e for e in NameToken.Colors if e.name.lower() == str[pos:closePos]]
            if 0 == len(selectingColor):
                raise SyntaxError("Failed to recognize color")
            color = selectingColor[0]
            pos = closePos + 1
        if pos == len(str) or '{' != str[pos]:
            raise SyntaxError("Failed to find '{' in color modifier")
        pos += 1
        modCount += 1

    for seqEnd in range(pos, len(str)):
        if not (str[seqEnd].isalpha() or str[seqEnd].isdigit()):
            if -1 == str.find('}' * modCount, seqEnd, seqEnd + modCount):
                raise SyntaxError("Not enough '}' in modificators")
            return seqEnd + modCount, NameToken(str[pos:seqEnd], list(labels), color)

    if 0 != modCount:
        raise SyntaxError("Not enough '}' in modificators")
    return len(str), NameToken(str[pos:], list(labels), color)


def __GetOperationsSequence(str, pos):
    for seqEnd in range(pos, len(str)):
        if (str[seqEnd].isalpha() or str[seqEnd].isdigit() or str[seqEnd] == '.'
            or __DetectedKeyword.NotDetected != __CheckEscapeSequence(str, seqEnd)):
            return seqEnd, OperationsToken(str[pos:seqEnd])
    return len(str), OperationsToken(str[pos:])


def __TokenizeLine(line):
    i = 0
    tokens = []
    while True:
        i = __SkipSpaces(line, i)
        if i == len(line):
            break
        token = None
        if line[i].isdigit() or '.' == line[i]:
            i, token = __GetNumber(line, i)
        elif line[i].isalpha() or __DetectedKeyword.NotDetected != __CheckEscapeSequence(line, i):
            i, token = __GetName(line, i)
        else:
            i, token = __GetOperationsSequence(line, i)
        tokens.append(token)
    return tokens


def Tokenize(filePath):
    with open(filePath, 'r') as file:
        tokens = []
        for line in file:
            tokens += __TokenizeLine(line.strip())
        return tokens


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Need only one argument: program text path")
        sys.exit()
    token_list = Tokenize(sys.argv[1])
    print("tokens:")
    for token in token_list:
        if Token.Type.INTEGER == token.type:
            print(f"Integer number: {token.number}")
        elif Token.Type.FLOAT == token.type:
            print(f"Float number: {token.number}")
        elif Token.Type.NAME == token.type:
            print(f"Name: {token.name}. Labels: {token.labels}. Color: {token.color}")
        elif Token.Type.OPERATIONS_SEQ == token.type:
            print(f"Operations sequence: {token.sequence}")
