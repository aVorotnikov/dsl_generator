from enum import Enum


class SyntaxDescriptionType(Enum):
    VIRT_DIAGRAMS = "virt"
    RBNF = "rbnf"


class NodeType(Enum):
    TERMINAL = 0
    KEY = 1
    NONTERMINAL = 2
    START = 3
    END = 4


class Node:
    def __init__(self, type, str):
        self.type = type
        self.str = str
        self.nextNodes = []
