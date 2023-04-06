from dsl_token import *
from enum import Enum


class Token:
    class Type(Enum):
        TERMINAL = 0
        KEY = 1


    def __init__(self, type):
        self.type = type
        self.attribute = None
