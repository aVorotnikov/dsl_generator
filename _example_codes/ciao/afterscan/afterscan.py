import dsl_info
from dsl_token import *


def __ReplaceOneToken(tokenList, converter):
    res = []
    for token in tokenList:
        res += converter(token)
    return res


def __ReplaceKeywords(terminalMap, token):
    if token.type != Token.Type.TERMINAL:
        return [token]
    if token.terminalType not in terminalMap:
        return [token]
    if token.str not in terminalMap[token.terminalType]:
        return [token]
    token.type = Token.Type.KEY
    return [token]


def Afterscan(tokenList):
    terminalMap = dict()
    for keyInfo in dsl_info.keys:
        if keyInfo[1] not in terminalMap:
            terminalMap[keyInfo[1]] = [keyInfo[0]]
        else:
            terminalMap[keyInfo[1]].append(keyInfo[0])

    tmp = __ReplaceOneToken(tokenList, lambda token: __ReplaceKeywords(terminalMap, token))

    for token in tmp:
        if token.type == Token.Type.KEY:
            if token.str == "else":
                token.attribute = token.str
            elif token.str == "false":
                token.attribute = False
            elif token.str == "true":
                token.attribute = True
            continue
        if dsl_info.Terminal.name == token.terminalType:
            token.attribute = token.str
        elif dsl_info.Terminal.string == token.terminalType:
            token.attribute = token.str[1:-1]
        elif dsl_info.Terminal.code == token.terminalType:
            token.attribute = token.str[1:-1]
        elif dsl_info.Terminal.number == token.terminalType:
            if '.' in token.str:
                token.attribute = float(token.str)
            else:
                token.attribute = int(token.str)

    return tmp
