from dsl_token import *


def __CheckString(str, prefix):
    return -1 != str.find(prefix, 0, len(prefix))


def SplitOperations(token, operationList):
    if Token.Type.OPERATIONS_SEQ != token.type:
        raise TypeError("Cannot split not operations sequnce token")
    residualStr = token.sequence
    result = []
    while len(residualStr) > 1:
        findOperation = False
        for operation in operationList:
            if __CheckString(residualStr, operation):
                result.append(OperationsToken(operation))
                residualStr = residualStr[len(operation):]
                findOperation = True
                break
        if not findOperation:
            break
    if 0 != len(residualStr):
        result.append(OperationsToken(residualStr))
    return result
