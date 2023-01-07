from afterscan.afterscan_tokens import *


def __ConvertNameTokenToKeywordAbstarct(token, strComparator):
    if Token.Type.NAME != token.type:
        raise TypeError("Cannot convert not name token to keyword token")
    keywordTokens = [keyword for keyword in Keyword if strComparator(keyword.name, token.name)]
    if 0 == len(keywordTokens):
        return token
    return  KeywordToken(keywordTokens[0])


def ConvertNameTokenToKeyword(token):
    return __ConvertNameTokenToKeywordAbstarct(token, lambda s1, s2: s1 == s2)


def ConvertNameTokenToKeywordCaseInsesitive(token):
    return __ConvertNameTokenToKeywordAbstarct(token, lambda s1, s2: s1.lower() == s2.lower())
