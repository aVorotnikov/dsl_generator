from enum import Enum


class Terminal(Enum):
    number = "number"
    name = "name"
    string = "string"
    code = "code"
    char_key = "char_key"


tokenRegularExpressions = [
    (Terminal.number, r"[0-9]+(.[0-9]*)?"),
    (Terminal.name, r"[\w^\d][\w]*"),
    (Terminal.string, r'"(\\.|[^\\"]+)"'),
    (Terminal.code, r"\{[^\}]*\}"),
    (Terminal.char_key, r"/|\(|\)|,|;|\.|:|=|\->"),
]


keys = [
    ("VAR", Terminal.name),
    ("REQUIRED", Terminal.name),
    ("PROVIDED", Terminal.name),
    ("INNER", Terminal.name),
    ("STATE", Terminal.name),
    ("else", Terminal.name),
    ("true", Terminal.name),
    ("false", Terminal.name),
    ("=", Terminal.char_key),
    ("->", Terminal.char_key),
    ("/", Terminal.char_key),
    ("(", Terminal.char_key),
    (")", Terminal.char_key),
    (",", Terminal.char_key),
    (".", Terminal.char_key),
    (":", Terminal.char_key),
    (";", Terminal.char_key),
]


class Nonterminal(Enum):
    CIAO = "CIAO"
    AUTOMATA_OBJECT = "AUTOMATA_OBJECT"
    VAR_BLOCK = "VAR_BLOCK"
    REQUIRED_BLOCK = "REQUIRED_BLOCK"
    PROVIDED_BLOCK = "PROVIDED_BLOCK"
    INNER_BLOCK = "INNER_BLOCK"
    FUNCTION = "FUNCTION"
    STATE_BLOCK = "STATE_BLOCK"
    TRANSITION_DESCRIPTION = "TRANSITION_DESCRIPTION"


axiom = Nonterminal.CIAO
