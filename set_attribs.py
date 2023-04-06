def __SetAttributes(ast):
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
        if TreeNode.Type.NONTERMINAL == node.type:
            if dsl_info.Nonterminal.TERM == node.nonterminalType:
                node.attribute = 1
                for child in node.childs:
                    if child.token.attribute is not None:
                        node.attribute *= child.token.attribute
            elif dsl_info.Nonterminal.EXPRESSION == node.nonterminalType:
                node.attribute = 0
                for child in node.childs:
                    if child.attribute is not None:
                        node.attribute += child.attribute
            elif dsl_info.Nonterminal.EXPRESSIONS == node.nonterminalType:
                node.attribute = [child.attribute for child in node.childs if child.attribute]
        nodes = nodes[:-1]