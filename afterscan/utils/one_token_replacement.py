def ReplaceOneToken(tokenList, converter):
    res = []
    for token in tokenList:
        res += converter(token)
