from dsl_info import *


def __RemoveNones(attributes):
    return [attribute for attribute in attributes if attribute is not None]


def __ForFunctions(attributes):
    attributes = __RemoveNones(attributes)
    return attributes[0], attributes[1:]


def __Pairs(attributes):
    attributes = __RemoveNones(attributes)
    if len(attributes) % 2 != 0:
        raise RuntimeError("Expect even number of attributes")
    return [(attributes[i], attributes[i + 1]) for i in range(0, len(attributes), 2)]


def __ForTransitions(attributes):
    attrib = dict()
    attrib["src"] = attributes[0]
    attrib["dst"] = attributes[-1]
    attributes = attributes[2:]
    attrib["cond"] = attributes[0]
    if attributes[0] is None:
        attributes = attributes[1:]
    else:
        attributes = attributes[2:]
    attrib["action"] = attributes[0]
    return attrib


attributesMap = {
    Nonterminal.VAR_BLOCK : __Pairs,
    Nonterminal.FUNCTION : __ForFunctions,
    Nonterminal.TRANSITION_DESCRIPTION : __ForTransitions
}
