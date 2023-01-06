import sys
from dsl_token import *


__ITALICS_KEYWORD = "textit"
__BOLD_KEYWORD = "textbf"
__UNDERLINE_KEYWORD = "underline"
__COLOR_KEYWORD = "textcolor"


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
    for seqEnd in range(pos, len(str)):
        if not (str[seqEnd].isalpha() or str[seqEnd].isdigit()):
            return seqEnd, NameToken(str[pos:seqEnd], [], NameToken.Colors.NoColor)
    return len(str), NameToken(str[pos:], [], NameToken.Colors.NoColor)


def __GetOperationsSequence(str, pos):
    for seqEnd in range(pos, len(str)):
        if str[seqEnd].isalpha() or str[seqEnd].isdigit() or str[seqEnd] == '.':
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
        elif line[i].isalpha():
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
