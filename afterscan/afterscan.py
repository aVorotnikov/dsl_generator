from afterscan.utils import *


__OPERATION_LIST = ['+']


def __Replacer(token):
    if Token.Type.NAME == token.type:
        return [ConvertNameTokenToKeyword(token)]
    if Token.Type.OPERATIONS_SEQ == token.type:
        return SplitOperations(token, __OPERATION_LIST)
    return [token]


def Afterscan(tokenList):
    return ReplaceOneToken(tokenList, __Replacer)
