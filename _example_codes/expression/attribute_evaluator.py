from dsl_info import *


def __RemoveNones(attributes):
    return [attribute for attribute in attributes if attribute]


def __Multiple(attributes):
    attributes = __RemoveNones(attributes)
    res = 1
    for num in attributes:
        res *= num
    return res


def __Add(attributes):
    attributes = __RemoveNones(attributes)
    res = 0
    for num in attributes:
        res += num
    return res


attributesMap = {
    Nonterminal.TERM : __Multiple,
    Nonterminal.EXPRESSION : __Add,
    Nonterminal.EXPRESSIONS : __RemoveNones
}
