from enum import Enum


class Terminal(Enum):
    name = "name",
    char_sequence = "char_sequence",
    string = "string"


tokenRegularExpressions = [
    (Terminal.name, r"[\w\D][\w]*"),
    (Terminal.char_sequence, r"[\W\S^']+"),
    (Terminal.string, r"'(\\.|[^\\']+)*'")
]


keys = [
    ("Terminal", Terminal.name),
    ("KEYS", Terminal.name),
    ("NONTerminal", Terminal.name),
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
    GRAMMAR = 'GRAMMAR',
    TERMINALS_BLOCK = 'TERMINALS_BLOCK',
    KEYS_BLOCK = 'KEYS_BLOCK',
    NONTERMINALS_BLOCK = 'NONTERMINALS_BLOCK',
    AXIOM_BLOCK = 'AXIOM_BLOCK',
    ERROR_BLOCK = 'ERROR_BLOCK',
    RULES_BLOCK = 'RULES_BLOCK',
    RULE = 'RULE',
    RHS = 'RHS',
    NONTERMINAL = 'NONTERMINAL',
    TERMINAL = 'TERMINAL'


axiom = Nonterminal.GRAMMAR
