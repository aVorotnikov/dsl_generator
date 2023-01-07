from dsl_token import *
from enum import Enum


class Keyword(Enum):
    # add keywords here
    SomeKeyWord = "someKeyWord"


class KeywordToken(Token):
    def __init__(self, keyword):
        super().__init__(Token.Type.KEYWORD)
        self.keyword = keyword
