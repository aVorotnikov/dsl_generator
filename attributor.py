from syntax import *


def SetAttributes(ast, attributeFunctions):
    nodes = [ast]
    front = [ast]
    while len(front):
        frontLen = len(front)
        for node in front:
            front += [child for child in node.childs if TreeNode.Type.NONTERMINAL == child.type]
        front = front[frontLen:]
        nodes += front
    while len(nodes):
        node = nodes[-1]
        if TreeNode.Type.NONTERMINAL == node.type and node.nonterminalType in attributeFunctions:
            node.attribute = attributeFunctions[node.nonterminalType]([child.attribute for child in node.childs])
        nodes = nodes[:-1]
