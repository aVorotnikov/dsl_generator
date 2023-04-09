from enum import Enum


class Terminal(Enum):
    name = "name"
    char_sequence = "char_sequence"
    string = "string"


tokenRegularExpressions = [
    (Terminal.name, r"[\w^\d][\w]*"),
    (Terminal.char_sequence, r"[^'\w\s]+"),
    (Terminal.string, r"'(\\.|[^\\']+)*'")
]


keys = [
    ("TERMINALS", Terminal.name),
    ("KEYS", Terminal.name),
    ("NONTERMINALS", Terminal.name),
    ("AXIOM", Terminal.name),
    ("RULES", Terminal.name),
    ("ERRORS", Terminal.name),
    (".", Terminal.char_sequence),
    (":", Terminal.char_sequence),
    ("::=", Terminal.char_sequence),
    (";", Terminal.char_sequence),
    ("(", Terminal.char_sequence),
    (")", Terminal.char_sequence),
    ("|", Terminal.char_sequence),
    ("[", Terminal.char_sequence),
    ("]", Terminal.char_sequence),
    ("{", Terminal.char_sequence),
    ("}", Terminal.char_sequence),
    ("#", Terminal.char_sequence),
]


class Nonterminal(Enum):
    GRAMMAR = 'GRAMMAR'
    TERMINALS_BLOCK = 'TERMINALS_BLOCK'
    KEYS_BLOCK = 'KEYS_BLOCK'
    NONTERMINALS_BLOCK = 'NONTERMINALS_BLOCK'
    AXIOM_BLOCK = 'AXIOM_BLOCK'
    ERROR_BLOCK = 'ERROR_BLOCK'
    RULES_BLOCK = 'RULES_BLOCK'
    RULE = 'RULE'
    RHS = 'RHS'
    SEQUENCE = 'SEQUENCE'
    BRACKETS = 'BRACKETS'
    OPTIONAL = 'OPTIONAL'
    TSEITIN_ITERATION = 'TSEITIN_ITERATION'


axiom = Nonterminal.GRAMMAR
