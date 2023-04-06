import dsl_info
from dsl_token import *


def __ReplaceOneToken(tokenList, converter):
    res = []
    for token in tokenList:
        res += converter(token)
    return res


def __SplitTokens(splitTerminalMap, token):
    def __CheckString(str, prefix):
        return -1 != str.find(prefix, 0, len(prefix))

    if token.type != Token.Type.TERMINAL:
        return [token]
    if token.terminalType not in splitTerminalMap:
        return [token]
    keys = splitTerminalMap[token.terminalType]
    residualStr = token.str
    result = []
    while len(residualStr) > 1:
        findKey = False
        for key in keys:
            if __CheckString(residualStr, key):
                newToken = Token(Token.Type.TERMINAL)
                newToken.terminalType = token.terminalType
                newToken.str = key
                result.append(newToken)
                residualStr = residualStr[len(key):]
                findKey = True
                break
        if not findKey:
            break
    if 0 != len(residualStr):
        newToken = Token(Token.Type.TERMINAL)
        newToken.terminalType = token.terminalType
        newToken.str = residualStr
        result.append(newToken)
    return result


def __ReplaceKeywords(terminalMap, token):
    if token.type != Token.Type.TERMINAL:
        return [token]
    if token.terminalType not in terminalMap:
        return [token]
    if token.str not in terminalMap[token.terminalType]:
        return [token]
    token.type = Token.Type.KEY
    return [token]


def __StringProcessing(token):
    if token.type != Token.Type.TERMINAL or token.terminalType != dsl_info.Terminal.string:
        return[token]
    token.str = token.str[1:-1]
    token.str.replace("\\'", "'")
    return [token]


def Afterscan(tokenList):
    terminalMap = dict()
    for keyInfo in dsl_info.keys:
        if keyInfo[1] not in terminalMap:
            terminalMap[keyInfo[1]] = [keyInfo[0]]
        else:
            terminalMap[keyInfo[1]].append(keyInfo[0])

    terminalTypesToSplit = [dsl_info.Terminal.char_sequence]
    splitTerminalMap = dict()
    for terminal, keys in terminalMap.items():
        if terminal in terminalTypesToSplit:
            splitTerminalMap[terminal] = keys
            splitTerminalMap[terminal].sort(reverse=True, key=lambda k: len(k))

    tmp = __ReplaceOneToken(tokenList, lambda token: __SplitTokens(splitTerminalMap, token))
    tmp = __ReplaceOneToken(tmp, lambda token: __ReplaceKeywords(terminalMap, token))
    tmp = __ReplaceOneToken(tmp, __StringProcessing)

    for token in tmp:
        if token.type != Token.Type.TERMINAL:
            continue
        if dsl_info.Terminal.name == token.terminalType or dsl_info.Terminal.string == token.terminalType:
            token.attribute = token.str

    return tmp
