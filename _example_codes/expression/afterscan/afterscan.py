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
        if Token.Type.TERMINAL == token.type and dsl_info.Terminal.number == token.terminalType:
            token.attribute = int(token.str)
    return tmp
