from dsl_token import *
from syntax.core import *


class TreeNode:
    class Type(Enum):
        TOKEN = 0
        NONTERMINAL = 1


    def __init__(self, type):
        self.type = type
        self.attribute = None


def __BuildAstElement(grammarDescription, nonterminal, tokenList, start, end):
    if nonterminal not in grammarDescription:
        raise Exception(f"Failed to find '{nonterminal}' description")
    result = TreeNode(TreeNode.Type.NONTERMINAL)
    result.nonterminalType = nonterminal
    result.childs = []
    result.commands = []
    node = grammarDescription[nonterminal]
    while start < end and NodeType.END != node.type:
        newToken = tokenList[start]
        exit = None
        success = False
        for next in node.nextNodes:
            if NodeType.END == next[0].type:
                exit = next
                continue
            if NodeType.KEY == next[0].type and Token.Type.KEY == newToken.type and newToken.str == next[0].str:
                element = TreeNode(TreeNode.Type.TOKEN)
                element.attribute = newToken.attribute
                element.token = newToken
                result.childs.append(element)
                result.commands.append(next[1])
                start += 1
                node = next[0]
                success = True
                findEnd = [nextNode for nextNode in node.nextNodes if NodeType.END == nextNode[0].type]
                if len(findEnd) != 0:
                    exit = findEnd[0]
                break
            if NodeType.TERMINAL == next[0].type and Token.Type.TERMINAL == newToken.type and newToken.terminalType == next[0].terminal:
                element = TreeNode(TreeNode.Type.TOKEN)
                element.attribute = newToken.attribute
                element.token = newToken
                result.childs.append(element)
                result.commands.append(next[1])
                start += 1
                node = next[0]
                success = True
                findEnd = [nextNode for nextNode in node.nextNodes if NodeType.END == nextNode[0].type]
                if len(findEnd) != 0:
                    exit = findEnd[0]
                break
            if NodeType.NONTERMINAL == next[0].type:
                try:
                    res = __BuildAstElement(grammarDescription, next[0].nonterminal, tokenList, start, end)
                    start = res[1]
                    end = res[2]
                    result.childs.append(res[0])
                    result.commands.append(next[1])
                    node = next[0]
                    success = True
                    findEnd = [nextNode for nextNode in node.nextNodes if NodeType.END == nextNode[0].type]
                    if len(findEnd) != 0:
                        exit = findEnd[0]
                except Exception:
                    continue
                break
        if success:
            continue
        if exit:
            node = exit[0]
            result.commands.append(exit[1])
            exit = None
        else:
            raise Exception(f"Failed to process token '{newToken.str}'")
    if exit is not None:
        result.commands.append(exit[1])
    return result, start, end


def BuildAst(grammarDescription, axiom, tokenList):
    return __BuildAstElement(grammarDescription, axiom, tokenList, 0, len(tokenList))[0]
